#!/usr/bin/env python3
"""KALİTE KAPISI — teslimden önceki tek karar noktası (GEÇTİ / KALDI).

Bütün denetimleri tek raporda toplar; eşik aşılırsa video teslim edilmez (promptfoo/deepeval "assertion",
CI kalite kapısı fikri). Model/API gerektirmez; ölçülebilen her şey araçla ölçülür ("araç karar verir").
Ölçülemeyen anlam doğruluğu için ayrı bir HAKEM listesi üretir (SKILL.md adım 8b).

  Senaryo   : şema hataları, ekranda olup okunmayan metin, yerleşim (taşma) ve senkron uyarıları
  Sadakat   : belgeden eksik satır, belgede olmayan sayı/İngilizce (uydurma), {İngilizce} içinde Türkçe
  Ses       : DNSMOS gürültü/kalite puanı (ses_puan.json), Whisper telaffuz puanı (kalite_raporu.txt)
  Video     : LUFS, gerçek tepe, beklenmedik sessizlik (_denetim.json)

Kullanım:
  python kalite_kapisi.py senaryo.json --belge belge.md [--ayar ayar.json] [--ses-dizini sesler] [--video v.mp4]
Çıktı: senaryo_karar.md (+ .json). Çıkış kodu 0 = GEÇTİ, 1 = KALDI.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

BURASI = Path(__file__).resolve().parent
sys.path.insert(0, str(BURASI))
import video_uret as v  # noqa: E402
import sadakat  # noqa: E402

ESIK = {"whisper": 0.8, "ses_kotu_oran": 0.02}


def kapisi(senaryo, belge=None, ayar=None, ses_dizini=None, video=None, ses_puanla=False):
    sen = json.loads(Path(senaryo).read_text(encoding="utf-8"))
    ayar_d = json.loads(Path(ayar).read_text(encoding="utf-8")) if ayar else {}
    kritik, uyari, hakem, olcum = [], [], [], {}

    # --- senaryo
    for h in v.senaryo_dogrula(sen):
        kritik.append(f"Senaryo: {h}")
    okunmayan = [(i, o) for i, sh in enumerate(sen["sahneler"], 1) for o in v.okunmayanlar(sh)]
    olcum["okunmayan"] = len(okunmayan)
    for i, o in okunmayan[:20]:
        kritik.append(f"Sahne {i}: ekranda var, okunmuyor «{o[:60]}»")
    k = subprocess.run([sys.executable, str(BURASI / "video_uret.py"), str(senaryo), "--kontrol"] +
                       (["--ses-dizini", ses_dizini] if ses_dizini else []), capture_output=True, text=True)
    yer = [ln.strip() for ln in (k.stdout + k.stderr).splitlines() if "⚠ yerleşim" in ln or "⚠ senkron" in ln]
    olcum["yerlesim_senkron"] = len(yer)
    for ln in yer[:20]:
        (kritik if "yerleşim" in ln else uyari).append(ln.replace("⚠ ", ""))

    # --- sadakat
    if belge:
        r = sadakat.denetle(sen, Path(belge).read_text(encoding="utf-8", errors="ignore"), ayar_d)
        olcum["sadakat"] = r["ozet"]
        for x in r["eksik"]:
            kritik.append(f"Belgeden eksik: «{x['satir'][:90]}»")
        for x in r["uydurma"]:
            kritik.append(f"Sahne {x['sahne']}: belgede olmayan {x['tur']} «{x['deger']}»")
        for x in r["telaffuz"]:
            kritik.append(f"Sahne {x['sahne']}: İngilizce öbekte Türkçe ({', '.join(x['turkce'])}) «{x['oge'][:50]}»")
        for x in r["kontrol"]:
            hakem.append(f"Sahne {x['sahne']}: belgede geçmeyen ad «{x['ad']}» — {x['baglam'][:80]}")
        for x in r["eklenti"]:
            hakem.append(f"Eklenti ({x['soru']}): {x['metin'][:120]}")
    else:
        uyari.append("Kaynak belge verilmedi: sadakat/bilgi kirliliği denetimi yapılamadı (--belge).")

    # --- ses
    if ses_dizini:
        for d in ses_dizini.split(","):
            d = Path(d)
            sp = d / "ses_puan.json"
            if ses_puanla and not sp.exists():
                import ses_puan
                ses_puan.klasor_puanla(d, sessiz=True)
            if sp.exists():
                p = json.loads(sp.read_text(encoding="utf-8"))
                olcum.setdefault("ses_puan", {})[d.name] = p["ozet"]
                kotu = p["yeniden_uret"]; n = max(1, len(p["cumleler"]))
                msg = (f"Ses ({d.name}): {len(kotu)}/{n} cümle gürültü/kalite eşiğinin altında "
                       f"(BAK<{p['esik']['bak']} ya da OVRL<{p['esik']['ovrl']}): {', '.join(kotu[:12])}")
                if kotu:
                    (kritik if len(kotu) / n > ESIK["ses_kotu_oran"] else uyari).append(msg)
            else:
                uyari.append(f"Ses ({d.name}): ses_puan.json yok — `python scripts/ses_puan.py {d}` çalıştır.")
            kr = d / "kalite_raporu.txt"
            if kr.exists():
                dusuk = []
                for ln in kr.read_text(encoding="utf-8").splitlines():
                    pr = ln.split("\t")
                    if len(pr) > 2:
                        try:
                            if float(pr[1]) < ESIK["whisper"]:
                                dusuk.append(f"{pr[0]} ({pr[1]})")
                        except ValueError:
                            pass
                if dusuk:
                    uyari.append(f"Telaffuz (Whisper < {ESIK['whisper']}): {', '.join(dusuk[:15])}")
                    hakem.append("Whisper puanı düşük cümleleri dinle: " + ", ".join(dusuk[:15]))

    # --- video
    if video:
        dj = Path(video).with_name(Path(video).stem + "_denetim.json")
        if not dj.exists():
            v.yayin_denetimi(Path(video))
        if dj.exists():
            d = json.loads(dj.read_text(encoding="utf-8")); olcum["video"] = d
            for u in d.get("uyarilar", []):
                kritik.append(f"Video: {u}")

    karar = "GEÇTİ" if not kritik else "KALDI"
    return {"karar": karar, "kritik": kritik, "uyari": uyari, "hakem": hakem, "olcum": olcum}


def yaz(r, hedef):
    md = [f"# Kalite kapısı: **{r['karar']}**", ""]
    md += [f"Kritik: {len(r['kritik'])} · Uyarı: {len(r['uyari'])} · Hakem incelemesi: {len(r['hakem'])}", ""]
    for bas, ana in (("Kritik (düzeltilmeden teslim yok)", "kritik"), ("Uyarılar", "uyari"),
                     ("Hakem için (anlam doğruluğu — bağımsız gözden geçirme)", "hakem")):
        if r[ana]:
            md += [f"## {bas}"] + [f"- {x}" for x in r[ana]] + [""]
    md += ["## Ölçümler", "```json", json.dumps(r["olcum"], ensure_ascii=False, indent=1), "```"]
    hedef.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    hedef.with_suffix(".json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("senaryo")
    ap.add_argument("--belge"); ap.add_argument("--ayar"); ap.add_argument("--ses-dizini"); ap.add_argument("--video")
    ap.add_argument("--ses-puanla", action="store_true", help="ses_puan.json yoksa DNSMOS ile hesapla")
    ap.add_argument("-o", "--cikti")
    a = ap.parse_args()
    r = kapisi(a.senaryo, a.belge, a.ayar, a.ses_dizini, a.video, a.ses_puanla)
    hedef = Path(a.cikti or Path(a.senaryo).with_name(Path(a.senaryo).stem + "_karar"))
    yaz(r, hedef)
    print(f"KALİTE KAPISI: {r['karar']} · kritik {len(r['kritik'])} · uyarı {len(r['uyari'])} · "
          f"hakem {len(r['hakem'])} → {hedef.with_suffix('.md')}")
    for x in r["kritik"][:25]:
        print("  ✗ " + x)
    sys.exit(0 if r["karar"] == "GEÇTİ" else 1)


if __name__ == "__main__":
    main()
