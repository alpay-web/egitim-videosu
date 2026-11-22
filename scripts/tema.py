"""Giriş/kapanış kartı ve YouTube kapağı için tema seti: her video farklı renk ve yazı tipiyle açılır.

Fikirler (kod kopyalanmadı): adobe/leonardo (hedef kontrast oranından renk), radix-ui/colors ve nordtheme/nord
(uyumlu koyu/açık paletler), seek-oss/capsize (yazı tipi metriğine göre dikey ortalama), shuding/react-wrap-balancer
(dengeli başlık satırları), LottieFiles/motion-design-skill (giriş hareketinde ease-out, kısa süre).
Yazı tipleri Google Fonts deposundan (github.com/google/fonts, OFL-1.1) ilk kullanımda indirilir; hepsi Türkçe
karakterleri (ğ ş ı İ ç ö ü) içerir. İndirilemezse sistem yazı tipine düşülür.

Senaryoda seçim: "tema": 3  (sıra no) | "tema": "bordo" (ad) | yoksa başlığın özetinden (aynı başlık = aynı tema).
"""
import hashlib
import os
import subprocess
from pathlib import Path

FONT_DIZIN = Path.home() / ".egitim_video" / "fontlar"
_KAYNAK = "https://raw.githubusercontent.com/google/fonts/main/ofl/"

# ad, üst renk, alt renk, vurgu, başlık yazı tipi (dosya, ağırlık), düzen
TEMALAR = [
    ("lacivert", (22, 38, 80), (8, 14, 38), (255, 196, 80), ("montserrat/Montserrat[wght].ttf", "Bold"), "orta"),
    ("bordo", (96, 26, 42), (40, 10, 20), (255, 214, 150), ("playfairdisplay/PlayfairDisplay[wght].ttf", "Bold"), "sol"),
    ("mor", (60, 32, 100), (22, 12, 44), (120, 226, 204), ("sora/Sora[wght].ttf", "Bold"), "cerceve"),
    ("petrol", (10, 72, 86), (4, 30, 40), (255, 146, 96), ("poppins/Poppins-Bold.ttf", None), "orta"),
    ("komur", (40, 42, 48), (16, 17, 20), (96, 204, 250), ("spacegrotesk/SpaceGrotesk[wght].ttf", "Bold"), "sol"),
    ("krem", (247, 241, 229), (226, 216, 196), (196, 66, 46), ("dmserifdisplay/DMSerifDisplay-Regular.ttf", None), "cerceve"),
    ("orman", (26, 66, 42), (10, 28, 18), (240, 220, 120), ("fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf", "Bold"), "orta"),
    ("kahve", (122, 60, 22), (50, 22, 8), (255, 230, 180), ("archivoblack/ArchivoBlack-Regular.ttf", None), "sol"),
    ("gece", (18, 42, 92), (4, 10, 30), (255, 116, 146), ("outfit/Outfit[wght].ttf", "SemiBold"), "cerceve"),
    ("gokyuzu", (228, 239, 251), (196, 218, 242), (22, 92, 182), ("manrope/Manrope[wght].ttf", "ExtraBold"), "orta"),
    ("erik", (82, 22, 72), (30, 8, 28), (250, 200, 92), ("merriweather/Merriweather[opsz,wdth,wght].ttf", "Black"), "sol"),
    ("deniz", (8, 92, 112), (2, 40, 56), (250, 240, 200), ("bebasneue/BebasNeue-Regular.ttf", None), "cerceve"),
    ("grafit", (46, 54, 50), (20, 24, 22), (132, 232, 142), ("worksans/WorkSans[wght].ttf", "Bold"), "orta"),
    ("kum", (251, 237, 211), (236, 212, 170), (28, 82, 92), ("lora/Lora[wght].ttf", "Bold"), "sol"),
    ("zumrut", (14, 80, 64), (6, 34, 28), (255, 204, 112), ("nunito/Nunito[wght].ttf", "ExtraBold"), "cerceve"),
]
GOVDE = ("inter/Inter[opsz,wght].ttf", "Medium")


def _goreli_parlaklik(c):
    def k(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (k(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def kontrast(a, b):
    """WCAG kontrast oranı (1–21)."""
    la, lb = sorted((_goreli_parlaklik(a), _goreli_parlaklik(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def font_dosyasi(goreli):
    """Google Fonts deposundan indirir; olmazsa None."""
    hedef = FONT_DIZIN / Path(goreli).name
    if hedef.exists() and hedef.stat().st_size > 10000:
        return hedef
    FONT_DIZIN.mkdir(parents=True, exist_ok=True)
    url = _KAYNAK + goreli.replace("[", "%5B").replace("]", "%5D")
    try:
        subprocess.run(["curl", "-fsSL", "--retry", "2", "-o", str(hedef), url], check=True, capture_output=True)
        return hedef if hedef.stat().st_size > 10000 else None
    except Exception:
        try:
            hedef.unlink()
        except OSError:
            pass
        return None


_FC = {}


def tema_fontu(spec, boyut, yedek):
    """spec=(dosya, ağırlık adı). yedek: font(boyut, kalin) fonksiyonu."""
    from PIL import ImageFont
    k = (spec, int(boyut))
    if k in _FC:
        return _FC[k]
    f = None
    yol = font_dosyasi(spec[0])
    if yol:
        try:
            f = ImageFont.truetype(str(yol), int(boyut))
            if spec[1]:
                try:
                    f.set_variation_by_name(spec[1])
                except Exception:
                    pass
        except OSError:
            f = None
    _FC[k] = f or yedek(boyut, True)
    return _FC[k]


def tema_sec(sen):
    t = sen.get("tema")
    if isinstance(t, str):
        for i, x in enumerate(TEMALAR):
            if x[0] == t:
                return tema(i)
        if t.isdigit():
            t = int(t)
    if isinstance(t, int):
        return tema((t - 1) % len(TEMALAR))
    h = int(hashlib.sha1(sen.get("baslik", "").encode("utf-8")).hexdigest(), 16)
    return tema(h % len(TEMALAR))


def tema(i):
    ad, ust, alt, vurgu, yazi, duzen = TEMALAR[i]
    acik = _goreli_parlaklik(ust) > 0.5
    baslik_rengi = (26, 30, 36) if acik else (255, 255, 255)
    # ikinci metin: arka plana karşı ≥ 4.5 kontrast sağlayana kadar başlık rengine yaklaştır (leonardo fikri)
    alt_renk = tuple(int(a * 0.55 + b * 0.45) for a, b in zip(baslik_rengi, ust))
    w = 0.45
    while kontrast(alt_renk, ust) < 4.5 and w > 0:
        w -= 0.05
        alt_renk = tuple(int(a * (1 - w) + b * w) for a, b in zip(baslik_rengi, ust))
    return {"ad": ad, "ust": ust, "alt": alt, "vurgu": vurgu, "yazi": yazi, "duzen": duzen,
            "baslik_rengi": baslik_rengi, "alt_renk": alt_renk, "acik": acik,
            "buyuk_harf": yazi[0].startswith("bebasneue")}

