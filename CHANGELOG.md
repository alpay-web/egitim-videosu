# Değişiklik günlüğü

Sürümleme: `ANA.ARA.YAMA` — ANA: senaryo biçimi geriye uyumsuz değişirse; ARA: yeni özellik; YAMA: düzeltme.



## 2.4.2 · 2026-11-22
- Sadakat: görsel satırlarında yalnız alt metin sayılır; tırnaklar kelimeden ayrılır; belgedeki tüm sayı parçaları tanınır; markdown bağlantı adresleri kapsam hesabına girmez (yalnız bağlantı metni okunur).
- Noktalı ve alt çizgili teknik tokenlar parça parça okunur (`ES|QL` → ESQL, `@` atılır).

## 2.4.1 · 2026-11-22
- Noktalama esleri (`es`): virgül, iki nokta, noktalı virgül ve tirede duraklama Whisper kelime zamanlarıyla tamamlanır; konuşma hızı değişmez. `cumle_arasi` 0,7, `sahne_arasi` 1,6 (yeni senaryolar). Soru ve iki nokta sonu araları cümle arasına göre ölçeklenir.
- Hız tavanı (varsayılan kapalı; kullanıcı genel hızın düşmesini istemedi): model uzun cümlelerde hızlanıyordu (kısa 1,7, uzun 2,5 kelime/sn). Senaryoda `hiz_tavani` (yeni senaryolarda 1,9 kelime/sn) aşan cümleyi perde değişmeden yavaşlatır (en çok %20); kelime zamanları da ölçeklenir. `cumle_arasi` (yeni: 0,6 sn) ayarlanabilir.
- Telaffuz A/B sonucu: kullanıcı B'yi (teknik terim sözlüğü) seçti; yeni senaryoların varsayılanı `sozluk`.

## 2.4.0 · 2026-11-22
- Teknik terim telaffuzu: `teknik_terimler.json` (449 terim, Türk BT ekiplerinin okunuşu) + `ingilizce_mod` (`sozluk` | `cmu` | `ayri`); yeni modda CMU yedeğinde W → u. Yeni senaryolar `sozluk` ile üretilir; eski senaryolar değişmez.
- Giriş kartı ve YouTube kapağı temalı (`scripts/tema.py`): 15 renk/yazı tipi/düzen teması, WCAG kontrast denetimi, OFL yazı tipleri ilk kullanımda indirilir. Senaryoda `"tema"`.
- Araştırma raporları: `docs/telaffuz_arastirmasi.md`, `docs/giris_tasarim_arastirmasi.md` (her biri 100 depo).

## 2.3.0 — 2026-11-17
**Ses modeli: Chatterbox Multilingual V3.** Açık kaynak TTS araştırması (VoxCPM2, FireRedTTS3, Chatterbox V2/V3;
`tts_karsilastir.yml` ile aynı paragraf, aynı referans ses) sonrası kullanıcı V3'ü seçti.
- Varsayılan model V3 (`--ses-modeli`, senaryoda `"ses_modeli"`); eski senaryolar `v2` olarak işaretlendi, önbellek
  sesleri geçerli kalır. Önbellek anahtarı modele göre ayrı: iki modelin sesi karışmaz.
- Tempo varsayılanı modele göre: V3 1.0 (zaten daha sakin), V2 0.9.
- Gürültü katmanları değişmeden V3'te çalışıyor (DeepFilterNet, klip temizliği, DNSMOS, Whisper); deneme
  sahnelerinde BAK 4,14, kalite kapısı GEÇTİ.
- `modeller.yml` V3 ağırlığını da yedekler; `tts_karsilastir.yml` yeni modelleri denemek için kalıcı.
- Render ses zinciri modele göre (`--ses-isleme tam|hafif|yok`): V3'te `hafif` (V2 için kurulan parlatma/
  kompresör V3 sesini sertleştiriyordu); AAC 192 kbps. `ses_uret.yml`: `ham_sakla` (temizlik öncesi sesler).
- Klip temizliği: uzun sessizlik + sondaki tık atılır (cümle sonlarında 0,5–2,7 sn yapay boşluk).

## 2.2.0 — 2026-11-16
**Kalite kapısı: karar mercii, ses denetçisi, sadakat ve bilgi kirliliği kontrolü** (`docs/kalite_denetim_arastirmasi.md`).
- `scripts/ses_puan.py`: DNSMOS (CPU, ~1 MB ONNX) ile cümle başına SIG/BAK/OVRL/P808; gürültülü cümleler listelenir.
  Seslendirme iş akışı her cümleyi puanlar, `ses_puan.json` yayına eklenir.
- `scripts/sadakat.py`: belgeden eksik satır, belgede olmayan sayı/İngilizce (uydurma), İngilizce öbeğe düşmüş
  Türkçe kelime, belgede geçmeyen ad, eklenen açıklamalar.
- `scripts/kalite_kapisi.py`: tüm denetimleri tek GEÇTİ/KALDI kararında toplar (`*_karar.md`); KALDI ise teslim yok.
- SKILL.md 8a (kapı) ve 8b (kanıtlı, 5 ölçütlü bağımsız hakem).
- Dönüştürücü: Türkçe karşılıklar ("ve", "fiilin ikinci hali", "değil", "İngiliz İngilizcesi") artık İngilizce
  öbeğin dışında (B1 senaryosunda 57 hata → 0); italik Türkçe vurgu İngilizce sayılmaz; kelime içi vurgu
  (smok*ing*) birleşir; "on/at/in ve …" edatları İngilizce okunur; ## ve okuma bölümü başlıkları okunur;
  uzun hücreli tablolar daha az satırla bölünür (yazı 30 px altına düşmez).
- `ayar.json`: `sadakat_yoksay` (bilerek çıkarılan ifadeler). 2 yeni test (toplam 15).

## 2.1.0 — 2026-11-16
**Önizleme kapısı ve 100 benzer deponun analizi** (`docs/benzer_projeler.md`).
- `--onizleme [SN]`: uzun videodan önce ~90 sn'lik temsili önizleme (açılış + her sahne türünden en kısa sahne +
  İngilizce geçişli sahne). `--onizleme-yaz` seçkiyi ayrı senaryoya yazar (yalnız o cümleler seslendirilir; tam
  videoda önbellekten gelir). SKILL.md kural 6b: kullanıcı onayı olmadan uzun video üretilmez.
- Ses yüksekliği YouTube standardına çekildi: −14 LUFS (`--lufs`), gerçek tepe ≤ −1.5 dBFS.
- Render sonunda yayın denetimi (`_denetim.json`): LUFS, tepe, beklenmedik uzun sessizlik (giriş/kapanış/soru
  bekleme hariç).
- Bölümler MP4'e chapter olarak gömülür; `--sesli-kitap` bölümlü `.m4a` anlatım üretir.
- Depo kökünde genel telaffuz sözlüğü `telaffuz.json` (senaryo sözlüğü onu ezer; `--genel-telaffuz-yok`).
- 2 yeni test (toplam 13).

## 2.0.0 — 2026-11-16
**Belgenin tamamı videoda (kesin kural).** `belge_senaryo.py` belgeyi eksiksiz sahnelere çevirir: her madde, her
tablonun tüm satır ve sütunları, her alıştırmanın her sorusu (soru + seçenekler okunur, geri sayım, doğru cevap,
açıklama), okuma parçaları ve dinleme metinleri (İngilizce), model cevaplar. Cevap ve açıklamalar `ayar.json`'dan.
- Yeni sahne türü `metin` (okuma/dinleme metni); `soru` artık 2–4 seçenek ya da boşluk doldurma (`cevap`).
- Tablo hücreleri satır içinde kayar; tahta başlıkları kısaltılır.
- Anlatım hızı `--tempo 0.9` (ses yeniden üretilmeden), cümle arası 0,45 sn.
- "B1" artık "be, bir" (Whisper testinde "be bir" birleşip "bebir" okunuyordu); A1/A2/B2/C1 aynı.
- Ses zincirinden `adeclick` kaldırıldı (uzun videoda dakikalarca sürüyordu).

## 1.2.0 — 2026-11-15
- **Doğal dil geçişi:** kısa İngilizce terimler Türkçe cümle içinde İngilizce okunuşla (CMU Pronouncing Dictionary,
  BSD → Türk harfleri); yalnızca ≥4 kelimelik örnek cümleler ayrı İngilizce ve 0,28 sn duraklamayla. Parça parça
  birleştirmenin kopukluğu giderildi.
- İşaretçi satırlar arasında 0,9 sn yumuşak (ease-in-out) kayıyor; madde belirmesi 0,6 sn.
- İngilizce parçalar kendi dilinde Whisper ile denetleniyor (5 denemeye kadar).

## 1.1.0 — 2026-11-15
**İngilizce doğru okunuyor:** anlatımdaki `{İngilizce}` parçalar Chatterbox'ta İngilizce (en), geri kalanı Türkçe
üretilip aynı referans sesle birleştiriliyor (kod geçişi). `--ingilizce-isaretle` taslağı otomatik işaretler.
**Ekrandaki her şey okunuyor:** `--kontrol` okunmayan tahta metnini bildirir; `goster` gerekmez (`oto_goster`),
öğeler aralarında en az 1,2 sn ile, kendilerini okuyan kelimede açılır. Sorular ve seçenekler sesli okunur.
**Gürültü:** DeepFilterNet3 seslendirme işine eklendi (+ `ses_temizle.yml`), render zincirine `agate`.
**Düzeltmeler:** Chatterbox'ın 5 belirteçten kısa metinde çökmesine koruma; parça çökse de başarılı sesler yayınlanır;
`{…}` içindeki noktalama cümle bölmez.

## 1.0.1 — 2026-11-15
**Düzeltmeler**
- Seslendirme işi Chatterbox referansı için gereken `piper-tts`'i kurmuyordu; sabitlendi (1.8.0). İş artık `pipefail`
  ile gerçek hatada kırmızı olur (önceden hata olsa bile yeşil görünebiliyordu).
- Referans ses repoya sabitlendi (`ses/referans_fahrettin.wav`): ses kimliği kütüphane sürümlerinden bağımsız.
- `klip_temizle` artık cümle içindeki alçak frekanslı mırıltıyı da kısıyor (yalnızca tiz nefesi değil); kenarlarda 20 ms pay.
- Boş kalite raporu release yüklemesini bozuyordu; korundu.

**Kanıt:** ses önbelleği ilk gerçek kullanımda 7 cümleyi yeniden üretmeden kopyaladı.

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
