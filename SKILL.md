---
name: egitim-videosu
description: Bir eğitim dokümanından (docx, pdf, md, txt, Claude Doc) anlatımlı, animasyonlu, altyazılı 1080p YouTube eğitim videosu (uzun dokümanlarda da tek, bölümlere ayrılmış video) ve kapak görseli üretir. Doğal Türkçe ses (Chatterbox, MIT), tablo/rakam/zaman çizelgesi/karşılaştırma/soru sahneleri, otomatik kalite denetimi. Ücretsiz ve açık kaynak. "bu dokümanı anlatan video yap", "eğitim videosu", "ders videosu", "YouTube videosu" isteklerinde kullan.
---

# Eğitim Videosu Üretici

Doküman → kapsam haritası → plan → senaryo → kapsam testi → storyboard → seslendirme → video → denetim → teslim.
GPU ve ücretli API gerekmez. Kod: https://github.com/alpay-web/egitim-videosu

## 0. Hazırlık
Sürüm: `cat $R/VERSION` (değişiklikler `CHANGELOG.md`'de). Her push'ta `Test` işi (birim testleri + kısa video)
çalışır; kırmızıysa önce onu düzelt. Senaryo hataları (yanlış tür, `goster` taşması, `cevap_cumle` dışı) her
komutta render'dan önce yakalanır.
Pakete kalıcı bir iyileştirme yapınca: `VERSION` ve `CHANGELOG.md`'yi güncelle, push et, `surum.yml` işini çalıştır.
```bash
[ -d /tmp/egitim-videosu ] || git clone --depth 1 https://github.com/alpay-web/egitim-videosu /tmp/egitim-videosu
R=/tmp/egitim-videosu
pip install -q -r $R/requirements.txt 2>/dev/null || pip install -q --break-system-packages -r $R/requirements.txt
```

## 1. Dokümanı anla → kapsam haritası
```bash
python $R/scripts/belge_oku.py belge.pdf -o belge.md     # PDF/Word/PowerPoint/Excel/HTML/EPUB → belge.md + belge_harita.md
```
Okuyucu sırası: markitdown (MIT) → pandoc → pdftotext. `belge_harita.md` her başlığın kelime sayısını, tablo
sayısını ve sahne önerisini verir; taranmış PDF'i (sayfa başına çok az metin) uyarır — o zaman OCR iste, uydurma.
Claude Doc / artifact linki: docs araçlarıyla oku, metni `.md` olarak kaydet ve aynı komutu çalıştır.
Haritadaki **her satır** ya bir sahneye eşlenir ya da "dışarıda bırakıldı: neden" diye not edilir.
Konuşma hızı ≈ 130 kelime/dk; tahmini anlatım süresi = içerik kelimesi ÷ 130 × 0.6 (özetleme payı).

## 2. Plan ve onay (pahalı adımlardan önce)
- **Varsayılan: dokümanın TAMAMI TEK VİDEODA** (kullanıcı bunu tercih ediyor). Uzun dokümanda 30–40 dk olabilir;
  YouTube bölüm (chapter) zaman damgaları ile gezinilir. Sıra: kanca + yol haritası → strateji → konu dersleri
  (her ders: kural sahnesi + "Kendini dene" sorusu) → kelime → okuma/dinleme/konuşma örnekleri → deneme → kapanış.
  Alıştırmaların hepsi okunmaz; her bloktan 1–2 temsili soru seçilir, gerisi için "rehberdeki alıştırmalar" denir.
- Seri (5–8 dk'lık videolar) yalnızca kullanıcı isterse. Önceki seslendirmeler **otomatik** yeniden kullanılır
  (aşağıda "Ses önbelleği").
- Kullanıcıya kısa bir plan sun (bölümler, tahmini süre, sahne türleri) ve hiçbir başlığın sessizce atlanmadığını
  göster. Onay gelmeden seslendirmeye geçme (kullanıcı "devam et" dediyse doğrudan ilerle).

## 3. Senaryo yaz → `senaryo.json` (örnek: `$R/ornek/senaryo_b1.json`)
**Senaryo sanatı (zorunlu):**
- **Kanca ile aç (ilk 5 sn):** şaşırtıcı bir gerçek, risk ya da soru; ilk sahneye `"kanca": "kısa vurucu cümle"`
  ekle — ilk madde gelene kadar tahtada büyük yazılır (tahta boş kalmaz). YASAK açılışlar: "Merhaba, bu videoda…",
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
  tek vurucu mesaj. **soru:** alıştırmalardan; soruyu ve seçenekleri SESLİ OKU ("{The museum} boşluk {in 1890}.
  Seçenekler: A, {built}; B, {was built}; C, {has built}."), `cevap_cumle` = "Doğru cevap…" cümlesinin indeksi;
  öncesinde geri sayım, sonra doğru seçenek yeşil + "ding".
- **EKRANDA YAZAN HER ŞEY OKUNUR (zorunlu):** tablonun iki sütunu da, karşılaştırmanın iki yanı da, rakam kartının
  etiketi de, soru ve seçenekler de anlatımda geçmeli. Her öğeye ayrı bir cümle ayır (madde temposu). `--kontrol`
  "okunmuyor" uyarısı verirse anlatımı düzelt. `goster` yazma: video her öğeyi onu okuyan cümlede, o kelime
  söylenirken açar (`oto_goster`); ardışık iki öğe arasında en az 1,2 sn olur.
- **İngilizce `{süslü parantez}` içinde (zorunlu):** "{had better}", "{I'm late, aren't I?}". Parantez içi Chatterbox'ta
  İngilizce (en) üretilir, dışı Türkçe; aynı referans ses, seviyeler eşitlenir (Chatterbox tek çağrıda dil
  değiştiremiyor: resemble-ai/chatterbox#346). İngilizce kelimeye Türkçe ek koyma ("{had better}'dan" değil,
  "{had better} kalıbından"). Taslağı otomatik işaretlemek için `--ingilizce-isaretle` (wordfreq), sonra gözden geçir:
  Türkçe "not", "on" gibi kelimeler yanlış işaretlenebilir; tek başına "{at}", "{I am}" gibi kısa öbekleri elle ekle.
- `goster`: her öğenin hangi cümlede (0'dan) açılacağı; o an işaretçi öğeye kayar (`--tik` verilirse hafif tık sesi).
  **Kelime senkronu (varsayılan):** öğe, cümlenin başında değil, öğenin ilk anlamlı kelimesi söylenirken açılır
  (Whisper kelime zamanı `SS_CC.json` varsa saniyesi saniyesine, yoksa cümle içindeki konumuna göre). Elle çapa:
  `"3:enough"` (3. cümlede "enough" kelimesinde) ya da `2.5` (2. cümlenin ortası). Kapatmak: `--kelime-senkron-yok`.
- **Ekran sesin önünde gider** (explainer-video kuralı): konuşma boş tahtada başlamasın, 14 sn'den uzun süre tahtada
  yeni bir şey olmasın. İlk öğe geç geliyorsa video ilk cümleyi tahtada büyük **giriş yazısı** olarak gösterir
  (metni `"giris"` alanıyla ver; kapatmak: `--giris-yok`).
- `bolum`: bölüm başlatan sahneye `"bolum": "Gramer 5: Passive"` yaz. Tahtanın alt bilgisinde görünür, ilerleme
  çubuğuna bölüm çizgisi düşer ve YouTube bölüm listesi otomatik çıkar. Senaryoya `youtube_baslik` (≤100 karakter)
  ve `etiketler` de ekle.
- `telaffuz`: kısaltma/seviye adları Türkçe harfle ("B1": "be bir", "C1": "se bir", "IELTS": "ay elts", "A": "a",
  "B": "be"). İngilizce kelimeler için telaffuz YAZMA, `{…}` kullan. `telaffuz_kok`: {"fiil": "fiyil"}.
  Chatterbox'ın zorlandığı "şık" yerine "seçenek" yaz.

## 4. Kapsam testi (PresentQuiz fikri)
Kaynaktan, video kapsamındaki bölümlerden 8–10 kritik soru çıkar (yalnızca dokümana dayalı). Her birinin cevabı
senaryoda geçiyor mu, tek tek işaretle. Cevapsız kalan kritik konu varsa senaryoya ekle ya da bilinçli olarak
dışarıda bıraktığını teslimde açıkça söyle.

## 5. Storyboard + kontrol (onay kapısı)
```bash
python $R/scripts/video_uret.py senaryo.json --kontrol [--ses-dizini sesler]  # tekdüzelik + YERLEŞİM + SENKRON raporu
python $R/scripts/video_uret.py senaryo.json --storyboard storyboard.png  # her sahnenin son hali, tek görsel
```
`--kontrol` raporları: **yerleşim** (taşan/kesilen metin, 30 px'ten küçük yazı, sığmayan seçenek/kart) ve
**senkron** (ölü hava: konuşma başladı ama tahta boş; donuk ekran: 14 sn+ yeni öğe yok). Ses üretildikten sonra
`--ses-dizini` ile gerçek sürelerle tekrar çalıştır. Yerleşim uyarısı bırakma.
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
**Ses önbelleği (içerik adresli, manim-voiceover fikri):** her ses klasöründe `dizin.json` cümle → metin özeti
eşlemesi tutar. Sahne eklemek/silmek/sırasını değiştirmek eski sesleri boşa çıkarmaz; metni değişen cümle ise asla
eski sesle çalmaz. Akış:
```bash
python $R/scripts/video_uret.py senaryo.json --eksik --ses-dizini eski1,eski2   # hangi cümleler eksik? parcalar + --cumleler verir
```
Workflow'a `"taban":"ses-b1-tam-kurs,ses-<ad>"` girdisi ver: o release'lerde aynı metin varsa kopyalanır, yalnızca
yeni/değişen cümleler sentezlenir. Render'da birden çok klasör verilebilir: `--ses-dizini sesler,eski_sesler`.
Eski (dizin.json'suz) klasörü etiketlemek için: `--dizin-olustur KLASOR` (o klasörün bu senaryoya ait olduğundan eminsen).
**Taslak:** seslendirmeyi beklemeden zamanlama/görsel kontrolü için `--ses sessiz` ile 720p taslak video çıkar.
**B) Bu ortamda (yavaş, ~10 dk/1 dk video):** `python $R/scripts/video_uret.py senaryo.json --sadece-ses sesler --ses chatterbox --kalite 3`
(arka planda çalıştır). `kalite_raporu.txt`'te puanı < 0.8 olan cümlelerde telaffuzu düzelt ve yalnızca onları
`--cumleler 04_05,06_07` ile yeniden üret.

## 7. Video
```bash
python $R/scripts/video_uret.py senaryo.json -o video.mp4 --ses-dizini sesler     # 1080p + video_kapak.jpg
```
Varsayılan: sade çizim profesör (kürsüde), yavaş kamera, işaretçi, yalnızca doğru cevapta "ding", müzik yok.
**Temiz ses (mikrofon sürtmesi/tık yok):** cümle klipleri yumuşak fade-in/out ile birleşir; zincirde `adeclick`,
`afftdn` (hafif gürültü azaltma) ve `deesser` var; konuşma üstündeki "tık" efekti varsayılan kapalı.
**Gürültü (genel çözüm, katmanlı):** (1) seslendirme işi her cümleyi **DeepFilterNet3** ile temizler
(`scripts/ses_temizle.py`, en fazla 30 dB bastırma; eski sesler için `ses_temizle.yml`), (2) `klip_temizle` cümle
başı/sonu kuyruklarını ve uzun kısık bölgeleri keser, (3) render zincirinde `agate` kelime aralarındaki artığı bastırır.
**Nefes/hışırtı temizliği (varsayılan):** Chatterbox bazı cümlelerin sonuna 0,5–2 sn'lik düşük seviyeli, tiz
(4–7 kHz) bir nefes/sürtme kuyruğu ekliyor; `klip_temizle` konuşma tepesinin 24 dB altındaki tonsuz kuyrukları
keser, cümle içindeki ≥150 ms'lik nefesleri 24 dB kısar. Sondaki "s/ş" gibi sesler daha yüksek olduğu için korunur.
Kapatmak: `--temizleme-yok`.
**Dudak senkronu:** çizim profesörün ağzı yalnızca açılıp kapanmaz; sesin formant bantlarından her kare için
'a' (açık), 'o' (yuvarlak) ve 'i' (yayvan, dişler görünür) biçimi seçilir. Model gerektirmez, render süresini
etkilemez. (SadTalker/Wav2Lip/LivePortrait gibi gerçekçi konuşan yüzler GPU ister ve üretimi çok yavaşlatır.)
Seçenekler: `--tik`, `--muzik`, `--efekt-yok`, `--kamera-yok`, `--altyazi-yok`, `--karakter yol.json` (fotoğraf karakter),
`--sahne 2-3 --cozunurluk 720` (hızlı deneme).

## 8. Denetim (teslimden önce zorunlu, en fazla 2 düzeltme turu)
```bash
python $R/scripts/kalite_raporu.py video.mp4      # süre, LUFS/tepe, sessizlik, siyah/donmuş kare + kare tablosu
```
Kare tablosuna bak. Bulguları ciddiyetle yaz (kritik / öneri) ve her birine somut düzeltme koy
("Sahne 6 tablo başlıkları üst üste → başlıkları kısalt"); "biraz uzun olabilir" gibi belirsiz bulgu yazma.
Kare tablosunu TheoremExplainAgent'in 5 ölçütüyle 1–5 puanla: **doğruluk** (dokümana sadık mı), **görsel ilgi**
(tahta anlatılanı mı gösteriyor), **akış** (konular mantıklı sırada mı), **yerleşim** (taşma/üst üste binme var mı),
**tutarlılık** (renk, yazı, stil aynı mı). 4'ün altındaki her ölçüt için somut düzeltme yap.
Kritikleri düzelt, yeniden üret; 2 turdan sonra kalanları teslimde açıkça söyle.

## 9. Teslim
Video her render'da yayın paketini de yazar: `video.srt` (YouTube altyazısı; ≤2 satır × 42 karakter) ve
`video_youtube.txt` (başlık, bölümlü açıklama, etiketler, yapay zekâ notu). MP4 + kapak + .srt + youtube.txt'yi
gönder; süreyi, sahne sayısını ve kapsadığı bölümleri söyle. SRT'nin YouTube Studio > Altyazılar'a
yükleneceğini ve "değiştirilmiş/yapay içerik" kutusunun işaretleneceğini hatırlat.
