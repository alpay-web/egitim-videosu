---
name: egitim-videosu
description: Bir eğitim dokümanından (docx, pdf, md, txt) konuşan animasyonlu karakterli (varsayılan: beyaz saçlı profesör), doğal Türkçe sesli, fon müzikli, altyazılı 1080p YouTube videosu ve kapak görseli üretir. Tamamen ücretsiz ve açık kaynak (Chatterbox TTS, MIT). "bu dokümanı anlatan video yap", "eğitim videosu", "ders videosu", "YouTube videosu" isteklerinde kullan.
---

# Eğitim Videosu Üretici

Doküman → senaryo (JSON) → doğal Türkçe seslendirme → konuşan karakter + kara tahta + altyazı → 1080p MP4 + YouTube kapağı.
Ücretli API, API anahtarı, GPU gerekmez. Ses: Chatterbox Multilingual (Resemble AI, **MIT** – ticari/YouTube kullanımı serbest).

Kod ve modeller: https://github.com/alpay-web/egitim-videosu (Hugging Face'e erişilemeyen ortamlar için
model dosyaları bu reponun release'lerinde kopyalı).

## 0. Hazırlık
```bash
[ -d /tmp/egitim-videosu ] || git clone --depth 1 https://github.com/alpay-web/egitim-videosu /tmp/egitim-videosu
R=/tmp/egitim-videosu
pip install -q -r $R/requirements.txt 2>/dev/null || pip install -q --break-system-packages -r $R/requirements.txt
```

## 1. Dokümanı oku
docx: `pandoc dosya.docx -t plain`, pdf: `pdftotext -layout`. Ana fikirleri çıkar. Marka/kurum adı istenmiyorsa kullanma.

## 2. Senaryoyu yaz → `senaryo.json`  (örnek: `$R/ornek/senaryo_b1.json`)
```json
{
  "baslik": "Ana başlık – Vurgulu kısa başlık",
  "alt_baslik": "Profesör anlatıyor",
  "kapanis": "Başarılar!",
  "telaffuz": {"B1": "be bir", "yesterday": "yesterdey"},
  "sahneler": [
    {"baslik": "Sahne başlığı", "maddeler": ["tahtaya kısa madde"], "anlatim": "Anlatım. Cümleler noktayla biter."}
  ]
}
```
- 8–14 sahne, her biri 60–110 kelime; toplam 5–8 dk. İlk sahne karşılama + içerik, son sahne özet + motivasyon.
- `maddeler`: sahne başına 3–6, ≤ 40 karakter, anlatım sırasıyla (cümleler ilerledikçe sırayla belirir).
- `anlatim`: konuşma dili, "sen" hitabı, kısa cümleler; sembol kullanma. Başlıktaki "–" sonrası kapakta büyük yazılır.
- `telaffuz`: anlatımdaki **her** İngilizce kelime / kısaltma için Türkçe okunuş. Seviye adları Türkçe harfle:
  "A2": "a iki", "B1": "be bir", "B2": "be iki", "C1": "se bir"; "IELTS": "ayelts". Altyazıda orijinal görünür.

## 3. Seslendirme (Chatterbox) — iki yol
**A) GitHub Actions (hızlı, ~10-15 dk, önerilen; repoya yazma erişimi gerekir):**
senaryoyu repoya `senaryolar/<ad>.json` olarak commit'le ve iş akışını başlat:
```bash
curl -X POST -H "Accept: application/vnd.github+json" -H "Content-Type: application/json" \
  https://api.github.com/repos/alpay-web/egitim-videosu/actions/workflows/ses_uret.yml/dispatches \
  -d '{"ref":"main","inputs":{"senaryo":"senaryolar/<ad>.json","etiket":"ses-<ad>","parcalar":"[\"1-3\",\"4-6\",\"7-9\",\"10-12\"]"}}'
# bitince:
curl -fsSL -o sesler.zip https://github.com/alpay-web/egitim-videosu/releases/download/ses-<ad>/sesler.zip && unzip -q sesler.zip -d sesler
```
**B) Bu ortamda (erişim yoksa; yavaş: 2 çekirdekte ~1 dk video ≈ 10 dk):** arka planda çalıştır, log'u izle.
```bash
python $R/scripts/video_uret.py senaryo.json --sadece-ses sesler --ses chatterbox
```
İlk çalıştırmada ~3 GB model GitHub kopyasından iner. Taslak için `--ses piper` hızlıdır ama robotiktir.

## 4. Video
```bash
python $R/scripts/video_uret.py senaryo.json -o video.mp4 --ses-dizini sesler            # 1080p, ~1 dk video/1 dk
python $R/scripts/video_uret.py senaryo.json -o deneme.mp4 --ses-dizini sesler --sahne 1-2 --cozunurluk 720
```
Uzun işleri arka planda çalıştır. 2–3 kare çıkarıp kontrol et (`ffmpeg -ss 30 -i video.mp4 -frames:v 1 k.png`).
Çıktılar: `video.mp4` + `video_kapak.jpg` (1280x720 YouTube kapağı).

Seçenekler: `--karakter yol/karakter.json` (ya da `cizim`), `--abarti 0.5 --cfg 0.5` (Chatterbox vurgu/tempo),
`--referans ses.wav` (sesi bu kayıttan kopyala; yalnızca izinli ses), `--muzik-yok`, `--altyazi-yok`, `--intro-outro-yok`.

## 5. Yeni karakter (isteğe bağlı)
Kullanıcı bir portre verirse: `python -c "import sys;sys.path.insert(0,'$R/scripts');from karakter_foto import arka_plan_sil;arka_plan_sil('girdi.png','karakterler/ad.png')"`
Sonra görseli 10 px ızgarayla büyütüp bak ve `karakterler/ad.json` yaz:
`{"agiz":[cx, cy(üst dişlerin alt sınırı), yarı_genişlik, gülüş_eğrisi_px], "cene_alt": y, "gozler":[[cx,cy,rx,ry],[...]] (göz akı elipsleri), "boyun": y}`.
Kısa bir deneme render'ında ağız/göz kırpmayı kontrol et.

## 6. Teslim
MP4 ve kapak görselini gönder; süre, sahne sayısı ve önerilen YouTube başlığı + açıklamasını (sahne başlıklarından
zaman damgalı bölümlerle) kısa ver. Video yapay zekâ sesiyle üretildiği için açıklamaya bunu belirtmeyi öner.
