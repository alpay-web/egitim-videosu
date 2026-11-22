#!/usr/bin/env python3
"""Görsellerdeki belirli kelimeleri (kurum/ürün adı) OCR ile bulup genel adlarla değiştirir.

Tesseract (Apache-2.0) kelime kutularını verir; kutu arka plan rengiyle boyanır ve yerine yeni metin, kutuya
sığacak boyutta yazılır. Kelimeye yapışık Türkçe ek korunur (Zebra'ya → Bayi portalı'ya).
Kullanım:
  python gorsel_maskele.py girdi_klasoru cikti_klasoru --degistir '{"vdf":"Şirket","Zebra":"Bayi portalı"}'
Çıktı klasörüne her görselin maskeli kopyası ve maskele_rapor.json yazılır. Sonucu MUTLAKA gözle kontrol et:
OCR küçük/eğik yazıyı kaçırabilir; raporda 'kalan' alanı ikinci OCR turunda hâlâ görülen eşleşmeleri listeler.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def ocr_kutular(img, olcek=2, aci=0):
    """(metin, x0, y0, x1, y1, aci) listesi; küçük yazı için büyütülür, dikey şerit adları için döndürülür.
    aci=90: görsel saat yönünün tersine çevrilmiş okunur, kutular özgün koordinata geri çevrilir."""
    b = img.convert("RGB")
    if aci:
        b = b.rotate(-aci, expand=True)          # dikey (aşağıdan yukarı) yazı yatay olur
    W, H = b.size
    b = b.resize((W * olcek, H * olcek), Image.LANCZOS)
    tmp = Path("/tmp/_maske_ocr.png"); b.save(tmp)
    tsv = subprocess.run(["tesseract", str(tmp), "-", "-l", "tur+eng", "--psm", "11", "tsv"],
                         capture_output=True, text=True).stdout
    out = []
    for ln in tsv.splitlines()[1:]:
        p = ln.split("\t")
        if len(p) < 12 or not p[11].strip():
            continue
        x, y, w, h = (int(p[i]) // olcek for i in (6, 7, 8, 9))
        if aci:      # saat yönünde 90° döndürülmüş görselde (u,v) → özgün (x=v, y=H-u)
            x0, x1 = y, y + h
            y0, y1 = img.height - (x + w), img.height - x
            out.append((p[11].strip(), x0, y0, x1, y1, aci))
        else:
            out.append((p[11].strip(), x, y, x + w, y + h, 0))
    return out


def tum_kutular(img):
    """Birden çok ölçek ve yön; aynı yerdeki tekrarlar birleştirilir."""
    sonuc = []
    for olcek, aci in ((2, 0), (3, 0), (2, 90)):
        for k in ocr_kutular(img, olcek, aci):
            if not any(k[0] == s[0] and abs(k[1] - s[1]) < 6 and abs(k[2] - s[2]) < 6 for s in sonuc):
                sonuc.append(k)
    return sonuc


def arka_plan(img, x0, y0, x1, y1):
    """Kutunun kenar piksellerinin en sık rengi (düz zemin varsayımı)."""
    px = img.convert("RGB").load()
    renk = {}
    for x in range(max(0, x0 - 2), min(img.width, x1 + 3)):
        for y in (max(0, y0 - 3), min(img.height - 1, y1 + 3)):
            renk[px[x, y]] = renk.get(px[x, y], 0) + 1
    return max(renk, key=renk.get) if renk else (255, 255, 255)


def yazi_rengi(img, x0, y0, x1, y1, zemin):
    px = img.convert("RGB").load()
    en, uz = zemin, -1
    for x in range(x0, x1):
        for y in range(y0, y1):
            c = px[x, y]; d = sum(abs(a - b) for a, b in zip(c, zemin))
            if d > uz:
                en, uz = c, d
    return en


def maskele(yol, cikti, degistir, elle=()):
    img = Image.open(yol).convert("RGB")
    desen = re.compile(r"^(" + "|".join(re.escape(k) for k in sorted(degistir, key=len, reverse=True)) +
                       r")((?:['’][\wçğıöşüÇĞİÖŞÜ]+)?)([.,:;)]*)$", re.I)
    d = ImageDraw.Draw(img); bulunan = []
    alt = re.compile(r"(?<![a-zA-ZçğıöşüÇĞİÖŞÜ])(" + "|".join(re.escape(k) for k in sorted(degistir, key=len, reverse=True))
                     + r")(?![a-zA-ZçğıöşüÇĞİÖŞÜ])", re.I)
    kutular = [k + (False,) for k in tum_kutular(img)] + [tuple(e[:6]) + (True,) for e in elle]
    for metin, x0, y0, x1, y1, aci, elle_mi in kutular:
        if elle_mi:                                          # elle kutu: "=yeni metin" doğrudan yazılır
            yeni = metin.lstrip("=")
        else:
            m = desen.match(metin)
            if m:
                anahtar = next(k for k in degistir if k.lower() == m.group(1).lower())
                yeni = degistir[anahtar] + m.group(2) + m.group(3)
            elif alt.search(metin):                          # kelimenin içinde: zebra.vdf.com.tr → portal.firma.com.tr
                yeni = alt.sub(lambda mm: next(v for k, v in degistir.items() if k.lower() == mm.group(1).lower())
                               .lower() if mm.group(1).islower() else
                               next(v for k, v in degistir.items() if k.lower() == mm.group(1).lower()), metin)
            else:
                continue
        zemin = arka_plan(img, x0, y0, x1, y1); renk = yazi_rengi(img, x0, y0, x1, y1, zemin)
        kw, kh = (x1 - x0, y1 - y0) if not aci else (y1 - y0, x1 - x0)   # yazı yönünde genişlik/yükseklik
        boy = int(max(8, kh) * 1.15)
        f = ImageFont.truetype(FONT, boy)
        while boy > 6 and d.textlength(yeni, font=f) > kw * 1.1 + 4:
            boy -= 1; f = ImageFont.truetype(FONT, boy)
        gen = int(d.textlength(yeni, font=f)) + 4
        d.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], fill=zemin)
        parca = Image.new("RGB", (gen, int(boy * 1.4)), zemin)
        ImageDraw.Draw(parca).text((2, parca.height / 2), yeni, font=f, fill=renk, anchor="lm")
        if aci:
            parca = parca.rotate(aci, expand=True)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        img.paste(parca, (int(cx - parca.width / 2), int(cy - parca.height / 2)))
        bulunan.append({"eski": metin, "yeni": yeni, "kutu": [x0, y0, x1, y1]})
    img.save(cikti, quality=92)
    kalan = [m[0] for m in tum_kutular(Image.open(cikti)) if alt.search(m[0])]
    return {"dosya": Path(yol).name, "degisen": bulunan, "kalan": kalan}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("girdi"); ap.add_argument("cikti")
    ap.add_argument("--degistir", required=True, help="JSON sözlük: eski → yeni")
    ap.add_argument("--elle", help='OCR\'ın kaçırdığı yerler: {"dosya.png": [["=yeni", x0, y0, x1, y1, 0|90]]}')
    a = ap.parse_args()
    deg = json.loads(a.degistir)
    elle = json.loads(a.elle) if a.elle else {}
    o = Path(a.cikti); o.mkdir(parents=True, exist_ok=True)
    rapor = []
    for f in sorted(Path(a.girdi).iterdir()):
        if f.suffix.lower() in (".png", ".jpg", ".jpeg"):
            r = maskele(f, o / f.name, deg, elle.get(f.name, [])); rapor.append(r)
            if r["degisen"] or r["kalan"]:
                print(f"{f.name}: {len(r['degisen'])} değişti" + (f" · KALAN: {r['kalan']}" if r["kalan"] else ""))
    (o / "maskele_rapor.json").write_text(json.dumps(rapor, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
