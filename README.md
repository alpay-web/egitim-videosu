# 🎓 egitim-videosu

**Dokümandan YouTube'a hazır, animasyonlu eğitim videosu üreten, tamamen ücretsiz ve açık kaynak bir Claude skill'i.**

Bir eğitim dokümanı ver; Claude onu sahnelere böler, doğal bir Türkçe sesle seslendirir ve konuşan animasyonlu
bir profesörle 1080p video + YouTube kapak görseli üretir.

- 🗣️ **Doğal Türkçe ses:** [Chatterbox Multilingual](https://github.com/resemble-ai/chatterbox) (MIT – ticari kullanım serbest)
- 👨‍🏫 **Konuşan karakter:** portre görselinden otomatik arka plan silme, sese göre çene hareketi, göz kırpma, baş hareketi
- 🧑‍🏫 Kara tahtada anlatımla eşzamanlı beliren maddeler, altyazı, intro/outro, sahne geçişleri, ilerleme çubuğu
- 🎵 Kodla sentezlenen telifsiz fon müziği (konuşmada otomatik kısılır), EBU R128 ses seviyesi
- 🖼️ Otomatik YouTube kapak görseli
- 💸 API anahtarı yok, GPU yok, ücret yok

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
