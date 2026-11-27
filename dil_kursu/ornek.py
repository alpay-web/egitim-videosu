# -*- coding: utf-8 -*-
"""Her Türkçe anlatıcı adayı için aynı ~50 sn'lik ders parçasını üretir (İngilizce kısımlar herkes için aynı)."""
import json, subprocess, sys
from pathlib import Path
import numpy as np, soundfile as sf
sys.path.insert(0, "/home/claude/kurs")
import birlestir as b  # noqa: E402
from en_ses import uret  # noqa: E402

SR = b.SR
CIK = Path("/home/claude/kurs/ses_ornekleri"); CIK.mkdir(exist_ok=True)
N = len(json.load(open("/home/claude/egitim-videosu/dil_kursu/ses_deneme/cumleler.json")))


def tr_klipler(klasor):
    k = Path(klasor); out = []
    for i in range(1, N + 1):
        if (k / f"{i:02d}.wav").exists():
            out.append([k / f"{i:02d}.wav"])
        else:
            out.append(sorted(k.glob(f"{i:02d}_*.wav")))
    return out


def yap(ad, klasor):
    tr = tr_klipler(klasor)
    def T(i):
        parca = []
        for j, y in enumerate(tr[i - 1]):
            if j: parca.append(b.sessiz(0.35))
            parca.append(b.esitle(b.kirp(b.oku(y))))
        return np.concatenate(parca)
    E = lambda m, v, h=1.0: b.esitle(b.kirp(b.oku(uret(m, v, h))))
    S = b.sessiz
    w1, w2 = E("pollution", "bf_emma"), E("pollution", "am_michael")
    ex1, ex2 = E("Air pollution is a serious problem in big cities.", "bf_emma", 0.95), E("Air pollution is a serious problem in big cities.", "am_michael", 0.95 * 0.95)
    seq = [S(0.4), T(1), S(0.3), T(2), S(0.2), T(3), S(0.3), T(4), S(0.8), T(5), S(0.5),
           w1, S(2.0), w2, S(2.0), T(6), S(0.4), T(7), S(0.3), ex1, S(0.5), T(8), S(0.5), T(9), S(0.3), ex2, S(3.5),
           T(10), S(0.3), T(6), S(0.2), T(11), S(3.0), w2, S(1.5), T(12), S(0.8), T(13), S(0.8)]
    x = np.concatenate(seq)
    wav = CIK / f"{ad}.wav"; sf.write(wav, x, SR)
    mp3 = CIK / f"{ad}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-ar", "44100", "-ac", "1", "-b:a", "128k", str(mp3)], check=True)
    wav.unlink(); return mp3, len(x) / SR


if __name__ == "__main__":
    for ad, k in [a.split("=") for a in sys.argv[1:]]:
        m, s = yap(ad, k); print(m.name, f"{s:.0f} sn")
