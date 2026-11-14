---
name: egitim-videosu
description: Bir eğitim dokümanından (docx, pdf, md, txt, Claude Doc) anlatımlı, animasyonlu, altyazılı 1080p YouTube eğitim videosu (uzun dokümanlarda video serisi) ve kapak görseli üretir. Doğal Türkçe ses (Chatterbox, MIT), tablo/rakam/zaman çizelgesi/karşılaştırma/soru sahneleri, otomatik kalite denetimi. Ücretsiz ve açık kaynak. "bu dokümanı anlatan video yap", "eğitim videosu", "ders videosu", "YouTube videosu" isteklerinde kullan.
---

# Eğitim Videosu Üretici

Doküman → kapsam haritası → (seri) planı → senaryo → kapsam testi → storyboard → seslendirme → video → denetim → teslim.
GPU ve ücretli API gerekmez. Kod: https://github.com/alpay-web/egitim-videosu

## 0. Hazırlık
```bash
[ -d /tmp/egitim-videosu ] || git clone --depth 1 https://github.com/alpay-web/egitim-videosu /tmp/egitim-videosu
R=/tmp/egitim-videosu
pip install -q -r $R/requirements.txt 2>/dev/null || pip install -q --break-system-packages -r $R/requirements.txt
```

## 1. Dokümanı anla → kapsam haritası
docx: `pandoc dosya.docx -t markdown`, pdf: `pdftotext -layout`, Claude Doc: docs araçlarıyla oku.
Başlık başlık kelime sayısını çıkar (tablo: bölüm · kelime · tür: kavram / tablo / liste / alıştırma / metin).
Konuşma hızı ≈ 130 kelime/dk; tahmini anlatım süresi = içerik kelimesi ÷ 130 × 0.6 (özetleme payı).

## 2. Plan ve onay (pahalı adımlardan önce)
- **Tahmini süre > 9 dk ya da doküman > ~2.500 kelime → VİDEO SERİSİ öner**: her video 5–8 dk, tek bir
  öğrenme hedefi. Örnek: 1) Strateji ve taktikler 2–4) Gramer dersleri (3–4 ders/video) 5) Kelime 6) Okuma
  7) Dinleme (metinler seslendirilir) 8) Konuşma modelleri 9) Deneme sınavı (soru sahneleriyle). Hangi bölümün
  hangi videoya gittiğini ve dışarıda kalanı açıkça yaz; hiçbir bölüm sessizce atlanmaz.
- Kullanıcıya kısa bir teklif sun: video listesi, her birinin süresi, sahne listesi ve türleri, ilk video önerisi.
  Onay gelmeden seslendirmeye geçme.

## 3. Senaryo yaz → `senaryo.json` (örnek: `$R/ornek/senaryo_b1.json`)
**Senaryo sanatı (zorunlu):**
- **Kanca ile aç (ilk 5 sn):** şaşırtıcı bir gerçek, risk ya da soru. YASAK açılışlar: "Merhaba, bu videoda…",
  "Bugün … öğreneceğiz". Kanca → neden önemli → yol haritası.
- **Yapı:** kanca → kurulum (neden umursamalı) → gelişme → doruk ("aha" anı) → kapanış (tek cümle özet + harekete
  geçirici). Sahneler arası "ve sonra" değil, "bu yüzden / ama" bağıyla geç.
- **Kelime bütçesi:** ~130 kelime/dk; sahne başına 50–110 kelime. Kısa cümleler, "sen" hitabı, konuşma dili.
- **Her 8–10 sn'de görsel bir olay:** yeni madde/satır/kart/adım ya da soru.
- **Ses performansı:** sahneye `"ton"`: `"merakli"` (giriş), `"canli"` (taktik), `"ciddi"` (uyarı), `"sakin"`
  (kapanış). Önemli bir cümleden sonra `[dur]` (0.9 sn sessizlik). Soru/ünlem cümleleri kendiliğinden uzun durur.
- **Sadakat:** yalnızca dokümandaki bilgiler; sayı/kural uydurma.

**Sahne türleri — içeriğin şekline göre seç (aynı türü art arda 3 kez kullanma):**
```json
{"baslik": "...", "maddeler": ["≤40 karakter", "..."], "anlatim": "...", "goster": [0, 2, 3]}
{"baslik": "...", "tur": "tablo", "tablo": {"basliklar": ["Görürsen", "Cevap"], "satirlar": [["since", "have + V3"]], "stil": "yanlis-dogru"}}
{"baslik": "...", "tur": "rakam", "kartlar": [{"deger": "30", "birim": "dakika", "etiket": "Sınav süresi"}]}
{"baslik": "...", "tur": "karsilastirma", "sol": {"baslik": "Dinlemede", "renk": "mavi"}, "sag": {"baslik": "Okumada", "renk": "yesil"}, "satirlar": [["sol", "sağ"]]}
{"baslik": "...", "tur": "zaman", "adimlar": [{"baslik": "1. Gün", "metin": "Gramer"}]}
{"baslik": "...", "tur": "ipucu", "ipucu": {"tip": "ipucu|uyari|not", "metin": "Tek güçlü mesaj"}}
{"baslik": "Kendini dene 1/3", "tur": "soru", "soru": {"metin": "Yes, ___.", "secenekler": ["I'm", "I am", "I do"], "dogru": 1, "cevap_cumle": 2, "bekle": 4}}
```
- **maddeler:** liste/özet. **tablo:** dokümandaki tablolar, "görürsen → cevap", yanlış/doğru listeleri.
  **rakam:** 1–3 çarpıcı sayı (süre, puan, adet). **karsilastirma:** iki yan (önce sol sütun, sonra sağ açılır;
  `goster` = sol satırlar + sağ satırlar sırasıyla). **zaman:** adımlar/plan/süreç (≥4 adımda dikey). **ipucu:**
  tek vurucu mesaj. **soru:** alıştırmalardan; anlatımda soruyu okuma ("Ekrandaki soruyu oku"), `cevap_cumle` =
  "Doğru cevap…" cümlesinin indeksi; öncesinde geri sayım, sonra doğru seçenek yeşil + "ding".
- `goster`: her öğenin hangi cümlede (0'dan) açılacağı; o an işaretçi öğeye kayar ve "tık" sesi çalar.
- `telaffuz`: kısaltma/seviye adları Türkçe harfle ("B1": "be bir", "C1": "se bir", "IELTS": "ay elts", "A": "a",
  "B": "be"); sorunlu İngilizce kelimeler ("had": "hed", "Enjoy": "inçoy"). `telaffuz_kok`: {"fiil": "fiyil"}.
  Chatterbox'ın zorlandığı "şık" yerine "seçenek" yaz.

## 4. Kapsam testi (PresentQuiz fikri)
Kaynaktan, video kapsamındaki bölümlerden 8–10 kritik soru çıkar (yalnızca dokümana dayalı). Her birinin cevabı
senaryoda geçiyor mu, tek tek işaretle. Cevapsız kalan kritik konu varsa senaryoya ekle ya da bilinçli olarak
serinin başka videosuna bırak ve bunu teslimde söyle.

## 5. Storyboard + kontrol (onay kapısı)
```bash
python $R/scripts/video_uret.py senaryo.json --kontrol                    # tekdüzelik/uzunluk uyarıları
python $R/scripts/video_uret.py senaryo.json --storyboard storyboard.png  # her sahnenin son hali, tek görsel
```
Storyboard'a **bak**: taşma, üst üste binme, boş tahta, yanlış tür. Düzelt, kullanıcıya göster, onay al.

## 6. Seslendirme (Chatterbox, MIT) — `--kalite 3` Whisper kapısı her cümleyi doğrular
**A) GitHub Actions (hızlı, paralel; repoya yazma erişimi gerekir):** senaryoyu `senaryolar/<ad>.json`
olarak commit'le, sonra:
```bash
curl -X POST -H "Accept: application/vnd.github+json" -H "Content-Type: application/json" \
  https://api.github.com/repos/alpay-web/egitim-videosu/actions/workflows/ses_uret.yml/dispatches \
  -d '{"ref":"main","inputs":{"senaryo":"senaryolar/<ad>.json","etiket":"ses-<ad>","parcalar":"[\"1-3\",\"4-6\",\"7-9\",\"10-12\",\"13-15\"]"}}'
curl -fsSL -o sesler.zip https://github.com/alpay-web/egitim-videosu/releases/download/ses-<ad>/sesler.zip && unzip -q sesler.zip -d sesler
```
**B) Bu ortamda (yavaş, ~10 dk/1 dk video):** `python $R/scripts/video_uret.py senaryo.json --sadece-ses sesler --ses chatterbox --kalite 3`
(arka planda çalıştır). `kalite_raporu.txt`'te puanı < 0.8 olan cümlelerde telaffuzu düzelt ve yalnızca onları
`--cumleler 04_05,06_07` ile yeniden üret.

## 7. Video
```bash
python $R/scripts/video_uret.py senaryo.json -o video.mp4 --ses-dizini sesler     # 1080p + video_kapak.jpg
```
Varsayılan: sade çizim profesör (kürsüde), yavaş kamera, işaretçi, tık/ding efektleri, müzik yok.
Seçenekler: `--muzik`, `--efekt-yok`, `--kamera-yok`, `--altyazi-yok`, `--karakter yol.json` (fotoğraf karakter),
`--sahne 2-3 --cozunurluk 720` (hızlı deneme).

## 8. Denetim (teslimden önce zorunlu, en fazla 2 düzeltme turu)
```bash
python $R/scripts/kalite_raporu.py video.mp4      # süre, LUFS/tepe, sessizlik, siyah/donmuş kare + kare tablosu
```
Kare tablosuna bak. Bulguları ciddiyetle yaz (kritik / öneri) ve her birine somut düzeltme koy
("Sahne 6 tablo başlıkları üst üste → başlıkları kısalt"); "biraz uzun olabilir" gibi belirsiz bulgu yazma.
Kritikleri düzelt, yeniden üret; 2 turdan sonra kalanları teslimde açıkça söyle.

## 9. Teslim
MP4 + kapak görselini gönder. Ver: süre, sahne sayısı, kapsadığı bölümler (ve serinin kalanı), önerilen YouTube
başlığı, sahne başlıklarından zaman damgalı bölümler, "Seslendirme yapay zekâ ile üretilmiştir" notu.
