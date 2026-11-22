#!/usr/bin/env python3
"""Belgeye sadakat ve bilgi kirliliği denetimi (deterministik; model/API gerektirmez).

"Model önerir, araç karar verir" (reverify) ve iddia-kanıt eşlemesi (FActScore, RefChecker, MiniCheck) fikriyle:
senaryodaki doğrulanabilir her öğe kaynak belgede aranır, bulunamayan her biri kanıtıyla raporlanır.

  1. EKSİK      belgenin anlamlı satırlarından videoda karşılığı olmayanlar ("belgenin tamamı videoda")
  2. UYDURMA    belgede geçmeyen sayılar ve İngilizce örnekler (bilgi kirliliği riski)  → kritik
  3. KONTROL    belgede geçmeyen özel adlar (yanlış alarm olabilir; hakem bakar)
  4. EKLENTİ    belgede olmayan, bizim eklediğimiz açıklama cümleleri (doğru olmalı; hakem bakar)

Kullanım:
  python sadakat.py senaryo.json belge.md [--ayar ayar.json] [-o rapor.json]
belge.md: belge_oku.py çıktısı (ya da herhangi bir düz metin/markdown).
"""
import argparse, json, re, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import video_uret as v  # noqa: E402

ETKISIZ = set("""ve ile bir bu şu o da de mi mu mü mı için gibi daha en çok her ya veya ama fakat çünkü olarak olan
the a an and or of to in on at is are was were be for with by it this that you your i we they he she""".split())


def norm(s):
    s = unicodedata.normalize("NFKC", str(s)).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("I", "ı").replace("İ", "i").lower()
    s = re.sub(r"\\([_*\[\]~])", r"\1", s)
    s = re.sub(r"[*`~]|_{1,2}(?=\w)|(?<=\w)_{1,2}", "", s)        # markdown vurgu işaretleri kelimeyi bölmesin
    s = re.sub(r"[_#>|\[\]()]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def norm_sik(s):
    """Noktalama da atılmış biçim (İngilizce öbek araması için; ı/i farkı yok sayılır: Izmir = İzmir)."""
    return re.sub(r"\s+", " ", re.sub(r"[^\w' ]", " ", norm(s).replace("&", " and "))).strip().replace("ı", "i")


def kelimeler(s):
    ws = (w.strip("'") for w in re.findall(r"[\wçğıöşüâî']+", norm(s)))    # 'Ayse' gibi tırnaklı değerler
    return [w for w in ws if len(w) > 2 and w not in ETKISIZ]


def sayilar(s):
    s = re.sub(r"\(\d+/\d+\)|\b\d+/\d+\b", " ", str(s))           # (1/2), 4/5 sahne parça numaraları
    return set(re.findall(r"\d+(?:[.,]\d+)?", s))


def senaryo_metinleri(sen):
    """(sahne_no, kaynak, metin) üçlüleri: anlatım cümleleri + ekrandaki öğeler."""
    out = []
    for i, sh in enumerate(sen["sahneler"], 1):
        for c in v.cumlelere_bol(sh.get("anlatim", "")):
            out.append((i, "anlatim", c))
        for o in v.ekran_ogeleri(sh):
            out.append((i, "ekran", str(o)))
    return out


KOD_IZ = re.compile(r"\s--\s|->|-->|::|<\|--|\*--|o--|\.\.>|@start|@end|^\s*(inv|implies|context|pre|post|participant|actor|class|"
                    r"state|note for|Rel|Person|System|!include|par|alt|else|end|\[\\?\*\])\b|self\.|^\s*[}{]\s*$")


def kod_mu(ln):
    """Belgedeki kod satırı (PlantUML, Mermaid, OCL): anlatımda satır satır okunmaz, açıklanır."""
    t = ln.strip()
    if KOD_IZ.search(t):
        return True
    sembol = sum(1 for c in t if not (c.isalnum() or c.isspace() or c in ".,;:'\"()%-–—/?!"))
    return len(t) > 0 and sembol / len(t) > 0.12


def belge_satirlari(belge):
    sat = []
    for ln in belge.splitlines():
        ln = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", ln)     # görsel: yalnız alt yazısı sayılır
        if kod_mu(ln):
            continue
        t = re.sub(r"^[\s#>*\-|0-9.)]+", "", ln).strip(" |")
        if len(kelimeler(t)) >= 3 and not re.fullmatch(r"[-|: ]+", t):
            sat.append(ln.strip())
    return sat


def denetle(sen, belge, ayar=None, esik_kapsam=0.6):
    ayar = ayar or {}
    yok_say = [norm(x) for x in ayar.get("sadakat_yoksay", [])]
    for k in ayar.get("on_degistir", {}) or {}:     # belgeden bilerek çıkarılan/değiştirilen ifadeler
        yok_say.append(norm(k))
    for k in ayar.get("degistir", {}) or {}:
        yok_say.append(norm(k))
    belge_n, belge_s = norm(belge), norm_sik(belge)
    belge_kel = set(kelimeler(belge))
    metin = senaryo_metinleri(sen)
    havuz_s = norm_sik(" ".join(v.temiz(m) for _, _, m in metin))
    havuz_kel = set(kelimeler(" ".join(v.temiz(m) for _, _, m in metin)))
    havuz_kok = {h[:5] for h in havuz_kel if len(h) >= 5}     # Türkçe ekler: ilk 5 harf (kök yaklaşığı)
    rapor = {"eksik": [], "uydurma": [], "telaffuz": [], "kontrol": [], "eklenti": []}

    # 1) EKSİK: belgenin her anlamlı satırı videoda karşılık buluyor mu?
    atla = [norm(x) for x in ayar.get("atla_satir", [])]
    for ln in belge_satirlari(belge):
        n = norm(ln)
        if any(a and a in n for a in atla + yok_say):
            continue
        kw = kelimeler(ln)
        oran = sum(1 for w in kw if w in havuz_kel or (len(w) >= 5 and w[:5] in havuz_kok)) / len(kw)
        if oran < esik_kapsam and norm_sik(ln)[:40] not in havuz_s:
            rapor["eksik"].append({"satir": ln[:160], "kapsam": round(oran, 2)})

    # 2) UYDURMA: sayı ve İngilizce öbekler belgede geçiyor mu?
    belge_sayi = sayilar(belge) | set(re.findall(r"\d+", belge))   # koddaki "(102,1,…" gibi dizilerin parçaları
    gorulen = set()
    for si, kaynak, m in metin:
        for s in sayilar(m) - belge_sayi:
            if (s, si) not in gorulen:
                gorulen.add((s, si))
                rapor["uydurma"].append({"sahne": si, "tur": "sayı", "deger": s, "baglam": v.temiz(m)[:120]})
        for en in re.findall(r"\{([^{}]+)\}", m):
            e = norm_sik(en)
            if len(e) < 3 or e in belge_s or any(a and a in norm(en) for a in yok_say):
                continue
            # dönüştürücünün eklediği bağlaçlar/boşluk sözcüğü: "/"→"ya da", "+"→"ve", "___"→"blank"
            parca = [p_.strip() for p_ in re.split(r"\b(?:ya da|ve|blank|veya|yani)\b|[:;]", e) if p_.strip()]
            if parca and all(p_ in belge_s or (len(p_.split()) == 1 and len(p_) <= 3) for p_ in parca):
                continue
            # uzun öbek: belgede kelimelerinin çoğu yan yana geçiyorsa (küçük biçim farkı) kabul
            kk = e.split()
            if len(kk) >= 4 and any(" ".join(kk[i:i + 4]) in belge_s for i in range(len(kk) - 3)):
                continue
            if len(kk) <= 3:     # kısa terim / okunuş yardımı (ör. "static", "draw dot io"): hakem baksın
                rapor["kontrol"].append({"sahne": si, "ad": "{" + en[:40] + "}", "baglam": v.temiz(m)[:120]})
                continue
            rapor["uydurma"].append({"sahne": si, "tur": "ingilizce", "deger": en[:100], "baglam": v.temiz(m)[:120]})

    # 2b) TELAFFUZ: İngilizce okunacak {…} öbeğine Türkçe kelime düşmüş mü? (İngilizce aksanla okunur)
    for si, kaynak, m in metin:
        if kaynak != "anlatim":
            continue
        for en in re.findall(r"\{([^{}]+)\}", m):
            tr = re.findall(r"[\wçğıöşüÇĞİÖŞÜ]*[çğıöşüÇĞİÖŞÜ][\wçğıöşüÇĞİÖŞÜ]*|(?<!['’])\b(?:ve|ya da|veya|yani|değil|ile)\b", en)
            if tr:
                rapor["telaffuz"].append({"sahne": si, "oge": en[:100], "turkce": tr[:5]})

    # 3) KONTROL: cümle ortasındaki özel adlar belgede var mı?
    gorulen = set()
    for si, kaynak, m in metin:
        if kaynak != "anlatim":
            continue
        t = re.sub(r"\{[^{}]*\}", " ", m)
        for w in re.findall(r"(?<=[a-zçğıöşü,;] )([A-ZÇĞİÖŞÜ][a-zçğıöşü]{2,})", t):
            kok = norm(w)[:5]
            if not any(b.startswith(kok) for b in belge_kel) and w not in gorulen:
                gorulen.add(w)
                rapor["kontrol"].append({"sahne": si, "ad": w, "baglam": v.temiz(m)[:120]})

    # 4) EKLENTİ: ayar dosyasından gelen açıklamalar (belgede yok; doğruluğu hakem denetler)
    for k, acik in (ayar.get("aciklamalar") or {}).items():
        rapor["eklenti"].append({"soru": k, "metin": str(acik)[:160]})

    satir_say = len(belge_satirlari(belge))
    # açıklama (ayar) cümlesinden gelen İngilizce: bizim eklentimiz; doğruluğu hakem denetler, otomatik kritik değil
    acik_n = [norm_sik(x) for x in (ayar.get("aciklamalar") or {}).values()]
    kalan = []
    for u in rapor["uydurma"]:
        b = norm_sik(u["baglam"])[:60]
        if u["tur"] == "ingilizce" and any(b and b[:40] in a for a in acik_n):
            rapor["eklenti"].append({"soru": f"sahne {u['sahne']}", "metin": "İngilizce örnek: " + u["deger"]})
        else:
            kalan.append(u)
    rapor["uydurma"] = kalan
    rapor["ozet"] = {
        "belge_satiri": satir_say,
        "kapsam_orani": round(1 - len(rapor["eksik"]) / max(1, satir_say), 3),
        "eksik": len(rapor["eksik"]), "uydurma": len(rapor["uydurma"]), "telaffuz": len(rapor["telaffuz"]),
        "kontrol": len(rapor["kontrol"]), "eklenti": len(rapor["eklenti"]),
    }
    return rapor


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("senaryo"); ap.add_argument("belge")
    ap.add_argument("--ayar", help="belge_senaryo ayar.json (atla_satir, on_degistir, aciklamalar, sadakat_yoksay)")
    ap.add_argument("-o", "--cikti")
    a = ap.parse_args()
    sen = json.loads(Path(a.senaryo).read_text(encoding="utf-8"))
    ayar = json.loads(Path(a.ayar).read_text(encoding="utf-8")) if a.ayar else {}
    r = denetle(sen, Path(a.belge).read_text(encoding="utf-8", errors="ignore"), ayar)
    cikti = Path(a.cikti or Path(a.senaryo).with_suffix(".sadakat.json"))
    cikti.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    o = r["ozet"]
    print(f"Sadakat: belge kapsamı %{o['kapsam_orani'] * 100:.1f} · eksik {o['eksik']} · uydurma {o['uydurma']} · "
          f"telaffuz {o['telaffuz']} · kontrol {o['kontrol']} · eklenti {o['eklenti']} → {cikti}")
    for x in r["telaffuz"][:15]:
        print(f"  TELAFFUZ sahne {x['sahne']}: {{{x['oge'][:60]}}} içinde Türkçe: {', '.join(x['turkce'])}")
    for x in r["eksik"][:15]:
        print("  EKSİK   ", x["satir"][:110])
    for x in r["uydurma"][:15]:
        print(f"  UYDURMA  sahne {x['sahne']} {x['tur']}: {x['deger']} « {x['baglam'][:70]} »")
    for x in r["kontrol"][:10]:
        print(f"  KONTROL  sahne {x['sahne']} {x['ad']}: « {x['baglam'][:70]} »")


if __name__ == "__main__":
    main()
