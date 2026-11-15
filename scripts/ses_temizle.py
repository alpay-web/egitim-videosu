#!/usr/bin/env python3
"""Cümle seslerini DeepFilterNet3 (MIT/Apache-2.0) ile temizler: hışırtı, nefes, mırıltı, arka gürültü.

Kullanım (ayrı bir sanal ortamda; DeepFilterNet numpy<2 ister):
    python -m venv /tmp/df && /tmp/df/bin/pip install torch==2.1.2 torchaudio==2.1.2 deepfilternet==0.5.6 soundfile
    /tmp/df/bin/python scripts/ses_temizle.py sesler/ [--sinir 30]

- Klasördeki SS_CC.wav dosyalarını yerinde temizler (24 kHz mono PCM16 olarak yazar).
- Aynı dosyayı iki kez işlemez (`temizlendi.txt`).
- `--sinir`: en fazla kaç dB bastırılsın (konuşmayı robotikleştirmemek için sınırlı; varsayılan 30).
"""
import argparse, sys
from pathlib import Path

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("klasor")
    ap.add_argument("--sinir", type=float, default=30.0, help="en fazla bastırma (dB)")
    a = ap.parse_args()

    import soundfile as sf
    import torch
    from df.enhance import enhance, init_df
    from df.io import resample

    d = Path(a.klasor)
    kayit = d / "temizlendi.txt"
    yapilmis = set(kayit.read_text().split()) if kayit.exists() else set()
    dosyalar = sorted(f for f in d.glob("[0-9]*.wav") if f.name not in yapilmis)
    if not dosyalar:
        print("Temizlenecek yeni dosya yok."); return
    model, df_state, _ = init_df()                 # DeepFilterNet3, GitHub release'ten iner
    sr_df = df_state.sr()
    torch.set_num_threads(2)
    for i, f in enumerate(dosyalar, 1):
        x, sr = sf.read(str(f), dtype="float32", always_2d=True)
        x = torch.from_numpy(x.mean(1, keepdims=True).T.copy())          # [1, T]
        y = resample(x, sr, sr_df)
        y = enhance(model, df_state, y, atten_lim_db=a.sinir)
        y = resample(y, sr_df, sr).squeeze(0).numpy()
        y = np.clip(y, -1, 1)
        sf.write(str(f), y, sr, subtype="PCM_16")
        yapilmis.add(f.name)
        if i % 20 == 0 or i == len(dosyalar):
            print(f"  {i}/{len(dosyalar)} temizlendi", flush=True)
    kayit.write_text("\n".join(sorted(yapilmis)) + "\n")


if __name__ == "__main__":
    sys.exit(main())
