#!/usr/bin/env python3
"""
Bitmiş videonun otomatik kalite raporu (teslimden önce çalıştır).
  python kalite_raporu.py video.mp4 [--sheet sheet.png]
Kontroller: çözünürlük/FPS/süre, EBU R128 ses seviyesi ve tepe, uzun sessizlikler,
siyah kareler, uzun donmuş görüntü, kare tablosu (gözle bakmak için).
Çıktı: Markdown rapor (stdout) — her bulgu ciddiyet + somut öneriyle.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path


def ffmpeg():
    import shutil
    f = shutil.which("ffmpeg")
    if not f:
        import imageio_ffmpeg
        f = imageio_ffmpeg.get_ffmpeg_exe()
    return f


def calistir(args):
    return subprocess.run(args, capture_output=True, text=True).stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--sheet", help="kare tablosu yolu (varsayılan: <video>_kareler.png)")
    ap.add_argument("--sessizlik", type=float, default=4.5, help="bu süreden uzun sessizlik uyarı verir (sn)")
    a = ap.parse_args()
    v = Path(a.video)
    ff = ffmpeg()
    bulgular = []

    bilgi = calistir([ff, "-hide_banner", "-i", str(v)])
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", bilgi)
    sure = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0
    cz = re.search(r"Video: .*?(\d{3,4})x(\d{3,4}).*?([\d.]+) fps", bilgi)
    w, h, fps = (int(cz.group(1)), int(cz.group(2)), float(cz.group(3))) if cz else (0, 0, 0)

    # ses seviyesi (EBU R128)
    lo = calistir([ff, "-hide_banner", "-i", str(v), "-af", "ebur128=peak=true", "-f", "null", "-"])
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", lo); TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", lo)
    I = float(I[-1]) if I else None; TP = float(TP[-1]) if TP else None
    if I is not None and not (-18 <= I <= -13):
        bulgular.append(("öneri", f"Ses seviyesi {I} LUFS; YouTube için -14…-16 hedefle (loudnorm I=-15)."))
    if TP is not None and TP > -1.0:
        bulgular.append(("kritik", f"Gerçek tepe {TP} dBFS; kırpılma riski. loudnorm TP=-1.5 ile yeniden işle."))

    # sessizlik
    si = calistir([ff, "-hide_banner", "-i", str(v), "-af", f"silencedetect=n=-45dB:d={a.sessizlik}", "-f", "null", "-"])
    ses_bosluk = [(float(x), float(y)) for x, y in re.findall(r"silence_start: ([\d.]+).*?\n.*?silence_end: ([\d.]+)", si, re.S)]
    for s0, s1 in ses_bosluk:
        if s0 > 5 and s1 < sure - 5:
            bulgular.append(("öneri", f"{s0:.0f}-{s1:.0f} sn arası {s1 - s0:.1f} sn sessizlik (soru beklemesi değilse kısalt)."))

    # siyah kare / donma
    bk = calistir([ff, "-hide_banner", "-i", str(v), "-vf", "blackdetect=d=0.5:pix_th=0.08", "-an", "-f", "null", "-"])
    for s0, s1 in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", bk):
        if float(s1) < sure - 1.5:
            bulgular.append(("kritik", f"{float(s0):.1f}-{float(s1):.1f} sn siyah görüntü."))
    fr = calistir([ff, "-hide_banner", "-i", str(v), "-vf", "freezedetect=n=0.001:d=12", "-an", "-f", "null", "-"])
    for s0 in re.findall(r"freeze_start: ([\d.]+)", fr):
        bulgular.append(("öneri", f"{float(s0):.0f}. sn'den itibaren 12+ sn hareketsiz görüntü (kamera/öğe animasyonu ekle)."))

    # kare tablosu
    sheet = Path(a.sheet) if a.sheet else v.with_name(v.stem + "_kareler.png")
    aralik = max(5, int(sure / 25))
    subprocess.run([ff, "-v", "error", "-y", "-i", str(v), "-vf", f"fps=1/{aralik},scale=426:240,tile=5x5",
                    "-frames:v", "1", str(sheet)])

    print(f"# Kalite raporu: {v.name}\n")
    print(f"| Ölçüt | Değer |\n|---|---|")
    print(f"| Süre | {sure / 60:.1f} dk |\n| Görüntü | {w}x{h} @ {fps:g} fps |")
    print(f"| Ses seviyesi | {I} LUFS (tepe {TP} dBFS) |\n| Kare tablosu | {sheet.name} (her {aralik} sn) |\n")
    if w and (w, h) not in ((1920, 1080), (1280, 720), (1080, 1920)):
        bulgular.append(("öneri", f"Alışılmadık çözünürlük {w}x{h}."))
    if not bulgular:
        print("Otomatik kontrollerde sorun yok. Kare tablosuna gözle bak: taşan yazı, boş tahta, üst üste binme.")
    else:
        print("## Bulgular\n")
        for c, b in sorted(bulgular, key=lambda x: x[0] != "kritik"):
            print(f"- **{c}**: {b}")
    print("\nSıradaki adım: kare tablosuna bak, seslendirme için kalite_raporu.txt'teki en düşük puanlı cümleleri dinle.")


if __name__ == "__main__":
    main()
