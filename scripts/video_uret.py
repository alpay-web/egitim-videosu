#!/usr/bin/env python3
"""
Eğitim Videosu Üretici v2 — tamamen ücretsiz / açık kaynak.

Senaryo (JSON) -> Türkçe nöral seslendirme (Piper, CC0 ses) -> ses işleme + arka plan müziği
-> konuşan animasyonlu profesör + kara tahta + altyazı + intro/outro -> 1080p MP4

    python video_uret.py senaryo.json -o video.mp4
    python video_uret.py senaryo.json -o deneme.mp4 --sahne 1-2 --cozunurluk 720
"""
import argparse, asyncio, json, math, os, random, re, shutil, subprocess, sys, tarfile, tempfile, wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FPS, SR = 25, 24000
CUMLE_ARASI, SAHNE_ARASI = 0.35, 1.0
INTRO_SN, OUTRO_SN = 4.0, 4.5
GECIS = 0.5        # sahne geçişi (sn)
MADDE_ANIM = 0.45  # madde belirme animasyonu (sn)

PIPER_SESLER = {  # GitHub (k2-fsa/sherpa-onnx) üzerinde barınan Piper sesleri
    "fahrettin": ("vits-piper-tr_TR-fahrettin-medium", "tr_TR-fahrettin-medium", "CC0"),
    "fettah": ("vits-piper-tr_TR-fettah-medium", "tr_TR-fettah-medium", "CC0"),
    "dfki": ("vits-piper-tr_TR-dfki-medium", "tr_TR-dfki-medium", "CC BY-NC-SA 4.0 (ticari kullanım yok)"),
}
SES_URL = "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/{}.tar.bz2"


def log(*a):
    print(*a, flush=True)


# ================================================================ araçlar
def ffmpeg_bin(_c=[]):
    if _c:
        return _c[0]
    f = shutil.which("ffmpeg")
    if not f:
        try:
            import imageio_ffmpeg
            f = imageio_ffmpeg.get_ffmpeg_exe()
        except ImportError:
            sys.exit("HATA: ffmpeg yok. 'pip install imageio-ffmpeg' ya da ffmpeg kurun.")
    _c.append(f)
    return f


def indir(url, hedef):
    if shutil.which("curl"):
        subprocess.run(["curl", "-fsSL", "--retry", "3", "-o", str(hedef), url], check=True)
    else:
        import urllib.request
        urllib.request.urlretrieve(url, hedef)


def font_yolu(kalin=False):
    adaylar = (["DejaVuSans-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf", "segoeuib.ttf", "LiberationSans-Bold.ttf"]
               if kalin else ["DejaVuSans.ttf", "arial.ttf", "Arial.ttf", "segoeui.ttf", "LiberationSans-Regular.ttf"])
    dizinler = ["/usr/share/fonts", "/usr/local/share/fonts", os.path.expanduser("~/.fonts"),
                "C:/Windows/Fonts", "/Library/Fonts", "/System/Library/Fonts", "/System/Library/Fonts/Supplemental"]
    for ad in adaylar:
        try:
            ImageFont.truetype(ad, 20); return ad
        except OSError:
            pass
        for d in dizinler:
            for kok, _, dosyalar in os.walk(d):
                if ad in dosyalar:
                    return os.path.join(kok, ad)
    return None


_FC = {}
def font(boyut, kalin=False):
    k = (int(boyut), kalin)
    if k not in _FC:
        y = font_yolu(kalin)
        _FC[k] = ImageFont.truetype(y, int(boyut)) if y else ImageFont.load_default(int(boyut))
    return _FC[k]


# ================================================================ Türkçe metin hazırlama
BIR = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
ON = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def sayi_yazi(n):
    if n == 0:
        return "sıfır"
    p = []
    if n >= 1_000_000:
        p.append(sayi_yazi(n // 1_000_000) + " milyon"); n %= 1_000_000
    if n >= 1000:
        b = n // 1000; p.append(("" if b == 1 else sayi_yazi(b) + " ") + "bin"); n %= 1000
    if n >= 100:
        h = n // 100; p.append(("" if h == 1 else BIR[h] + " ") + "yüz"); n %= 100
    if n >= 10:
        p.append(ON[n // 10]); n %= 10
    if n:
        p.append(BIR[n])
    return " ".join(p)


def seslendirme_metni(metin, telaffuz):
    t = metin
    for k in sorted(telaffuz, key=len, reverse=True):
        t = re.sub(r"(?<![\wçğıöşüÇĞİÖŞÜ])" + re.escape(k) + r"(?![\wçğıöşüÇĞİÖŞÜ])", telaffuz[k], t, flags=re.I)
    t = re.sub(r"%\s?(\d+)", lambda m: "yüzde " + sayi_yazi(int(m.group(1))), t)
    t = re.sub(r"(\d+)\s?[–-]\s?(\d+)", lambda m: f"{sayi_yazi(int(m.group(1)))} ile {sayi_yazi(int(m.group(2)))}", t)
    t = re.sub(r"\d+", lambda m: sayi_yazi(int(m.group(0))), t)
    t = t.replace("→", ", ").replace("/", ", ").replace("…", "...")
    return t


def cumlelere_bol(metin):
    return [p.strip() for p in re.split(r"(?<=[.!?…])\s+", metin.strip()) if p.strip()]


def oku_24k(yol):
    out = subprocess.run([ffmpeg_bin(), "-v", "error", "-i", str(yol), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype=np.int16).astype(np.float32) / 32768.0


# ================================================================ seslendirme motorları
class PiperSes:
    def __init__(self, ad, dizin, hiz):
        from piper import PiperVoice, SynthesisConfig
        paket, model, lisans = PIPER_SESLER[ad]
        dizin = Path(dizin); dizin.mkdir(parents=True, exist_ok=True)
        onnx = dizin / paket / f"{model}.onnx"
        if not onnx.exists():
            log(f"  Ses modeli indiriliyor (tek seferlik, ~65 MB): {paket}")
            arsiv = dizin / f"{paket}.tar.bz2"
            indir(SES_URL.format(paket), arsiv)
            with tarfile.open(arsiv) as tf:
                uyeler = [m for m in tf.getmembers() if m.name.endswith((".onnx", ".onnx.json", "MODEL_CARD"))]
                tf.extractall(dizin, members=uyeler, **({"filter": "data"} if hasattr(tarfile, "data_filter") else {}))
            arsiv.unlink()
        log(f"  Ses: Piper '{ad}' (lisans: {lisans})")
        self.v = PiperVoice.load(str(onnx))
        self.cfg = SynthesisConfig(length_scale=1.0 / hiz, noise_scale=0.55, noise_w_scale=0.7)

    def sentezle(self, metin, yol):
        with wave.open(str(yol), "wb") as wf:
            self.v.synthesize_wav(metin, wf, syn_config=self.cfg)


FREYA_URL = "https://github.com/alpay-web/egitim-videosu/releases/download/modeller-v1/{}"
FREYA_KOD = "https://github.com/freyavoiceai/FreyaTTS"


class FreyaSes:
    """FreyaTTS-small (Apache-2.0): doğal Türkçe nöral ses. İsteğe bağlı Praat ile erkek sesine dönüşüm."""

    def __init__(self, dizin, hiz, erkek, adim, tohum):
        import torch
        torch.set_num_threads(max(1, os.cpu_count() or 1))
        dizin = Path(dizin) / "freya"; dizin.mkdir(parents=True, exist_ok=True)
        for f in ("freya-model.safetensors", "freya-config.json", "voxcpm2-audiovae.pth"):
            if not (dizin / f).exists():
                log(f"  Model indiriliyor (tek seferlik): {f}")
                indir(FREYA_URL.format(f), dizin / (f + ".part")); (dizin / (f + ".part")).rename(dizin / f)
        kod = dizin / "FreyaTTS"
        if not (kod / "freyatts").exists():
            subprocess.run(["git", "clone", "-q", "--depth", "1", FREYA_KOD, str(kod)], check=True)
        sys.path.insert(0, str(kod))
        os.environ["HF_HUB_OFFLINE"] = "1"
        import freyatts.pipeline as fp

        def yerel_vae(device="cpu", token=None):
            from voxcpm.modules.audiovae import AudioVAEV2, AudioVAEConfigV2
            vae = AudioVAEV2(AudioVAEConfigV2())
            ck = torch.load(dizin / "voxcpm2-audiovae.pth", map_location="cpu", weights_only=True)
            vae.load_state_dict(ck.get("state_dict", ck), strict=False)
            vae = vae.float().eval()
            for p_ in vae.parameters():
                p_.requires_grad = False
            return vae
        fp.load_audio_vae = yerel_vae
        md = dizin / "model"; md.mkdir(exist_ok=True)
        for a, b in (("freya-config.json", "config.json"), ("freya-model.safetensors", "model.safetensors")):
            if not (md / b).exists():
                os.symlink(dizin / a, md / b)
        self.fp = fp
        self.tts = fp.FreyaTTS.from_pretrained(str(md), device="cpu")
        self.tts.t_floor = 8
        self.hiz, self.erkek, self.adim = hiz, erkek, adim
        self.tohum = fp.LEYLA_SEED if tohum is None else tohum
        # süre tahminini yavaşlatmak için orijinal fonksiyonu sarmala
        orj = self.tts.model.dur
        carpan = 1.0 / hiz

        class Yavas(torch.nn.Module):
            def __init__(s2, m):
                super().__init__(); s2.m = m
            def forward(s2, x):
                return s2.m(x) + math.log(carpan)
        self.tts.model.dur = Yavas(orj)
        log(f"  Ses: FreyaTTS-small (Apache-2.0){' + erkek dönüşümü' if erkek else ''}, hız x{hiz}")

    def sentezle(self, metin, yol):
        import soundfile as sf
        w = self.tts.synthesize(metin, steps=self.adim, seed=self.tohum)
        sr = self.tts.sample_rate
        if self.erkek:
            import parselmouth
            from parselmouth.praat import call
            snd = parselmouth.Sound(w.astype(np.float64), sr)
            f, p = self.erkek
            snd = call(snd, "Change gender", 75, 600, f, p, 1.0, 1.0)
            w, sr = snd.values[0], int(snd.sampling_frequency)
        sf.write(str(yol), w, sr)


class EdgeSes:
    def __init__(self, ad, hiz):
        import edge_tts  # noqa
        self.ad, self.hiz = ad, f"{round((hiz - 1) * 100):+d}%"
        log(f"  Ses: edge-tts '{ad}'")

    def sentezle(self, metin, yol):
        import edge_tts
        mp3 = str(yol) + ".mp3"
        asyncio.run(edge_tts.Communicate(metin, self.ad, rate=self.hiz).save(mp3))
        os.replace(mp3, yol)


class EspeakSes:
    def __init__(self):
        self.cli = shutil.which("espeak-ng") or shutil.which("espeak")
        log("  Ses: espeak-ng (robotik yedek)")

    def sentezle(self, metin, yol):
        if not self.cli:
            sys.exit("espeak-ng kurulu değil.")
        subprocess.run([self.cli, "-v", "tr", "-s", "150", "-w", str(yol), metin], check=True)


# ================================================================ ses işleme ve müzik
def tek_kutuplu_lp(x, fc):
    a = math.exp(-2 * math.pi * fc / SR)
    try:
        from scipy.signal import lfilter
        return lfilter([1 - a], [1, -a], x).astype(np.float32)
    except ImportError:  # scipy yoksa FFT ile yaklaşık
        X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
        return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 2), len(x)).astype(np.float32)


def muzik_uret(sure_sn, tohum=3):
    """Telif derdi olmayan, kod ile sentezlenen yumuşak 'lo-fi pad' fon müziği."""
    n = int(sure_sn * SR); t = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    akorlar = [[48, 55, 59, 64], [45, 52, 55, 60], [41, 48, 52, 57], [43, 50, 53, 59]]  # Cmaj7 Am7 Fmaj7 G7sus
    bar = 4.0
    rnd = random.Random(tohum)
    for i in range(int(sure_sn / bar) + 1):
        ak = akorlar[i % 4]; b0 = i * bar
        s, e = int(b0 * SR), min(n, int((b0 + bar + 1.5) * SR))
        if s >= n:
            break
        tt = t[s:e] - b0
        env = np.minimum(1, tt / 1.2) * np.clip((bar + 1.5 - tt) / 1.5, 0, 1)
        for m in ak:
            for det in (-0.08, 0.08):
                f = hz(m + det)
                out[s:e] += (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt)) * env * 0.05
        out[s:e] += np.sin(2 * np.pi * hz(ak[0] - 12) * tt) * env * 0.07          # bas
        for j in range(8):                                                       # arpej
            nt = b0 + j * 0.5
            if rnd.random() < 0.7:
                s2, e2 = int(nt * SR), min(n, int((nt + 1.6) * SR))
                if s2 >= n:
                    break
                t2 = t[s2:e2] - nt
                f = hz(ak[rnd.randrange(4)] + 24)
                out[s2:e2] += np.sin(2 * np.pi * f * t2) * np.exp(-t2 * 3.2) * 0.035
    out = tek_kutuplu_lp(out, 2200)
    d = int(0.23 * SR); y = out.copy()                                           # basit yankı
    for k in range(1, 4):
        y[k * d:] += out[:-k * d] * (0.35 ** k)
    return y / (np.max(np.abs(y)) + 1e-9)


def ses_zarfi(x, pencere=0.05):
    w = int(pencere * SR)
    e = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, mode="same"))
    return e


# ================================================================ karakter
def karakter_ciz(agiz, goz_kapali, kas, isaret, S):
    """Özgün 'Profesör' karakteri. S: son boyut ölçeği. Tuval taban: 520x560."""
    s = 2 * S
    Wc, Hc = int(520 * s), int(560 * s)
    im = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    P = lambda *xs: [x * s for x in xs]
    L = lambda w: max(1, int(w * s))

    TEN, TEN_G = (246, 208, 178), (222, 172, 140)
    SAC, SAC_G = (247, 247, 243), (208, 208, 203)
    HIRKA, HIRKA_G = (122, 84, 56), (96, 64, 42)

    d.rounded_rectangle(P(40, 390, 380, 640), radius=90 * s, fill=HIRKA)
    d.polygon(P(160, 390, 260, 390, 210, 500), fill=(250, 250, 250))
    d.line(P(210, 500, 210, 560), fill=HIRKA_G, width=L(4))
    for y in (520, 548):
        d.ellipse(P(203, y, 217, y + 14), fill=(230, 200, 120))
    d.polygon(P(178, 395, 210, 410, 178, 425), fill=(190, 40, 50))
    d.polygon(P(242, 395, 210, 410, 242, 425), fill=(190, 40, 50))
    d.ellipse(P(202, 402, 218, 418), fill=(160, 30, 40))
    d.line(P(150, 392, 205, 520), fill=HIRKA_G, width=L(6))
    d.line(P(270, 392, 215, 520), fill=HIRKA_G, width=L(6))
    d.rectangle(P(180, 340, 240, 400), fill=TEN_G)

    rnd = random.Random(7)
    for _ in range(46):
        a = rnd.uniform(math.pi * 0.95, math.pi * 2.05); r = rnd.uniform(145, 170)
        cx, cy = 210 + math.cos(a) * r * 1.05, 205 + math.sin(a) * r * 0.85
        rr = rnd.uniform(26, 44)
        d.ellipse(P(cx - rr, cy - rr, cx + rr, cy + rr), fill=SAC_G if rnd.random() < .35 else SAC)
    for side in (-1, 1):
        for _ in range(7):
            cx = 210 + side * rnd.uniform(125, 160); cy = rnd.uniform(200, 300); rr = rnd.uniform(24, 36)
            d.ellipse(P(cx - rr, cy - rr, cx + rr, cy + rr), fill=SAC)

    for x in (58, 362):
        d.ellipse(P(x - 22, 215, x + 22, 275), fill=TEN_G)
    d.ellipse(P(65, 90, 355, 365), fill=TEN)
    for cx, cy, rr in [(120, 105, 34), (165, 85, 36), (215, 80, 38), (262, 88, 34), (305, 108, 30), (95, 135, 24), (330, 140, 22)]:
        d.ellipse(P(cx - rr, cy - rr, cx + rr, cy + rr), fill=SAC)
    for y in (150, 162):
        d.arc(P(150, y, 270, y + 24), 200, 340, fill=TEN_G, width=L(2))

    ky = 180 - 9 * kas
    for x0, x1 in ((120, 182), (238, 300)):
        d.rounded_rectangle(P(x0, ky - 5, x1, ky + 7), radius=6 * s, fill=(212, 212, 208))

    for cx in (152, 268):
        if goz_kapali:
            d.arc(P(cx - 18, 200, cx + 18, 226), 10, 170, fill=(60, 45, 40), width=L(4))
        else:
            d.ellipse(P(cx - 17, 198, cx + 17, 230), fill=(255, 255, 255))
            px = cx + 3  # tahtaya doğru bakış
            d.ellipse(P(px - 9, 204, px + 9, 226), fill=(70, 110, 160))
            d.ellipse(P(px - 5, 209, px + 5, 221), fill=(25, 25, 30))
            d.ellipse(P(px - 1, 207, px + 4, 212), fill=(255, 255, 255))
    for cx in (152, 268):
        d.ellipse(P(cx - 38, 176, cx + 38, 250), outline=(60, 50, 45), width=L(5))
    d.arc(P(190, 196, 230, 222), 200, 340, fill=(60, 50, 45), width=L(5))
    d.line(P(114, 205, 70, 225), fill=(60, 50, 45), width=L(4))
    d.line(P(306, 205, 350, 225), fill=(60, 50, 45), width=L(4))

    d.ellipse(P(188, 228, 232, 282), fill=TEN_G)
    d.ellipse(P(192, 226, 228, 274), fill=(240, 196, 166))

    my = 312
    acik = [0, 8, 15, 23, 30][max(0, min(4, agiz))]
    if acik == 0:
        d.arc(P(178, my - 12, 242, my + 12), 15, 165, fill=(130, 60, 60), width=L(4))
    else:
        gen = 26 + acik * 0.4
        d.ellipse(P(210 - gen, my - 4, 210 + gen, my + acik), fill=(110, 35, 45))
        if acik > 12:
            d.ellipse(P(210 - gen * .6, my + acik * .45, 210 + gen * .6, my + acik - 1), fill=(220, 100, 110))
        d.rectangle(P(210 - gen * .7, my - 4, 210 + gen * .7, my + 2), fill=(250, 250, 250))
    for cx, cy, rr in [(170, 294, 22), (192, 288, 22), (228, 288, 22), (250, 294, 22), (150, 302, 16), (270, 302, 16)]:
        d.ellipse(P(cx - rr, cy - rr * .65, cx + rr, cy + rr * .65), fill=(222, 222, 218))
    for cx in (120, 300):
        d.ellipse(P(cx - 22, 262, cx + 22, 290), fill=(250, 170, 160, 90))

    if isaret:  # tahtayı gösteren kol + çubuk
        d.line(P(330, 450, 425, 352), fill=HIRKA_G, width=L(62))
        d.line(P(330, 450, 425, 352), fill=HIRKA, width=L(54))
        d.line(P(440, 340, 515, 210), fill=(90, 60, 35), width=L(9))
        d.ellipse(P(508, 200, 520, 214), fill=(250, 240, 220))
        d.ellipse(P(418, 322, 462, 366), fill=TEN)
        d.ellipse(P(430, 316, 448, 340), fill=TEN_G)
    return im.resize((int(520 * S), int(560 * S)), Image.LANCZOS)


# ================================================================ görsel katmanlar
def satir_kir(metin, fnt, gen, d):
    s, out = "", []
    for k in metin.split():
        t = (s + " " + k).strip()
        if d.textlength(t, font=fnt) <= gen:
            s = t
        else:
            if s:
                out.append(s)
            s = k
    if s:
        out.append(s)
    return out


class Sahne:
    def __init__(self, W, H):
        self.W, self.H, self.S = W, H, W / 1280

    def k(self, *v):
        return [int(round(x * self.S)) for x in v] if len(v) > 1 else int(round(v[0] * self.S))

    def arka_plan(self):
        W, H, k = self.W, self.H, self.k
        t = np.linspace(0, 1, H)[:, None, None]
        ust, alt = np.array([248, 238, 218]), np.array([228, 208, 176])
        arr = np.broadcast_to((ust * (1 - t) + alt * t), (H, W, 3)).astype(np.uint8)
        im = Image.fromarray(arr.copy())
        d = ImageDraw.Draw(im)
        for x in range(0, W, k(26)):  # ince duvar çizgileri
            d.line((x, 0, x, k(640)), fill=(240, 228, 205), width=1)
        d.rectangle(k(0, 630, 1280, 640), fill=(196, 160, 120))
        d.rectangle(k(0, 640, 1280, 720), fill=(150, 104, 70))
        for x in range(0, 1400, 90):
            d.line(k(x, 640, x - 40, 720), fill=(135, 92, 60), width=k(2))
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle(k(528, 40, 1266, 586), radius=k(16), fill=(0, 0, 0, 70))
        im.paste(sh.filter(ImageFilter.GaussianBlur(k(10))), (0, 0), sh.filter(ImageFilter.GaussianBlur(k(10))))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(k(520, 28, 1256, 572), radius=k(14), fill=(120, 80, 50))
        d.rectangle(k(538, 46, 1238, 554), fill=(36, 72, 57))
        rnd = random.Random(5)
        for _ in range(9):  # tebeşir izi dokusu
            x, y = rnd.randint(570, 1150), rnd.randint(80, 520)
            d.arc(k(x, y, x + rnd.randint(80, 220), y + rnd.randint(30, 90)), rnd.randint(0, 180), rnd.randint(190, 360),
                  fill=(48, 86, 70), width=k(6))
        d.rectangle(k(528, 560, 1248, 578), fill=(140, 96, 62))
        d.rectangle(k(588, 553, 628, 561), fill=(250, 250, 245))
        d.rectangle(k(648, 553, 674, 561), fill=(250, 230, 120))
        return im

    def tahta(self, taban, sh, gorunen, no, toplam, ust):
        im = taban.copy(); d = ImageDraw.Draw(im); k = self.k
        fb, fk = font(k(38), True), font(k(16))
        y = 66
        for s in satir_kir(sh["baslik"], fb, k(640), d)[:2]:
            d.text(k(568, y), s, font=fb, fill=(255, 224, 115)); y += 48
        d.line(k(568, y + 6, 1210, y + 6), fill=(190, 205, 195), width=k(2))
        self.madde_y0 = y + 28
        yy = self.madde_y0
        konumlar = []
        for i, m in enumerate(sh.get("maddeler", [])):
            konumlar.append(yy)
            yy += self.madde_yuk(m, d)
        for i in range(gorunen):
            self.madde_ciz(d, sh["maddeler"][i], konumlar[i], vurgu=(i == gorunen - 1))
        d.text(k(1238 - 52, 528), f"{no}/{toplam}", font=fk, fill=(160, 185, 172))
        d.text(k(558, 528), ust, font=fk, fill=(160, 185, 172))
        return im, konumlar

    def madde_yuk(self, m, d):
        return (len(satir_kir(m, font(self.k(29)), self.k(600), d)) * 38 + 14)

    def madde_ciz(self, d, m, y, vurgu, dx=0):
        k = self.k
        fm = font(k(29))
        renk = (255, 255, 255) if vurgu else (200, 216, 206)
        d.ellipse((k(570) + dx, k(y + 12), k(584) + dx, k(y + 26)), fill=(255, 196, 80))
        for s in satir_kir(m, fm, k(600), d):
            d.text((k(600) + dx, k(y)), s, font=fm, fill=renk); y += 38

    def madde_katmani(self, m, y):
        im = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        self.madde_ciz(ImageDraw.Draw(im), m, y, True)
        bb = im.getbbox()
        return im.crop(bb), bb

    def altyazi(self, metin):
        k = self.k
        im = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        if not metin:
            return None
        d = ImageDraw.Draw(im)
        fnt = font(k(24))
        sat = satir_kir(metin, fnt, k(690), d)[:3]
        h = 14 + 31 * len(sat)
        y0 = 590 + (3 - len(sat)) * 10
        d.rounded_rectangle(k(520, y0, 1256, y0 + h), radius=k(12), fill=(18, 20, 26, 215))
        for i, s in enumerate(sat):
            tw = d.textlength(s, font=fnt)
            d.text((k(888) - tw / 2, k(y0 + 7 + i * 31)), s, font=fnt, fill=(255, 255, 255))
        bb = im.getbbox()
        return im.crop(bb), bb

    def kapak(self, baslik, alt, ilerleme, karakter=None):
        """intro/outro kartı; ilerleme 0..1 animasyon için"""
        W, H, k = self.W, self.H, self.k
        t = np.linspace(0, 1, H)[:, None, None]
        a, b = np.array([24, 58, 52]), np.array([12, 30, 34])
        im = Image.fromarray(np.broadcast_to(a * (1 - t) + b * t, (H, W, 3)).astype(np.uint8).copy())
        d = ImageDraw.Draw(im, "RGBA")
        e = 1 - (1 - min(1, ilerleme)) ** 3
        fb = font(k(58), True); fa = font(k(28))
        satirlar = [x for parca in re.split(r"\s+[–—-]\s+|\n", baslik) for x in satir_kir(parca, fb, k(1100), d)]
        y = 280 - len(satirlar) * 34 + (1 - e) * 30
        al = int(255 * e)
        for s in satirlar:
            tw = d.textlength(s, font=fb)
            d.text((W / 2 - tw / 2, k(y)), s, font=fb, fill=(255, 255, 255, al)); y += 72
        lw = k(320) * e
        d.rectangle((W / 2 - lw / 2, k(y + 12), W / 2 + lw / 2, k(y + 17)), fill=(255, 196, 80, al))
        if alt:
            tw = d.textlength(alt, font=fa)
            d.text((W / 2 - tw / 2, k(y + 40)), alt, font=fa, fill=(205, 225, 215, al))
        return im


# ================================================================ ana akış
def main():
    ap = argparse.ArgumentParser(description="Senaryodan animasyonlu eğitim videosu (ücretsiz/açık kaynak).")
    ap.add_argument("senaryo")
    ap.add_argument("-o", "--cikti", default="egitim_videosu.mp4")
    ap.add_argument("--ses", choices=["piper", "edge", "freya", "espeak"], default="piper")
    ap.add_argument("--ses-dizini", help="hazır cümle sesleri (SS_CC.mp3/wav) bu klasörden alınır")
    ap.add_argument("--sadece-ses", metavar="KLASOR", help="video üretmeden sadece cümle seslerini bu klasöre yaz")
    ap.add_argument("--karakter", default=str(Path(__file__).resolve().parent.parent / "karakter" / "profesor.json"),
                    help="karakter JSON'u (yanında aynı adlı .png) ya da 'cizim'")
    ap.add_argument("--freya-erkek", help="FreyaTTS sesine erkek dönüşümü: 'formant,perde' ör. 0.84,118")
    ap.add_argument("--piper-ses", default="fahrettin", choices=list(PIPER_SESLER))
    ap.add_argument("--edge-ses", default="tr-TR-AhmetNeural")
    ap.add_argument("--hiz", type=float, default=0.95, help="konuşma hızı çarpanı (1.0 = normal)")
    ap.add_argument("--model-dizini", default=str(Path.home() / ".egitim_video" / "sesler"))
    ap.add_argument("--cozunurluk", type=int, choices=[720, 1080], default=1080)
    ap.add_argument("--sahne", help="sadece bu sahneler, ör. 1-3")
    ap.add_argument("--muzik-yok", action="store_true")
    ap.add_argument("--altyazi-yok", action="store_true")
    ap.add_argument("--intro-outro-yok", action="store_true")
    args = ap.parse_args()

    H = args.cozunurluk; W = H * 16 // 9
    sen = json.loads(Path(args.senaryo).read_text(encoding="utf-8"))
    tum = sen["sahneler"]; toplam = len(tum)
    ilk = 1
    sahneler = tum
    if args.sahne:
        a, _, b = args.sahne.partition("-"); ilk = int(a)
        sahneler = tum[int(a) - 1:int(b or a)]
    telaffuz = sen.get("telaffuz", {})
    ust = sen.get("baslik", "")
    intro = 0 if args.intro_outro_yok else INTRO_SN
    outro = 0 if args.intro_outro_yok else OUTRO_SN

    tmp = Path(tempfile.mkdtemp(prefix="egitim_video_"))
    log("[1/4] Seslendirme...")
    motor = None
    if not args.ses_dizini:
        motor = (PiperSes(args.piper_ses, args.model_dizini, args.hiz) if args.ses == "piper"
                 else EdgeSes(args.edge_ses, args.hiz) if args.ses == "edge"
                 else FreyaSes(Path(args.model_dizini).parent, args.hiz,
                               tuple(float(x) for x in args.freya_erkek.split(",")) if args.freya_erkek else None,
                               32, None) if args.ses == "freya"
                 else EspeakSes())
    if args.sadece_ses:
        hedef = Path(args.sadece_ses); hedef.mkdir(parents=True, exist_ok=True)
        for si, sh in enumerate(sahneler):
            for ci, c in enumerate(cumlelere_bol(sh["anlatim"])):
                yol = hedef / f"{ilk + si:02d}_{ci:02d}.wav"
                motor.sentezle(seslendirme_metni(c, telaffuz), yol)
                log(f"   {yol.name}: {c[:60]}")
        log("TAMAM ✔ sesler: " + str(hedef))
        return

    parcalar = [np.zeros(int(intro * SR), np.float32)]
    t = intro; zc = []
    for si, sh in enumerate(sahneler):
        bas = t; cz = []
        for ci, c in enumerate(cumlelere_bol(sh["anlatim"])):
            if args.ses_dizini:
                adaylar = sorted(Path(args.ses_dizini).glob(f"{ilk + si:02d}_{ci:02d}.*"))
                if not adaylar:
                    sys.exit(f"HATA: {args.ses_dizini} içinde {ilk + si:02d}_{ci:02d} sesi yok")
                yol = adaylar[0]
            else:
                yol = tmp / f"s{si}_{ci}.wav"
                motor.sentezle(seslendirme_metni(c, telaffuz), yol)
            x = oku_24k(yol)
            nz = np.nonzero(np.abs(x) > 0.01)[0]       # baş/son sessizliği kırp
            if len(nz):
                x = x[max(0, nz[0] - 600): nz[-1] + 1200]
            cz.append((t, t + len(x) / SR, c))
            parcalar += [x, np.zeros(int(CUMLE_ARASI * SR), np.float32)]
            t += len(x) / SR + CUMLE_ARASI
        parcalar.append(np.zeros(int(SAHNE_ARASI * SR), np.float32)); t += SAHNE_ARASI
        zc.append((bas, t, cz))
        log(f"   sahne {ilk + si}/{toplam}: {len(cz)} cümle, {t - bas:.1f} sn")
    parcalar.append(np.zeros(int(outro * SR), np.float32)); t += outro
    ses = np.concatenate(parcalar)
    ses = ses / (np.max(np.abs(ses)) + 1e-9) * 0.9
    sure = len(ses) / SR

    log("[2/4] Ses işleme ve fon müziği...")
    karisim = ses.copy()
    if not args.muzik_yok:
        m = muzik_uret(sure)
        zarf = ses_zarfi(ses, 0.4)
        konusma = np.clip(zarf / 0.02, 0, 1)
        konusma = tek_kutuplu_lp(konusma, 1.5)  # yumuşak ducking
        kazanc = 0.10 - 0.07 * np.clip(konusma * 1.5, 0, 1)
        f = np.ones(len(m), np.float32)
        fi_n, fo_n = int(1.5 * SR), int(3.0 * SR)
        f[:fi_n] = np.linspace(0, 1, fi_n); f[-fo_n:] = np.linspace(1, 0, fo_n)
        karisim = ses + m * kazanc * f
    ham = tmp / "karisim.wav"
    with wave.open(str(ham), "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes((np.clip(karisim, -1, 1) * 32767).astype(np.int16).tobytes())
    son_ses = tmp / "son.wav"
    zincir = "highpass=f=70,equalizer=f=3000:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=3:attack=10:release=200"
    olc = subprocess.run([ffmpeg_bin(), "-hide_banner", "-i", str(ham), "-af",
                          zincir + ",loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    try:
        m = json.loads(olc[olc.rindex("{"):olc.rindex("}") + 1])
        ln = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
              f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    except Exception:
        ln = "loudnorm=I=-16:TP=-1.5:LRA=11"
    subprocess.run([ffmpeg_bin(), "-v", "error", "-y", "-i", str(ham), "-af", zincir + "," + ln,
                    "-ar", "48000", "-ac", "2", str(son_ses)], check=True)

    n_kare = int(math.ceil(sure * FPS)); spf = SR // FPS
    rms = np.array([np.sqrt(np.mean(ses[i * spf:(i + 1) * spf] ** 2) + 1e-12) for i in range(n_kare)])
    act = rms[rms > 0.01]
    esik = np.percentile(act, 85) if len(act) else 1
    sev = np.convolve(np.clip(rms / esik * 4.0, 0, 4), [0.25, 0.5, 0.25], mode="same")
    agiz = np.where(rms < 0.012, 0, np.clip(np.round(sev), 1, 4)).astype(int)
    agiz_s = np.where(rms < 0.012, 0, np.clip(sev / 4.0, 0.12, 1.0))         # foto karakter için sürekli
    agiz_s = np.convolve(agiz_s, [0.2, 0.6, 0.2], mode="same")

    log("[3/4] Karakter ve sahneler hazırlanıyor...")
    S = Sahne(W, H); k = S.k
    foto = None
    if args.karakter != "cizim":
        from karakter_foto import FotoKarakter
        kj = Path(args.karakter)
        foto = FotoKarakter(kj.with_suffix(".png"), kj, int(H * 0.8))
        log(f"  Karakter: {kj.stem}")
    else:
        kar = {(a, g, kk, i): karakter_ciz(a, g, kk, i, S.S)
               for a in range(5) for g in (False, True) for kk in (0.0, 1.0) for i in (False, True)}
    golge = Image.new("RGBA", k(520, 50), (0, 0, 0, 0))
    ImageDraw.Draw(golge).ellipse(k(60, 8, 360, 40), fill=(0, 0, 0, 70))
    golge = golge.filter(ImageFilter.GaussianBlur(k(6)))
    taban = S.arka_plan()

    rnd = random.Random(1); kirp = set(); f = int(FPS * 1.5)
    while f < n_kare:
        kirp.update({f, f + 1, f + 2}); f += rnd.randint(int(FPS * 2.5), int(FPS * 5))

    # madde zamanları: cümlelere orantılı dağıt
    madde_t = []
    for si, sh in enumerate(sahneler):
        cz = zc[si][2]; mm = sh.get("maddeler", []); nc = max(1, len(cz)); ts = []
        for j in range(len(mm)):
            ci = min(len(cz) - 1, int(math.floor(j * nc / max(1, len(mm)))))
            ts.append(cz[ci][0] if cz else zc[si][0])
        madde_t.append(ts)

    tahta_c, alt_c, madde_c = {}, {}, {}
    def tahta(si, g):
        if (si, g) not in tahta_c:
            if len(tahta_c) > 30:
                tahta_c.clear()
            tahta_c[(si, g)] = S.tahta(taban, sahneler[si], g, ilk + si, toplam, ust)
        return tahta_c[(si, g)]

    def altyazi(si, ci):
        if (si, ci) not in alt_c:
            alt_c[(si, ci)] = S.altyazi(zc[si][2][ci][2])
        return alt_c[(si, ci)]

    def sahne_karesi(si, tt, fi, karakter=True):
        bas, bit, cz = zc[si]
        ts = madde_t[si]
        g = sum(1 for x in ts if tt >= x)
        im, konum = tahta(si, max(0, g - 1) if (g and tt - ts[g - 1] < MADDE_ANIM) else g)
        im = im.copy()
        if g and tt - ts[g - 1] < MADDE_ANIM:  # yeni madde kayarak belirir
            p = (tt - ts[g - 1]) / MADDE_ANIM; e = 1 - (1 - p) ** 3
            key = (si, g - 1)
            if key not in madde_c:
                madde_c[key] = S.madde_katmani(sahneler[si]["maddeler"][g - 1], konum[g - 1])
            lay, bb = madde_c[key]
            lay2 = lay.copy(); lay2.putalpha(lay.getchannel("A").point(lambda v: int(v * e)))
            im.paste(lay2, (bb[0] - int(k(30) * (1 - e)), bb[1]), lay2)
        ci = None
        for j, (a, b, _) in enumerate(cz):
            if a - 0.05 <= tt < b + CUMLE_ARASI:
                ci = j; break
        if ci is not None and not args.altyazi_yok:
            r = altyazi(si, ci)
            if r:
                im.paste(r[0], r[1][:2], r[0])
        if karakter:
            karakter_yapistir(im, tt, fi, any(0 <= tt - x < 1.8 for x in ts))
        return im

    def karakter_yapistir(im, tt, fi, isaret=False):
        if foto is not None:
            a = float(agiz_s[fi]) if fi < len(agiz_s) else 0.0
            b = 0.0
            if fi in kirp:
                b = {0: 0.5, 1: 1.0, 2: 0.5}[min(2, sum(1 for d in (1, 2) if fi - d in kirp))]
            konus = min(1.0, float(np.mean(agiz_s[max(0, fi - 12):fi + 1])) * 3) if fi < len(agiz_s) else 0
            kr, (dx, dy) = foto.poz(foto.kare(a, b), tt, konus)
            x = k(-75) + int(dx); y = H - kr.height + k(10) + int(dy)
            im.paste(kr, (x, y), kr)
            return
        a = int(agiz[fi]) if fi < len(agiz) else 0
        kas = 1.0 if (a >= 3 and (fi // 10) % 6 == 0) else 0.0
        kr = kar[(a, fi in kirp, kas, isaret)]
        sal = int(k(4) * math.sin(tt * 2.0)) + (k(2) if a >= 3 else 0)
        im.paste(golge, k(20, 632), golge)
        im.paste(kr, (k(20), k(105) + sal), kr)

    log(f"[4/4] Video kodlanıyor: {W}x{H}, {n_kare} kare ({sure:.0f} sn)...")
    cikti = Path(args.cikti).resolve()
    ff = subprocess.Popen([ffmpeg_bin(), "-y", "-v", "error",
                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", str(son_ses),
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(cikti)],
                          stdin=subprocess.PIPE)
    sahne_bas = intro
    siyah = Image.new("RGB", (W, H), (0, 0, 0))
    si = 0
    for fi in range(n_kare):
        tt = fi / FPS
        if tt < intro:
            kare = S.kapak(ust, sen.get("alt_baslik", f"Anlatan: {sen.get('karakter_adi', 'Profesör Bilgin')}"),
                           (tt - 0.3) / 1.2 if tt > 0.3 else 0)
            if tt > intro - GECIS:  # sınıfa geçiş
                kare = Image.blend(kare, sahne_karesi(0, intro, 0), (tt - (intro - GECIS)) / GECIS)
        elif tt >= sure - outro:
            to = tt - (sure - outro)
            kare = S.kapak(sen.get("kapanis", "Başarılar!"), ust, to / 1.0)
            if to < GECIS:
                kare = Image.blend(sahne_karesi(len(sahneler) - 1, sure - outro - 0.01, fi), kare, to / GECIS)
            if to > outro - 1.0:
                kare = Image.blend(kare, siyah, min(1, (to - (outro - 1.0)) / 1.0))
        else:
            while si < len(sahneler) - 1 and tt >= zc[si][1]:
                si += 1
            kare = sahne_karesi(si, tt, fi)
            bit = zc[si][1]
            if si < len(sahneler) - 1 and tt > bit - GECIS:  # sahneler arası çapraz geçiş (tahta)
                p = (tt - (bit - GECIS)) / GECIS
                bos = taban.copy(); karakter_yapistir(bos, tt, fi)
                kare = (Image.blend(kare, bos, p * 2) if p < 0.5
                        else Image.blend(bos, sahne_karesi(si + 1, zc[si + 1][0], fi), (p - 0.5) * 2))
            # ilerleme çubuğu
            d = ImageDraw.Draw(kare)
            d.rectangle((0, H - k(5), int(W * (tt - intro) / max(1, sure - intro - outro)), H), fill=(255, 196, 80))
        ff.stdin.write(kare.tobytes())
        if fi % (FPS * 60) == 0:
            log(f"   {tt:5.0f} / {sure:.0f} sn")
    ff.stdin.close(); ff.wait()
    shutil.rmtree(tmp, ignore_errors=True)
    if ff.returncode:
        sys.exit("ffmpeg hata verdi.")
    log(f"\nTAMAM ✔  {cikti}  ({sure / 60:.1f} dk)")


if __name__ == "__main__":
    main()
