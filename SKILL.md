---
name: egitim-videosu
description: Bir eğitim dokümanından (docx, pdf, md, txt ya da yapıştırılmış metin) konuşan animasyonlu profesör karakterli, Türkçe nöral seslendirmeli, fon müzikli ve altyazılı 1080p MP4 eğitim videosu üretir. Tamamen ücretsiz ve açık kaynak (Piper TTS + Pillow + ffmpeg). "bu dokümanı anlatan video yap", "eğitim videosu", "animasyonlu anlatım videosu", "ders videosu" isteklerinde kullan.
---

# Eğitim Videosu Üretici

Doküman → sahne senaryosu (JSON) → Türkçe nöral ses (Piper, CC0) → animasyonlu 1080p video.
Ücretli API, API anahtarı ya da GPU gerekmez. Claude'un kendi çalışma ortamında (claude.ai, Claude Code) çalışır;
ihtiyaç duyulan her şey pip ve GitHub'dan iner.

## 0. Kodu hazırla
Bu SKILL.md'nin yanında `scripts/video_uret.py` varsa onu kullan. Yoksa repoyu klonla:
```bash
[ -d /tmp/egitim-videosu ] || git clone --depth 1 https://github.com/alpay-web/egitim-videosu /tmp/egitim-videosu
SKILL_DIR=/tmp/egitim-videosu
pip install -q -r $SKILL_DIR/requirements.txt 2>/dev/null || pip install -q --break-system-packages -r $SKILL_DIR/requirements.txt
```
ffmpeg yoksa `imageio-ffmpeg` paketi otomatik kullanılır. Türkçe ses modeli (~65 MB) ilk çalıştırmada
GitHub'dan (k2-fsa/sherpa-onnx sürümleri) `~/.egitim_video/sesler` içine iner.

## 1. Dokümanı oku
docx: `pandoc dosya.docx -t plain` (ya da python-docx), pdf: `pdftotext -layout`. Ana başlıkları ve en önemli fikirleri çıkar.

## 2. Senaryoyu yaz → `senaryo.json`
Örnek: `$SKILL_DIR/ornek/senaryo_wse_b1.json`. Şema:
```json
{
  "baslik": "Videonun adı (intro kartı ve tahta altı)",
  "alt_baslik": "Profesör Bilgin anlatıyor",
  "kapanis": "Başarılar!",
  "telaffuz": {"Wall Street English": "Vol Strit İngliş", "yesterday": "yesterdey"},
  "sahneler": [
    {"baslik": "Sahne başlığı",
     "maddeler": ["tahtaya yazılacak kısa madde", "..."],
     "anlatim": "Profesörün söyleyeceği metin. Cümleler nokta ile biter."}
  ]
}
```
Senaryo kuralları (profesyonel sonuç için önemli):
- 8–14 sahne, her biri 60–110 kelime anlatım (≈ 25–45 sn). Toplam 5–8 dk.
- İlk sahne: karşılama + içerikte ne var. Son sahne: özet + motivasyon.
- `maddeler`: sahne başına 3–6, her biri ≤ 40 karakter, anlatımdaki sırayla (cümleler ilerledikçe sırayla belirir).
- `anlatim`: konuşma dili, "sen" hitabı, kısa cümleler. Sayılar otomatik okunur ama "1." gibi sıra sayılarını yazıyla yaz.
  Sembol kullanma. Uzun İngilizce cümleleri tahtaya koy, anlatımda Türkçe açıkla.
- `telaffuz`: anlatımda geçen her İngilizce kelime/kalıp/kısaltma için Türkçe okunuşu ekle
  (ör. "actually": "ekçuali", "WSE": "dabılyu es i", "B1": "bi bir"). Altyazıda orijinali görünür, ses okunuşu kullanır.
- Dokümanı kelimesi kelimesine okuma; özetle, tablolardan en kritik 4–6 öğeyi seç.

## 3. Üret
```bash
python $SKILL_DIR/scripts/video_uret.py senaryo.json -o deneme.mp4 --sahne 1-2 --cozunurluk 720   # hızlı deneme
python $SKILL_DIR/scripts/video_uret.py senaryo.json -o egitim_videosu.mp4                       # 1080p tam video
```
Uzun videolarda komutu arka planda çalıştırıp log'u izle (≈ 1 dk video için 40–60 sn CPU).
Deneme videosundan 2–3 kare çıkarıp (`ffmpeg -ss 10 -i deneme.mp4 -frames:v 1 kare.png`) taşma/okunurluk kontrol et.

Seçenekler:
- `--piper-ses fahrettin` (varsayılan, erkek, CC0) | `fettah` (CC0) | `dfki` (ticari kullanım yok)
- `--hiz 0.95` konuşma hızı (1.0 normal) · `--ses edge` (internet varsa Microsoft'un ücretsiz nöral sesi)
- `--muzik-yok`, `--altyazi-yok`, `--intro-outro-yok`, `--cozunurluk 720`

## 4. Teslim
MP4'ü kullanıcıya gönder; süreyi, kullanılan sesi ve sahne sayısını tek cümleyle söyle.
