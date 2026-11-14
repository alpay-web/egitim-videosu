# 🎓 egitim-videosu

**Dokümandan animasyonlu eğitim videosu üreten, tamamen ücretsiz ve açık kaynak bir Claude skill'i.**

Bir eğitim dokümanı ver; Claude onu sahnelere böler, Türkçe nöral sesle seslendirir ve konuşan animasyonlu
bir profesör karakteriyle 1080p MP4 video üretir.

- 🗣️ Türkçe nöral ses: [Piper](https://github.com/rhasspy/piper) — `fahrettin` sesi (CC0, ticari kullanım serbest)
- 👨‍🏫 Özgün, kodla çizilen "Profesör Bilgin": sese göre ağız hareketi, göz kırpma, tahtayı gösteren kol
- 🧑‍🏫 Kara tahta: maddeler anlatımla eşzamanlı kayarak belirir
- 💬 Altyazı, intro/outro kartları, sahne geçişleri, ilerleme çubuğu
- 🎵 Kodla sentezlenen telifsiz fon müziği, konuşmada otomatik kısılır (ducking); EBU R128 ses normalizasyonu
- 💸 API anahtarı yok, GPU yok, ücret yok

## Claude'da kullanım

**claude.ai / Claude uygulaması:** Ayarlar → Capabilities → Skills → bu reponun zip'ini yükle
(ya da sadece `SKILL.md`'yi; kod gerekince repodan otomatik klonlanır). Sonra:
> "Ekteki dokümandan eğitim videosu yap."

**Claude Code:**
```bash
git clone https://github.com/alpay-web/egitim-videosu ~/.claude/skills/egitim-videosu
```

## Elle kullanım
```bash
pip install -r requirements.txt
python scripts/video_uret.py ornek/senaryo_wse_b1.json -o video.mp4
python scripts/video_uret.py ornek/senaryo_wse_b1.json -o deneme.mp4 --sahne 1-2 --cozunurluk 720
```

| Seçenek | Açıklama |
|---|---|
| `--piper-ses fahrettin\|fettah\|dfki` | Ses (dfki ticari kullanıma kapalı) |
| `--hiz 0.95` | Konuşma hızı |
| `--ses edge` | İnternet varsa Microsoft'un ücretsiz nöral sesi (`--edge-ses tr-TR-EmelNeural`) |
| `--muzik-yok` / `--altyazi-yok` / `--intro-outro-yok` | İlgili öğeyi kapatır |
| `--cozunurluk 720` | Daha hızlı render |

Senaryo formatı ve yazım kuralları için `SKILL.md`'ye bak.

## Lisans
Kod: MIT. Ses modelleri kendi lisanslarıyla (fahrettin/fettah: CC0) çalışma anında indirilir.
