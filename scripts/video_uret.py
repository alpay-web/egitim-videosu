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
KAR_OLCEK = 0.52  # çizim karakterin boyutu (1 = eski tam boy)
CUMLE_ARASI, SAHNE_ARASI = 0.45, 1.2
INTRO_SN, OUTRO_SN = 4.0, 4.5
GECIS = 0.5        # sahne geçişi (sn)
MADDE_ANIM = 0.6   # madde belirme animasyonu (sn)
ISARETCI_SURE = 0.9   # işaretçinin bir satırdan diğerine kayma süresi (sn)
MIN_OGE_ARALIK = 1.2  # ardışık iki öğenin belirmesi arasında en az (sn): okunmadan geçmesin

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


# ---- İngilizce → Türkçe okunuş (CMU Pronouncing Dictionary, BSD; ARPAbet → Türk harfleri)
_ARPA = {"AA": "a", "AE": "e", "AH": "a", "AO": "o", "AW": "au", "AY": "ay", "EH": "e", "ER": "ör", "EY": "ey",
         "IH": "i", "IY": "i", "OW": "ou", "OY": "oy", "UH": "u", "UW": "u", "B": "b", "CH": "ç", "D": "d",
         "DH": "d", "F": "f", "G": "g", "HH": "h", "JH": "c", "K": "k", "L": "l", "M": "m", "N": "n", "NG": "ng",
         "P": "p", "R": "r", "S": "s", "SH": "ş", "T": "t", "TH": "t", "V": "v", "W": "v", "Y": "y", "Z": "z", "ZH": "j"}
_CMU = {}


def _cmu():
    if not _CMU:
        yol = Path.home() / ".egitim_video" / "cmudict.dict"
        if not yol.exists():
            yol.parent.mkdir(parents=True, exist_ok=True)
            indir("https://raw.githubusercontent.com/cmusphinx/cmudict/master/cmudict.dict", yol)
        for satir in yol.read_text(encoding="utf-8", errors="ignore").splitlines():
            p = satir.split("#")[0].split()
            if p and "(" not in p[0]:
                _CMU[p[0]] = p[1:]
    return _CMU


def _en_sayi(n):
    b = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
        "seventeen eighteen nineteen".split()
    o = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
    if n < 20:
        return b[n]
    if n < 100:
        return o[n // 10] + ("" if n % 10 == 0 else " " + b[n % 10])
    if 1100 <= n < 2100 and n % 100:                     # yıllar: 1890 → eighteen ninety
        return _en_sayi(n // 100) + " " + _en_sayi(n % 100)
    if n < 1000:
        return b[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + _en_sayi(n % 100))
    return _en_sayi(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + _en_sayi(n % 1000))


def ingilizce_okunus(metin):
    """'had better' → 'hed betır': Türkçe motorun İngilizceyi doğru vurgu ve akışla, cümleden kopmadan okuması için.
    Sözlükte olmayan kelime olduğu gibi kalır."""
    d = _cmu()
    ozel = {"aren't": "arnt", "worth": "vörs"}          # Whisper denetiminde zayıf çıkanlar
    metin = re.sub(r"[A-Za-z][A-Za-z'’]*", lambda m: ozel.get(m.group(0).lower(), m.group(0)), metin)
    metin = re.sub(r"\d+", lambda m: _en_sayi(int(m.group(0))), metin)

    def kelime(m):
        w = m.group(0); fon = d.get(w.lower().replace("’", "'"))
        if not fon:
            return w
        out = []
        for i, f in enumerate(fon):
            ana, vurgu = re.match(r"([A-Z]+)(\d?)", f).groups()
            if ana == "AH" and vurgu == "0":
                out.append("ı")
            elif ana == "ER" and vurgu == "0":
                out.append("ır")
            else:
                out.append(_ARPA.get(ana, ""))
        return "".join(out)
    return re.sub(r"[A-Za-z][A-Za-z'’]*", kelime, metin)


def _bagimsiz_mi(once, sonra, parca):
    """Örnek cümle gibi uzun (≥4 kelime) ve noktalamayla ayrılmış öbek ayrı İngilizce söylenir (alıntı gibi, doğal
    duraklamayla); kısa terimler Türkçe cümlenin içinde İngilizce okunuşuyla söylenir (dil geçişi kopukluğu olmaz)."""
    sol = once.rstrip()[-1:] if once.strip() else ""
    sag = sonra.lstrip()[:1]
    kelime_say = len(re.findall(r"[A-Za-z0-9']+", parca))
    return kelime_say >= 4 and (sol == "" or sol in ":;,—–(\"“") and (sag == "" or sag in ".,;:?!—–)\"”")


def seslendirme_metni(metin, telaffuz, kok=None):
    """TTS'e giden metin. Bağımsız {İngilizce} öbekler parantezde kalır (motor İngilizce okur);
    cümle içine gömülü olanlar İngilizce okunuşlarıyla Türkçe metne katılır."""
    if "{" in metin:
        m_ = metin.replace("[dur]", "").strip()
        parcalar, son = [], 0
        for m in re.finditer(r"\{([^{}]*)\}", m_):
            parcalar.append(("tr", m_[son:m.start()]))
            once, sonra = m_[:m.start()], m_[m.end():]
            parcalar.append(("en" if _bagimsiz_mi(once, sonra, m.group(1)) else "ici", m.group(1)))
            son = m.end()
        parcalar.append(("tr", m_[son:]))
        out = ""
        for tur, t in parcalar:
            if tur == "tr":
                out += _tr_metin(t, telaffuz, kok)
            elif tur == "ici":
                out += ingilizce_okunus(t)
            else:
                out += "{" + t + "}"
        return out
    return _tr_metin(temiz(metin), telaffuz, kok)


def _tr_metin(t, telaffuz, kok=None):
    for k, v in (kok or {}).items():  # kelime başı eşleşmesi (ekleriyle birlikte), ör. fiil -> fiyil
        t = re.sub(r"(?<![\wçğıöşüÇĞİÖŞÜ])" + re.escape(k), v, t, flags=re.I)
    for k in sorted(telaffuz, key=len, reverse=True):
        t = re.sub(r"(?<![\wçğıöşüÇĞİÖŞÜ])" + re.escape(k) + r"(?![\wçğıöşüÇĞİÖŞÜ])", telaffuz[k], t, flags=re.I)
    t = re.sub(r"%\s?(\d+)", lambda m: "yüzde " + sayi_yazi(int(m.group(1))), t)
    t = re.sub(r"(\d+)\s?[–-]\s?(\d+)", lambda m: f"{sayi_yazi(int(m.group(1)))} ile {sayi_yazi(int(m.group(2)))}", t)
    t = re.sub(r"\d+", lambda m: sayi_yazi(int(m.group(0))), t)
    t = t.replace("→", ", ").replace("/", ", ").replace("…", "...")
    return t


def cumlelere_bol(metin):
    """Cümlelere böler. '[dur]' işareti bir cümle sonu sayılır ve sonrasına uzun duraklama ekler.
    {İngilizce parça} içindeki noktalama cümleyi bölmez."""
    metin = re.sub(r"([.!?…])\s*\[dur\]", r"\1[dur]", metin.strip())
    out, cur, derin, i = [], "", 0, 0
    while i < len(metin):
        ch = metin[i]; cur += ch
        derin += (ch == "{") - (ch == "}")
        son_bosluk = i + 1 == len(metin) or metin[i + 1].isspace()
        if derin == 0:
            if cur.endswith("[dur]") or (ch in ".!?…" and son_bosluk) or (
                    ch == "}" and len(cur) > 1 and cur[-2] in ".!?…" and son_bosluk):
                if ch in ".!?…" and i + 1 < len(metin) and metin[i + 1] in ".!?…":
                    i += 1; continue
                out.append(cur.strip()); cur = ""
        i += 1
    if cur.strip():
        out.append(cur.strip())
    return [p for p in out if p]


def temiz(c):
    """Ekranda/altyazıda görünen metin: [dur] ve {İngilizce} işaretleri olmadan."""
    return c.replace("[dur]", "").replace("{", "").replace("}", "").strip()


# ================================================================ İngilizce parçalar (kod geçişi)
# Chatterbox tek çağrıda dil değiştiremiyor (resemble-ai/chatterbox#346). Çözüm: cümleyi {İngilizce} ve Türkçe
# parçalara ayırıp her parçayı kendi diliyle, AYNI referans sesle üretmek ve birleştirmek.
_EN_KISALTMA = {"t", "s", "re", "m", "ll", "ve", "d"}


def ingilizce_isaretle(metin):
    """Metindeki İngilizce kelime öbeklerini {…} içine alır (wordfreq: İngilizce/Türkçe kelime sıklığı)."""
    from wordfreq import zipf_frequency as z
    if "{" in metin:
        return metin
    parca = re.findall(r"\[dur\]|[\wçğıöşüÇĞİÖŞÜ]+(?:['’][\wçğıöşüÇĞİÖŞÜ]+)?|\s+|[^\s\w]", metin)

    def sinif(t):
        if not re.match(r"^[A-Za-z]+(?:['’][A-Za-z]+)?$", t):
            return "tr" if re.match(r"[\wçğıöşüÇĞİÖŞÜ]", t) else "isaret"
        if "'" in t or "’" in t:
            kok, ek = re.split(r"['’]", t, maxsplit=1)
            if ek.lower() not in _EN_KISALTMA:
                return "tr"                                      # better'dan: Türkçe ek → işaretleme
        w = t.lower()
        if len(w) == 1 and t not in ("I",):
            return "tr"                                          # A/B/C şıkları
        fark = z(w.replace("’", "'"), "en") - z(w.replace("’", "'"), "tr")
        if fark >= 1.5 and len(w) >= 2 or t == "I":
            return "guclu" if t != "I" else "zayif"
        if fark >= 0.5:
            return "zayif"
        return "tr"
    sin = [sinif(t) for t in parca]
    out, i, n = [], 0, len(parca)
    while i < n:
        if sin[i] in ("guclu", "zayif"):
            j = i; guclu = False; son_kelime = i
            while j < n and (sin[j] in ("guclu", "zayif") or parca[j].isspace()
                             or (sin[j] == "isaret" and parca[j] in ",'’?!-")):
                if sin[j] in ("guclu", "zayif"):
                    son_kelime = j; guclu = guclu or sin[j] == "guclu"
                j += 1
            bit = son_kelime + 1
            if bit < n and parca[bit] in "?!":                  # soru tonlaması İngilizce parçada kalsın
                bit += 1
            if guclu:
                out.append("{" + "".join(parca[i:bit]) + "}")
            else:
                out.append("".join(parca[i:bit]))
            i = bit
        else:
            out.append(parca[i]); i += 1
    return "".join(out)


def parcalara_ayir(metin_tts):
    """'Doğru cevap {was built}. Müze…' → [("tr", "Doğru cevap"), ("en", "was built"), ("tr", ". Müze…")]"""
    out = []
    for m in re.finditer(r"\{([^{}]*)\}|[^{}]+", metin_tts):
        if m.group(1) is not None:
            out.append(("en", m.group(1).strip()))
        elif m.group(0).strip():
            out.append(("tr", m.group(0).strip()))
    # harf içermeyen parçaları (yalnızca noktalama) bir öncekine yapıştır
    birlesik = []
    for dil, t in out:
        if not re.search(r"[\wçğıöşü]", t, flags=re.I) and birlesik:
            birlesik[-1] = (birlesik[-1][0], birlesik[-1][1] + t)
        else:
            birlesik.append((dil, t))
    return birlesik


def duraklama(c):
    """Cümle sonrası sessizlik: soru/ünlemde biraz uzun, [dur] işaretinde belirgin."""
    if c.endswith("[dur]"):
        return 0.9
    if c.rstrip().endswith(("?", "!")):
        return 0.5
    return CUMLE_ARASI


def tempo_uygula(x, tempo):
    p_ = subprocess.run([ffmpeg_bin(), "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                         "-af", f"atempo={tempo}", "-f", "f32le", "-"], input=x.astype(np.float32).tobytes(),
                        capture_output=True, check=True)
    return np.frombuffer(p_.stdout, dtype=np.float32).copy()


def oku_24k(yol):
    out = subprocess.run([ffmpeg_bin(), "-v", "error", "-i", str(yol), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype=np.int16).astype(np.float32) / 32768.0


def sahne_ogeleri(sh):
    tur = sh.get("tur", "maddeler")
    return {"tablo": lambda: sh["tablo"]["satirlar"], "soru": lambda: [], "rakam": lambda: sh["kartlar"],
            "karsilastirma": lambda: sh["satirlar"] * 2, "ipucu": lambda: [1], "metin": lambda: [1], "zaman": lambda: sh["adimlar"]
            }.get(tur, lambda: sh.get("maddeler", []))()


# ================================================================ ses önbelleği (içerik adresli)
# manim-voiceover'ın yaklaşımı: ses dosyası, seslendirilen metnin özetiyle (hash) eşlenir. Sahne eklemek,
# silmek ya da sırasını değiştirmek eski sesleri boşa çıkarmaz; değişen cümle de asla eski sesle çalmaz.
def ses_anahtari(metin_tts, ton):
    import hashlib
    veri = json.dumps({"m": metin_tts, "t": ton}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(veri.encode("utf-8")).hexdigest()[:12]


def dizin_oku(d):
    f = Path(d) / "dizin.json"
    try:
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None
    except Exception:
        return None


class SesDeposu:
    """Bir ya da daha çok ses klasöründe (virgülle) cümle sesini bulur: önce anahtar (içerik), sonra eski usul
    SS_CC adı — o klasörün dizin.json'ı bu ada farklı bir metin yazmışsa eski ses KULLANILMAZ."""

    def __init__(self, klasorler, ad_ile=True):
        self.ad_ile = ad_ile                  # False: yalnızca içerik anahtarı (önbellek için güvenli)
        self.klasorler = [Path(k) for k in str(klasorler or "").split(",") if k]
        self.anahtar = {}; self.dizinler = {}
        for k in self.klasorler:
            dz = dizin_oku(k); self.dizinler[k] = dz
            for ad, bilgi in (dz or {}).items():
                y = k / f"{ad}.wav"
                if y.exists():
                    self.anahtar.setdefault(bilgi["anahtar"], y)

    def bul(self, ad, anahtar):
        if anahtar in self.anahtar:
            return self.anahtar[anahtar]
        for k in (self.klasorler if self.ad_ile else []):
            dz = self.dizinler[k]
            if dz is not None and ad in dz and dz[ad]["anahtar"] != anahtar:
                continue                      # metin değişmiş: eski ses bu cümleye ait değil
            if dz is not None and ad not in dz:
                continue
            for uz in (".wav", ".mp3", ".flac", ".ogg"):
                if (k / f"{ad}{uz}").exists():
                    return k / f"{ad}{uz}"
        return None


# ================================================================ ekran ↔ anlatım kapsamı
def _kelimeler(t):
    t = re.sub(r"\d+", lambda m: " " + sayi_yazi(int(m.group(0))) + " ", str(t))
    t = t.replace("İ", "i").lower().replace("ı", "i")      # büyük/küçük ve noktalı/noktasız i farkı yok
    return [w for w in re.findall(r"[\wçğıöşü']+", t) if len(w) >= 3 or w.isdigit()]


def _var(w, havuz):
    k = w[:5]
    return any(h.startswith(k) or w.startswith(h[:5]) and len(h) >= 4 for h in havuz)


def ekran_ogeleri(sh):
    """Görsel öğe başına ekranda yazan metin (tablo: satırın tüm hücreleri)."""
    tur = sh.get("tur", "maddeler")
    if tur == "tablo":
        return [" ".join(map(str, r)) for r in sh["tablo"]["satirlar"]]
    if tur == "karsilastirma":
        n = sh["satirlar"]; return [r[0] for r in n] + [r[1] for r in n]
    if tur == "zaman":
        return [f"{a['baslik'] if len(a['baslik']) > 2 else ''} {a.get('metin', '')}" for a in sh["adimlar"]]
    if tur == "rakam":
        return [f"{c['deger']} {c.get('birim', '')} {c.get('etiket', '')}" for c in sh["kartlar"]]
    if tur == "ipucu":
        return [sh["ipucu"]["metin"]]
    if tur == "soru":
        q = sh["soru"]; return [q["metin"]] + list(q.get("secenekler") or []) + ([q["cevap"]] if q.get("cevap") else [])
    if tur == "metin":
        return [sh["metin"]]
    return list(sh.get("maddeler", []))


def kapsam_orani(oge, metin):
    kw = _kelimeler(oge.replace("___", " "))
    if not kw:
        return 1.0
    havuz = set(_kelimeler(temiz(metin)))
    return sum(_var(w, havuz) for w in kw) / len(kw)


def okunmayanlar(sh, esik=0.6):
    """Ekranda olup anlatımda okunmayan metinler: 'ekrandaki her şey okunmalı' kuralı."""
    return [o for o in ekran_ogeleri(sh) if kapsam_orani(o, sh.get("anlatim", "")) < esik]


def oto_goster(sh, cumleler):
    """goster verilmemişse: her öğe, onu en iyi okuyan (önceki öğeden sonraki) cümlede açılır."""
    ogeler = ekran_ogeleri(sh) if sh.get("tur") not in ("soru", "ipucu", "metin") else []
    n = len(cumleler); out, onceki = [], 0
    for j, o in enumerate(ogeler):
        en, en_ci = 0.0, None
        for ci in range(onceki, n):
            r = kapsam_orani(o, cumleler[ci])
            if r > en + 1e-9:
                en, en_ci = r, ci
        if en_ci is None or en < 0.3:
            en_ci = max(onceki, min(n - 1, int(j * n / max(1, len(ogeler)))))
        out.append(en_ci); onceki = en_ci
    return out


# ================================================================ senaryo doğrulama
TURLER = {"maddeler", "tablo", "soru", "rakam", "karsilastirma", "ipucu", "zaman", "metin"}


def senaryo_dogrula(sen):
    """Yazım hatalarını render'dan ÖNCE yakalar (saatlerce süren üretim boşa gitmesin)."""
    h = []
    sah = sen.get("sahneler")
    if not isinstance(sah, list) or not sah:
        return ["'sahneler' listesi yok ya da boş"]
    for i, sh in enumerate(sah, 1):
        yer = f"sahne {i} «{sh.get('baslik', '?')}»"
        tur = sh.get("tur", "maddeler")
        if tur not in TURLER:
            h.append(f"{yer}: bilinmeyen tur '{tur}' (geçerli: {', '.join(sorted(TURLER))})"); continue
        if not sh.get("baslik"):
            h.append(f"{yer}: 'baslik' yok")
        if not str(sh.get("anlatim", "")).strip():
            h.append(f"{yer}: 'anlatim' boş"); continue
        nc = len(cumlelere_bol(sh["anlatim"]))
        try:
            if tur == "tablo":
                assert sh["tablo"]["satirlar"], "tablo.satirlar boş"
            elif tur == "soru":
                q = sh["soru"]
                assert q.get("metin") and (len(q.get("secenekler") or []) >= 2 or q.get("cevap")), \
                    "soru.metin ve en az 2 seçenek ya da 'cevap' (boşluk doldurma) gerekli"
                if q.get("secenekler"):
                    assert 0 <= q["dogru"] < len(q["secenekler"]), "soru.dogru seçenek sırası dışında"
                cc = q.get("cevap_cumle", -1)
                assert -1 <= cc < nc, f"soru.cevap_cumle={cc} ama anlatımda {nc} cümle var"
            elif tur == "rakam":
                assert 1 <= len(sh["kartlar"]) <= 3, "kartlar 1-3 adet olmalı"
            elif tur == "karsilastirma":
                assert sh["sol"].get("baslik") and sh["sag"].get("baslik"), "sol/sag başlığı gerekli"
                assert all(len(r) == 2 for r in sh["satirlar"]), "her satır [sol, sağ] olmalı"
            elif tur == "ipucu":
                assert sh["ipucu"].get("metin"), "ipucu.metin gerekli"
            elif tur == "metin":
                assert str(sh.get("metin", "")).strip(), "metin gerekli"
            elif tur == "zaman":
                assert sh["adimlar"] and all("baslik" in a for a in sh["adimlar"]), "adimlar[].baslik gerekli"
        except (KeyError, TypeError, AssertionError) as e:
            h.append(f"{yer}: {e if isinstance(e, AssertionError) else 'eksik alan ' + str(e)}"); continue
        g = sh.get("goster") or []
        n_oge = len(sahne_ogeleri(sh))
        if len(g) > n_oge and tur != "ipucu":
            h.append(f"{yer}: goster {len(g)} öğe veriyor ama sahnede {n_oge} öğe var")
        for x in g:
            try:
                ci = int(float(str(x).split(":")[0]))
            except ValueError:
                h.append(f"{yer}: goster değeri anlaşılmadı: {x!r}"); continue
            if not 0 <= ci < nc:
                h.append(f"{yer}: goster {x!r} → anlatımda {nc} cümle var (0–{nc - 1})")
    return h


def oge_metni(sh, j):
    """j. görsel öğenin metni (kelime senkronu için çapa aranır)."""
    tur = sh.get("tur", "maddeler")
    try:
        if tur == "tablo":
            return str(sh["tablo"]["satirlar"][j][0])
        if tur == "karsilastirma":
            n = len(sh["satirlar"]); return str(sh["satirlar"][j % n][j // n])
        if tur == "zaman":
            a = sh["adimlar"][j]; return a.get("metin") if len(a["baslik"]) <= 2 else a["baslik"]
        if tur == "rakam":
            return str(sh["kartlar"][j].get("etiket", ""))
        if tur == "maddeler":
            return str(sh["maddeler"][j]).split(":")[-1]
    except (KeyError, IndexError):
        pass
    return ""


def _kok(w):
    w = w.replace("İ", "i").replace("I", "ı").lower()
    return re.sub(r"[^\wçğıöşü]", "", w)


def capa_orani(cumle, oge, kelimeler=None):
    """Öğenin ilk anlamlı kelimesi cümlede nerede söyleniyor? (0-1 oran ya da Whisper saniyesi)
    manim-voiceover'ın 'bookmark' ve explainer-video'nun [köşeli parantez] fikri, işaretlemesiz hâli."""
    adaylar = [_kok(w) for w in re.split(r"[\s/·,()+=→]+", oge) if len(_kok(w)) >= 3]
    if not adaylar:
        return None
    hedef = adaylar[0]
    if kelimeler:
        for w in kelimeler:
            k_ = _kok(w["w"])
            if k_ and (k_.startswith(hedef[:5]) or hedef.startswith(k_[:5])) and len(k_) >= 3:
                return ("sn", w["s"])
    c = cumle.replace("İ", "i").replace("I", "ı").lower()
    m = re.search(r"(?<![\wçğıöşü])" + re.escape(hedef[:6]), c)
    if not m:
        return None
    return ("oran", m.start() / max(1, len(c)))


def giris_metni(sh):
    """Tahta boşken söylenen ilk cümle; 'ölü hava'yı (konuşma + boş ekran) önler."""
    if sh.get("giris"):
        return sh["giris"]
    c = temiz(cumlelere_bol(sh.get("anlatim", ""))[0]) if sh.get("anlatim") else ""
    c = c.rstrip(".!? ")
    if len(c) > 70:
        c = c[:70].rsplit(" ", 1)[0] + "…"
    return c


def senkron_raporu(sahneler, ilk, sureler):
    """explainer-video'nun sync_report fikri: ölü hava ve donuk ekran.
    sureler[si] = [cümle süresi, ...] (gerçek ses ya da tahmin)."""
    out = []
    for si, sh in enumerate(sahneler):
        cs = sureler[si]
        if not cs:
            continue
        bas = [sum(cs[:i]) + i * 0.4 for i in range(len(cs))]
        son = bas[-1] + cs[-1]
        gos = sh.get("goster") or []
        n_oge = len(sahne_ogeleri(sh))
        if gos:
            ts = sorted(bas[min(len(cs) - 1, int(float(str(g).split(":")[0])))] for g in gos)
        else:   # goster yoksa video öğeleri onları okuyan cümlede açar
            ts = [bas[min(len(cs) - 1, c_)] for c_ in oto_goster(sh, cumlelere_bol(sh["anlatim"]))] or []
        if sh.get("tur") in ("soru", "ipucu", "metin"):
            continue
        if ts and ts[0] > 4 and not sh.get("kanca"):
            out.append(f"sahne {ilk + si}: ilk öğe {ts[0]:.0f} sn sonra (giriş yazısı otomatik gösterilir)")
        olaylar = ([] if sh.get("kanca") else [0]) + ts + [son]
        bosluk = max(b - a for a, b in zip(olaylar, olaylar[1:]))
        if bosluk > 14:
            out.append(f"sahne {ilk + si}: {bosluk:.0f} sn boyunca tahtada yeni bir şey yok (donuk ekran) — öğe ekle ya da cümleyi böl")
    return out


def klip_temizle(x):
    """Chatterbox'ın cümle başı/sonundaki nefes ve 'hışırtı' seslerini temizler.
    Ölçüm: hışırtı = konuşma tepesinin ~25 dB altında, 4-7 kHz ağırlıklı, sesiz (unvoiced) uzun kuyruk.
    Konuşmanın sonundaki 's/ş' gibi sürtünmeli sesler daha yüksek ve kısa olduğu için korunur.
    Döner: (temiz ses, baştan kırpılan saniye)."""
    if len(x) < SR // 5:
        return x, 0.0
    w = SR // 100                                   # 10 ms
    n = len(x) // w
    fr = x[:n * w].reshape(n, w)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
    F = np.abs(np.fft.rfft(fr * np.hanning(w), axis=1)); f = np.fft.rfftfreq(w, 1 / SR)
    merkez = (F * f).sum(1) / (F.sum(1) + 1e-9)
    tepe = np.percentile(db, 95)
    # düşük seviye; ama tepeye 30 dB'den yakın ve tonlu (düşük frekanslı) kare konuşmadır, korunur
    dusuk = (db < tepe - 24) & ~((db > tepe - 30) & (merkez < 1500))
    # baş ve son: düşük seviyeli kuyrukları at
    i0 = 0
    while i0 < n and dusuk[i0]:
        i0 += 1
    i1 = n
    while i1 > i0 and dusuk[i1 - 1]:
        i1 -= 1
    if i1 <= i0:
        return x, 0.0
    a = max(0, i0 - 3) * w; b = min(len(x), (i1 + 4) * w)
    y = x[a:b].copy()
    # iç kısım: ≥150 ms süren düşük seviyeli bölgeler (nefes, hışırtı, mırıltı) → -24 dB
    d2, m2 = dusuk[max(0, i0 - 3):i1 + 4], merkez[max(0, i0 - 3):i1 + 4]
    hedef = d2.copy()   # tiz nefes ya da alçak mırıltı fark etmez: konuşmanın 24 dB altı ve ≥150 ms ise kıs
    kaz = np.ones(len(hedef))
    j = 0
    while j < len(hedef):
        if hedef[j]:
            k_ = j
            while k_ < len(hedef) and (hedef[k_] or (k_ + 1 < len(hedef) and hedef[k_ + 1])):
                k_ += 1
            if k_ - j >= 15:
                kaz[j + 2:k_ - 2] = 0.06      # kenarlarda 20 ms pay: geçiş konuşmayı kırpmasın
            j = k_
        else:
            j += 1
    if (kaz < 1).any():
        g = np.repeat(kaz, w)
        g = np.convolve(np.pad(g, (w, w), mode="edge"), np.ones(w * 2) / (w * 2), mode="same")[w:-w]
        y[:len(g)] *= g[:len(y)]
    return y, a / SR


def yumusat(x, giris=0.015, cikis=0.06):
    """Cümle kliplerinin kenarlarında tık/sürtme sesi olmasın: kısa fade-in/out + DC temizliği."""
    x = x - np.mean(x) if len(x) else x
    a, b = min(len(x) // 4, int(giris * SR)), min(len(x) // 4, int(cikis * SR))
    if a: x[:a] *= np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    if b: x[-b:] *= np.cos(np.linspace(0, np.pi / 2, b)) ** 2
    return x.astype(np.float32)


def efekt_tik():
    n = int(0.05 * SR); t = np.arange(n) / SR
    # gürültüsüz, yumuşak atak: 'mikrofon sürtmesi' gibi duyulmaz
    x = np.sin(2 * np.pi * 1200 * t) * np.exp(-t * 70) * np.minimum(1, t / 0.004)
    return (x * 0.02).astype(np.float32)


def efekt_ding():
    n = int(0.9 * SR); t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * 880 * t) + 0.6 * np.sin(2 * np.pi * 1318.5 * t) * (t > 0.09)) * np.exp(-t * 4.5)
    return (x * 0.06).astype(np.float32)


def cesitlilik_raporu(sahneler):
    """'Slayt gösterisi riski': tekdüzeliği ve aşırı yazıyı yakalar. (OpenMontage'ın fikrinden esinlenildi.)"""
    uyarilar = []
    turler = [sh.get("tur", "maddeler") for sh in sahneler]
    from collections import Counter
    en, sayi = Counter(turler).most_common(1)[0]
    if len(sahneler) >= 5 and sayi / len(turler) > 0.6:
        uyarilar.append(f"Sahnelerin %{100 * sayi // len(turler)}'i '{en}' türünde; tablo/rakam/zaman/karsilastirma/ipucu/soru ile çeşitlendir.")
    seri = 1
    for i in range(1, len(turler)):
        seri = seri + 1 if turler[i] == turler[i - 1] else 1
        if seri == 3 and turler[i] != "soru":
            uyarilar.append(f"{i - 1}.-{i + 1}. sahneler art arda '{turler[i]}'; araya farklı bir tür koy.")
    for i, sh in enumerate(sahneler, 1):
        kelime = len(temiz(sh.get("anlatim", "")).split())
        if kelime > 130:
            uyarilar.append(f"{i}. sahne anlatımı {kelime} kelime (önerilen ≤ 110); böl.")
        for m in sh.get("maddeler", []):
            if len(m) > 45:
                uyarilar.append(f"{i}. sahnede uzun madde ({len(m)} karakter): '{m[:30]}…'")
    if not any(t == "soru" for t in turler) and len(sahneler) >= 8:
        uyarilar.append("Hiç 'soru' sahnesi yok; izleyiciyi katmak için 2-3 'Kendini dene' ekle.")
    return uyarilar


# ================================================================ Whisper kalite kapısı
def _norm_kelimeler(t):
    import unicodedata
    t = unicodedata.normalize("NFC", t).replace("İ", "i").replace("I", "ı").lower()
    t = re.sub(r"\d+", lambda m: " " + sayi_yazi(int(m.group(0))) + " ", t)
    t = re.sub(r"[^\wçğıöşü ]+", " ", t)
    return t.split()


class Denetci:
    """Üretilen cümleyi Whisper ile dinler; metinle benzerliği (0-1) döndürür. faster-whisper gerekir."""

    def __init__(self, model="medium"):
        from faster_whisper import WhisperModel
        self.m = WhisperModel(model, device="cpu", compute_type="int8")

    def puan_parca(self, x, sr, metin, dil):
        """Tek bir parçayı (numpy, sr) kendi dilinde dinler: İngilizce parça 'en' ile, Türkçe 'tr' ile.
        Tüm cümleyi 'tr' ile dinlemek İngilizceyi Türkçeye çevirip yanıltıyordu."""
        import difflib
        n = int(len(x) * 16000 / sr)
        x16 = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
        segs, _ = self.m.transcribe(x16, language=dil, beam_size=5)
        duyulan = " ".join(s_.text.strip() for s_ in segs)
        if dil == "en":
            a = re.findall(r"[a-z0-9']+", metin.lower()); b = re.findall(r"[a-z0-9']+", duyulan.lower())
            b = [re.sub(r"\d+", lambda m: m.group(0), w) for w in b]
        else:
            a, b = _norm_kelimeler(metin), _norm_kelimeler(duyulan)
        return difflib.SequenceMatcher(a=a, b=b).ratio(), duyulan

    def puan(self, yol, metin):
        import difflib
        segs, _ = self.m.transcribe(str(yol), language="tr", beam_size=5, word_timestamps=True)
        segs = list(segs)
        duyulan = " ".join(x.text.strip() for x in segs)
        # kelime zamanları: video, tahtadaki öğeyi tam o kelime söylenirken açar
        self.kelimeler = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)}
                          for x in segs for w in (x.words or [])]
        return difflib.SequenceMatcher(a=_norm_kelimeler(metin), b=_norm_kelimeler(duyulan)).ratio(), duyulan


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
        metin = metin.replace("{", "").replace("}", "")   # bu motor dil değiştiremez
        with wave.open(str(yol), "wb") as wf:
            self.v.synthesize_wav(metin, wf, syn_config=self.cfg)


CHATTERBOX_URL = "https://github.com/alpay-web/egitim-videosu/releases/download/modeller-chatterbox/{}"
CHATTERBOX_DOSYALAR = ["ve.pt", "t3_mtl23ls_v2.safetensors", "s3gen.pt", "grapheme_mtl_merged_expanded_v1.json",
                       "conds.pt", "Cangjie5_TC.json"]


def chatterbox_yukle(d):
    """Önce yerel kopya, sonra Hugging Face, o da yoksa GitHub kopyası (parçalı dosyaları birleştirerek)."""
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    d = Path(d)
    if not all((d / f).exists() for f in CHATTERBOX_DOSYALAR):
        try:
            return ChatterboxMultilingualTTS.from_pretrained(device="cpu")
        except Exception:
            log("  Hugging Face'e erişilemedi; model GitHub kopyasından indiriliyor (tek seferlik, ~3 GB)...")
        d.mkdir(parents=True, exist_ok=True)
        for f in CHATTERBOX_DOSYALAR:
            if (d / f).exists():
                continue
            try:
                indir(CHATTERBOX_URL.format(f), d / (f + ".part"))
                (d / (f + ".part")).rename(d / f)
            except subprocess.CalledProcessError:
                parcalar, i = [], 0
                while True:
                    hedef = d / f"{f}.parca{i:02d}"
                    try:
                        indir(CHATTERBOX_URL.format(hedef.name), hedef)
                    except subprocess.CalledProcessError:
                        break
                    parcalar.append(hedef); i += 1
                if not parcalar:
                    raise
                with open(d / f, "wb") as out:
                    for p_ in parcalar:
                        out.write(p_.read_bytes()); p_.unlink()
    return ChatterboxMultilingualTTS.from_local(d, "cpu")


class ChatterboxSes:
    """Chatterbox Multilingual (Resemble AI, MIT lisansı): doğal tonlamalı Türkçe, referans sesten ses kopyalama.
    Referans verilmezse Piper 'fahrettin' (CC0) sesinden kısa bir referans üretilir."""

    def __init__(self, referans, dizin, hiz, abarti, cfg):
        import torch
        torch.set_num_threads(max(1, os.cpu_count() or 1))
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        sabit = Path(__file__).resolve().parents[1] / "ses" / "referans_fahrettin.wav"
        if not referans and sabit.exists():      # repodaki sabit referans: ses kimliği yıllarca aynı kalır
            referans = sabit
        if not referans:
            referans = Path(dizin) / "referans_fahrettin.wav"
            if not referans.exists():
                p = PiperSes("fahrettin", dizin, 0.92)
                metin = ("Merhaba, ben bugün size İngilizce öğrenmenin en etkili yollarını anlatacağım. "
                         "Hazırsanız başlayalım, çünkü önümüzde gerçekten keyifli bir yol var.")
                p.sentezle(metin, referans)
        self.ref = str(referans)
        self.m = chatterbox_yukle(Path(dizin) / "chatterbox")
        # Chatterbox 0.1.7 hatası: 5 belirteçten kısa metinde (ör. "so", "on") hizalama denetçisi IndexError atıyor.
        # Denetçiyi o adımda atla; süre kontrolü kaçak üretimi zaten yakalar.
        try:
            from chatterbox.models.t3.inference import alignment_stream_analyzer as _asa
            if not getattr(_asa.AlignmentStreamAnalyzer.step, "_guvenli", False):
                _asil = _asa.AlignmentStreamAnalyzer.step

                def _guvenli(self_, logits, *a, **k):
                    try:
                        return _asil(self_, logits, *a, **k)
                    except IndexError:
                        return logits
                _guvenli._guvenli = True
                _asa.AlignmentStreamAnalyzer.step = _guvenli
        except Exception:
            pass
        self.abarti, self.cfg, self.hiz = abarti, cfg, hiz
        self._varsayilan = (abarti, cfg)

    def ton(self, t):
        """Sahne bazında ses tonu: {"abarti": 0.6, "cfg": 0.4} ya da "sakin" / "canli" / "ciddi"."""
        hazir = {"sakin": (0.35, 0.45), "canli": (0.65, 0.5), "ciddi": (0.4, 0.55), "merakli": (0.6, 0.45)}
        if isinstance(t, str):
            self.abarti, self.cfg = hazir.get(t, self._varsayilan)
        elif isinstance(t, dict):
            self.abarti = t.get("abarti", self._varsayilan[0]); self.cfg = t.get("cfg", self._varsayilan[1])
        else:
            self.abarti, self.cfg = self._varsayilan
        log(f"  Ses: Chatterbox Multilingual (MIT), referans: {Path(self.ref).name}")

    def _uret(self, metin, dil):
        """Tek dilli bir parça. Denetçi bağlıysa (kod geçişli cümlelerde) her İngilizce parça kendi dilinde
        Whisper ile dinlenir; anlaşılır okunana kadar (en fazla 5 deneme) yeniden üretilir."""
        if getattr(self, "denetci", None) is not None and dil == "en":
            en, en_x = -1, None
            for d_ in range(5):
                x = self._uret_ham(metin, dil)
                p, duyulan = self.denetci.puan_parca(x, self.m.sr, metin, dil)
                log(f"     [en] «{metin[:40]}» deneme {d_ + 1}: {p:.2f} «{duyulan[:40]}»")
                if p > en:
                    en, en_x = p, x
                if p >= 0.85:
                    break
            return en_x
        return self._uret_ham(metin, dil)

    def _uret_ham(self, metin, dil):
        tahmin = max(0.7 if dil == "en" else 1.5, len(metin) / (13.0 if dil == "en" else 14.0))
        en_iyi = None
        for deneme in range(3):
            w = self.m.generate(metin, language_id=dil, audio_prompt_path=self.ref,
                                exaggeration=self.abarti, cfg_weight=self.cfg)
            x = w.squeeze().numpy()
            nz = np.nonzero(np.abs(x) > 0.02)[0]
            sure = (nz[-1] - nz[0]) / self.m.sr if len(nz) else 0
            sapma = abs(sure - tahmin) / tahmin
            if en_iyi is None or sapma < en_iyi[0]:
                en_iyi = (sapma, x, nz)
            if 0.5 * tahmin <= sure <= 1.6 * tahmin + 0.6:
                break
            log(f"   ! [{dil}] süre şüpheli ({sure:.1f} sn, beklenen ~{tahmin:.1f}), yeniden")
        _, x, nz = en_iyi
        if len(nz):
            x = x[max(0, nz[0] - int(0.02 * self.m.sr)): nz[-1] + int(0.06 * self.m.sr)]
        return x.astype(np.float32)

    def sentezle(self, metin, yol):
        import torch, torchaudio
        parcalar = parcalara_ayir(metin) if "{" in metin else [("tr", metin)]
        if len(parcalar) > 1 or parcalar[0][0] == "en":
            # kod geçişi: her parça kendi diliyle, aynı referans sesle; ses seviyeleri eşitlenir
            sesler = [self._uret(t, d) for d, t in parcalar]
            hedef = np.median([np.sqrt(np.mean(x ** 2)) + 1e-9 for x in sesler])
            bosluk = np.zeros(int(0.28 * self.m.sr), np.float32)   # alıntı öncesi/sonrası doğal virgül duraklaması
            birlesik = []
            for i, x in enumerate(sesler):
                x = x * min(2.0, hedef / (np.sqrt(np.mean(x ** 2)) + 1e-9))
                f = min(len(x) // 4, int(0.01 * self.m.sr))
                if f:
                    x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
                birlesik += ([bosluk] if i else []) + [x]
            w = torch.from_numpy(np.concatenate(birlesik)).unsqueeze(0)
            tmp = str(yol) + ".tmp.wav"
            torchaudio.save(tmp, w, self.m.sr)
            if abs(self.hiz - 1.0) > 0.01:
                subprocess.run([ffmpeg_bin(), "-v", "error", "-y", "-i", tmp, "-af", f"atempo={self.hiz}", str(yol)], check=True)
                os.remove(tmp)
            else:
                os.replace(tmp, yol)
            return
        metin = parcalar[0][1]
        tahmin = max(1.5, len(metin) / 14.0)  # ~14 karakter/sn
        en_iyi = None
        for deneme in range(3):  # model bazen cümle sonuna fazladan ses ekler: süre kontrolü
            w = self.m.generate(metin, language_id="tr", audio_prompt_path=self.ref,
                                exaggeration=self.abarti, cfg_weight=self.cfg)
            x = w.squeeze().numpy()
            nz = np.nonzero(np.abs(x) > 0.02)[0]
            sure = (nz[-1] - nz[0]) / self.m.sr if len(nz) else 0
            sapma = abs(sure - tahmin) / tahmin
            if en_iyi is None or sapma < en_iyi[0]:
                en_iyi = (sapma, w)
            if 0.55 * tahmin <= sure <= 1.6 * tahmin + 0.6:
                break
            log(f"   ! süre şüpheli ({sure:.1f} sn, beklenen ~{tahmin:.1f}), yeniden deneniyor")
        w = en_iyi[1]
        tmp = str(yol) + ".tmp.wav"
        torchaudio.save(tmp, w, self.m.sr)
        if abs(self.hiz - 1.0) > 0.01:  # perdeyi bozmadan yavaşlat
            subprocess.run([ffmpeg_bin(), "-v", "error", "-y", "-i", tmp, "-af", f"atempo={self.hiz}", str(yol)], check=True)
            os.remove(tmp)
        else:
            os.replace(tmp, yol)


class EdgeSes:
    def __init__(self, ad, hiz):
        import edge_tts  # noqa
        self.ad, self.hiz = ad, f"{round((hiz - 1) * 100):+d}%"
        log(f"  Ses: edge-tts '{ad}'")

    def sentezle(self, metin, yol):
        metin = metin.replace("{", "").replace("}", "")   # bu motor dil değiştiremez
        import edge_tts
        mp3 = str(yol) + ".mp3"
        asyncio.run(edge_tts.Communicate(metin, self.ad, rate=self.hiz).save(mp3))
        os.replace(mp3, yol)


class SessizSes:
    """Taslak/önizleme için: konuşma süresi kadar sessizlik (kelime başına ~0,43 sn). Seslendirme beklemeden
    zamanlamayı ve görselleri kontrol etmeye yarar; testlerde de kullanılır."""
    def __init__(self):
        log("  Ses: sessiz taslak (önizleme)")

    def sentezle(self, metin, yol):
        metin = metin.replace("{", "").replace("}", "")   # bu motor dil değiştiremez
        n = int(SR * (0.3 + len(metin.split()) / 2.3))
        with wave.open(str(yol), "wb") as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
            wf.writeframes(np.zeros(n, np.int16).tobytes())


class EspeakSes:
    def __init__(self):
        self.cli = shutil.which("espeak-ng") or shutil.which("espeak")
        log("  Ses: espeak-ng (robotik yedek)")

    def sentezle(self, metin, yol):
        metin = metin.replace("{", "").replace("}", "")   # bu motor dil değiştiremez
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
def agiz_bicimleri(ses, n_kare, spf):
    """Her kare için ağız biçimi: 'a' (açık), 'o' (yuvarlak: o/u/ö/ü), 'i' (yayvan: i/e, s/ş).
    Formant bantlarının enerji oranından; hiçbir model gerekmez (Rhubarb/Wav2Lip yerine maliyetsiz)."""
    f = np.fft.rfftfreq(spf, 1 / SR); pen = np.hanning(spf)
    b1, b2, b3 = (f >= 200) & (f < 550), (f >= 550) & (f < 1100), (f >= 1700) & (f < 3300)
    r13 = np.zeros(n_kare); r12 = np.zeros(n_kare); kon = np.zeros(n_kare, bool)
    for i in range(n_kare):
        v = ses[i * spf:(i + 1) * spf]
        if len(v) < spf or np.sqrt(np.mean(v ** 2)) < 0.02:
            continue
        F = np.abs(np.fft.rfft(v * pen)) ** 2
        e1, e2, e3 = F[b1].sum() + 1e-9, F[b2].sum() + 1e-9, F[b3].sum() + 1e-9
        r13[i], r12[i], kon[i] = e3 / (e1 + e2), e1 / e2, True
    # eşikler sesin kendisine göre (konuşan kişiden bağımsız): ~%25 'i', ~%20 'o', gerisi 'a'
    ei = np.percentile(r13[kon], 75) if kon.any() else 1
    eo = np.percentile(r12[kon], 80) if kon.any() else 1e9
    out = ["i" if kon[i] and r13[i] >= ei else "o" if kon[i] and r12[i] >= eo else "a" for i in range(n_kare)]
    for i in range(1, len(out) - 1):            # tek karelik titremeyi süz
        if out[i - 1] == out[i + 1] != out[i]:
            out[i] = out[i - 1]
    return out


def karakter_ciz(agiz, goz_kapali, kas, isaret, S, bicim="a"):
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
        if bicim == "o":     # yuvarlak dudak
            gen = 13 + acik * 0.35; yuk = acik * 0.9 + 6
            d.ellipse(P(210 - gen - 4, my - 7, 210 + gen + 4, my + yuk + 4), fill=(170, 80, 85))
            d.ellipse(P(210 - gen, my - 3, 210 + gen, my + yuk), fill=(105, 32, 42))
        elif bicim == "i":   # yayvan, dişler görünür
            gen = 32 + acik * 0.3; yuk = max(5, acik * 0.55)
            d.ellipse(P(210 - gen, my - 4, 210 + gen, my + yuk), fill=(110, 35, 45))
            d.rectangle(P(210 - gen * .75, my - 4, 210 + gen * .75, my + min(5, yuk * .5)), fill=(250, 250, 250))
        else:                # açık 'a'
            gen = 26 + acik * 0.4
            d.ellipse(P(210 - gen, my - 4, 210 + gen, my + acik), fill=(110, 35, 45))
            if acik > 12:
                d.ellipse(P(210 - gen * .6, my + acik * .45, 210 + gen * .6, my + acik - 1), fill=(220, 100, 110))
            d.rectangle(P(210 - gen * .7, my - 4, 210 + gen * .7, my + 2), fill=(250, 250, 250))
    for cx, cy, rr in [(170, 294, 22), (192, 288, 22), (228, 288, 22), (250, 294, 22), (150, 302, 16), (270, 302, 16)]:
        d.ellipse(P(cx - rr, cy - rr * .65, cx + rr, cy + rr * .65), fill=(222, 222, 218))
    yanak = Image.new("RGBA", im.size, (0, 0, 0, 0)); dy_ = ImageDraw.Draw(yanak)
    for cx in (120, 300):
        dy_.ellipse(P(cx - 22, 262, cx + 22, 290), fill=(250, 150, 140, 70))
    im.alpha_composite(yanak.filter(ImageFilter.GaussianBlur(4 * s)))
    d = ImageDraw.Draw(im)

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
        iz = Image.new("RGBA", im.size, (0, 0, 0, 0)); di = ImageDraw.Draw(iz)
        for _ in range(9):  # tebeşir izi dokusu (yalnızca tahtanın içinde)
            x, y = rnd.randint(560, 1080), rnd.randint(70, 470)
            di.arc(k(x, y, x + rnd.randint(80, 150), y + rnd.randint(30, 80)), rnd.randint(0, 180), rnd.randint(190, 360),
                   fill=(48, 86, 70, 255), width=k(6))
        maske = Image.new("L", im.size, 0); ImageDraw.Draw(maske).rectangle(k(538, 46, 1238, 554), fill=255)
        iz.putalpha(Image.fromarray(np.minimum(np.asarray(iz.getchannel("A")), np.asarray(maske))))
        im.paste(iz, (0, 0), iz)
        d = ImageDraw.Draw(im)
        d.rectangle(k(528, 560, 1248, 578), fill=(140, 96, 62))
        d.rectangle(k(588, 553, 628, 561), fill=(250, 250, 245))
        d.rectangle(k(648, 553, 674, 561), fill=(250, 230, 120))
        return im

    KURSU = (215, 389, 568, 690)  # x0, x1, üst, alt (taban birimi 1280x720)

    def kursu(self):
        """Profesörün önündeki ahşap kürsü (karakterin üstüne çizilir)."""
        k = self.k
        im = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        x0, x1, ust, alt = self.KURSU
        g = (x1 - x0) / 330  # ölçek
        # zemindeki gölge
        go = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        ImageDraw.Draw(go).ellipse(k(x0 - 10, alt - 8, x1 + 10, alt + 10), fill=(0, 0, 0, 80))
        go = go.filter(ImageFilter.GaussianBlur(k(5)))
        im.alpha_composite(go); d = ImageDraw.Draw(im)
        d.polygon(k(x0 + 18 * g, ust + 22 * g, x1 - 18 * g, ust + 22 * g, x1 - 30 * g, alt, x0 + 30 * g, alt), fill=(118, 78, 48))
        n = 4
        for i in range(n):  # tahta damarları
            y = ust + 22 * g + (alt - ust - 22 * g) * (i + 1) / (n + 1)
            d.line(k(x0 + 34 * g, y, x1 - 34 * g, y + 2), fill=(106, 70, 43), width=k(2))
        d.rounded_rectangle(k(x0 + 70 * g, ust + 50 * g, x1 - 70 * g, ust + 50 * g + (alt - ust) * 0.45), radius=k(4),
                            outline=(150, 108, 70), width=k(2))
        d.rounded_rectangle(k(x0, ust, x1, ust + 26 * g), radius=k(5), fill=(150, 104, 66))
        d.rectangle(k(x0 + 4, ust + 20 * g, x1 - 4, ust + 26 * g), fill=(96, 62, 38))
        sh = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle(k(x0 + 20 * g, ust + 26 * g, x1 - 20 * g, ust + 40 * g), fill=(0, 0, 0, 70))
        sh = sh.filter(ImageFilter.GaussianBlur(k(6)))
        sh.alpha_composite(im)
        return sh

    def _u(self, m):
        if m not in self.uyari:
            self.uyari.append(m)

    def giris_katmani(self, metin):
        """Tahta boşken büyük giriş yazısı (yarı saydam panel üstünde)."""
        k = self.k
        im = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        fs = 40
        while fs > 26 and len(satir_kir(metin, font(k(fs), True), k(560), d)) * fs * 1.35 > 230:
            fs -= 2
        sat = satir_kir(metin, font(k(fs), True), k(560), d)[:4]
        h = len(sat) * fs * 1.35 + 50
        y0 = 335 - h / 2
        d.rounded_rectangle(k(590, y0, 1190, y0 + h), radius=k(18), fill=(40, 78, 62, 235), outline=(255, 196, 80, 200), width=k(2))
        y = y0 + 25
        for t_ in sat:
            tw = d.textlength(t_, font=font(k(fs), True))
            d.text((k(890) - tw / 2, k(y)), t_, font=font(k(fs), True), fill=(255, 255, 255)); y += fs * 1.35
        return im

    def tahta(self, taban, sh, gorunen, no, toplam, ust, acik=False):
        tur = sh.get("tur", "maddeler")
        self._nokta = []; self.uyari = []
        if len(satir_kir(sh.get("baslik", ""), font(self.k(40), True), self.k(640), ImageDraw.Draw(taban))) > 2:
            self._u("başlık 2 satıra sığmıyor (kesildi)")
        if tur == "tablo":
            return self.tahta_tablo(taban, sh, gorunen, no, toplam, ust), []
        if tur == "soru":
            return self.tahta_soru(taban, sh, acik, no, toplam, ust), []
        if tur in ("rakam", "karsilastirma", "ipucu", "zaman", "metin"):
            return getattr(self, "tahta_" + tur)(taban, sh, gorunen, no, toplam, ust), []
        im = taban.copy(); d = ImageDraw.Draw(im); k = self.k
        fb, fk = font(k(40), True), font(k(16))
        y = 66
        for s in satir_kir(sh["baslik"], fb, k(640), d)[:2]:
            d.text(k(568, y), s, font=fb, fill=(255, 224, 115)); y += 48
        d.line(k(568, y + 6, 1210, y + 6), fill=(190, 205, 195), width=k(2))
        self.madde_y0 = y + 28
        self.fs = 34
        while self.fs > 24 and self.madde_y0 + sum(self.madde_yuk(m, d) for m in sh.get("maddeler", [])) > 515:
            self.fs -= 1
        if self.madde_y0 + sum(self.madde_yuk(m, d) for m in sh.get("maddeler", [])) > 515:
            self._u("maddeler tahtaya sığmıyor (taşma)")
        yy = self.madde_y0
        konumlar = []
        for i, m in enumerate(sh.get("maddeler", [])):
            konumlar.append(yy)
            self._nokta.append((556, yy + self.fs * 0.62))
            yy += self.madde_yuk(m, d)
        if gorunen == 0 and sh.get("kanca"):  # ilk madde gelene kadar büyük kanca cümlesi
            fs = 46
            while fs > 28 and len(satir_kir(sh["kanca"], font(k(fs), True), k(600), d)) * fs * 1.3 > k(330):
                fs -= 2
            yy = 150 + max(0, (330 - len(satir_kir(sh["kanca"], font(k(fs), True), k(600), d)) * fs * 1.3) / 2)
            for t_ in satir_kir(sh["kanca"], font(k(fs), True), k(600), d):
                tw = d.textlength(t_, font=font(k(fs), True))
                d.text((k(888) - tw / 2, k(yy)), t_, font=font(k(fs), True), fill=(255, 255, 255)); yy += fs * 1.3
        for i in range(gorunen):
            self.madde_ciz(d, sh["maddeler"][i], konumlar[i], vurgu=(i == gorunen - 1))
        d.text(k(1238 - 52, 528), f"{no}/{toplam}", font=fk, fill=(160, 185, 172))
        d.text(k(558, 528), ust, font=fk, fill=(160, 185, 172))
        return im, konumlar

    def _cerceve(self, taban, baslik, no, toplam, ust):
        im = taban.copy(); d = ImageDraw.Draw(im); k = self.k
        fb, fk = font(k(40), True), font(k(16))
        y = 66
        for s_ in satir_kir(baslik, fb, k(640), d)[:2]:
            d.text(k(568, y), s_, font=fb, fill=(255, 224, 115)); y += 48
        d.line(k(568, y + 6, 1210, y + 6), fill=(190, 205, 195), width=k(2))
        d.text(k(1238 - 52, 528), f"{no}/{toplam}", font=fk, fill=(160, 185, 172))
        d.text(k(558, 528), ust, font=fk, fill=(160, 185, 172))
        return im, d, y + 28

    def tahta_tablo(self, taban, sh, gorunen, no, toplam, ust):
        """Tablo: tüm sütunlar; uzun hücreler satır içinde alt satıra kayar, yazı sığana kadar küçülür."""
        im, d, y0 = self._cerceve(taban, sh["baslik"], no, toplam, ust)
        k = self.k
        tb = sh["tablo"]; bas = tb.get("basliklar", []); sat = tb["satirlar"]; stil = tb.get("stil")
        nk = max(len(bas), max(len(r) for r in sat))
        sat = [list(r) + [""] * (nk - len(r)) for r in sat]
        x0, x1 = 568, 1212
        on = "✗ " if stil else ""
        f0 = font(30)
        enk = []
        for j in range(nk):
            uz = max([d.textlength(on + str(r[j]), font=f0) for r in sat] + ([d.textlength(bas[j], font=font(30, True))] if j < len(bas) else [0]))
            enk.append(min(uz, 520) + 40)
        gens = [e / sum(enk) * (x1 - x0) for e in enk]
        gens = [max(g_, (x1 - x0) * 0.16) for g_ in gens]
        gens = [g_ / sum(gens) * (x1 - x0) for g_ in gens]
        xs_ = [x0 + sum(gens[:j]) for j in range(nk)]
        for fs in range(32, 15, -1):
            f_, fh = font(k(fs)), font(k(fs), True)
            hucre = [[satir_kir((on if (stil and j == 0) else "") + str(c), f_, k(gens[j] - 18), d) or [""]
                      for j, c in enumerate(r)] for r in sat]
            bas_s = [satir_kir(b_, fh, k(gens[j] - 18), d) or [""] for j, b_ in enumerate(bas)]
            lh = fs * 1.28
            rh = [max(len(x) for x in r) * lh + fs * 0.55 for r in hucre]
            bh = (max(len(x) for x in bas_s) * lh + fs * 0.45) if bas else 0
            if y0 + bh + sum(rh) <= 515:
                break
        else:
            self._u("tablo sığmıyor: hücre metnini kısalt ya da satırları ikiye böl")
        if fs < 20:
            self._u(f"tablo yazısı küçük ({int(fs * 1.5)} px @1080p, en az 30 px önerilir)")
        y = y0
        if bas:
            for j, b_ in enumerate(bas_s):
                renk = (255, 140, 130) if stil == "yanlis-dogru" and j == 0 else (150, 225, 160) if stil == "yanlis-dogru" and j == 1 else (255, 224, 115)
                yy = y + fs * 0.2
                for t_ in b_:
                    d.text((k(xs_[j] + 9), k(yy)), t_, font=fh, fill=renk); yy += lh
            y += bh
            d.line(k(x0, y - 4, x1, y - 4), fill=(190, 205, 195), width=k(2))
        y_ = y
        for i_, r in enumerate(sat):
            self._nokta.append((x0 - 14, y_ + min(rh[i_], lh * 1.2) / 2)); y_ += rh[i_]
        for i, r in enumerate(sat[:gorunen]):
            h = rh[i]
            if i == gorunen - 1:
                d.rounded_rectangle(k(x0 - 6, y + 2, x1 + 6, y + h - 3), radius=k(8), fill=(52, 98, 80))
            for j, c in enumerate(r):
                yy = y + fs * 0.25
                for t_ in hucre[i][j]:
                    tx = k(xs_[j] + 9)
                    if stil == "yanlis-dogru" and j == 0:
                        d.text((tx, k(yy)), t_, font=f_, fill=(255, 150, 140))
                        w_ = d.textlength(t_, font=f_)
                        d.line((tx, k(yy + fs * 0.62), tx + w_, k(yy + fs * 0.62)), fill=(255, 150, 140), width=k(2))
                    elif stil == "yanlis-dogru" and j == 1:
                        d.text((tx, k(yy)), t_, font=f_, fill=(165, 235, 170))
                    else:
                        d.text((tx, k(yy)), t_, font=f_, fill=(255, 255, 255) if i == gorunen - 1 else (205, 220, 210))
                    yy += lh
            y += h
            d.line(k(x0, y - 2, x1, y - 2), fill=(60, 100, 84), width=k(1))
        return im

    def tahta_soru(self, taban, sh, acik, no, toplam, ust):
        """Çoktan seçmeli (2-4 seçenek) ya da boşluk doldurma (secenekler yok, "cevap" var). Yazılar sığacak
        şekilde küçülür; boşluk doldurmada doğru cevap açılınca yeşil kutuda belirir."""
        im, d, y0 = self._cerceve(taban, sh["baslik"], no, toplam, ust)
        k = self.k
        q = sh["soru"]; sec = q.get("secenekler") or []
        alt = 512
        for fs in range(34, 17, -1):
            fq = font(k(fs), True); fo = font(k(max(18, fs - 3)))
            sat = satir_kir(q["metin"], fq, k(630), d)
            kutu_h = max(40, fs * 1.55)
            sec_sat = [satir_kir(o, fo, k(1140 - 652), d) for o in sec]
            yuk = 6 + len(sat) * fs * 1.35 + 16 + sum(max(kutu_h, len(x) * (fs - 3) * 1.3 + 14) + 10 for x in sec_sat)
            if not sec:
                yuk += kutu_h + 20
            if y0 + yuk <= alt:
                break
        else:
            self._u("soru ve seçenekler tahtaya sığmıyor")
        if fs < 20:
            self._u(f"soru yazısı küçük ({int(fs * 1.5)} px)")
        y = y0 + 6
        for s_ in sat:
            d.text(k(578, y), s_, font=fq, fill=(255, 255, 255)); y += fs * 1.35
        y += 16
        harfler = "ABCD"
        for i, o in enumerate(sec):
            dogru = i == q.get("dogru")
            if acik and dogru:
                kutu, yazi, harf = (58, 150, 92), (255, 255, 255), (255, 255, 255)
            elif acik:
                kutu, yazi, harf = (40, 78, 63), (140, 165, 150), (140, 165, 150)
            else:
                kutu, yazi, harf = (48, 92, 74), (235, 242, 238), (255, 210, 90)
            h = max(kutu_h, len(sec_sat[i]) * (fs - 3) * 1.3 + 14)
            d.rounded_rectangle(k(578, y, 1180, y + h), radius=k(10), fill=kutu)
            r = min(19, kutu_h / 2 - 5)
            d.ellipse(k(611 - r, y + h / 2 - r, 611 + r, y + h / 2 + r), outline=harf, width=k(3))
            ht = harfler[i] if i < 4 else str(i + 1)
            fh = font(k(max(16, fs - 10)), True); tw = d.textlength(ht, font=fh)
            d.text((k(611) - tw / 2, k(y + h / 2) - k(max(16, fs - 10)) * 0.6), ht, font=fh, fill=harf)
            yy = y + (h - len(sec_sat[i]) * (fs - 3) * 1.3) / 2
            for t_ in sec_sat[i]:
                d.text(k(648, yy), t_, font=fo, fill=yazi); yy += (fs - 3) * 1.3
            if acik and dogru:
                d.text(k(1148, y + h / 2 - 18), "✓", font=font(k(30), True), fill=(255, 255, 255))
            y += h + 10
        if not sec and q.get("cevap"):
            if acik:
                fc = font(k(fs), True)
                d.rounded_rectangle(k(578, y, 1180, y + kutu_h + 8), radius=k(10), fill=(58, 150, 92))
                d.text(k(600, y + 6), "✓  " + q["cevap"], font=fc, fill=(255, 255, 255))
            else:
                d.rounded_rectangle(k(578, y, 1180, y + kutu_h + 8), radius=k(10), outline=(90, 130, 112), width=k(2))
                d.text(k(600, y + 6), "?", font=font(k(fs), True), fill=(150, 180, 165))
        return im

    def tahta_metin(self, taban, sh, gorunen, no, toplam, ust):
        """Okuma parçası / dinleme metni / model cevap: {"tur": "metin", "metin": "..."} (sığacak kadar küçülür)."""
        im, d, y0 = self._cerceve(taban, sh["baslik"], no, toplam, ust)
        k = self.k
        paragraflar = [p_ for p_ in str(sh["metin"]).split("\n") if p_.strip()]
        for fs in range(30, 15, -1):
            f_ = font(k(fs))
            satirlar = [satir_kir(p_, f_, k(630), d) for p_ in paragraflar]
            yuk = sum(len(x) for x in satirlar) * fs * 1.32 + (len(paragraflar) - 1) * fs * 0.5
            if y0 + yuk <= 512:
                break
        else:
            self._u("metin tahtaya sığmıyor: daha kısa parçalara böl")
        if fs < 18:
            self._u(f"metin yazısı küçük ({int(fs * 1.5)} px)")
        y = y0
        for x in satirlar:
            for t_ in x:
                d.text(k(578, y), t_, font=f_, fill=(240, 246, 242)); y += fs * 1.32
            y += fs * 0.5
        self._nokta.append((566, y0 + 10))
        return im

    def tahta_rakam(self, taban, sh, gorunen, no, toplam, ust):
        """1-3 büyük rakam kartı: {"kartlar": [{"deger": "30", "birim": "dk", "etiket": "Sınav süresi"}]}"""
        im, d, y0 = self._cerceve(taban, sh["baslik"], no, toplam, ust)
        k = self.k
        kartlar = sh["kartlar"]; n = len(kartlar)
        x0, x1 = 568, 1212; ara = 22
        gen = (x1 - x0 - ara * (n - 1)) / n
        yk0, yk1 = y0 + 20, 500
        for i, c in enumerate(kartlar):
            cx0 = x0 + i * (gen + ara)
            self._nokta.append((cx0 + gen / 2, yk1 + 12))
            if i >= gorunen:
                d.rounded_rectangle(k(cx0, yk0, cx0 + gen, yk1), radius=k(16), outline=(52, 92, 76), width=k(2))
                continue
            vurgu = i == gorunen - 1
            d.rounded_rectangle(k(cx0, yk0, cx0 + gen, yk1), radius=k(16), fill=(50, 96, 78) if vurgu else (44, 84, 68))
            fs = 96
            while fs > 28 and d.textlength(c["deger"], font=font(k(fs), True)) > k(gen - 30):
                fs -= 4
            fv = font(k(fs), True)
            if d.textlength(c["deger"], font=fv) > k(gen - 30):
                self._u(f"rakam kartı '{c['deger']}' sığmıyor")
            tw = d.textlength(c["deger"], font=fv)
            d.text((k(cx0 + gen / 2) - tw / 2, k(yk0 + 40)), c["deger"], font=fv, fill=(255, 210, 90))
            if c.get("birim"):
                fb_ = font(k(32), True); tw = d.textlength(c["birim"], font=fb_)
                d.text((k(cx0 + gen / 2) - tw / 2, k(yk0 + 50 + fs * 1.05)), c["birim"], font=fb_, fill=(255, 255, 255))
            yy = yk0 + 100 + fs * 1.05
            fe_s = 24
            while fe_s > 16 and yy + len(satir_kir(c.get("etiket", ""), font(k(fe_s)), k(gen - 26), d)) * fe_s * 1.3 > yk1 - 8:
                fe_s -= 1
            fe = font(k(fe_s))
            for sat in satir_kir(c.get("etiket", ""), fe, k(gen - 26), d):
                tw = d.textlength(sat, font=fe)
                d.text((k(cx0 + gen / 2) - tw / 2, k(yy)), sat, font=fe, fill=(210, 226, 216)); yy += fe_s * 1.3
        return im

    def tahta_karsilastirma(self, taban, sh, gorunen, no, toplam, ust):
        """İki kart yan yana: {"sol": {"baslik": .., "renk": "kirmizi"}, "sag": {...}, "satirlar": [["sol", "sağ"], ...]}"""
        im, d, y0 = self._cerceve(taban, sh["baslik"], no, toplam, ust)
        k = self.k
        renkler = {"kirmizi": (255, 150, 140), "yesil": (165, 235, 170), "sari": (255, 210, 90), "mavi": (150, 200, 255)}
        sol, sag = sh["sol"], sh["sag"]; sat = sh["satirlar"]
        x0, x1, ort = 568, 1212, 890
        fs = 30
        while fs > 20:
            f_ = font(k(fs))
            satir_say = sum(max(len(satir_kir(a, f_, k(285), d)), len(satir_kir(b, f_, k(285), d))) for a, b in sat)
            if y0 + 70 + satir_say * fs * 1.35 + len(sat) * 18 <= 512:
                break
            fs -= 1
        else:
            self._u("karşılaştırma kartları taşıyor: satır metinlerini kısalt")
        f_ = font(k(fs))
        for j, (yan, xa, xb) in enumerate(((sol, x0, ort - 12), (sag, ort + 12, x1))):
            r = renkler.get(yan.get("renk", "sari" if j == 0 else "yesil"), (255, 210, 90))
            d.rounded_rectangle(k(xa, y0, xb, 515), radius=k(14), fill=(42, 82, 66))
            d.text(k(xa + 18, y0 + 12), yan["baslik"], font=font(k(30), True), fill=r)
            d.line(k(xa + 18, y0 + 56, xb - 18, y0 + 56), fill=r, width=k(2))
        # önce sol sütun satır satır, sonra sağ sütun (anlatım sırasıyla)
        n = len(sat); y = y0 + 70; ys_ = []
        for a, b in sat:
            la, lb = satir_kir(a, f_, k(285), d), satir_kir(b, f_, k(285), d)
            ys_.append((y, la, lb)); y += max(len(la), len(lb)) * fs * 1.35 + 18
        for j in range(2):
            for i, (y, la, lb) in enumerate(ys_):
                idx = j * n + i
                self._nokta.append(((x0 + 16) if j == 0 else (ort + 28), y + fs * 0.65))
                if idx < gorunen:
                    renk = (255, 255, 255) if idx == gorunen - 1 else (200, 216, 206)
                    yy = y
                    for t_ in (la if j == 0 else lb):
                        d.text(k((x0 + 22) if j == 0 else (ort + 34), yy), t_, font=f_, fill=renk); yy += fs * 1.35
        return im

    def tahta_ipucu(self, taban, sh, gorunen, no, toplam, ust):
        """Büyük vurgu kutusu: {"ipucu": {"tip": "ipucu|uyari|not", "metin": "..."}}"""
        im, d, y0 = self._cerceve(taban, sh["baslik"], no, toplam, ust)
        k = self.k
        ip = sh["ipucu"]; tip = ip.get("tip", "ipucu")
        renk, ikon, ad = {"uyari": ((235, 120, 90), "!", "DİKKAT"), "not": ((150, 200, 255), "i", "NOT")}.get(
            tip, ((255, 205, 90), "★", "İPUCU"))
        d.rounded_rectangle(k(578, y0 + 10, 1200, 505), radius=k(18), fill=(44, 84, 68), outline=renk, width=k(4))
        d.ellipse(k(600, y0 + 32, 664, y0 + 96), fill=renk)
        fi = font(k(40), True); tw = d.textlength(ikon, font=fi)
        d.text((k(632) - tw / 2, k(y0 + 38)), ikon, font=fi, fill=(30, 50, 42))
        d.text(k(682, y0 + 46), ad, font=font(k(30), True), fill=renk)
        fs = 40
        while fs > 24:
            ls_ = satir_kir(ip["metin"], font(k(fs), True), k(560), d)
            if y0 + 120 + len(ls_) * fs * 1.3 <= 495:
                break
            fs -= 2
        else:
            self._u("ipucu metni kutudan taşıyor")
        y = y0 + 120
        for t_ in satir_kir(ip["metin"], font(k(fs), True), k(560), d):
            d.text(k(610, y), t_, font=font(k(fs), True), fill=(255, 255, 255)); y += fs * 1.3
        self._nokta.append((590, y0 + 64))
        return im

    def tahta_zaman(self, taban, sh, gorunen, no, toplam, ust):
        """Yatay zaman çizelgesi: {"adimlar": [{"baslik": "1. Gün", "metin": "..."}]} (en fazla 5)"""
        im, d, y0 = self._cerceve(taban, sh["baslik"], no, toplam, ust)
        k = self.k
        ad = sh["adimlar"]; n = len(ad)
        if n >= 4:  # dikey düzen: çok adımda yazılar sığsın
            xl = 604; ya, yb = y0 + 22, 500
            adim = (yb - ya) / max(1, n - 1)
            d.line(k(xl, ya, xl, yb), fill=(70, 112, 96), width=k(6))
            if gorunen > 1:
                d.line(k(xl, ya, xl, ya + adim * (min(gorunen, n) - 1)), fill=(255, 196, 80), width=k(6))
            fb_, f_ = font(k(27), True), font(k(27))
            for i, a in enumerate(ad):
                yc_ = ya + adim * i
                self._nokta.append((xl - 16, yc_))
                acik = i < gorunen; vurgu = i == gorunen - 1
                r = 15 if vurgu else 11
                d.ellipse(k(xl - r, yc_ - r, xl + r, yc_ + r), fill=(255, 196, 80) if acik else (70, 112, 96),
                          outline=(255, 255, 255) if vurgu else None, width=k(3))
                if acik:
                    d.text(k(xl + 30, yc_ - 18), a["baslik"], font=fb_, fill=(255, 224, 115))
                    bw = d.textlength(a["baslik"], font=fb_)
                    kalan = k(1205) - (k(xl + 30) + bw + k(18))
                    metin = satir_kir(a.get("metin", ""), f_, kalan, d)
                    if len(metin) > 1:
                        self._u(f"zaman adımı '{a['baslik']}' metni tek satıra sığmıyor (kesildi)")
                    d.text((k(xl + 30) + bw + k(18), k(yc_ - 18)), metin[0] if metin else "", font=f_,
                           fill=(255, 255, 255) if vurgu else (205, 220, 210))
            return im
        x0, x1 = 600, 1180; yc = y0 + 60
        aralik = (x1 - x0) / max(1, n - 1)
        d.line(k(x0, yc, x1, yc), fill=(70, 112, 96), width=k(6))
        if gorunen > 1:
            d.line(k(x0, yc, x0 + aralik * (min(gorunen, n) - 1), yc), fill=(255, 196, 80), width=k(6))
        gen = min(220, aralik + 40) if n > 1 else 400
        for i, a in enumerate(ad):
            cx = x0 + aralik * i if n > 1 else (x0 + x1) / 2
            self._nokta.append((cx, yc + 34))
            acik = i < gorunen; vurgu = i == gorunen - 1
            r = 18 if vurgu else 14
            d.ellipse(k(cx - r, yc - r, cx + r, yc + r), fill=(255, 196, 80) if acik else (70, 112, 96),
                      outline=(255, 255, 255) if vurgu else None, width=k(3))
            if not acik:
                continue
            fb_ = font(k(24), True); f_ = font(k(21))
            yy = yc + 34
            for t_ in satir_kir(a["baslik"], fb_, k(gen - 10), d)[:2]:
                tw = d.textlength(t_, font=fb_)
                d.text((k(cx) - tw / 2, k(yy)), t_, font=fb_, fill=(255, 224, 115)); yy += 30
            if len(satir_kir(a.get("metin", ""), f_, k(gen - 10), d)) > 6 or len(satir_kir(a["baslik"], fb_, k(gen - 10), d)) > 2:
                self._u(f"zaman adımı '{a['baslik']}' kesildi")
            for t_ in satir_kir(a.get("metin", ""), f_, k(gen - 10), d)[:6]:
                tw = d.textlength(t_, font=f_)
                d.text((k(cx) - tw / 2, k(yy)), t_, font=f_, fill=(255, 255, 255) if vurgu else (205, 220, 210)); yy += 27
        return im

    def isaretci(self, im, x, y, t):
        """Anlatılan öğeyi gösteren tebeşir işaretçisi (hafif nabız)."""
        d = ImageDraw.Draw(im); k = self.k
        n = 1 + 0.12 * math.sin(t * 6)
        r = 9 * n
        d.polygon([k(x - 26 * n, y - r), k(x - 6, y), k(x - 26 * n, y + r)], fill=(255, 196, 80))

    def geri_sayim(self, im, kalan, oran):
        """Soru sahnesinde düşünme süresi göstergesi."""
        d = ImageDraw.Draw(im); k = self.k
        cx, cy, r = 1170, 110, 34
        d.ellipse(k(cx - r, cy - r, cx + r, cy + r), outline=(80, 120, 100), width=k(7))
        d.arc(k(cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * (1 - oran), fill=(255, 196, 80), width=k(7))
        t_ = str(max(1, math.ceil(kalan)))
        f_ = font(k(30), True); tw = d.textlength(t_, font=f_)
        d.text((k(cx) - tw / 2, k(cy - 19)), t_, font=f_, fill=(255, 255, 255))

    def madde_yuk(self, m, d):
        return (len(satir_kir(m, font(self.k(self.fs)), self.k(600), d)) * self.fs * 1.3 + self.fs * 0.6)

    def madde_ciz(self, d, m, y, vurgu, dx=0):
        k = self.k
        fm = font(k(self.fs))
        renk = (255, 255, 255) if vurgu else (200, 216, 206)
        r = self.fs * 0.24; cy_ = y + self.fs * 0.62
        d.ellipse((k(578 - r) + dx, k(cy_ - r), k(578 + r) + dx, k(cy_ + r)), fill=(255, 196, 80))
        for s in satir_kir(m, fm, k(600), d):
            d.text((k(600) + dx, k(y)), s, font=fm, fill=renk); y += self.fs * 1.3

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
        sat = satir_kir(metin, fnt, k(690), d)
        if len(sat) > 1:  # satırları dengele (tek kelimelik dul satır olmasın)
            toplam = d.textlength(metin, font=fnt)
            sat = satir_kir(metin, fnt, min(k(690), toplam / len(sat) * 1.08 + k(30)), d)
        sat = sat[:3]
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


# ================================================================ YouTube kapak görseli
def kapak_gorseli(sen, karakter_png, yol):
    W, H = 1280, 720
    t = np.linspace(0, 1, W)[None, :, None]
    a, b = np.array([20, 62, 52]), np.array([10, 28, 32])
    im = Image.fromarray(np.broadcast_to(a * (1 - t) + b * t, (H, W, 3)).astype(np.uint8).copy()).convert("RGBA")
    d = ImageDraw.Draw(im)
    rnd = random.Random(9)
    for _ in range(14):
        x, y = rnd.randint(0, 700), rnd.randint(0, 680)
        d.arc((x, y, x + rnd.randint(120, 300), y + rnd.randint(40, 120)), 0, rnd.randint(120, 300), fill=(40, 90, 75), width=5)
    if karakter_png is None:
        k = karakter_ciz(0, False, 1.0, False, 1.15)
        im.alpha_composite(k, (W - k.width + 20, H - k.height + 40))
    elif Path(karakter_png).exists():
        k = Image.open(karakter_png).convert("RGBA")
        s = 780 / k.height
        k = k.resize((int(k.width * s), 780), Image.LANCZOS)
        im.alpha_composite(k, (W - k.width + 130, H - k.height + 60))
    d = ImageDraw.Draw(im)
    baslik = sen.get("kapak_baslik") or sen.get("baslik", "")
    parcalar = [x.strip() for x in re.split(r"\s+[–—-]\s+", baslik) if x.strip()]
    vurgu = parcalar[-1] if len(parcalar) > 1 else baslik
    ust = parcalar[0] if len(parcalar) > 1 else ""
    buyuk = vurgu.replace("i", "İ").replace("ı", "I").upper()  # Türkçe büyük harf
    fs_ = 118
    while fs_ > 60:
        fb = font(fs_, True)
        satirlar = satir_kir(buyuk, fb, 600, d)
        if len(satirlar) <= 3 and all(d.textlength(x, font=fb) <= 600 for x in satirlar):
            break
        fs_ -= 6
    satirlar = satirlar[:3]
    y = 360 - len(satirlar) * fs_ * 0.56
    if ust:
        fu = font(40, True)
        us = satir_kir(ust, fu, 600, d)[:2]
        for i_, sat in enumerate(us):
            d.text((60, y - 70 - (len(us) - 1 - i_) * 50), sat, font=fu, fill=(205, 230, 218))
    for sat in satirlar:
        for ox, oy in ((5, 6),):
            d.text((60 + ox, y + oy), sat, font=fb, fill=(0, 0, 0, 160))
        d.text((60, y), sat, font=fb, fill=(255, 210, 80)); y += fs_ * 1.12
    d.rectangle((60, y + 8, 360, y + 18), fill=(255, 255, 255))
    im.convert("RGB").save(yol, quality=92)


# ================================================================ ana akış
def _sn(t, srt=True):
    h, m, s_ = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h:02d}:{m:02d}:{s_:06.3f}".replace(".", ",") if srt else (f"{h}:{m:02d}:{int(s_):02d}" if h else f"{m:02d}:{int(s_):02d}")


def yayin_paketi(cikti, sen, sahneler, zc, bolum_adi):
    """YouTube'a hazır paket: .srt altyazı + bölümlü açıklama (explainer-video .srt, MoneyPrinterTurbo altyazı)."""
    # 1) SRT: uzun cümleler ≤ 2 satır × 42 karakterlik parçalara bölünür, süre karakterle orantılı
    girdiler = []
    for bas, bit, cz in zc:
        for a, b, metin in cz:
            parca, cur = [], ""
            for w in metin.split():
                if len(cur) + len(w) + 1 > 84 and cur:
                    parca.append(cur); cur = w
                else:
                    cur = (cur + " " + w).strip()
            if cur:
                parca.append(cur)
            top = sum(len(x) for x in parca) or 1; t0 = a
            for x in parca:
                t1 = t0 + (b - a) * len(x) / top
                if len(x) > 42:   # iki satıra dengeli böl
                    ks = x.split(); yarim = len(x) / 2; acc, i_ = 0, 0
                    for i_, w in enumerate(ks):
                        acc += len(w) + 1
                        if acc >= yarim:
                            break
                    x = " ".join(ks[:i_ + 1]) + "\n" + " ".join(ks[i_ + 1:])
                girdiler.append((t0, t1, x)); t0 = t1
    srt = "\n".join(f"{i + 1}\n{_sn(a)} --> {_sn(b)}\n{x}\n" for i, (a, b, x) in enumerate(girdiler))
    cikti.with_suffix(".srt").write_text(srt, encoding="utf-8")
    # 2) Bölümler: "bolum" alanı varsa onlar; yoksa soru olmayan sahne başlıkları (en az 10 sn arayla)
    bol = []
    if any(sh.get("bolum") for sh in sahneler):
        for i, sh in enumerate(sahneler):
            if sh.get("bolum"):
                bol.append([zc[i][0] if i else 0.0, sh["bolum"]])
    else:
        for i, sh in enumerate(sahneler):
            if sh.get("tur") != "soru":
                bol.append([zc[i][0] if i else 0.0, sh.get("baslik", "")])
    temiz_bol = []
    for t, ad in bol:
        if temiz_bol and t - temiz_bol[-1][0] < 10:
            continue
        temiz_bol.append([t, ad])
    if temiz_bol:
        temiz_bol[0][0] = 0.0
    aciklama = [sen.get("alt_baslik", ""), ""]
    if len(temiz_bol) >= 3:
        aciklama += ["Bölümler:"] + [f"{_sn(t, False)} {ad}" for t, ad in temiz_bol] + [""]
    aciklama += ["Seslendirme ve animasyon açık kaynak araçlarla, yapay zekâ desteğiyle üretilmiştir."]
    paket = (f"BAŞLIK:\n{sen.get('youtube_baslik', sen.get('baslik', ''))}\n\nAÇIKLAMA:\n" + "\n".join(aciklama) +
             "\n\nETİKETLER:\n" + ", ".join(sen.get("etiketler", [])) +
             "\n\nNOT: YouTube Studio > Altyazılar bölümüne " + cikti.with_suffix(".srt").name +
             " dosyasını yükleyin; 'Değiştirilmiş veya yapay içerik' kutusunu işaretleyin.\n")
    cikti.with_name(cikti.stem + "_youtube.txt").write_text(paket, encoding="utf-8")
    if len(sen.get("youtube_baslik", sen.get("baslik", ""))) > 100:
        log("  ⚠ YouTube başlığı 100 karakteri aşıyor; 'youtube_baslik' alanını kısalt.")
    log(f"  Yayın paketi: {cikti.with_suffix('.srt').name}, {cikti.stem}_youtube.txt ({len(temiz_bol)} bölüm)")
    return temiz_bol


def bolumleri_gom(cikti, bolumler, sure):
    """MP4'e bölüm işaretleri (chapter) gömer: VLC/oynatıcılarda bölüm menüsü (abogen M4B bölümleri)."""
    if len(bolumler) < 2:
        return
    md = [";FFMETADATA1"]
    for i, (t, ad) in enumerate(bolumler):
        son = bolumler[i + 1][0] if i + 1 < len(bolumler) else sure
        ad_ = str(ad).replace("=", "\\=").replace(";", "\\;").replace("#", "\\#").replace("\n", " ")
        md += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(t * 1000)}", f"END={int(son * 1000)}", f"title={ad_}"]
    mdf = cikti.with_name(cikti.stem + ".ffmeta")
    mdf.write_text("\n".join(md) + "\n", encoding="utf-8")
    gecici = cikti.with_name(cikti.stem + ".bolumlu.mp4")
    r = subprocess.run([ffmpeg_bin(), "-v", "error", "-y", "-i", str(cikti), "-i", str(mdf), "-map", "0",
                        "-map_metadata", "1", "-map_chapters", "1", "-c", "copy", "-movflags", "+faststart", str(gecici)])
    mdf.unlink(missing_ok=True)
    if r.returncode == 0 and gecici.exists():
        gecici.replace(cikti); log(f"  {len(bolumler)} bölüm işareti MP4'e gömüldü")
    else:
        gecici.unlink(missing_ok=True)


def yayin_denetimi(cikti, hedef_lufs=-14.0, beklenen=()):
    """Son dosyayı ölçer (explainroo/ffmpeg-skill 'check'): ses yüksekliği, tepe, uzun sessizlik, çözünürlük."""
    sonuc, uyari = {}, []
    o = subprocess.run([ffmpeg_bin(), "-hide_banner", "-i", str(cikti), "-af",
                        "ebur128=peak=true,silencedetect=n=-45dB:d=3", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", o); tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", o)
    sessiz = []
    for b_, d_ in re.findall(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", o):
        bit_, d_ = float(b_), float(d_); bas_ = bit_ - d_
        ortak = sum(max(0.0, min(bit_, y) - max(bas_, x)) for x, y in beklenen)
        if d_ - ortak > 2.5:      # giriş/kapanış/soru bekleme dışında kalan sessizlik
            sessiz.append(round(bas_, 1))
    if m:
        sonuc["lufs"] = float(m[-1])
        if abs(sonuc["lufs"] - hedef_lufs) > 1.5:
            uyari.append(f"ses yüksekliği {sonuc['lufs']:.1f} LUFS (hedef {hedef_lufs})")
    if tp:
        sonuc["tepe_dbfs"] = float(tp[-1])
        if sonuc["tepe_dbfs"] > -1.0:
            uyari.append(f"gerçek tepe {sonuc['tepe_dbfs']:.1f} dBFS (> -1, kırpılma riski)")
    sonuc["beklenmedik_sessizlik_sn"] = sessiz
    if sessiz:
        uyari.append("beklenmedik uzun sessizlik: " + ", ".join(_sn(x, False) for x in sessiz[:8]))
    sonuc["uyarilar"] = uyari
    cikti.with_name(cikti.stem + "_denetim.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    log("  Yayın denetimi: " + (" · ".join(uyari) if uyari else
        f"ses {sonuc.get('lufs', '?')} LUFS, tepe {sonuc.get('tepe_dbfs', '?')} dBFS ✔"))
    return sonuc


def sahne_suresi_tahmin(sh, tempo=0.9):
    """Bir sahnenin yaklaşık süresi (sn): ~2.3 kelime/sn, tempo ve cümle/sahne araları dahil."""
    cs = cumlelere_bol(sh.get("anlatim", ""))
    return sum(len(temiz(c).split()) / 2.3 + 0.3 for c in cs) / max(0.5, tempo) + len(cs) * CUMLE_ARASI + SAHNE_ARASI


def onizleme_sec(sahneler, hedef_sn=90, tempo=0.9):
    """Uzun videodan önce onay için 1-2 dk'lık temsili seçki (anything2explainer 'ilk 30 sn',
    vox-director/frametell onay kapıları). Açılış sahnesi + her sahne türünden en kısa temsilci,
    belge sırasıyla; hedef süre dolana kadar. Dönen: seçilen sahne indisleri (0 tabanlı)."""
    if not sahneler:
        return []
    sec = [0]; top = sahne_suresi_tahmin(sahneler[0], tempo)
    turler = {}
    for i, sh in enumerate(sahneler[1:], 1):
        turler.setdefault(sh.get("tur", "maddeler"), []).append(i)
    adaylar = []
    for tur, ix in turler.items():   # her türün en kısa (ama boş olmayan) sahnesi
        ix = sorted(ix, key=lambda i: sahne_suresi_tahmin(sahneler[i], tempo))
        adaylar.append(ix[0])
    adaylar.sort(key=lambda i: sahne_suresi_tahmin(sahneler[i], tempo))
    for i in adaylar:
        d = sahne_suresi_tahmin(sahneler[i], tempo)
        if top + d <= hedef_sn * 1.35 or len(sec) < 3:
            sec.append(i); top += d
    # İngilizce geçişli (code-switch) bir sahne mutlaka olsun: telaffuz en çok orada bozuluyor
    if not any("{" in sahneler[i].get("anlatim", "") for i in sec):
        ing = [i for i in range(1, len(sahneler)) if "{" in sahneler[i].get("anlatim", "")]
        if ing:
            i = min(ing, key=lambda i: sahne_suresi_tahmin(sahneler[i], tempo)); sec.append(i)
            top += sahne_suresi_tahmin(sahneler[i], tempo)
    if top < hedef_sn * 0.6:          # kısa kaldıysa aynı türlerden ikinci örnekler
        for i in sorted(range(1, len(sahneler)), key=lambda i: sahne_suresi_tahmin(sahneler[i], tempo)):
            if i not in sec and top + sahne_suresi_tahmin(sahneler[i], tempo) <= hedef_sn * 1.2:
                sec.append(i); top += sahne_suresi_tahmin(sahneler[i], tempo)
    return sorted(sec)


def main():
    ap = argparse.ArgumentParser(description="Senaryodan animasyonlu eğitim videosu (ücretsiz/açık kaynak).")
    ap.add_argument("senaryo")
    ap.add_argument("-o", "--cikti", default="egitim_videosu.mp4")
    ap.add_argument("--ses", choices=["chatterbox", "piper", "edge", "espeak", "sessiz"], default="chatterbox",
                    help="sessiz = seslendirmesiz hızlı taslak (zamanlama ve görsel kontrolü)")
    ap.add_argument("--referans", help="chatterbox için referans ses dosyası (wav/mp3, 10-20 sn)")
    ap.add_argument("--abarti", type=float, default=0.5, help="chatterbox duygu/vurgu (0.25-0.7)")
    ap.add_argument("--cfg", type=float, default=0.5, help="chatterbox tempo/sadakat (düşük = daha sakin)")
    ap.add_argument("--ses-dizini", help="hazır cümle sesleri; virgülle birden çok klasör. Önce içerik anahtarıyla (dizin.json), sonra SS_CC adıyla aranır")
    ap.add_argument("--sadece-ses", metavar="KLASOR", help="video üretmeden sadece cümle seslerini bu klasöre yaz")
    ap.add_argument("--kalite", type=int, default=0, help="Whisper kalite kapısı: cümle başına en fazla N deneme")
    ap.add_argument("--esik", type=float, default=0.9, help="kalite kapısı kabul eşiği (0-1)")
    ap.add_argument("--cumleler", help="sadece bu cümleleri üret, ör. 02_03,05_00")
    ap.add_argument("--taban-ses", help="--sadece-ses ile: bu klasör(ler)de aynı metnin sesi varsa yeniden üretmeden kopyala (önbellek)")
    ap.add_argument("--karakter", default="cizim",
                    help="karakter JSON'u (yanında aynı adlı .png) ya da 'cizim'")
    ap.add_argument("--piper-ses", default="fahrettin", choices=list(PIPER_SESLER))
    ap.add_argument("--edge-ses", default="tr-TR-AhmetNeural")
    ap.add_argument("--hiz", type=float, default=1.0, help="konuşma hızı çarpanı (1.0 = normal)")
    ap.add_argument("--model-dizini", default=str(Path.home() / ".egitim_video" / "sesler"))
    ap.add_argument("--cozunurluk", type=int, choices=[720, 1080], default=1080)
    ap.add_argument("--sahne", help="sadece bu sahneler, ör. 1-3")
    ap.add_argument("--kamera-yok", action="store_true", help="sahnelerdeki yavaş yakınlaşmayı kapat")
    ap.add_argument("--efekt-yok", action="store_true", help="tık/ding ses efektlerini kapat")
    ap.add_argument("--kelime-senkron-yok", action="store_true",
                    help="öğeleri cümle başında aç (varsayılan: öğenin anahtar kelimesi söylenirken)")
    ap.add_argument("--giris-yok", action="store_true", help="boş tahtada otomatik giriş yazısını kapat")
    ap.add_argument("--temizleme-yok", action="store_true", help="cümle başı/sonu nefes-hışırtı temizliğini kapat")
    ap.add_argument("--eksik", action="store_true", help="--ses-dizini'nde sesi olmayan cümleleri ve seslendirme parametrelerini yaz")
    ap.add_argument("--dizin-olustur", metavar="KLASOR", help="eski ses klasörüne bu senaryoya göre dizin.json yaz (göç)")
    ap.add_argument("--ingilizce-isaretle", action="store_true",
                    help="anlatımdaki İngilizce öbekleri {…} ile işaretleyip senaryoya yaz (wordfreq gerekir); sonra gözden geçir")
    ap.add_argument("--tempo", type=float, default=0.9,
                    help="anlatım hızı çarpanı (perdeyi bozmadan; 0.9 = %%10 daha yavaş). Ses yeniden üretilmez")
    ap.add_argument("--tik", action="store_true", help="madde belirirken hafif 'tık' sesi (varsayılan kapalı; konuşma üstünde sürtme gibi duyulabiliyor)")
    ap.add_argument("--storyboard", metavar="PNG", help="ses/video üretmeden her sahnenin son halini tek görselde göster")
    ap.add_argument("--kontrol", action="store_true", help="sadece senaryo çeşitlilik/uzunluk kontrolü yap")
    ap.add_argument("--muzik", action="store_true", help="hafif fon müziği ekle (varsayılan: yok)")
    ap.add_argument("--muzik-yok", action="store_true", help="(eski seçenek; artık varsayılan)")
    ap.add_argument("--altyazi-yok", action="store_true")
    ap.add_argument("--intro-outro-yok", action="store_true")
    ap.add_argument("--onizleme", nargs="?", const=90.0, type=float, metavar="SN",
                    help="uzun videodan önce onay için ~SN saniyelik (varsayılan 90) temsili önizleme üret")
    ap.add_argument("--onizleme-yaz", metavar="JSON",
                    help="önizleme sahnelerini ayrı senaryo dosyasına yaz (ses üretimi/iş akışı için) ve çık")
    ap.add_argument("--lufs", type=float, default=-14.0, help="hedef ses yüksekliği (YouTube: -14 LUFS)")
    ap.add_argument("--sesli-kitap", action="store_true", help="ayrıca bölümlü .m4a sesli anlatım dosyası üret")
    ap.add_argument("--genel-telaffuz-yok", action="store_true", help="depo kökündeki telaffuz.json'u kullanma")
    args = ap.parse_args()

    H = args.cozunurluk; W = H * 16 // 9
    sen = json.loads(Path(args.senaryo).read_text(encoding="utf-8"))
    tum = sen["sahneler"]; toplam = len(tum)
    ilk = 1
    sahneler = tum
    if args.sahne:
        a, _, b = args.sahne.partition("-"); ilk = int(a)
        sahneler = tum[int(a) - 1:int(b or a)]
    if args.onizleme or args.onizleme_yaz:
        idx = onizleme_sec(sahneler, args.onizleme or 90.0, args.tempo)
        sahneler = [sahneler[i] for i in idx]
        tahmin = sum(sahne_suresi_tahmin(sh, args.tempo) for sh in sahneler)
        log(f"Önizleme: {len(sahneler)} sahne ({', '.join(str(ilk + i) for i in idx)}) · tahmini {tahmin:.0f} sn")
        for i in idx:
            log(f"   {ilk + i:3d}. [{tum[ilk - 1 + i].get('tur', 'maddeler')}] {tum[ilk - 1 + i].get('baslik', '')[:60]}")
        if args.onizleme_yaz:
            yeni = {k: v for k, v in sen.items() if k != "sahneler"}
            yeni["onizleme_kaynak"] = [ilk + i for i in idx]
            yeni["sahneler"] = sahneler
            Path(args.onizleme_yaz).write_text(json.dumps(yeni, ensure_ascii=False, indent=1), encoding="utf-8")
            log(f"Önizleme senaryosu → {args.onizleme_yaz}"); return
        ilk, toplam = 1, len(sahneler)
        if args.cikti == "egitim_videosu.mp4" or not args.cikti.endswith("_onizleme.mp4"):
            args.cikti = str(Path(args.cikti).with_name(Path(args.cikti).stem + "_onizleme.mp4"))
    genel = {}
    gt = Path(__file__).resolve().parent.parent / "telaffuz.json"
    if gt.exists() and not args.genel_telaffuz_yok:
        genel = json.loads(gt.read_text(encoding="utf-8"))
    telaffuz = {**genel.get("telaffuz", {}), **sen.get("telaffuz", {})}
    kok = {**genel.get("telaffuz_kok", {}), **sen.get("telaffuz_kok", {})}
    ust = sen.get("baslik", "")
    # bölümler: sahnedeki "bolum" alanı yeni bölüm başlatır (YouTube bölümleri + tahta alt bilgisi)
    bolum_adi, b_ = [], None
    for sh in sahneler:
        b_ = sh.get("bolum", b_); bolum_adi.append(b_)
    intro = 0 if args.intro_outro_yok else INTRO_SN
    outro = 0 if args.intro_outro_yok else OUTRO_SN

    if args.ingilizce_isaretle:
        n_ = 0
        for sh in tum:
            yeni = " ".join(c if "{" in c else ingilizce_isaretle(c) for c in cumlelere_bol(sh["anlatim"]))
            if yeni != sh["anlatim"]:
                n_ += 1; log(f"  {sh.get('baslik', '')}: {yeni[:110]}")
                sh["anlatim"] = yeni
        Path(args.senaryo).write_text(json.dumps(sen, ensure_ascii=False, indent=1), encoding="utf-8")
        log(f"{n_} sahnede İngilizce öbek işaretlendi → {args.senaryo}. Yanlış işaretleri elle düzelt."); return
    hatalar = senaryo_dogrula(sen)
    if hatalar:
        sys.exit("Senaryo hataları:\n  " + "\n  ".join(hatalar))
    for u in cesitlilik_raporu(sahneler):
        log("  ⚠ " + u)
    if args.kontrol:
        # yerleşim raporu (explainer-video layout_report / TheoremExplainAgent 'element layout')
        S0 = Sahne(1280, 720); tb0 = S0.arka_plan(); sorun = 0
        for si, sh in enumerate(sahneler):
            S0.tahta(tb0, sh, len(sahne_ogeleri(sh)), ilk + si, toplam, ust, True)
            for u in S0.uyari:
                log(f"  ⚠ yerleşim · sahne {ilk + si} «{sh.get('baslik', '')}»: {u}"); sorun += 1
        # kapsam: ekranda yazan her şey anlatımda okunuyor mu?
        for si, sh in enumerate(sahneler):
            for o in okunmayanlar(sh):
                log(f"  ⚠ okunmuyor · sahne {ilk + si} «{sh.get('baslik', '')}»: {o[:70]}"); sorun += 1
        # senkron raporu: gerçek ses varsa onun süreleri, yoksa tahmin (~2.3 kelime/sn)
        depo0 = SesDeposu(args.ses_dizini) if args.ses_dizini else None
        sureler = []
        for si, sh in enumerate(sahneler):
            cs = []
            for ci, c in enumerate(cumlelere_bol(sh.get("anlatim", ""))):
                y_ = depo0.bul(f"{ilk + si:02d}_{ci:02d}",
                               ses_anahtari(seslendirme_metni(c, telaffuz, kok), sh.get("ton"))) if depo0 else None
                if y_:
                    cs.append(len(klip_temizle(oku_24k(y_))[0]) / SR)
                else:
                    cs.append(len(temiz(c).split()) / 2.3 + 0.3)
            sureler.append(cs)
        for u in senkron_raporu(sahneler, ilk, sureler):
            log("  ⚠ senkron · " + u); sorun += 1
        top = sum(map(sum, sureler)) + len(sahneler) * 1.4
        log(f"Kontrol bitti: {sorun} yerleşim/senkron uyarısı · tahmini süre {top / 60:.1f} dk."); return
    if args.storyboard:
        S0 = Sahne(1280, 720); tb0 = S0.arka_plan(); kareler = []
        for si, sh in enumerate(sahneler):
            n_ = len(sahne_ogeleri(sh))
            im0, _ = S0.tahta(tb0, sh, n_, ilk + si, toplam, ust, True)
            d0 = ImageDraw.Draw(im0)
            bilgi = f"{ilk + si}. {sh.get('tur', 'maddeler')} · {len(temiz(sh.get('anlatim', '')).split())} kelime"
            d0.rectangle((0, 0, 520, 40), fill=(20, 20, 26)); d0.text((12, 8), bilgi, font=font(22, True), fill=(255, 255, 255))
            kareler.append(im0.resize((640, 360)))
        sut = 3; sat_ = math.ceil(len(kareler) / sut)
        sb = Image.new("RGB", (640 * sut, 360 * sat_), (30, 30, 30))
        for i, im0 in enumerate(kareler):
            sb.paste(im0, ((i % sut) * 640, (i // sut) * 360))
        sb.save(args.storyboard); log(f"Storyboard: {args.storyboard}"); return

    if args.dizin_olustur:   # eski usul (dizin.json'suz) ses klasörünü bu senaryoya göre etiketle
        d_ = Path(args.dizin_olustur); dz = dizin_oku(d_) or {}; n_ = 0
        for si, sh in enumerate(sahneler):
            for ci, c in enumerate(cumlelere_bol(sh["anlatim"])):
                ad = f"{ilk + si:02d}_{ci:02d}"
                if (d_ / f"{ad}.wav").exists():
                    dz[ad] = {"anahtar": ses_anahtari(seslendirme_metni(c, telaffuz, kok), sh.get("ton")), "metin": c}; n_ += 1
        (d_ / "dizin.json").write_text(json.dumps(dz, ensure_ascii=False, indent=0), encoding="utf-8")
        log(f"dizin.json yazıldı: {n_} cümle → {d_}"); return
    if args.eksik:           # hangi cümlelerin sesi yok? → seslendirme için hazır parametreler
        depo = SesDeposu(args.ses_dizini); eksik = []; sahne_eksik = set()
        for si, sh in enumerate(sahneler):
            for ci, c in enumerate(cumlelere_bol(sh["anlatim"])):
                ad = f"{ilk + si:02d}_{ci:02d}"
                if not depo.bul(ad, ses_anahtari(seslendirme_metni(c, telaffuz, kok), sh.get("ton"))):
                    eksik.append(ad); sahne_eksik.add(ilk + si)
        if not eksik:
            log("Tüm cümlelerin sesi hazır ✔"); return
        ss = sorted(sahne_eksik); gr = []
        for x in ss:
            if gr and x == gr[-1][1] + 1 and x - gr[-1][0] < 3:
                gr[-1][1] = x
            else:
                gr.append([x, x])
        log(f"{len(eksik)} cümlenin sesi yok ({len(ss)} sahne).")
        log("parcalar = " + json.dumps([f"{a}-{b}" for a, b in gr]))
        log("ekstra  += --cumleler " + ",".join(eksik)); return

    tmp = Path(tempfile.mkdtemp(prefix="egitim_video_"))
    log("[1/4] Seslendirme...")
    _motor = []

    def motor_al():          # ses motoru yalnızca gerçekten sentez gerekince yüklenir
        if not _motor:
            _motor.append(PiperSes(args.piper_ses, args.model_dizini, args.hiz) if args.ses == "piper"
                          else EdgeSes(args.edge_ses, args.hiz) if args.ses == "edge"
                          else ChatterboxSes(args.referans, args.model_dizini, args.hiz, args.abarti, args.cfg)
                          if args.ses == "chatterbox" else SessizSes() if args.ses == "sessiz" else EspeakSes())
        return _motor[0]
    if args.sadece_ses:
        hedef = Path(args.sadece_ses); hedef.mkdir(parents=True, exist_ok=True)
        taban = SesDeposu(args.taban_ses, ad_ile=False) if args.taban_ses else None
        dizin = dizin_oku(hedef) or {}
        secili = set(args.cumleler.split(",")) if args.cumleler else None
        den = Denetci() if args.kalite else None
        rapor = []
        _ilk_motor = [True]
        for si, sh in enumerate(sahneler):
            for ci, c in enumerate(cumlelere_bol(sh["anlatim"])):
                ad = f"{ilk + si:02d}_{ci:02d}"
                if secili is not None and ad not in secili:
                    continue
                yol = hedef / f"{ad}.wav"
                anahtar = ses_anahtari(seslendirme_metni(c, telaffuz, kok), sh.get("ton"))
                eski = taban.bul(ad, anahtar) if (taban and secili is None) else None
                if eski:                                   # aynı metin daha önce seslendirilmiş: kopyala
                    if Path(eski).resolve() != yol.resolve():
                        shutil.copy(eski, yol)
                        if Path(eski).with_suffix(".json").exists():
                            shutil.copy(Path(eski).with_suffix(".json"), yol.with_suffix(".json"))
                        tk = Path(eski).parent / "temizlendi.txt"   # zaten temizlenmişse tekrar temizlenmesin
                        if tk.exists() and Path(eski).name in tk.read_text().split():
                            with open(hedef / "temizlendi.txt", "a") as f_:
                                f_.write(yol.name + "\n")
                    dizin[ad] = {"anahtar": anahtar, "metin": c}
                    log(f"   {ad}: önbellekten"); continue
                en_iyi = None
                motor = motor_al()
                if den is not None and _ilk_motor[0]:
                    motor.denetci = den; _ilk_motor[0] = False
                for deneme in range(max(1, args.kalite)):
                    aday = hedef / f"{ad}.aday{deneme}.wav"
                    if hasattr(motor, "ton"):
                        motor.ton(sh.get("ton"))
                    motor.sentezle(seslendirme_metni(c, telaffuz, kok), aday)
                    if not den:
                        en_iyi = (1.0, aday, ""); break
                    p, duyulan = den.puan(aday, temiz(c))
                    aday.with_suffix(".json").write_text(json.dumps(den.kelimeler, ensure_ascii=False))
                    log(f"   {ad} deneme {deneme + 1}: {p:.2f}  «{duyulan[:70]}»")
                    if en_iyi is None or p > en_iyi[0]:
                        en_iyi = (p, aday, duyulan)
                    if p >= args.esik:
                        break
                os.replace(en_iyi[1], yol)
                kz = en_iyi[1].with_suffix(".json")
                if kz.exists():
                    os.replace(kz, yol.with_suffix(".json"))
                for f in list(hedef.glob(f"{ad}.aday*.wav")) + list(hedef.glob(f"{ad}.aday*.json")):
                    f.unlink()
                dizin[ad] = {"anahtar": anahtar, "metin": c}
                rapor.append(f"{ad}\t{en_iyi[0]:.2f}\t{c}\t|\t{en_iyi[2]}")
                log(f"   {yol.name}: {c[:60]}")
        (hedef / "kalite_raporu.txt").write_text("\n".join(rapor), encoding="utf-8")
        (hedef / "dizin.json").write_text(json.dumps(dizin, ensure_ascii=False, indent=0), encoding="utf-8")
        log("TAMAM ✔ sesler: " + str(hedef))
        return

    parcalar = [np.zeros(int(intro * SR), np.float32)]
    t = intro; zc = []; kelime_z = {}
    depo = SesDeposu(args.ses_dizini) if args.ses_dizini else None
    for si, sh in enumerate(sahneler):
        bas = t; cz = []
        for ci, c in enumerate(cumlelere_bol(sh["anlatim"])):
            if sh.get("tur") == "soru" and ci == sh["soru"].get("cevap_cumle", -1):
                bek = float(sh["soru"].get("bekle", 4))
                sh["_bekle"] = (t, t + bek)
                parcalar.append(np.zeros(int(bek * SR), np.float32)); t += bek
                sh["_acilis"] = t
            if args.ses_dizini:
                yol = depo.bul(f"{ilk + si:02d}_{ci:02d}", ses_anahtari(seslendirme_metni(c, telaffuz, kok), sh.get("ton")))
                if not yol:
                    sys.exit(f"HATA: {ilk + si:02d}_{ci:02d} cümlesinin sesi yok ya da metni değişmiş: «{c[:60]}»\n"
                             f"  Eksikleri görmek için: --eksik --ses-dizini {args.ses_dizini}")
            else:
                yol = tmp / f"s{si}_{ci}.wav"
                motor_al().sentezle(seslendirme_metni(c, telaffuz, kok), yol)
            x = oku_24k(yol)
            if abs(args.tempo - 1.0) > 0.005:          # yavaşlat (perde aynı kalır)
                x = tempo_uygula(x, args.tempo)
            nz = np.nonzero(np.abs(x) > 0.01)[0]       # baş/son sessizliği kırp
            ofs = max(0, nz[0] - 600) / SR if len(nz) else 0.0
            if len(nz):
                x = x[max(0, nz[0] - 600): nz[-1] + 1200].copy()
            if not args.temizleme_yok:                   # nefes / hışırtı kuyrukları
                x, ofs2 = klip_temizle(x); ofs += ofs2
            kj = Path(yol).with_suffix(".json")
            kelime_z[(si, ci)] = ([dict(w, s=w["s"] - ofs) for w in json.loads(kj.read_text())]
                                  if kj.exists() else None)
            x = yumusat(x)
            cz.append((t, t + len(x) / SR, temiz(c)))
            dur_ = duraklama(c)
            parcalar += [x, np.zeros(int(dur_ * SR), np.float32)]
            t += len(x) / SR + dur_
        parcalar.append(np.zeros(int(SAHNE_ARASI * SR), np.float32)); t += SAHNE_ARASI
        zc.append((bas, t, cz))
        log(f"   sahne {ilk + si}/{toplam}: {len(cz)} cümle, {t - bas:.1f} sn")
    parcalar.append(np.zeros(int(outro * SR), np.float32)); t += outro
    ses = np.concatenate(parcalar)
    ses = ses / (np.max(np.abs(ses)) + 1e-9) * 0.9
    sure = len(ses) / SR

    # öğe zamanları: "goster" ile belirtilen cümlede, yoksa cümlelere orantılı
    madde_t = []
    for si, sh in enumerate(sahneler):
        cz = zc[si][2]; nc = max(1, len(cz)); ts = []
        mm = sahne_ogeleri(sh)
        oto = None if sh.get("goster") else oto_goster(sh, [c_[2] for c_ in cz])
        for j in range(len(mm)):
            capa = None
            if oto is not None and j < len(oto):
                ci = min(len(cz) - 1, oto[j]); capa = None if args.kelime_senkron_yok else oge_metni(sh, j)
            elif sh.get("goster") and j < len(sh["goster"]):
                gj = sh["goster"][j]
                if isinstance(gj, str) and ":" in gj:      # "3:kelime" → 3. cümlede o kelimede
                    a_, _, capa = gj.partition(":"); ci = min(len(cz) - 1, int(a_))
                elif isinstance(gj, float):                  # 2.5 → 2. cümlenin ortası
                    ci = min(len(cz) - 1, int(gj))
                    ts.append(cz[ci][0] + (cz[ci][1] - cz[ci][0]) * (gj - int(gj)) if cz else zc[si][0]); continue
                else:
                    ci = min(len(cz) - 1, int(gj)); capa = None if args.kelime_senkron_yok else oge_metni(sh, j)
            else:
                ci = min(len(cz) - 1, int(math.floor(j * nc / max(1, len(mm)))))
            if not cz:
                ts.append(zc[si][0]); continue
            a_, b_, metin_ = cz[ci]
            zaman_ = a_
            if capa and sh.get("tur") != "soru":
                r_ = capa_orani(metin_, capa, kelime_z.get((si, ci)))
                if r_ and r_[0] == "sn":
                    zaman_ = a_ + max(0.0, r_[1] - 0.12)
                elif r_ and r_[1] > 0.15:
                    zaman_ = a_ + (b_ - a_) * r_[1] - 0.15
            ts.append(min(b_, zaman_))
        for j in range(1, len(ts)):                         # sıra bozulmasın; öğeler arası en az 1,2 sn
            ts[j] = max(ts[j], ts[j - 1] + MIN_OGE_ARALIK)
        madde_t.append(ts)

    log("[2/4] Ses işleme, efektler" + (" ve fon müziği..." if args.muzik else "..."))
    karisim = ses.copy()
    if not args.efekt_yok:  # ölçülü ses efektleri: öğe belirirken "tık", doğru cevapta "ding"
        tik, ding = efekt_tik(), efekt_ding()
        for si, sh in enumerate(sahneler):
            for x_ in (madde_t[si] if args.tik else []):
                i0 = int(x_ * SR); karisim[i0:i0 + len(tik)] += tik[:max(0, len(karisim) - i0)]
            if "_acilis" in sh:
                i0 = int(sh["_acilis"] * SR) - int(0.15 * SR); karisim[i0:i0 + len(ding)] += ding[:max(0, len(karisim) - i0)]
    if args.muzik and not args.muzik_yok:
        m = muzik_uret(sure + 0.1)[:len(ses)]
        if len(m) < len(ses):
            m = np.pad(m, (0, len(ses) - len(m)))
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
    # agate: kelime aralarında kalan kısık hışırtıyı 24 dB'e kadar bastırır (konuşma eşiğin çok üstünde)
    zincir = "highpass=f=80,afftdn=nf=-45:nr=8,agate=threshold=0.008:ratio=3:range=0.06:attack=3:release=120,deesser=i=0.3,equalizer=f=3000:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=3:attack=10:release=200"
    olc = subprocess.run([ffmpeg_bin(), "-hide_banner", "-i", str(ham), "-af",
                          zincir + f",loudnorm=I={args.lufs}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    try:
        m = json.loads(olc[olc.rindex("{"):olc.rindex("}") + 1])
        if not all(math.isfinite(float(m[x])) for x in ("input_i", "input_tp", "target_offset")):
            raise ValueError("sessiz ses")             # tamamen sessiz taslak: ölçüm yapılamaz
        ln = (f"loudnorm=I={args.lufs}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
              f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    except Exception:
        ln = f"loudnorm=I={args.lufs}:TP=-1.5:LRA=11" if "input_i" in olc and "-inf" not in olc else "anull"
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
        foto = FotoKarakter(kj.with_suffix(".png"), kj, int(H * 0.34))
        kursu = S.kursu()
        log(f"  Karakter: {kj.stem}")
    else:
        kursu = S.kursu()
        kar = {(a, g, kk, i, b): karakter_ciz(a, g, kk, i, S.S * KAR_OLCEK, b)
               for a in range(5) for g in (False, True) for kk in (0.0, 1.0) for i in (False, True)
               for b in ("a", "o", "i")}
        bicimler = agiz_bicimleri(ses, n_kare, spf)
    golge = Image.new("RGBA", k(520, 50), (0, 0, 0, 0))
    ImageDraw.Draw(golge).ellipse(k(60, 8, 360, 40), fill=(0, 0, 0, 70))
    golge = golge.filter(ImageFilter.GaussianBlur(k(6)))
    taban = S.arka_plan()

    rnd = random.Random(1); kirp = set(); f = int(FPS * 1.5)
    while f < n_kare:
        kirp.update({f, f + 1, f + 2}); f += rnd.randint(int(FPS * 2.5), int(FPS * 5))


    tahta_c, alt_c, madde_c, noktalar, giris_c = {}, {}, {}, {}, {}
    def tahta(si, g, acik=False):
        if (si, g, acik) not in tahta_c:
            if len(tahta_c) > 30:
                tahta_c.clear()
            tahta_c[(si, g, acik)] = S.tahta(taban, sahneler[si], g, ilk + si, toplam,
                                             bolum_adi[si] if bolum_adi[si] else ust, acik)
            noktalar[si] = S._nokta
        return tahta_c[(si, g, acik)]

    def altyazi(si, ci):
        if (si, ci) not in alt_c:
            alt_c[(si, ci)] = S.altyazi(zc[si][2][ci][2])
        return alt_c[(si, ci)]

    def sahne_karesi(si, tt, fi, karakter=True):
        bas, bit, cz = zc[si]
        ts = madde_t[si]
        g = sum(1 for x in ts if tt >= x)
        sh_ = sahneler[si]; tur = sh_.get("tur", "maddeler")
        if tur != "maddeler":
            acik = tur == "soru" and tt >= sh_.get("_acilis", 1e9)
            im = tahta(si, g, acik)[0]
            if g and tt - ts[g - 1] < MADDE_ANIM:          # yeni tablo satırı yumuşakça belirir
                im = Image.blend(tahta(si, g - 1, acik)[0], im, (tt - ts[g - 1]) / MADDE_ANIM)
            elif acik and tt - sh_["_acilis"] < MADDE_ANIM:  # doğru cevap açılışı
                im = Image.blend(tahta(si, g, False)[0], im, (tt - sh_["_acilis"]) / MADDE_ANIM)
            else:
                im = im.copy()
            if tur == "soru" and "_bekle" in sh_ and sh_["_bekle"][0] <= tt < sh_["_bekle"][1]:
                b0, b1 = sh_["_bekle"]
                S.geri_sayim(im, b1 - tt, (tt - b0) / (b1 - b0))
        else:
          im, konum = tahta(si, max(0, g - 1) if (g and tt - ts[g - 1] < MADDE_ANIM) else g)
          im = im.copy()
        if tur == "maddeler" and g and tt - ts[g - 1] < MADDE_ANIM:  # yeni madde kayarak belirir
            p = (tt - ts[g - 1]) / MADDE_ANIM; e = 1 - (1 - p) ** 3
            key = (si, g - 1)
            if key not in madde_c:
                madde_c[key] = S.madde_katmani(sahneler[si]["maddeler"][g - 1], konum[g - 1])
            lay, bb = madde_c[key]
            lay2 = lay.copy(); lay2.putalpha(lay.getchannel("A").point(lambda v: int(v * e)))
            im.paste(lay2, (bb[0] - int(k(30) * (1 - e)), bb[1]), lay2)
        # giriş yazısı: tahta boşken konuşma başladıysa (ölü hava önleme)
        if ts and tur not in ("soru", "ipucu", "metin") and not sh_.get("kanca") and ts[0] - bas > 2.5 and not args.giris_yok:
            gorunurluk = 1.0 if g == 0 else max(0.0, 1 - (tt - ts[0]) / MADDE_ANIM) if g == 1 else 0.0
            gorunurluk *= min(1.0, (tt - bas) / 0.4)
            if gorunurluk > 0:
                if si not in giris_c:
                    giris_c[si] = S.giris_katmani(giris_metni(sh_))
                lay = giris_c[si]
                if gorunurluk < 1:
                    lay = lay.copy(); lay.putalpha(lay.getchannel("A").point(lambda v: int(v * gorunurluk)))
                im.paste(lay, (0, 0), lay)
        ci = None
        for j, (a, b, _) in enumerate(cz):
            if a - 0.05 <= tt < b + CUMLE_ARASI:
                ci = j; break
        if ci is not None and not args.altyazi_yok:
            r = altyazi(si, ci)
            if r:
                im.paste(r[0], r[1][:2], r[0])
        # işaretçi: anlatılan öğeye kayar (Paper2Video'nun imleç fikri)
        nk = noktalar.get(si) or []
        if g and tur not in ("soru", "ipucu", "metin") and nk and g - 1 < len(nk):
            hedef = nk[g - 1]
            onceki = nk[g - 2] if g >= 2 and g - 2 < len(nk) else (hedef[0], hedef[1] - 40)
            p_ = min(1.0, (tt - ts[g - 1]) / ISARETCI_SURE)
            e_ = 4 * p_ ** 3 if p_ < 0.5 else 1 - (-2 * p_ + 2) ** 3 / 2      # yumuşak başla, yumuşak dur
            S.isaretci(im, onceki[0] + (hedef[0] - onceki[0]) * e_, onceki[1] + (hedef[1] - onceki[1]) * e_, tt)
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
            kx0, kx1, kust, _ = S.KURSU
            x = k((kx0 + kx1) / 2) - kr.width // 2 + int(dx); y = k(kust + 20) - kr.height + int(dy)
            im.paste(kr, (x, y), kr)
            im.paste(kursu, (0, 0), kursu)
            return
        a = int(agiz[fi]) if fi < len(agiz) else 0
        kas = 1.0 if (a >= 3 and (fi // 10) % 6 == 0) else 0.0
        kr = kar[(a, fi in kirp, kas, isaret, bicimler[fi] if fi < len(bicimler) else "a")]
        sal = int(k(2) * math.sin(tt * 2.0)) + (k(1) if a >= 3 else 0)
        kx0, kx1, kust, _ = S.KURSU
        im.paste(kr, (k((kx0 + kx1) / 2 - 210 * KAR_OLCEK), k(kust + 28) - kr.height + sal), kr)
        im.paste(kursu, (0, 0), kursu)

    bolum_x = [int(W * (zc[i][0] - intro) / max(1, sure - intro - outro))
               for i in range(1, len(sahneler)) if sahneler[i].get("bolum")]
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
            if not args.kamera_yok:  # yavaş kamera: sahne ortasında %3 yakınlaş, sonda geri dön
                bas_, bit_ = zc[si][0], zc[si][1]
                pr = min(1.0, max(0.0, (tt - bas_) / max(0.1, bit_ - bas_)))
                z = 1 + 0.03 * math.sin(math.pi * pr)
                cx_, cy_ = W * 0.66, H * 0.44
                bw, bh = W / z, H / z
                kare = kare.resize((W, H), Image.BILINEAR, box=(cx_ - bw * 0.66, cy_ - bh * 0.44, cx_ + bw * 0.34, cy_ + bh * 0.56))
            # ilerleme çubuğu
            d = ImageDraw.Draw(kare)
            d.rectangle((0, H - k(5), int(W * (tt - intro) / max(1, sure - intro - outro)), H), fill=(255, 196, 80))
            for x_ in bolum_x:   # bölüm sınırları
                d.rectangle((x_ - 1, H - k(5), x_ + 1, H), fill=(30, 30, 30))
        ff.stdin.write(kare.tobytes())
        if fi % (FPS * 60) == 0:
            log(f"   {tt:5.0f} / {sure:.0f} sn")
    ff.stdin.close(); ff.wait()
    shutil.rmtree(tmp, ignore_errors=True)
    if ff.returncode:
        sys.exit("ffmpeg hata verdi.")
    bolumler = yayin_paketi(cikti, sen, sahneler, zc, bolum_adi)
    bolumleri_gom(cikti, bolumler, sure)
    beklenen = [(0, intro + 0.6), (sure - outro - 1.5, sure + 1)] + [
        sh_["_bekle"] for sh_ in sahneler if "_bekle" in sh_]
    yayin_denetimi(cikti, args.lufs, beklenen)
    if args.sesli_kitap:     # abogen/Pandrator: dinlemek için bölümlü sesli anlatım
        m4a = cikti.with_suffix(".m4a")
        subprocess.run([ffmpeg_bin(), "-v", "error", "-y", "-i", str(cikti), "-vn", "-map_chapters", "0",
                        "-c:a", "copy", str(m4a)], check=False)
        if m4a.exists():
            log(f"  Sesli anlatım: {m4a.name}")
    if args.onizleme:
        log("\nÖNİZLEME hazır. Kullanıcı onaylamadan uzun videoya geçme (SKILL.md kural 0).")
    kapak = cikti.with_name(cikti.stem + "_kapak.jpg")
    kapak_gorseli(sen, None if args.karakter == "cizim" else Path(args.karakter).with_suffix(".png"), kapak)
    log(f"\nTAMAM ✔  {cikti}  ({sure / 60:.1f} dk)  + kapak: {kapak.name}")


if __name__ == "__main__":
    main()
