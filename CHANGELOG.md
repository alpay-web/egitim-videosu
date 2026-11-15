# Değişiklik günlüğü

Sürümleme: `ANA.ARA.YAMA` — ANA: senaryo biçimi geriye uyumsuz değişirse; ARA: yeni özellik; YAMA: düzeltme.

## 1.0.0 — 2026-11-15
İlk kararlı paket.

**Üretim hattı:** belge → kapsam haritası → senaryo → doğrulama/storyboard → seslendirme (Chatterbox, Whisper kalite
kapısı, GitHub Actions'ta paralel) → render (Pillow + ffmpeg, 1080p) → denetim raporu → YouTube paketi.

**Eklenenler**
- `belge_oku.py`: PDF/Word/PowerPoint/Excel/HTML/EPUB okuma (markitdown → pandoc → pdftotext) + kapsam haritası.
- İçerik adresli ses önbelleği (`dizin.json`), `--eksik`, `--dizin-olustur`, workflow `taban` girdisi.
- Senaryo doğrulama (render'dan önce), `--ses sessiz` taslak modu.
- Kelime senkronu (Whisper kelime zamanları), otomatik giriş yazısı, yerleşim + senkron raporları.
- Bölümler (`bolum`), `.srt` altyazı ve `_youtube.txt` (başlık, bölümlü açıklama, etiketler).
- Nefes/hışırtı temizliği (`klip_temizle`), formant tabanlı ağız biçimleri (a/o/i).
- Sahne türleri: maddeler, tablo, soru, rakam, karşılaştırma, ipucu, zaman; işaretçi, kamera, kanca, ton.
- Testler (`tests/`), `Test` CI işi (her push + ayda bir), sabitlenmiş bağımlılıklar.
- Hazır ses önbelleği: `ses-b1-tam-kurs` release'i (385 cümle).

**Bilinen sınırlar**
- Ses modelleri Hugging Face'ten indirilemeyen ortamlarda GitHub release aynasından gelir (`modeller.yml`).
- Gerçekçi konuşan yüz (SadTalker/Wav2Lip) bilinçli olarak yok: GPU ister, üretimi yavaşlatır.
