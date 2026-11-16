#!/usr/bin/env python3
"""Belgenin TAMAMINI senaryo taslağına çevirir: hiçbir başlık, madde, tablo satırı ya da alıştırma sorusu atlanmaz.

Kullanım:
    python belge_oku.py belge.docx -o belge.md
    python belge_senaryo.py belge.md ayar.json -o senaryo.json

Ne üretir:
- Her ## / ### başlık → yeni bölüm (YouTube bölümü + tahta alt bilgisi)
- Paragraf → ipucu (kısa) ya da metin (uzun) sahnesi; anlatım = paragrafın kendisi
- Madde listesi → en fazla 4 maddelik "maddeler" sahneleri; tahtada kalın başlık, anlatımda maddenin tamamı
- Tablo → en fazla 4 satırlık "tablo" sahneleri, TÜM sütunlar; her satır ayrı cümleyle okunur
- Alıştırma (numaralı liste, boşluklu ya da (a)(b)(c) seçenekli) → her soru ayrı "soru" sahnesi: soru ve seçenekler
  okunur, geri sayım, doğru cevap ve kısa açıklama. Cevaplar/açıklamalar ayar dosyasından gelir.
- *italik* (İngilizce örnekler) → {İngilizce} işareti; kalan İngilizce kelimeler wordfreq ile işaretlenir.

Ayar dosyası (JSON):
  "degistir":   {"WSE'nin": "kursun", ...}         metin değişimleri (ör. kurum adını çıkarmak)
  "cevaplar":   {"Alıştırma X": ["b", "a", ...], "Alıştırma G-A": ["have lived", ...]}
  "aciklamalar":{"Alıştırma X": ["...", ...]}
  "atla_satir": ["Nov 14, 2026"]                  yalnızca biçim satırları (içerik değil!)
  "sira":       {"D1 soruları": "D1"}             blok yeniden sıralama (ör. dinleme: soru → metin → cevap)
Taslak her zaman `video_uret.py --kontrol` ile denetlenmeli ve elle cilalanmalıdır.
"""
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import video_uret as v  # noqa: E402

HARF = "abcd"


# ------------------------------------------------------------------ markdown ayrıştırma
def bloklar(md):
    satirlar = md.splitlines()
    out, i = [], 0
    while i < len(satirlar):
        s = satirlar[i].rstrip()
        if not s.strip():
            i += 1; continue
        m = re.match(r"^(#{1,4})\s+(.*)", s)
        if m:
            out.append(("baslik", len(m.group(1)), m.group(2).strip())); i += 1; continue
        if s.lstrip().startswith("|"):
            tablo = []
            while i < len(satirlar) and satirlar[i].lstrip().startswith("|"):
                hucre = [c.strip() for c in satirlar[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in hucre if c):
                    tablo.append(hucre)
                i += 1
            out.append(("tablo", tablo[0], tablo[1:])); continue
        if re.match(r"^\s*[*•-]\s+", s):
            liste = []
            while i < len(satirlar) and re.match(r"^\s*[*•-]\s+", satirlar[i]):
                liste.append(re.sub(r"^\s*[*•-]\s+", "", satirlar[i]).strip()); i += 1
            out.append(("madde", liste)); continue
        if re.match(r"^\s*\d+\.\s+", s):
            liste = []
            while i < len(satirlar) and re.match(r"^\s*\d+\.\s+", satirlar[i]):
                liste.append(re.sub(r"^\s*\d+\.\s+", "", satirlar[i]).strip()); i += 1
            out.append(("numara", liste)); continue
        out.append(("paragraf", s.strip())); i += 1
    return out


# ------------------------------------------------------------------ metin temizleme
SEMBOL = [("⚠️", ""), ("☐", ""), ("✓", ""), ("✗", ""), ("\\_", "_"), ("\\", "")]


def ekran(t):
    """Tahtada görünecek hali: markdown işaretleri kalkar, semboller kalır."""
    for a, b in SEMBOL:
        t = t.replace(a, b)
    t = re.sub(r"~~(.+?)~~", r"\1 ✗", t)
    t = t.replace("***", "").replace("**", "").replace("*", "")
    t = re.sub(r"_{2,}", "___", t)
    return re.sub(r"\s+", " ", t).strip()


def anlatim(t, ayar):
    """Seslendirilecek hali: italik İngilizce → {…}; semboller okunur hale gelir."""
    for a, b in SEMBOL:
        t = t.replace(a, b)
    for a, b in ayar.get("degistir", {}).items():
        t = t.replace(a, b)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)                         # bağlantılar
    t = re.sub(r"\[([^\]]+)\]", r"⟦\1⟧", t)            # [yer], [kimle]: şablon boşluğu Türkçedir, İngilizce öbeğe girmez
    t = re.sub(r"~~(.+?)~~", r"\1 ⟦değil⟧", t)
    t = t.replace("***", "*")                                              # kalın-italik → italik
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)                                 # kalın → düz
    t = re.sub(r"\*\s+\*", " ", t)                                         # bitişik italik parçaları birleştir
    t = re.sub(r"\*([^*]+)\*", lambda m: m.group(1) if re.search(r"[çğıöşüÇĞİÖŞÜ]", m.group(1))
               else "{" + m.group(1).strip() + "}", t)              # italik Türkçe vurgu İngilizce değildir
    t = t.replace("*", "")
    t = re.sub(r"_{2,}", " boşluk ", t)
    rep = [(" → ", ", "), ("→", ", "), (" · ", ", "), ("·", ", "), (" ≠ ", " değil, "), (" = ", ", yani "),
           ("…", ""), ("—", ","), (" – ", ", "), ("BrE", "İngiliz İngilizcesi"), ("V-ing", "fiilin ing hali"),
           ("V1", "fiilin yalın hali"), ("V2", "fiilin ikinci hali"), ("V3", "fiilin üçüncü hali"), ("-ing", "ing takısı"),
           (" + ", " ve "), ("(a)", "a,"), ("(b)", "be,"), ("(c)", "ce,"), ("(d)", "de,")]
    for a, b in rep:
        t = t.replace(a, (" " if a.startswith(" ") else "") + f"⟦{b.strip()}⟧" + (" " if a.endswith(" ") else "")
                      if re.search(r"[a-zçğıöşü]", b) else b)
    # Türkçe karşılıklar ({…} İngilizce öbeğinin içine düşmüşse) öbeğin dışına çıkar: aksi halde İngilizce okunur
    t = re.sub(r"\{([^{}]*)\}", lambda m: "{" + re.sub(r"\s*⟦([^⟧]*)⟧\s*", r"} \1 {", m.group(1)) + "}", t)
    t = re.sub(r"\{[\s,;:]*\}", " ", t)
    t = re.sub(r"\{\s*([,;:]?)\s*", r"{", t); t = re.sub(r"\s*\}", "}", t)
    t = re.sub(r"\s+", " ", t).strip()
    # parantez dışındaki İngilizceyi işaretle (wordfreq)
    try:
        parca = re.split(r"(\{[^}]*\}|⟦[^⟧]*⟧)", t)
        t = "".join(p if p.startswith(("{", "⟦")) else v.ingilizce_isaretle(p) for p in parca)
    except Exception:
        pass
    t = re.sub(r"\s*\(\}", "} (", t); t = re.sub(r"\{\)", ") {", t)               # öbek sınırında kalan parantez
    t = re.sub(r"(?<![{\w])(in|on|at|by|for|since)(?= ve )", r"{\1}", t)       # "on ve gün": on = İngilizce edat
    t = re.sub(r"\{([^\w{}]*)\}", r"\1", t)                                # yalnızca noktalama içeren öbek
    t = re.sub(r"\}(\s*)\{(?=(ing|ed|es|s|er|est|ly|n't)\b)", "", t)       # smok{ing} → smoking (kelime içi vurgu)
    t = re.sub(r"\}(\s*)\{", lambda m: m.group(1) or ", ", t)              # {a} {b} → {a b}; {a}{b} → {a, b}
    t = re.sub(r"\}(\s+)(\d[\d:.,]*)(?![\wçğıöşü'])", r"\1\2}", t)             # {in} 2019 → {in 2019}
    t = re.sub(r"\{([^}]*)\}", lambda m: "{" + m.group(1).replace(" / ", ", ").replace("/", ", ") + "}", t)
    t = t.replace(" / ", " ya da ")
    t = re.sub(r"\s+([,.;:!?])", r"\1", t); t = re.sub(r",\s*,", ",", t)
    # cümlenin çoğu İngilizceyse tamamı tek İngilizce öbek olsun (parça parça okunmasın)
    cumleler = re.split(r"(?<=[.!?])\s+(?![^{]*\})", t)
    yeni = []
    for c in cumleler:
        harf = len(re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü]", c))
        en = sum(len(re.findall(r"[A-Za-z]", x)) for x in re.findall(r"\{([^}]*)\}", c))
        disari = re.sub(r"\{[^}]*\}", " ", c)
        tr_kelime = (re.findall(r"(?<![{\w])[\wçğıöşüÇĞİÖŞÜ]*[çğıöşüÇĞİÖŞÜ][\wçğıöşüÇĞİÖŞÜ]*", disari) +
                     re.findall(r"\b(?:ve|ya da|veya|yani|değil|ile|gibi)\b|⟦", disari))
        if harf and en / harf >= 0.6 and not tr_kelime:
            c = "{" + c.replace("{", "").replace("}", "") + "}"
        yeni.append(c)
    t = " ".join(yeni)
    while "⟦" in t:
        t2 = re.sub(r"⟦([^⟦⟧]*)⟧", r"\1", t)
        if t2 == t:
            t = t.replace("⟦", "").replace("⟧", ""); break
        t = t2
    if t and t[-1] not in ".!?…}":
        t += "."
    return t


def kisa_baslik(t, n=40):
    """Tahta başlığı: parantez içi açıklamalar ve uzun kuyruk atılır."""
    t = re.sub(r"\s*\([^)]*\)", "", t).strip()
    t = re.sub(r"^\d+\.\s+", "", t)
    if len(t) > n:
        t = re.split(r"[:—–]", t)[0].strip()
    if len(t) > n:
        t = t[:n].rsplit(" ", 1)[0] + "…"
    return t


def lead(madde):
    """Maddenin tahtadaki kısa hali: '**Başlık:** açıklama' → 'Başlık'; yoksa ilk ~44 karakter."""
    m = re.match(r"^\*\*(.+?)\*\*", madde)
    if m and len(ekran(m.group(1))) >= 3:
        return ekran(m.group(1)).rstrip(":.")
    e = ekran(madde)
    if len(e) <= 46:
        return e
    kes = e[:46].rsplit(" ", 1)[0]
    return kes.rstrip(",;:") + "…"


# ------------------------------------------------------------------ sahne üreticiler
def madde_sahneleri(baslik, liste, ayar, numarali=False):
    out = []
    for k in range(0, len(liste), 4):
        parca = liste[k:k + 4]
        ad = f"{baslik}" + (f" ({k // 4 + 1}/{(len(liste) + 3) // 4})" if len(liste) > 4 else "")
        maddeler = [(f"{k + j + 1}. " if numarali else "") + lead(m) for j, m in enumerate(parca)]
        cumleler = [anlatim(m, ayar) for m in parca]
        out.append({"baslik": ad, "maddeler": maddeler, "anlatim": " ".join(cumleler)})
    return out


def tablo_sahneleri(baslik, bas, satirlar, ayar):
    out = []
    n_ = 4 if len(bas) <= 2 else 3                          # çok sütunlu tablolarda sahne başına 3 satır
    gruplar, g, uz = [], [], 0
    for r in satirlar:                                      # uzun hücreli satırlar daha az satırla: yazı küçülmesin
        L = sum(len(ekran(x)) for x in r)
        if g and (len(g) >= n_ or uz + L > 230):
            gruplar.append(g); g, uz = [], 0
        g.append(r); uz += L
    if g:
        gruplar.append(g)
    for gi, parca in enumerate(gruplar):
        ad = baslik + (f" ({gi + 1}/{len(gruplar)})" if len(gruplar) > 1 else "")
        cumleler = []
        for r in parca:
            r = r + [""] * (len(bas) - len(r))
            c = anlatim(r[0], ayar).rstrip(".") + ": " + anlatim(r[1], ayar).rstrip(".") + "."
            for h, x in zip(bas[2:], r[2:]):
                if x.strip():
                    c += f" {ekran(h)}: " + anlatim(x, ayar)
            cumleler.append(c if c.endswith((".", "?", "!", "}")) else c + ".")
        out.append({"baslik": ad, "tur": "tablo",
                    "tablo": {"basliklar": [ekran(h) for h in bas],
                              "satirlar": [[ekran(x) for x in r] for r in parca]},
                    "anlatim": " ".join(cumleler)})
    return out


def secenek_ayir(metin):
    """'Soru metni (a) x (b) y (c) z' → ('Soru metni', ['x','y','z'])"""
    m = re.split(r"\s*\(([a-d])\)\s*", metin)
    if len(m) >= 5:
        return m[0].strip(), [x.strip() for x in m[2::2]]
    return metin.strip(), []


def secenek_okunus(x, ayar):
    """Seçenek/cevap tamamen Latin harfli bir İngilizce öbekse İngilizce okunur ({…}); değilse normal anlatım."""
    e = ekran(x).strip().rstrip(".")
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9' ,:/()!?\-]*", e) and len(e) > 0:
        e = re.sub(r"\s*/\s*", ", ", e)
        return "{" + e + "}"
    return anlatim(x, ayar).rstrip(".")


def soru_sahneleri(blok, sorular, ayar, baslik):
    cev = ayar.get("cevaplar", {}).get(blok)
    aci = ayar.get("aciklamalar", {}).get(blok, [])
    if not cev:
        print(f"  ! '{blok}' için cevap yok: sorular cevapsız okunacak", file=sys.stderr)
    out = []
    for n, ham in enumerate(sorular, 1):
        soru_m, sec = secenek_ayir(ham)
        c = (cev[n - 1] if cev and n - 1 < len(cev) else "").strip()
        acik = aci[n - 1] if n - 1 < len(aci) else ""
        sh = {"baslik": f"{baslik} · {n}/{len(sorular)}", "tur": "soru", "soru": {"metin": ekran(soru_m), "bekle": 4}}
        soru_okunus = anlatim(soru_m, ayar)
        ing = anlatim(re.sub(r"_{2,}", " blank ", soru_m.replace("\\_", "_")), ayar)
        if ing.startswith("{") and ing.rstrip(".").endswith("}") and ing.count("{") == 1:
            soru_okunus = ing                                    # tamamen İngilizce soru: "blank" ile, tek akışta
        else:
            on_, govde = "", ekran(re.sub(r"_{2,}", " blank ", soru_m.replace("\\_", "_")))
            m_ = re.match(r"^([A-ZÇĞİÖŞÜ][a-zçğıöşü]+:)\s*(.*)", govde)
            if m_ and re.search(r"[çğıöşü]", m_.group(1).lower() + "ş" * 0) or (m_ and m_.group(1) in ("Anons:",)):
                on_, govde = m_.group(1) + " ", m_.group(2)
            govde = govde.replace("İ", "I")
            if not re.search(r"[çğıöşüÇĞÖŞÜ]", govde) and len(re.findall(r"[A-Za-z]+", govde)) >= 3:
                soru_okunus = on_ + "{" + govde.replace("{", "").replace("}", "") + "}"
        if soru_okunus.endswith("}") and soru_okunus[-2:-1] not in (".", "?", "!"):
            soru_okunus += "."
        cumle = [f"Soru {v.sayi_yazi(n)}.", soru_okunus]
        if sec:
            harf = c[:1].lower() if c and c[:1].lower() in HARF and (len(c) == 1 or not c[1].isalpha()) else None
            sh["soru"]["secenekler"] = [ekran(x) for x in sec]
            sh["soru"]["dogru"] = HARF.index(harf) if harf else 0
            okunus = "; ".join(f"{'ABCD'[i]}, {secenek_okunus(x, ayar)}" for i, x in enumerate(sec))
            cumle.append(f"Seçenekler: {okunus}.")
            dogru_metin = secenek_okunus(sec[sh['soru']['dogru']], ayar)
            cumle.append(f"Doğru cevap {'ABCD'[sh['soru']['dogru']]}: {dogru_metin}.")
        else:
            sh["soru"]["cevap"] = ekran(c) if c else "(cevap anahtarına bak)"
            cumle.append(f"Doğru cevap: {secenek_okunus(c, ayar)}." if c else "Cevabı rehberdeki anahtarda.")
        if acik:
            cumle.append(acik if acik.endswith((".", "!", "?")) else acik + ".")
        sh["anlatim"] = " ".join(cumle)
        cs = v.cumlelere_bol(sh["anlatim"])
        sh["soru"]["cevap_cumle"] = next(i for i, x in enumerate(cs) if x.startswith("Doğru cevap") or x.startswith("Cevabı"))
        out.append(sh)
    return out


def metin_sahneleri(baslik, paragraflar, ayar, kelime_siniri=70):
    """Uzun metin (okuma parçası, dinleme metni, model cevap) → okunabilir parçalara bölünmüş 'metin' sahneleri."""
    out, kova, say = [], [], 0
    for p in paragraflar:
        e_ = ekran(p)
        if re.fullmatch(r"\*\*[^*]+\*\*", p.strip()) and e_[-1:] not in ".!?:":
            e_ += "."                                            # kalın başlık satırı ayrı cümle olsun
        cumleler = re.split(r"(?<=[.!?])\s+", e_)
        for c in cumleler:
            w = len(c.split())
            if kova and say + w > kelime_siniri:
                out.append(kova); kova, say = [], 0
            kova.append(c); say += w
        kova.append("\n")
    if [x for x in kova if x != "\n"]:
        out.append(kova)
    sahneler = []
    for i, k in enumerate(out, 1):
        metin = " ".join(k).replace(" \n ", "\n").replace(" \n", "\n").strip()
        okunus = anlatim(metin.replace("\n", " "), ayar)
        sahneler.append({"baslik": baslik + (f" ({i}/{len(out)})" if len(out) > 1 else ""), "tur": "metin",
                         "metin": metin, "anlatim": okunus})
    if sahneler and v.kapsam_orani(baslik, sahneler[0]["anlatim"]) < 0.6:   # başlık ekranda: okunmalı
        sahneler[0]["anlatim"] = anlatim(baslik, ayar).rstrip(".") + ". " + sahneler[0]["anlatim"]
    return sahneler


# ------------------------------------------------------------------ ana akış
def donustur(md, ayar):
    bl = bloklar(md)
    atla = set(ayar.get("atla_satir", []))
    sahneler, bolum, alt_baslik, bekleyen_bolum = [], "", "", None
    ex_ad = None
    yerine = ayar.get("yerine", {})
    metin_b = set(ayar.get("metin_bolumleri", []))
    atla_bolum = False
    ust_basliklar = []          # (## başlık, o başlıktan sonraki ilk sahnenin sırası): ekranda görünen başlık okunmalı
    bekleyen_ust = False
    i = 0
    while i < len(bl):
        b = bl[i]
        if b[0] == "baslik":
            if b[1] == 1:
                i += 1; continue
            ad = ekran(b[2])
            for a, x in ayar.get("degistir", {}).items():
                ad = ad.replace(a, x)
            if b[1] == 2:
                ust_basliklar.append((ad, len(sahneler)))
            alt_baslik = ad; ex_ad = None
            if b[1] <= 2 or not atla_bolum:                   # "yerine" ile değişen bölümün alt başlıkları da atlanır
                atla_bolum = False
            elif atla_bolum:
                i += 1; continue
            if b[1] <= 3 and not (b[1] == 3 and bekleyen_ust and bekleyen_bolum):
                bekleyen_bolum = ad              # ## hemen ardından ### gelirse bölüm adı ## kalır
            bekleyen_ust = b[1] == 2
            if ad in yerine:                              # bu bölüm elle yazılmış sahnelerle değişir
                yeni = [dict(x) for x in yerine[ad]]
                yeni[0]["bolum"] = bekleyen_bolum or ad; bekleyen_bolum = None
                sahneler += yeni; atla_bolum = True
            i += 1; continue
        if atla_bolum:
            i += 1; continue
        if b[0] == "paragraf" and alt_baslik in metin_b and not re.match(r"^\*\*(Alıştırma|Yöntem)", b[1]):
            # ardışık paragraflar tek parça metin olur; yalnızca kalın kısa satır ("**D1**") yeni parça başlatır
            baslik_, paragraflar = alt_baslik, []
            while i < len(bl) and bl[i][0] == "paragraf":
                t = bl[i][1]
                if re.fullmatch(r"\*\*[^*]{1,12}\*\*", t):
                    if paragraflar:
                        yeni = metin_sahneleri(baslik_, paragraflar, ayar)
                        if bekleyen_bolum:
                            yeni[0]["bolum"] = bekleyen_bolum; bekleyen_bolum = None
                        sahneler += yeni; paragraflar = []
                    baslik_ = f"Dinleme metni {ekran(t)}" if "Dinleme" in str(ayar.get("dinleme_adi", "Dinleme")) else ekran(t)
                else:
                    paragraflar.append(t)
                i += 1
            if paragraflar:
                yeni = metin_sahneleri(baslik_, paragraflar, ayar)
                if bekleyen_bolum:
                    yeni[0]["bolum"] = bekleyen_bolum; bekleyen_bolum = None
                sahneler += yeni
            continue
        yeni = []
        if b[0] == "paragraf":
            if b[1] in atla:
                i += 1; continue
            m = re.match(r"^\*\*(Alıştırma [^*]+|[A-Z]-bonus)\*\*\s*(.*)", b[1])
            if m:                                        # alıştırma başlığı paragrafı
                ex_ad = ekran(m.group(1)); talimat = m.group(2)
                if talimat:
                    yeni = [{"baslik": ex_ad, "tur": "ipucu", "ipucu": {"tip": "not", "metin": ekran(talimat)},
                             "anlatim": f"{ex_ad}. " + anlatim(talimat, ayar), "goster": [1]}]
            elif re.match(r"^\*\*Cevaplar:\*\*", b[1]):
                i += 1; continue                         # cevaplar sorularla birlikte okunuyor
            else:
                metin = ekran(b[1])
                if len(metin.split()) > 28:
                    yeni = metin_sahneleri(alt_baslik, [b[1]], ayar)
                else:
                    yeni = [{"baslik": alt_baslik, "tur": "ipucu", "ipucu": {"tip": "not", "metin": metin},
                             "anlatim": anlatim(b[1], ayar), "goster": [0]}]
        elif b[0] == "madde":
            yeni = madde_sahneleri(alt_baslik, b[1], ayar)
        elif b[0] == "tablo":
            yeni = tablo_sahneleri(alt_baslik, b[1], b[2], ayar)
        elif b[0] == "numara":
            sorulu = any("___" in ekran(x) or re.search(r"\([a-d]\)", x) or x.rstrip().endswith("?")
                         or re.search(r"\([^()]+ / [^()]+\)", x) for x in b[1])
            blok = ex_ad or alt_baslik
            if blok in ayar.get("liste_olarak", []):
                sorulu = False
            if sorulu and (blok in ayar.get("cevaplar", {}) or "Alıştırma" in blok or "soru" in blok.lower()):
                yeni = soru_sahneleri(blok, b[1], ayar, blok)
            else:
                yeni = madde_sahneleri(alt_baslik, b[1], ayar, numarali=True)
        if yeni:
            if bekleyen_bolum:
                yeni[0]["bolum"] = bekleyen_bolum
                giris = re.sub(r"^[A-ZÇĞİÖŞÜ]?\d*[A-Z]?[.\-–—]\s*|^[A-Z]-[A-Z]\.\s*", "", bekleyen_bolum).strip()
                if giris and not yeni[0]["anlatim"].startswith(giris[:15]):
                    yeni[0]["anlatim"] = anlatim(giris, ayar).rstrip(".") + ". " + yeni[0]["anlatim"]
                    if yeni[0].get("tur") == "soru":
                        yeni[0]["soru"]["cevap_cumle"] += len(v.cumlelere_bol(anlatim(giris, ayar)))
                    if yeni[0].get("tur") == "ipucu" and yeni[0].get("goster"):
                        yeni[0]["goster"] = [1]
                bekleyen_bolum = None
            sahneler += yeni
        i += 1
    # ## başlığı videoda okunmuyorsa bölümün ilk sahnesine eklenir ("ekrandaki/belgedeki her şey okunur")
    for ad, k in ust_basliklar:
        if k < len(sahneler) and v.kapsam_orani(ad, sahneler[k].get("anlatim", "")) < 0.6 \
                and not (k > 0 and v.kapsam_orani(ad, sahneler[k - 1].get("anlatim", "")) >= 0.6):
            sahneler[k]["anlatim"] = anlatim(ad, ayar).rstrip(".") + ". " + sahneler[k].get("anlatim", "")

    return sahneler


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("belge_md"); ap.add_argument("ayar"); ap.add_argument("-o", "--cikti", required=True)
    a = ap.parse_args()
    ayar = json.loads(Path(a.ayar).read_text(encoding="utf-8"))
    md = Path(a.belge_md).read_text(encoding="utf-8")
    for x, y in ayar.get("on_degistir", {}).items():
        md = md.replace(x, y)
    sahneler = donustur(md, ayar)
    for blok, metin_ad in ayar.get("once_metin", {}).items():   # ör. dinleme: önce metin, sonra sorular
        m_ = [s for s in sahneler if s.get("tur") == "metin" and s["baslik"].startswith(metin_ad)]
        if not m_:
            continue
        for s in m_:
            sahneler.remove(s)
        i_ = next(i for i, s in enumerate(sahneler) if s["baslik"].startswith(blok))
        if "bolum" in sahneler[i_]:
            m_[0]["bolum"] = sahneler[i_].pop("bolum")
        sahneler[i_:i_] = m_
    for ek in ayar.get("ekle", []):                       # elle yazılmış sahneler (giriş, kapanış, yeniden sıralama)
        sahneler.insert(ek["sira"] if ek["sira"] >= 0 else len(sahneler) + 1 + ek["sira"], ek["sahne"])
    for s_ in sahneler:                                   # tahta başlığı kısa; parça numarası korunur
        m_ = re.search(r"\s(\(\d+/\d+\)|·\s*\d+/\d+)$", s_["baslik"])
        ek_ = (" " + m_.group(1)) if m_ else ""
        govde_ = s_["baslik"][:m_.start()] if m_ else s_["baslik"]
        s_["baslik"] = kisa_baslik(govde_, 40 - len(ek_)) + ek_
    sen = {"baslik": ayar.get("baslik", "Eğitim videosu"), "alt_baslik": ayar.get("alt_baslik", ""),
           "youtube_baslik": ayar.get("youtube_baslik", ""), "etiketler": ayar.get("etiketler", []),
           "kapanis": ayar.get("kapanis", "Başarılar!"), "telaffuz": ayar.get("telaffuz", {}),
           "telaffuz_kok": ayar.get("telaffuz_kok", {}), "sahneler": sahneler}
    Path(a.cikti).write_text(json.dumps(sen, ensure_ascii=False, indent=1), encoding="utf-8")
    n_soru = sum(1 for s in sahneler if s.get("tur") == "soru")
    kel = sum(len(v.temiz(s["anlatim"]).split()) for s in sahneler)
    print(f"✔ {a.cikti}: {len(sahneler)} sahne, {n_soru} soru, ~{kel} kelime (≈{kel / 120:.0f} dk)")


if __name__ == "__main__":
    main()
