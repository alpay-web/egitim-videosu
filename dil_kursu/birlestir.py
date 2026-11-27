# -*- coding: utf-8 -*-
"""Olay listesini tek bir MP3 derse dönüştürür: klipler + duraklamalar + sinyal + bölümler (ID3 CHAP)."""
import json, re, subprocess, sys, unicodedata
from pathlib import Path
import numpy as np, soundfile as sf

sys.path.insert(0, "/home/claude/kurs")
import icerik, motor  # noqa: E402
from en_ses import uret as en_uret  # noqa: E402

SR = motor.SR
TR_DIZIN = Path("/home/claude/kurs/tr_ses")
CIKTI = Path("/home/claude/kurs/cikti"); CIKTI.mkdir(exist_ok=True)
HEDEF_RMS = 10 ** (-20 / 20)


def oku(yol):
    x, sr = sf.read(str(yol), dtype="float32", always_2d=False)
    if x.ndim > 1:
        x = x.mean(1)
    if sr != SR:
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(yol), "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"],
                           capture_output=True, check=True)
        x = np.frombuffer(r.stdout, np.float32).copy()
    return x


_VAD = []


def vad_sinirlari(x):
    """Silero VAD (snakers4/silero-vad, MIT): konuşmanın gerçek başı ve sonu (örnek indeksi, SR'de)."""
    try:
        import torch
        from silero_vad import load_silero_vad, get_speech_timestamps
        if not _VAD:
            _VAD.append(load_silero_vad())
        n16 = int(len(x) * 16000 / SR)
        y = np.interp(np.linspace(0, len(x) - 1, n16), np.arange(len(x)), x).astype(np.float32)
        ts = get_speech_timestamps(torch.from_numpy(y), _VAD[0], sampling_rate=16000, threshold=0.35,
                                   min_silence_duration_ms=250, speech_pad_ms=40)
        if ts:
            return int(ts[0]["start"] * SR / 16000), int(ts[-1]["end"] * SR / 16000)
    except Exception:
        pass
    return None


def kirp(x, esik=0.012, bas=0.06, son=0.10):
    v = vad_sinirlari(x)
    nz = np.nonzero(np.abs(x) > esik)[0]
    if not len(nz):
        return x
    a, b = nz[0], nz[-1]
    if v:                                   # VAD ile eşiği birleştir: yumuşak başlangıç ünsüzleri kesilmesin
        a, b = min(a, v[0]), max(min(b, v[1] + int(0.25 * SR)), v[1])
    x = x[max(0, a - int(bas * SR)): b + int(son * SR)]
    f = min(len(x) // 4, int(0.012 * SR))
    if f:
        x = x.copy(); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    return x


def esitle(x):
    # konuşma bölümlerinin RMS'i (sessiz kısımlar hariç) hedefe çekilir
    blok = int(0.05 * SR); n = len(x) // blok
    if n == 0:
        return x
    e = np.sqrt((x[:n * blok].reshape(n, blok) ** 2).mean(1))
    aktif = e[e > e.max() * 0.1]
    rms = np.sqrt((aktif ** 2).mean()) if len(aktif) else 1e-4
    y = x * min(4.0, HEDEF_RMS / (rms + 1e-9))
    tepe = np.abs(y).max()
    return y / tepe * 0.95 if tepe > 0.95 else y


def bip():
    t = np.arange(int(0.32 * SR)) / SR
    x = 0.22 * np.sin(2 * np.pi * 880 * t) * np.minimum(1, np.minimum(t, t[::-1]) / 0.03)
    return x.astype(np.float32)


def tr_dizini():
    out = {}
    for d in [TR_DIZIN, TR_DIZIN.parent / "tr_ses_duzeltme", TR_DIZIN.parent / "tr_ses_d2", TR_DIZIN.parent / "tr_ses_ba", TR_DIZIN.parent / "tr_ses_ba_d", TR_DIZIN.parent / "tr_ses_ba_d2"]:      # sonraki klasör öncekini ezer
        if (d / "dizin.json").exists():
            for k, v in json.load(open(d / "dizin.json")).items():
                out[v["metin"]] = d / f"{k}.wav"
    return out


def sessiz(s):
    return np.zeros(int(round(s * SR)), np.float32)


def dosya_adi(s):
    s = unicodedata.normalize("NFKD", s.replace("ı", "i").replace("İ", "I")).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")


def birlestir(d, no, trd, cache={}, gunluk=False):
    ev = motor.plan_gunluk(d) if gunluk else motor.plan(d)
    parcalar, son_sure, t, bolumler = [], 0.0, 0.0, []
    for x in ev:
        if x[0] == "BOLUM":
            bolumler.append((t, x[1])); continue
        if x[0] == "T":
            cs = motor.cumlelere_bol(x[1])
            for j, c in enumerate(cs):
                if c not in cache:
                    cache[c] = esitle(kirp(oku(trd[c])))
                a = cache[c]
                parcalar.append(a); t += len(a) / SR; son_sure = len(a) / SR
                if j < len(cs) - 1:
                    parcalar.append(sessiz(0.35)); t += 0.35
        elif x[0] == "E":
            key = (x[1], x[2], x[3])
            if key not in cache:
                cache[key] = esitle(kirp(oku(en_uret(*key))))
            a = cache[key]
            parcalar.append(a); t += len(a) / SR; son_sure = len(a) / SR
        elif x[0] == "S":
            parcalar.append(sessiz(x[1])); t += x[1]
        elif x[0] == "R":
            s = min(12.0, x[1] * son_sure + x[2]); parcalar.append(sessiz(s)); t += s
        elif x[0] == "B":
            b = bip(); parcalar.append(b); t += len(b) / SR
    ses = np.concatenate(parcalar)
    ad = f"{no:02d}_{d['id']}_{dosya_adi(d['baslik'])}" + ("_gunluk_tekrar" if gunluk else "")
    wav = CIKTI / f"{ad}.wav"; sf.write(wav, ses, SR)
    # bölümler (ffmetadata → ID3 CHAP)
    meta = CIKTI / f"{ad}.meta"
    sat = [";FFMETADATA1", f"title={d['id']} · {d['baslik']}" + (" · günlük tekrar" if gunluk else ""), "artist=İngilizce Sesli Kurs (YDS · IELTS · İş Analizi)",
           "album=İngilizce Sesli Kurs · Pilot", f"track={no}", "genre=Speech"]
    bit = [b[0] for b in bolumler[1:]] + [len(ses) / SR]
    for (bas, isim), son in zip(bolumler, bit):
        sat += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(bas * 1000)}", f"END={int(son * 1000)}", f"title={isim}"]
    meta.write_text("\n".join(sat) + "\n", encoding="utf-8")
    mp3 = CIKTI / f"{ad}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-i", str(meta), "-map_metadata", "1", "-map_chapters", "1",
                    "-af", "highpass=f=60,loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "1",
                    "-c:a", "libmp3lame", "-b:a", "96k", "-id3v2_version", "3", str(mp3)], check=True)
    wav.unlink(); meta.unlink()
    return mp3, len(ses) / SR, bolumler


if __name__ == "__main__":
    trd = tr_dizini()
    secim = sys.argv[1:] or [d["id"] for d in icerik.DERSLER]
    for no, d in enumerate(icerik.DERSLER, 1):
        if d["id"] in secim:
            mp3, sure, b = birlestir(d, no, trd)
            print(f"{mp3.name}: {sure / 60:.1f} dk, {len(b)} bölüm", flush=True)
