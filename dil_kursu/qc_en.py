# -*- coding: utf-8 -*-
"""İngilizce klipleri Whisper small.en (sherpa-onnx) ile yazıya döküp metinle karşılaştırır."""
import difflib, json, re, sys
from pathlib import Path
import numpy as np, soundfile as sf, sherpa_onnx

M = "/home/claude/modeller/sherpa-onnx-whisper-small.en/small.en-"
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M + "encoder.int8.onnx", decoder=M + "decoder.int8.onnx",
                                                 tokens=M + "tokens.txt", language="en", task="transcribe", num_threads=2)
SAYI = {"1773": "seventeen seventy three"}


def norm(t):
    t = t.lower().replace("’", "'")
    for k, v in SAYI.items():
        t = t.replace(k, v)
    t = t.replace("-", " ").replace("analyze", "analyse").replace("analyzed", "analysed")
    return re.sub(r"[^a-z0-9' ]+", " ", t).split()


cache = Path("/home/claude/kurs/en_cache")
dz = json.load(open(cache / "dizin.json"))
sonuc, kotu = {}, []
for ad, v in dz.items():
    x, sr = sf.read(cache / ad, dtype="float32")
    s = rec.create_stream(); s.accept_waveform(sr, x); rec.decode_stream(s)
    duy = s.result.text.strip()
    a, b = norm(v["metin"]), norm(duy)
    oran = difflib.SequenceMatcher(None, a, b).ratio()
    sonuc[ad] = {"metin": v["metin"], "duyulan": duy, "oran": round(oran, 3), "ses": v["ses"]}
    if oran < 0.9:
        kotu.append((oran, v["metin"], duy, v["ses"], ad))
json.dump(sonuc, open("/home/claude/kurs/qc_en.json", "w"), ensure_ascii=False, indent=0)
print(f"{len(sonuc)} klip, {len(kotu)} şüpheli (<0.90)")
for k in sorted(kotu):
    print(f"{k[0]:.2f} | {k[1]} | duyulan: {k[2]} | {k[3]} | {k[4]}")
