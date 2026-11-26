# -*- coding: utf-8 -*-
"""Derslerdeki tüm İngilizce parçaları Kokoro (Apache-2.0) ile üretir; içerik anahtarıyla önbellekler.
Kalite kapısı: tek kelime / kısa kalıplar Whisper small.en ile dinlenir; doğru duyulmazsa aynı aksandaki
başka hız/ses denenir (Kokoro tek kelimede bazen kelimeyi bozar)."""
import json, re, sys
from pathlib import Path
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

sys.path.insert(0, "/home/claude/kurs")
import icerik, motor  # noqa: E402

CACHE = Path("/home/claude/kurs/en_cache2"); CACHE.mkdir(exist_ok=True)
SECIM = CACHE / "secim.json"
secim = json.load(open(SECIM)) if SECIM.exists() else {}
k = Kokoro("/home/claude/modeller/kokoro-v1.0.onnx", "/home/claude/modeller/voices-v1.0.bin")
YEDEK = {"b": ["bm_lewis", "bf_emma", "bf_isabella", "bm_daniel"], "a": ["af_heart", "am_michael", "af_bella", "am_adam"]}
_asr = []


def asr():
    if not _asr:
        import asr as a; _asr.append(a)
    return _asr[0]


def sentez(metin, ses, hiz):
    x, sr = k.create(metin, voice=ses, speed=hiz, lang="en-gb" if ses.startswith("b") else "en-us")
    return x.astype(np.float32)


def uret(metin, ses, hiz):
    key = motor.anahtar(metin, ses, round(hiz, 3))
    yol = CACHE / f"{key}.wav"
    if yol.exists():
        return yol
    kisa = len(metin.split()) <= 3 and not re.match(r"^[A-E]\.", metin)
    if not kisa:
        sf.write(yol, sentez(metin, ses, hiz), motor.SR); return yol
    a = asr()
    adaylar = [(ses, hiz), (ses, 0.95)] + [(v, 1.0) for v in YEDEK[ses[0]] if v != ses]
    ilk = None
    for v, h in adaylar:
        x = sentez(metin, v, h)
        ilk = ilk if ilk is not None else x
        duyulan = a.duy(x)
        if a.n(duyulan) == a.n(metin):
            sf.write(yol, x, motor.SR); secim[key] = {"metin": metin, "ses": v, "hiz": h, "ok": True}; return yol
    sf.write(yol, ilk, motor.SR); secim[key] = {"metin": metin, "ses": ses, "hiz": hiz, "ok": False}
    return yol


if __name__ == "__main__":
    for d in icerik.DERSLER:
        for x in motor.plan(d):
            if x[0] == "E":
                uret(x[1], x[2], x[3])
        json.dump(secim, open(SECIM, "w"), ensure_ascii=False, indent=0)
        print(d["id"], "tamam", flush=True)
    kotu = [v for v in secim.values() if not v["ok"]]
    print(len(secim), "kısa klip denetlendi;", len(kotu), "tanesi hiçbir seste doğru duyulmadı:",
          ", ".join(v["metin"] for v in kotu))
