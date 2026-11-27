# -*- coding: utf-8 -*-
"""Türkçe anlatıcı karşılaştırması: aynı cümleleri bir motorla üretir ve Whisper ile denetler.
Kullanım: python uret.py MOTOR CIKTI_KLASORU
Motorlar: ema, ahenk_cep, freya, seslen_ayse, seslen_emre, trendyol, edge_emel, edge_ahmet
(Chatterbox varyantları depodaki video_uret.py ile ayrı adımda üretilir.)"""
import json, sys, time, subprocess
from pathlib import Path
import numpy as np, soundfile as sf

BURA = Path(__file__).resolve().parent
CUMLELER = json.load(open(BURA / "cumleler.json"))
REF_METIN = ("Merhaba, ben bu kursun anlatıcısıyım. Her gün biraz pratik yaparak İngilizcenizi adım adım "
             "geliştireceğiz. Acele etmeyin; dinleyin, tekrar edin ve kendinize güvenin. Hazırsanız başlayalım.")


def motor(ad):
    if ad == "ema":
        from ema_lightning import EMA
        t = EMA()
        def f(s):
            try:
                sp = t.say(s, seed=7)
            except TypeError:
                sp = t.say(s)
            return np.asarray(sp.audio, np.float32), sp.sample_rate
        return f
    if ad == "ahenk_cep":
        from huggingface_hub import snapshot_download
        d = snapshot_download("ozgurguler/ahenk-cep-tr", allow_patterns=["*.pt", "ahenk_cep.py"])
        sys.path.insert(0, d)
        from ahenk_cep import AhenkCep
        t = AhenkCep(f"{d}/student.pt", f"{d}/decoder.pt")
        def f(s):
            a, sr = t.say(s)
            return np.asarray(a, np.float32), sr
        return f
    if ad == "freya":
        sys.path.insert(0, str(Path("FreyaTTS").resolve()))
        from freyatts import FreyaTTS
        t = FreyaTTS.from_pretrained("freyavoice/freya-tts", device="cpu")
        return lambda s: (np.asarray(t.synthesize(s), np.float32), 48000)
    if ad.startswith("seslen_"):
        from seslen_tts import Seslen
        from seslen_tts.seslen import ORAN
        t = Seslen(); v = ad.split("_", 1)[1]
        return lambda s: (np.asarray(t.tum(s, ses=v), np.float32), ORAN)
    if ad == "trendyol":
        from turkish_tts import TurkishTTS
        t = TurkishTTS(device="cpu", optimize=False)
        def f(s):
            pcm = t.synthesize(s)
            return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768, t.sample_rate
        return f
    if ad.startswith("edge_"):
        v = {"edge_emel": "tr-TR-EmelNeural", "edge_ahmet": "tr-TR-AhmetNeural"}[ad]
        def f(s):
            subprocess.run(["edge-tts", "--voice", v, "--text", s, "--write-media", "/tmp/e.mp3"], check=True)
            r = subprocess.run(["ffmpeg", "-v", "error", "-i", "/tmp/e.mp3", "-ac", "1", "-ar", "24000", "-f", "f32le", "-"],
                               capture_output=True, check=True)
            return np.frombuffer(r.stdout, np.float32).copy(), 24000
        return f
    raise SystemExit(f"bilinmeyen motor {ad}")


def denetle(klasor, metinler):
    from faster_whisper import WhisperModel
    import difflib, re
    m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
    n = lambda t: re.sub(r"[^a-zçğıöşü0-9 ]", " ", t.replace("İ", "i").replace("I", "ı").lower()).split()
    out = []
    for i, c in enumerate(metinler, 1):
        seg, _ = m.transcribe(str(klasor / f"{i:02d}.wav"), language="tr", beam_size=5)
        duy = " ".join(s.text for s in seg).strip()
        out.append({"no": i, "metin": c, "duyulan": duy,
                    "oran": round(difflib.SequenceMatcher(None, n(c), n(duy)).ratio(), 3)})
    return out


if __name__ == "__main__":
    ad, cikti = sys.argv[1], Path(sys.argv[2]); cikti.mkdir(parents=True, exist_ok=True)
    t0 = time.time(); f = motor(ad); yukle = time.time() - t0
    sure = ses = 0.0
    for i, c in enumerate(CUMLELER, 1):
        t = time.time(); x, sr = f(c); sure += time.time() - t; ses += len(x) / sr
        sf.write(cikti / f"{i:02d}.wav", x, sr)
    if ad == "ahenk_cep":            # Chatterbox kadın sesi denemesi için referans (CC BY 4.0 tasarlanmış ses)
        x, sr = f(REF_METIN); sf.write(cikti / "referans.wav", x, sr)
    rapor = {"motor": ad, "model_yukleme_sn": round(yukle, 1), "uretim_sn": round(sure, 1), "ses_sn": round(ses, 1),
             "rtf": round(sure / max(ses, 1e-6), 2)}
    try:
        rapor["whisper"] = denetle(cikti, CUMLELER)
        rapor["ortalama"] = round(sum(r["oran"] for r in rapor["whisper"]) / len(CUMLELER), 3)
    except Exception as e:  # denetim olmasa da sesler yayınlansın
        rapor["whisper_hata"] = str(e)
    json.dump(rapor, open(cikti / "rapor.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in rapor.items() if k != "whisper"}, ensure_ascii=False))
