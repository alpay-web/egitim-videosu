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
Önce kullanıcıya 1 paragraflık bir **plan** sun (sahne listesi, süre, soru sayısı); onay gelirse yaz.
```json
{
  "baslik": "Ana başlık – Vurgulu kısa başlık",
  "alt_baslik": "Profesör anlatıyor", "kapanis": "Başarılar!",
  "telaffuz": {"B1": "be bir"}, "telaffuz_kok": {"fiil": "fiyil"},
  "sahneler": [
    {"baslik": "Madde sahnesi", "maddeler": ["kısa madde", "..."], "anlatim": "..."},
    {"baslik": "Tablo sahnesi", "tur": "tablo", "goster": [2, 3, 4],
     "tablo": {"basliklar": ["Görürsen", "Cevap"], "satirlar": [["yesterday", "V2"], ["since", "have + V3"], ["if + past", "would"]]},
     "anlatim": "..."},
    {"baslik": "Kendini dene 1/3", "tur": "soru",
     "soru": {"metin": "Yes, ___.", "secenekler": ["I'm", "I am", "I do"], "dogru": 1, "cevap_cumle": 2, "bekle": 4},
     "anlatim": "Kendini deneme zamanı. Ekrandaki soruyu oku ve düşün. Doğru cevap B: I am. Açıklama..."}
  ]
}
```
Sahne türleri — içeriğe göre seç, tekdüze madde listesinden kaçın:
- **maddeler** (varsayılan): 3–6 kısa madde; anlatım ilerledikçe sırayla kayarak belirir.
- **tablo**: dokümandaki tablolar, karşılaştırmalar, "görürsen → cevap" listeleri. `stil: "yanlis-dogru"` ile
  ✗ üstü çizili / ✓ yeşil sütunlar. `goster`: her satırın hangi cümle indeksinde (0'dan) açılacağı.
- **soru**: dokümandaki alıştırmalardan 2–4 soru, sona doğru "Kendini dene". `cevap_cumle` = "Doğru cevap…" cümlesinin
  indeksi; ondan önce `bekle` saniye geri sayım olur, sonra doğru seçenek yeşil yanar. Soruyu anlatımda okuma
  ("Ekrandaki soruyu oku"), ekranda göster.
Genel: 10–16 sahne, sahne başına 60–110 kelime, toplam 5–8 dk. İlk sahne karşılama + içerik, son sahne özet + motivasyon.
- `anlatim`: konuşma dili, "sen" hitabı, kısa cümleler; sembol kullanma. Başlıktaki "–" sonrası kapakta büyük yazılır.
- `telaffuz`: Seviye adları ve kısaltmalar Türkçe harfle ("B1": "be bir", "C1": "se bir", "IELTS": "ay elts",
  seçenek harfleri "A": "a", "B": "be"). Sorunlu çıkan İngilizce kelimeler: "had": "hed", "Enjoy": "inçoy".
- Chatterbox'ın zorlandığı Türkçe kelimelerden kaçın: "şık" yerine "seçenek" yaz (tahtada "şık" kalabilir).

## 3. Seslendirme (Chatterbox) — iki yol
Her iki yolda da `--kalite 3` (Actions'ta varsayılan) Whisper kalite kapısını açar: her cümle yazıya dökülüp metinle
karşılaştırılır, uymazsa yeniden üretilir; `kalite_raporu.txt` en düşük puanlı cümleleri gösterir. Sorunlu birkaç cümleyi
yeniden üretmek için `--cumleler 04_05,06_07` kullan ve yeni dosyaları ses klasörüne kopyala.
Bitmiş seslendirmeyi denetlemek için: Actions → "Seslendirmeyi denetle" (`scripts/denetle.py`).

**A) GitHub Actions (hızlı, ~15-30 dk, önerilen; repoya yazma erişimi gerekir):**
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

Varsayılan: sade çizim profesör (kürsü arkasında), müzik yok, yavaş kamera açık.
Seçenekler: `--karakter yol/karakter.json` (fotoğraf tabanlı karakter), `--muzik`, `--kamera-yok`, `--abarti 0.5 --cfg 0.5` (Chatterbox vurgu/tempo),
`--referans ses.wav` (sesi bu kayıttan kopyala; yalnızca izinli ses), `--muzik-yok`, `--altyazi-yok`, `--intro-outro-yok`.

## 5. Yeni karakter (isteğe bağlı)
Kullanıcı bir portre verirse: `python -c "import sys;sys.path.insert(0,'$R/scripts');from karakter_foto import arka_plan_sil;arka_plan_sil('girdi.png','karakterler/ad.png')"`
Sonra görseli 10 px ızgarayla büyütüp bak ve `karakterler/ad.json` yaz:
`{"agiz":[cx, cy(üst dişlerin alt sınırı), yarı_genişlik, gülüş_eğrisi_px], "cene_alt": y, "gozler":[[cx,cy,rx,ry],[...]] (göz akı elipsleri), "boyun": y}`.
Kısa bir deneme render'ında ağız/göz kırpmayı kontrol et.

## 5b. Kendi kendini denetle (teslimden önce zorunlu)
- `ffmpeg -i video.mp4 -vf "fps=1/15,scale=426:240,tile=5x5" -frames:v 1 sheet.png` ile kare tablosu çıkar ve **bak**:
  taşan yazı, boş tahta, üst üste binen öğe, yanlış sahne türü var mı?
- Seslendirme için `kalite_raporu.txt`'teki en düşük puanlı cümleleri incele; yanlış okunanı `telaffuz` ile düzelt ve
  `--cumleler` ile yalnızca onları yeniden üret.
- Senaryodaki bilgileri kaynak dokümanla karşılaştır (uydurma bilgi yok).

## 6. Teslim
MP4 ve kapak görselini gönder; süre, sahne sayısı ve önerilen YouTube başlığı + açıklamasını (sahne başlıklarından
zaman damgalı bölümlerle) kısa ver. Video yapay zekâ sesiyle üretildiği için açıklamaya bunu belirtmeyi öner.
