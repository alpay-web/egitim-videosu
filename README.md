# 🎓 egitim-videosu

**Dokümandan YouTube'a hazır, animasyonlu eğitim videosu üreten, tamamen ücretsiz ve açık kaynak bir Claude skill'i.**

Bir eğitim dokümanı ver; Claude onu sahnelere böler, doğal bir Türkçe sesle seslendirir ve konuşan animasyonlu
bir profesörle 1080p video + YouTube kapak görseli üretir.

- 🗣️ **Doğal Türkçe ses:** [Chatterbox Multilingual](https://github.com/resemble-ai/chatterbox) (MIT) + her cümleyi Whisper ile doğrulayan kalite kapısı
- 🎬 **Sahne türleri:** madde, tablo (yanlış ✗ / doğru ✓), rakam kartı, karşılaştırma, zaman çizelgesi, ipucu kutusu, geri sayımlı soru
- 👉 **İşaretçi:** anlatılan madde/satır tam o cümlede vurgulanır; ölçülü "tık / ding" efektleri
- ✍️ **Senaryo sanatı:** kancalı açılış, kanca→kurulum→gelişme→doruk→kapanış yapısı, sahne bazında ses tonu ve duraklamalar
- 📚 **Uzun dokümanlar:** kapsam haritası ve video serisi planı; kapsam testiyle hiçbir bölüm sessizce atlanmaz
- 🧪 **Öz-denetim:** tekdüzelik kontrolü, storyboard onayı, otomatik kalite raporu (LUFS, sessizlik, siyah/donmuş kare, kare tablosu)
- 👨‍🏫 Sade çizim profesör (kürsüde), yavaş kamera, altyazı, intro/outro, YouTube kapağı
- 💸 API anahtarı yok, GPU yok, ücret yok

Esinlenilen projeler (yalnızca fikirler; kod kopyalanmadı): [Paper2Video](https://github.com/showlab/Paper2Video) (imleç),
[Code2Video](https://github.com/showlab/Code2Video) (etkin satır vurgusu), [OpenMontage](https://github.com/OpenMontageInc/OpenMontage)
(sahne şablonları, slayt-gösterisi riski, öz-denetim, senaryo yapısı).

## Nasıl çalışır
| Adım | Nerede |
|---|---|
| Senaryo yazımı | Claude |
| Seslendirme (Chatterbox) | GitHub Actions (paralel, ~10-15 dk) **ya da** doğrudan Claude ortamında (yavaş) |
| Animasyon + video | Claude ortamı (Pillow + ffmpeg) |

Claude'un ortamı Hugging Face'e erişemediği için model dosyaları bu reponun release'lerine kopyalanır
(`Modelleri GitHub'a kopyala` iş akışı).

## Claude'da kullanım
- **claude.ai:** Ayarlar → Capabilities → Skills → bu repodaki `SKILL.md`'yi (ya da repo zip'ini) yükle. Sonra:
  > "Ekteki dokümandan eğitim videosu yap."
- **Claude Code:** `git clone https://github.com/alpay-web/egitim-videosu ~/.claude/skills/egitim-videosu`

## Elle kullanım
```bash
pip install -r requirements.txt chatterbox-tts
python scripts/video_uret.py ornek/senaryo_b1.json --sadece-ses sesler          # seslendirme
python scripts/video_uret.py ornek/senaryo_b1.json -o video.mp4 --ses-dizini sesler
```
GitHub'da: Actions → **Seslendirme üret** → Run workflow → release'ten `sesler.zip`.

## Lisanslar
Kod: MIT. Chatterbox: MIT. Piper fahrettin sesi (referans): CC0. Karakter görseli: repo sahibine aittir.
YouTube açıklamasında sesin yapay zekâ ile üretildiğini belirtmeniz önerilir.

### Benzer projelerden alınan fikirler (yalnızca fikir; kod kopyalanmadı)
| Fikir | Kaynak (lisans) | Bizde |
|---|---|---|
| Animasyonu kelimeye bağlama | manim-voiceover "bookmark" (MIT), explainer-video [köşeli parantez] (MIT) | Öğe, anahtar kelimesi söylenirken açılır; Whisper kelime zamanları `SS_CC.json` |
| "Ekran sesin önünde" + senkron raporu | explainer-video (MIT) | Ölü hava / donuk ekran uyarısı, otomatik giriş yazısı |
| Yerleşim raporu | explainer-video (MIT), TheoremExplainAgent "element layout" (MIT) | Taşan/kesilen metin, küçük yazı uyarıları (`--kontrol`) |
| .srt teslimi | explainer-video, MoneyPrinterTurbo (MIT) | Her render'da `video.srt` |
| Bölüm başlıkları | explainer-video `SECTIONS`, Remotion/Manim header | `bolum` alanı → tahta alt bilgisi, ilerleme çizgisi, YouTube bölümleri |
| 5 ölçütlü değerlendirme | TheoremExplainAgent (MIT) | Denetim adımında doğruluk/görsel ilgi/akış/yerleşim/tutarlılık puanı |
| Sahne türleri, tekdüzelik kontrolü, senaryo kuralları | OpenMontage (AGPL — yalnızca fikir) | Rakam/karşılaştırma/ipucu/zaman, `cesitlilik_raporu` |
| İmleç / etkin öğe | Paper2Video, Code2Video (MIT) | İşaretçi + vurgu |
