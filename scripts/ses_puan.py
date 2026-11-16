#!/usr/bin/env python3
"""Ses kalitesi puanı (DNSMOS P.835, Microsoft; kod MIT, modeller CC-BY-4.0 — yalnızca CPU, ~1 MB ONNX).

Her cümle sesi için SIG (konuşma temizliği), BAK (arka plan gürültüsü: hışırtı/uğultu), OVRL (genel) ve
P808 (genel MOS) verir; 1–5 ölçeği, yüksek = iyi. BAK düşükse cümlede gürültü/hışırtı vardır.
Kullanım:
  python ses_puan.py sesler/                 # klasördeki tüm .wav'lar → sesler/ses_puan.json + özet
  python ses_puan.py sesler/ --esik-bak 3.5  # bu eşiğin altındakiler 'yeniden üret' listesine girer
Fikir kaynağı: microsoft/DNS-Challenge (DNSMOS), tarepan/SpeechMOS, VERSA (çok ölçütlü ses denetimi)."""
import argparse, json, sys, urllib.request
from pathlib import Path

import numpy as np

MODEL_DIZ = Path.home() / ".egitim_video" / "dnsmos"
KAYNAK = "https://raw.githubusercontent.com/microsoft/DNS-Challenge/master/DNSMOS/DNSMOS/"
SR, PENCERE = 16000, 9.01
ESIK_BAK, ESIK_OVRL = 3.2, 2.0      # B1 belgesinin 1270 cümlesiyle kalibre edildi (~%2 işaretlenir)


def modeller():
    MODEL_DIZ.mkdir(parents=True, exist_ok=True)
    for ad in ("sig_bak_ovr.onnx", "model_v8.onnx"):
        h = MODEL_DIZ / ad
        if not h.exists() or h.stat().st_size < 100_000:
            urllib.request.urlretrieve(KAYNAK + ad, h)
    import onnxruntime as ort
    o = ort.SessionOptions(); o.intra_op_num_threads = 2; o.log_severity_level = 3
    return (ort.InferenceSession(str(MODEL_DIZ / "sig_bak_ovr.onnx"), o),
            ort.InferenceSession(str(MODEL_DIZ / "model_v8.onnx"), o))


def _mel(x):
    import librosa
    m = librosa.feature.melspectrogram(y=x, sr=SR, n_fft=321, hop_length=160, n_mels=120)
    return ((librosa.power_to_db(m, ref=np.max) + 40) / 40).T


def _poly(sig, bak, ovr):   # DNSMOS P.835 kalibrasyonu (kişiselleştirilmemiş)
    return (np.poly1d([-0.08397278, 1.22083953, 0.0052439])(sig),
            np.poly1d([-0.13166888, 1.60915514, -0.39604546])(bak),
            np.poly1d([-0.06766283, 1.11546468, 0.04602535])(ovr))


def puanla(ses, sr, oturum):
    """ses: mono float dizi. Döner: {sig, bak, ovrl, p808}."""
    import librosa
    if sr != SR:
        ses = librosa.resample(np.asarray(ses, np.float32), orig_sr=sr, target_sr=SR)
    ses = np.asarray(ses, np.float32)
    n = int(PENCERE * SR)
    if len(ses) == 0:
        return None
    if len(ses) < n:               # kısa cümle: model 9 sn ister, kendini tekrarlayarak doldurulur (DNSMOS yöntemi)
        ses = np.tile(ses, int(np.ceil(n / len(ses))))[:n]
    ana, p808 = oturum
    adim = max(1, int(np.floor(len(ses) / SR - PENCERE)) + 1)
    s_, b_, o_, p_ = [], [], [], []
    for i in range(adim):
        par = ses[i * SR: i * SR + n]
        if len(par) < n:
            break
        sig, bak, ovr = ana.run(None, {"input_1": par[np.newaxis, :]})[0][0]
        s, b, o = _poly(sig, bak, ovr)
        p = p808.run(None, {"input_1": _mel(par[:-160]).astype(np.float32)[np.newaxis]})[0][0][0]
        s_.append(s); b_.append(b); o_.append(o); p_.append(p)
    return {"sig": round(float(np.mean(s_)), 2), "bak": round(float(np.mean(b_)), 2),
            "ovrl": round(float(np.mean(o_)), 2), "p808": round(float(np.mean(p_)), 2)}


def rapor_yaz(klasor, sonuc, esik_bak=ESIK_BAK, esik_ovrl=ESIK_OVRL):
    kotu = sorted([k for k, v in sonuc.items() if v["bak"] < esik_bak or v["ovrl"] < esik_ovrl],
                  key=lambda k: sonuc[k]["bak"])
    ozet = {}
    if sonuc:
        for olc in ("sig", "bak", "ovrl", "p808"):
            d = np.array([v[olc] for v in sonuc.values()])
            ozet[olc] = {"ort": round(float(d.mean()), 2), "en_dusuk": round(float(d.min()), 2),
                         "p10": round(float(np.percentile(d, 10)), 2)}
    rapor = {"ozet": ozet, "esik": {"bak": esik_bak, "ovrl": esik_ovrl}, "yeniden_uret": kotu, "cumleler": sonuc}
    (Path(klasor) / "ses_puan.json").write_text(json.dumps(rapor, ensure_ascii=False, indent=0), encoding="utf-8")
    return rapor


def klasor_puanla(klasor, esik_bak=ESIK_BAK, esik_ovrl=ESIK_OVRL, sessiz=False, sadece=None):
    import soundfile as sf
    oturum = modeller(); sonuc = {}
    eski = Path(klasor) / "ses_puan.json"          # önceden puanlanmış (önbellekten gelen) cümleler tekrar puanlanmaz
    if eski.exists():
        sonuc = json.loads(eski.read_text(encoding="utf-8")).get("cumleler", {})
    dosyalar = sorted(p for p in Path(klasor).glob("*.wav") if ".aday" not in p.name and p.stem not in sonuc
                      and not p.stem.startswith("_") and (sadece is None or p.stem in sadece))
    for i, f in enumerate(dosyalar):
        x, sr = sf.read(str(f), dtype="float32", always_2d=True)
        p = puanla(x.mean(1), sr, oturum)
        if p:
            sonuc[f.stem] = p
        if not sessiz and i % 100 == 0:
            print(f"  {i}/{len(dosyalar)}", file=sys.stderr)
    return rapor_yaz(klasor, sonuc, esik_bak, esik_ovrl)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("klasor")
    ap.add_argument("--birlestir", nargs="+", metavar="JSON", help="parça ses_puan json'larını klasörde birleştir")
    ap.add_argument("--esik-bak", type=float, default=3.2)
    ap.add_argument("--esik-ovrl", type=float, default=2.0)
    a = ap.parse_args()
    if a.birlestir:
        c = {}
        for f in a.birlestir:
            c.update(json.loads(Path(f).read_text(encoding="utf-8")).get("cumleler", {}))
        r = rapor_yaz(a.klasor, c, a.esik_bak, a.esik_ovrl)
    else:
        r = klasor_puanla(a.klasor, a.esik_bak, a.esik_ovrl)
    o = r["ozet"]
    print(f"{len(r['cumleler'])} cümle · SIG {o['sig']['ort']} · BAK {o['bak']['ort']} (en düşük {o['bak']['en_dusuk']}) · "
          f"OVRL {o['ovrl']['ort']} · P808 {o['p808']['ort']}")
    if r["yeniden_uret"]:
        print(f"{len(r['yeniden_uret'])} cümle eşik altında → --cumleler " + ",".join(r["yeniden_uret"][:60]))
    else:
        print("Tüm cümleler eşiğin üstünde ✔")


if __name__ == "__main__":
    main()
