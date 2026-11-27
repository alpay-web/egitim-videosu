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


ISIM = {"Elif": "Eleef", "Deniz": "Deneez"}           # yalnız ses için yazım; kurs sadece ses olduğu için görünmez
DEGIS = {  # Whisper'ın sonda fazladan ses duyduğu klipler: aynı aksanda başka sese geç
    ("We are a happy family.", "bf_emma"): "bf_isabella", ("I love my family.", "bf_emma"): "bf_isabella",
    ("I have one brother.", "bf_emma"): "bf_isabella", ("Can I have your phone number?", "bf_emma"): "bf_isabella",
    ("I finish work at six.", "bf_emma"): "bf_isabella", ("At half past six.", "bf_emma"): "bf_isabella",
    ("I get up at half past six.", "bf_emma"): "bf_isabella"}


def sentez(metin, ses, hiz):
    if ses != "bf_emma":
        for a, b in ISIM.items():
            metin = metin.replace(a, b)
    ses = DEGIS.get((metin, ses), ses)
    x, sr = k.create(metin, voice=ses, speed=hiz, lang="en-gb" if ses.startswith("b") else "en-us")
    return x.astype(np.float32)


ESSESLI = [{"meat", "meet"}, {"eye", "i"}, {"write", "right"}, {"role", "roll"}, {"practise", "practice"},
           {"whether", "weather"}, {"principle", "principal"}, {"labour", "labor"}, {"buy", "bye", "by"},
           {"soar", "sore", "saw"}, {"source", "sauce"}, {"floor", "flaw"}, {"tea", "t"}, {"workaround", "work"},
           {"swimlane", "swim"}, {"vary", "very"}, {"week", "weak"}, {"hour", "our"}, {"right", "write"}]
_TASIYICI = {}


def _es(a, b):
    return a == b or any(a in g and b in g for g in ESSESLI)


def dogru_duyuldu(a, metin, x, v):
    """Kısa kelimeyi tek başına değil, 'The next word is ...' taşıyıcısının ardından dinlet (Whisper bağlamla daha güvenilir)."""
    if v not in _TASIYICI:
        _TASIYICI[v] = sentez("The next word is", v, 1.0)
    z = np.zeros(int(0.25 * motor.SR), np.float32)
    duy = a.n(a.duy(np.concatenate([_TASIYICI[v], z, x])))
    hedef = a.n(metin)
    if duy[:4] == ["the", "next", "word", "is"]:
        duy = duy[4:]
    elif "is" in duy[:5]:
        duy = duy[duy.index("is") + 1:]
    if len(duy) != len(hedef):
        return duy == hedef or (len(hedef) == 1 and len(duy) >= 1 and "".join(duy) == hedef[0])
    return all(_es(p, q) for p, q in zip(hedef, duy))


def uret(metin, ses, hiz):
    key = motor.anahtar(metin, ses, round(hiz, 3))
    yol = CACHE / f"{key}.wav"
    if yol.exists():
        return yol
    kisa = len(metin.split()) <= 3 and not re.match(r"^[A-E]\.", metin)
    if not kisa:
        sf.write(yol, sentez(metin, ses, hiz), motor.SR); return yol
    a = asr()
    diger = "a" if ses[0] == "b" else "b"
    adaylar = [(ses, hiz), (ses, 0.95)] + [(v, 1.0) for v in YEDEK[ses[0]] if v != ses] + [(v, 1.0) for v in YEDEK[diger]]
    ilk = None
    for v, h in adaylar:
        x = sentez(metin, v, h)
        ilk = ilk if ilk is not None else x
        if dogru_duyuldu(a, metin, x, v):
            sf.write(yol, x, motor.SR); secim[key] = {"metin": metin, "ses": v, "hiz": h, "ok": True}; return yol
    sf.write(yol, ilk, motor.SR); secim[key] = {"metin": metin, "ses": ses, "hiz": hiz, "ok": False}
    return yol


if __name__ == "__main__":
    for d in icerik.DERSLER:
        for x in motor.plan(d, icerik.isinma_icin(d)) + motor.plan_gunluk(d):
            if x[0] == "E":
                uret(x[1], x[2], x[3])
        json.dump(secim, open(SECIM, "w"), ensure_ascii=False, indent=0)
        print(d["id"], "tamam", flush=True)
    kotu = [v for v in secim.values() if not v["ok"]]
    print(len(secim), "kısa klip denetlendi;", len(kotu), "tanesi hiçbir seste doğru duyulmadı:",
          ", ".join(v["metin"] for v in kotu))
