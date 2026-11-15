#!/usr/bin/env python3
"""Belgeyi (PDF, Word, PowerPoint, Excel, HTML, EPUB, Markdown, TXT) Markdown'a çevirir ve
senaryo yazımı için bir KAPSAM HARİTASI çıkarır (başlıklar + kelime sayıları + tahmini video süresi).

Kullanım:
    python belge_oku.py belge.pdf -o belge.md        # belge.md + belge_harita.md

Okuyucu sırası: markitdown (Microsoft, MIT) → pandoc → pdftotext. Taranmış (resim) PDF'te metin
çok azsa uyarır: OCR gerekir (ör. `ocrmypdf`), metni uydurma.
"""
import argparse, re, shutil, subprocess, sys
from pathlib import Path

DAKIKA_BASI_KELIME = 130   # anlatım hızı; video_uret ile aynı varsayım


def markitdown_oku(yol):
    from markitdown import MarkItDown
    return MarkItDown().convert(str(yol)).text_content


def pandoc_oku(yol):
    if not shutil.which("pandoc"):
        raise RuntimeError("pandoc yok")
    return subprocess.run(["pandoc", str(yol), "-t", "gfm", "--wrap=none"], capture_output=True,
                          text=True, check=True).stdout


def pdftotext_oku(yol):
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext yok")
    return subprocess.run(["pdftotext", "-layout", str(yol), "-"], capture_output=True, text=True, check=True).stdout


def oku(yol):
    yol = Path(yol); uz = yol.suffix.lower()
    if uz in (".md", ".txt"):
        return yol.read_text(encoding="utf-8", errors="replace"), "düz metin"
    sira = [("markitdown", markitdown_oku)]
    if uz in (".docx", ".odt", ".epub", ".html", ".htm", ".rtf"):
        sira.append(("pandoc", pandoc_oku))
    if uz == ".pdf":
        sira.append(("pdftotext", pdftotext_oku))
    hatalar = []
    for ad, f in sira:
        try:
            metin = f(yol)
            if metin and len(metin.split()) > 20:
                return metin, ad
            hatalar.append(f"{ad}: boş çıktı")
        except Exception as e:  # bir sonraki okuyucuyu dene
            hatalar.append(f"{ad}: {e}")
    raise SystemExit("Belge okunamadı:\n  " + "\n  ".join(hatalar) +
                     "\n(markitdown kurulu değilse: pip install 'markitdown[pdf,docx,pptx,xlsx]')")


def pdf_sayfa_sayisi(yol):
    try:
        cik = subprocess.run(["pdfinfo", str(yol)], capture_output=True, text=True).stdout
        return int(re.search(r"Pages:\s+(\d+)", cik).group(1))
    except Exception:
        return None


def harita(metin):
    """Başlık ağacı + her bölümün kelime sayısı."""
    bolumler, ad, sev, kel = [], "(başlıksız giriş)", 0, 0
    for satir in metin.splitlines():
        m = re.match(r"^(#{1,4})\s+(.*)", satir)
        if m:
            if kel or bolumler:
                bolumler.append((sev, ad, kel))
            sev, ad, kel = len(m.group(1)), m.group(2).strip(), 0
        else:
            kel += len(satir.split())
    bolumler.append((sev, ad, kel))
    return [b for b in bolumler if b[2] or b[0]]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("belge")
    ap.add_argument("-o", "--cikti", help="Markdown çıktısı (varsayılan: belge adı .md)")
    a = ap.parse_args()
    yol = Path(a.belge)
    metin, okuyucu = oku(yol)
    metin = re.sub(r"\n{3,}", "\n\n", metin).strip() + "\n"
    cikti = Path(a.cikti) if a.cikti else yol.with_suffix(".md")
    if cikti.resolve() == yol.resolve():
        cikti = yol.with_name(yol.stem + "_okunan.md")
    cikti.write_text(metin, encoding="utf-8")

    toplam = len(metin.split())
    sat = [f"# Kapsam haritası: {yol.name}", "",
           f"- Okuyucu: {okuyucu} · {toplam} kelime · anlatılırsa ≈ {toplam / DAKIKA_BASI_KELIME:.0f} dk "
           f"(özetlenmiş anlatım genelde bunun %35–60'ı)"]
    if yol.suffix.lower() == ".pdf":
        s = pdf_sayfa_sayisi(yol)
        if s:
            sat.append(f"- {s} sayfa · sayfa başına {toplam / s:.0f} kelime")
            if toplam / s < 40:
                sat.append("- ⚠ Çok az metin: taranmış (resim) PDF olabilir. OCR gerekir (ör. `ocrmypdf girdi.pdf cikti.pdf`).")
    tablo_say = len(re.findall(r"^\|.*\|\s*$\n^\|[\s:|-]+\|\s*$", metin, flags=re.M))
    sat += [f"- Tablo: {tablo_say} · madde satırı: {len(re.findall(r'^\s*[-*•] ', metin, flags=re.M))}", "",
            "| Bölüm | Kelime | Sahne önerisi |", "|---|---|---|"]
    for sev, ad, kel in harita(metin):
        oneri = "—" if kel < 25 else "1 sahne" if kel < 150 else f"{min(6, round(kel / 120))} sahne"
        sat.append(f"| {'  ' * max(0, sev - 1)}{ad[:70]} | {kel} | {oneri} |")
    sat += ["", "Her satır videoda ya bir sahneye eşlenmeli ya da 'dışarıda bırakıldı: neden' diye not edilmeli."]
    hp = cikti.with_name(cikti.stem + "_harita.md")
    hp.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"✔ {cikti}  ({toplam} kelime, {okuyucu})\n✔ {hp}")


if __name__ == "__main__":
    main()
