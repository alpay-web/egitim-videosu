# Benzer projeler: en çok yıldızlı 100 GitHub deposu (Kasım 2026)

**Yöntem.** GitHub arama API'siyle ~45 sorgu (ör. *explainer video, pdf to video, paper to video, slides to video,
manim, remotion, talking head, ai video generator, document to podcast, whiteboard animation, youtube automation*,
konu etiketleri `video-generation`, `text-to-video`, `manim`, `text-to-speech`, `youtube-automation`) → 700 aday.
Her aday açıklama/konu etiketlerinden ilgi puanı aldı; indirme aracı, proxy, "awesome" listesi, eğitim kodu
depoları gibi alakasızlar elendi; kalan yüksek yıldızlılar + yıldızı biraz düşük ama **bizim işimize en yakın**
olanlar (belge/konu → anlatımlı video) ile 100'lük liste kuruldu. Her deponun README'si indirildi (99/100 + rhubarb
`.adoc`), 27 özellik için tarandı (önizleme, storyboard, altyazı, kelime zamanlaması, önbellek, kalite denetimi,
telaffuz sözlüğü, bölümler, ses normalizasyonu…). En yakın ~25 depo elle okundu.

**Lisans kuralı:** AGPL/GPL (ör. OpenMontage) ve lisanssız depolardan **kod alınmadı**; yalnızca fikirler kendi
kodumuzla uygulandı. Ücretli API isteyen özellikler (ElevenLabs, HeyGen, Kling, Sora…) bilinçli olarak dışarıda.

## 100'lük liste özeti
| Kategori | Depo |
|---|---|
| Belge/konu → anlatımlı video (bize en yakın) | 27 |
| Kısa video / YouTube otomasyonu | 22 |
| Seslendirme / TTS | 22 |
| Programatik animasyon / motion (Manim, Remotion) | 15 |
| Konuşan yüz / avatar / dudak senkronu | 9 |
| Video düzenleme / ajan araçları | 4 |
| Altyazı / çeviri / dublaj | 1 |

README taramasında en sık görülen özellikler (100 depoda): LLM ile senaryo 74, CLI 74, PDF/belge girişi 63,
altyazı 52, çoklu TTS motoru 47, şablon/tema 47, **önizleme/onay** 44, Claude Code/Codex skill'i 43, dikey/shorts 43,
önbellek/devam 31, kalite denetimi 25, telaffuz sözlüğü 25, storyboard 23, ses normalizasyonu 20,
kelime düzeyinde zamanlama 17, bölümler 13, görsel (VLM) denetim 7.

## Bizden iyi yaptıkları ve uyguladıklarımız (v2.1.0)
| Fikir | Kaynak | Bizde |
|---|---|---|
| **Önizleme / onay kapısı**: tam render'dan önce kısa taslak, insan onayı | anything2explainer ("ilk 30 sn", 4 kontrol noktası), vox-director (2 kapı), frametell, OpenMontage (storyboard kapısı), cinecode (yarım boy taslak) | `--onizleme [SN]`, `--onizleme-yaz`; SKILL.md kural 6b: onaysız uzun video yok. Seçki = açılış + her sahne türünden en kısa temsilci + İngilizce geçişli sahne. Önizleme sesleri önbellekle tam videoda yeniden kullanılır |
| **YouTube ses standardı −14 LUFS**, gerçek tepe ≤ −1.5 dBFS | cinecode, ffmpeg-skill | `--lufs` (varsayılan −14; önce −16 idi) |
| **Son dosya denetimi**: LUFS, tepe, sessizlik | explainroo, ffmpeg-skill `check.py` | `yayin_denetimi` → `_denetim.json`; giriş/kapanış/soru bekleme süreleri hariç tutulur, yanlış alarm yok |
| **Bölüm işaretleri dosyanın içinde** | abogen (M4B bölümleri), explainroo (YouTube chapters) | MP4'e chapter gömülür; `--sesli-kitap` ile bölümlü `.m4a` anlatım |
| **Genel + proje telaffuz sözlüğü** | video-podcast-maker (`phonemes.json`), ThioJoe (fonem listesi) | depo kökünde `telaffuz.json`; senaryo sözlüğü onu ezer |
| Süre bütçesi / tahmin | video-podcast-maker (dk başına kelime), mulmocast (`--estimate`) | `sahne_suresi_tahmin`; önizleme ve `--kontrol` tahmini süre verir |

## Zaten bizde olanlar (doğrulandı)
İçerik adresli ses önbelleği (mulmocast, abogen'de de var) · Whisper kalite kapısı + yeniden deneme (TheoremExplainAgent
retry, ThioJoe "two pass") · SRT ≤2×42 karakter (VideoLingo, ffmpeg-skill) · storyboard görseli (OpenMontage contact sheet)
· yerleşim/kapsam/senkron raporu (frametell lint, anything2explainer QC) · kural tabanlı ağız biçimleri (Rhubarb fikri,
modelsiz) · YouTube açıklama/bölüm paketi · CI testleri ve sürümleme.

## Bilerek almadıklarımız
- **Gerçekçi konuşan yüz** (LivePortrait, SadTalker, EchoMimic, Duix-Avatar, LatentSync): GPU ister, render'ı
  saatlerce uzatır; kullanıcının "efor/token/hız" şartına aykırı.
- **Görsel üretim modelleri / video difüzyon** (Kling, Sora, VACE, Wan): ücretli API veya büyük GPU; eğitim tahtası
  için gereksiz.
- **Edge TTS**: kullanıcı lisans nedeniyle reddetti (Chatterbox MIT kalıyor).
- **Remotion/React yığını**: güçlü ama ~2 GB npm bağımlılığı ve ticari kullanımda şirket lisansı koşulları var;
  Pillow+ffmpeg yığınımız hafif ve tamamen serbest.
- **Fon müziği ducking'i**: kullanıcı müzik istemiyor (`--muzik` ile isteğe bağlı duruyor).

## Sonraki adaylar (ileride)
1. Kelime düzeyinde zamanlama ile karaoke altyazı (whisper word timestamps; anything2explainer, explainroo) —
   şu an cümle düzeyi.
2. Bölüm başına ayrı denetim ajanı (anything2explainer: bölüm başına QC) — uzun belgelerde paralel inceleme.
3. Dikey (9:16) kısa kesitler: uzun videodan bölüm bazlı Shorts (AI-Youtube-Shorts-Generator fikri).

## Tam liste (yıldıza göre)
Özellik sütunu README'de geçen anahtar özellikleri gösterir (otomatik tarama; yokluk "özellik yok" demek değildir).

| # | Depo | ⭐ | Lisans | Kategori | Açıklama | README'de geçen özellikler |
|---|---|---|---|---|---|---|
| 1 | [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | 143,801 | MIT | Kısa video / YouTube otomasyonu | 利用 AI 大模型和自动化工作流，根据主题或关键词一键生成高清短视频。Generate HD short videos from a topic or keyword with an automated AI workf | altyazi, onbellek |
| 2 | [3b1b/manim](https://github.com/3b1b/manim) | 96,565 | MIT | Programatik animasyon / motion | Animation engine for explanatory math videos | storyboard |
| 3 | [OpenMontageInc/OpenMontage](https://github.com/OpenMontageInc/OpenMontage) | 80,703 | AGPL-3.0 | Programatik animasyon / motion | World's first open-source, agentic video production system. 12 production pipelines, 100+ tools, 700+ agent sk | onizleme, storyboard, altyazi, kelime-zaman, onbellek, kalite-denetim, ses-normalize |
| 4 | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | 73,432 | NOASSERTION | Programatik animasyon / motion | 🎥      Make videos programmatically with React | altyazi |
| 5 | [RVC-Boss/GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) | 65,196 | MIT | Seslendirme / TTS | 1 min voice data can also be used to train a good TTS model! (few shot voice cloning) | ses-normalize, telaffuz |
| 6 | [coqui-ai/TTS](https://github.com/coqui-ai/TTS) | 46,229 | MPL-2.0 | Seslendirme / TTS | 🐸💬 - a deep learning toolkit for Text-to-Speech, battle-tested in research and production |  |
| 7 | [OpenBMB/VoxCPM](https://github.com/OpenBMB/VoxCPM) | 42,526 | Apache-2.0 | Belge/konu → anlatımlı video (en yakın) | VoxCPM2: Tokenizer-Free TTS for Multilingual Speech Generation, Creative Voice Design, and True-to-Life Clonin | onbellek, ses-normalize |
| 8 | [2noise/ChatTTS](https://github.com/2noise/ChatTTS) | 40,010 | AGPL-3.0 | Seslendirme / TTS | A generative speech model for daily dialogue. | kelime-zaman |
| 9 | [myshell-ai/OpenVoice](https://github.com/myshell-ai/OpenVoice) | 38,261 | MIT | Seslendirme / TTS | Instant voice cloning by MIT and MyShell. Audio foundation model. |  |
| 10 | [babysor/MockingBird](https://github.com/babysor/MockingBird) | 36,865 | NOASSERTION | Seslendirme / TTS | 🚀Clone a voice in 5 seconds to generate arbitrary speech in real-time | onizleme, kalite-denetim |
| 11 | [ATH-MaaS/Pixelle-Video](https://github.com/ATH-MaaS/Pixelle-Video) | 30,127 | Apache-2.0 | Kısa video / YouTube otomasyonu | 🚀 AI 全自动短视频引擎 / AI Fully Automated Short Video Engine |  |
| 12 | [hypit-ai/hypit](https://github.com/hypit-ai/hypit) | 30,003 | NOASSERTION | Kısa video / YouTube otomasyonu | Clone any viral video with AI agents. Not just a script, the whole workflow: swap the face, the words, the B-r | onizleme, altyazi, kelime-zaman |
| 13 | [index-tts/index-tts](https://github.com/index-tts/index-tts) | 25,110 | NOASSERTION | Seslendirme / TTS | An Industrial-Level Controllable and Efficient Zero-Shot Text-To-Speech System | telaffuz |
| 14 | [QwenAudio/CosyVoice](https://github.com/QwenAudio/CosyVoice) | 24,412 | Apache-2.0 | Seslendirme / TTS | Multi-lingual large voice generation model, providing inference, training and deployment full-stack ability. | onbellek, ses-normalize, telaffuz |
| 15 | [HBAI-Ltd/Toonflow-app](https://github.com/HBAI-Ltd/Toonflow-app) | 21,887 | MIT | Kısa video / YouTube otomasyonu | 短剧、漫剧制作工具 Toonflow：开源 AI 视频创作平台，集成剧本创作、智能分镜、角色与场景资产管理、图像生成和视频生成。融合无限画布、AI Agent 与可视化工作流，支持本地部署、自选模型、跨平台客户端、MCP |  |
| 16 | [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | 20,043 | Apache-2.0 | Programatik animasyon / motion | AI video skill for Claude Code & Codex — cinematic, editable product promos with Remotion: 124 shot recipe car | onizleme, storyboard, altyazi, kalite-denetim |
| 17 | [jianchang512/pyvideotrans](https://github.com/jianchang512/pyvideotrans) | 19,753 | GPL-3.0 | Seslendirme / TTS | Translate the video from one language to another and embed dubbing & subtitles. | altyazi, kelime-zaman |
| 18 | [KlingAIResearch/LivePortrait](https://github.com/KlingAIResearch/LivePortrait) | 19,493 | NOASSERTION | Konuşan yüz / avatar / dudak | Bring portraits to life! | onizleme |
| 19 | [Huanshere/VideoLingo](https://github.com/Huanshere/VideoLingo) | 19,269 | Apache-2.0 | Seslendirme / TTS | Netflix-level subtitle cutting, translation, alignment, and even dubbing - one-click fully automated AI video  | altyazi, kelime-zaman, onbellek |
| 20 | [ahmedkhaleel2004/gitdiagram](https://github.com/ahmedkhaleel2004/gitdiagram) | 18,943 | MIT | Belge/konu → anlatımlı video (en yakın) | Visualize any GitHub codebase: free interactive architecture diagrams and one-minute explainer videos. Replace | altyazi, kalite-denetim |
| 21 | [jub0t/Concat](https://github.com/jub0t/Concat) | 17,826 | AGPL-3.0 | Kısa video / YouTube otomasyonu | Beta: The truly free, open-source, local-first, cross-platform video editor. Scriptable through a JSON-RPC API | onizleme, altyazi, ses-normalize, telaffuz |
| 22 | [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) | 16,753 | NOASSERTION | Kısa video / YouTube otomasyonu | A toolbox of film styles made in code for Claude Code: 99 ready to use, and your own. Each style is a style pr | storyboard, altyazi, kalite-denetim, telaffuz |
| 23 | [Zulko/moviepy](https://github.com/Zulko/moviepy) | 15,150 | MIT | Video düzenleme / ajan araçları | Video editing with Python | onizleme |
| 24 | [waooAI/waoowaoo](https://github.com/waooAI/waoowaoo) | 14,865 | NOASSERTION | Kısa video / YouTube otomasyonu | 首家工业级全流程 AI 影视生产平台。Industry-first professional AI Agent platform for controllable film & video production. Fro | onizleme, onbellek |
| 25 | [mozilla/TTS](https://github.com/mozilla/TTS) | 10,187 | MPL-2.0 | Belge/konu → anlatımlı video (en yakın) | :robot: :speech_balloon: Deep learning for Text to Speech  (Discussion forum: https://discourse.mozilla.org/c/ | ses-normalize, telaffuz |
| 26 | [nexu-io/openmotion](https://github.com/nexu-io/openmotion) | 9,998 | Apache-2.0 | Programatik animasyon / motion | The open-source full-stack studio for Opus 5.5 motion video. Reverse engineering for any video. Code video wit | onizleme, altyazi, kalite-denetim |
| 27 | [JuneYaooo/rea-video](https://github.com/JuneYaooo/rea-video) | 9,158 | Apache-2.0 | Kısa video / YouTube otomasyonu | Reverse-engineer any video, shot by shot: filmed, AI-generated or coded, and how to remake it. Breakdowns in t | storyboard, altyazi |
| 28 | [netease-youdao/EmotiVoice](https://github.com/netease-youdao/EmotiVoice) | 8,544 | Apache-2.0 | Programatik animasyon / motion | EmotiVoice 😊: a Multi-Voice and Prompt-Controlled TTS Engine | telaffuz |
| 29 | [RayVentura/ShortGPT](https://github.com/RayVentura/ShortGPT) | 8,174 | MIT | Kısa video / YouTube otomasyonu | 🚀🎬 ShortGPT - Experimental AI framework for youtube shorts / tiktok channel automation | altyazi |
| 30 | [Plachtaa/VALL-E-X](https://github.com/Plachtaa/VALL-E-X) | 7,907 | MIT | Programatik animasyon / motion | An open source implementation of Microsoft's VALL-E X zero-shot TTS model. Demo is available in https://placht | telaffuz |
| 31 | [Osmantic/ODS](https://github.com/Osmantic/ODS) | 7,833 | Apache-2.0 | Seslendirme / TTS | ODS V3 Pre-Release: Public testing and refinement ahead of the official V3 launch. Turn your PC, Mac, or Linux | onizleme, onbellek, kalite-denetim |
| 32 | [dramaclaw/dramaclaw](https://github.com/dramaclaw/dramaclaw) | 7,717 | NOASSERTION | Seslendirme / TTS | A general-purpose AIGC video engine: script to finished film in one pipeline — dramas, ads, product videos, ot | onizleme, storyboard, altyazi, bolumler, onbellek, kalite-denetim |
| 33 | [OpenTalker/video-retalking](https://github.com/OpenTalker/video-retalking) | 7,307 | Apache-2.0 | Konuşan yüz / avatar / dudak | [SIGGRAPH Asia 2022] VideoReTalking: Audio-based Lip Synchronization for Talking Head Video Editing In the Wil |  |
| 34 | [Forget-C/Jellyfish](https://github.com/Forget-C/Jellyfish) | 7,189 | Apache-2.0 | Kısa video / YouTube otomasyonu | An end-to-end production workspace for AI-generated short dramas. From script input to structured storyboardin | onizleme, storyboard, bolumler, onbellek |
| 35 | [ArcReel/ArcReel](https://github.com/ArcReel/ArcReel) | 6,563 | AGPL-3.0 | Kısa video / YouTube otomasyonu | AI Agent 驱动的开源可自部署视频工作台：将小说与剧本转为角色、场景、道具资产、分镜、视频和剪映草稿，支持跨镜头一致性、多供应商与费用追踪 / Self-hosted AI video workspace for  |  |
| 36 | [modelscope/FunClip](https://github.com/modelscope/FunClip) | 6,562 | MIT | Konuşan yüz / avatar / dudak | FunASR-powered video transcription, subtitle generation, and LLM-assisted clipping tool with a local Gradio UI | altyazi, ses-normalize, telaffuz |
| 37 | [joeseesun/qiaomu-anything-to-notebooklm](https://github.com/joeseesun/qiaomu-anything-to-notebooklm) | 6,516 | MIT | Belge/konu → anlatımlı video (en yakın) | Claude Skill: Multi-source content processor for NotebookLM. Supports WeChat articles, web pages, YouTube, PDF | onbellek, kalite-denetim |
| 38 | [kaomei/stickman-video-director](https://github.com/kaomei/stickman-video-director) | 6,444 | MIT | Belge/konu → anlatımlı video (en yakın) | Turn any script into viral, multi-style animated stickman videos for Faceless YouTube Channels. Automate visua | onizleme, storyboard, altyazi |
| 39 | [bytedance/LatentSync](https://github.com/bytedance/LatentSync) | 6,286 | Apache-2.0 | Konuşan yüz / avatar / dudak | Taming Stable Diffusion for Lip Sync! |  |
| 40 | [denizsafak/abogen](https://github.com/denizsafak/abogen) | 6,234 | MIT | Belge/konu → anlatımlı video (en yakın) | Generate audiobooks from EPUBs, PDFs and text with synchronized captions. | onizleme, altyazi, kelime-zaman, bolumler, onbellek, ses-normalize |
| 41 | [netease-youdao/LobsterAI](https://github.com/netease-youdao/LobsterAI) | 6,189 | MIT | Video düzenleme / ajan araçları | Open-source, desktop-grade AI agent that gets real work done — data analysis, slides, docs, video & web resear | onizleme, onbellek |
| 42 | [Anil-matcha/AI-Youtube-Shorts-Generator](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator) | 6,108 | MIT | Kısa video / YouTube otomasyonu | Open-source alternative to Opus Clip, Vidyo.ai, Klap & SubMagic. Turn long-form YouTube videos into viral 9:16 | altyazi, onbellek |
| 43 | [kajisho5/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) | 5,956 | MIT | Seslendirme / TTS | Local video editor for coding agents: 42 FFmpeg tools with a machine-readable contract and an MCP server, for  | onizleme, storyboard, altyazi, bolumler, onbellek, kalite-denetim, ses-normalize |
| 44 | [liuzhao1225/YouDub-webui](https://github.com/liuzhao1225/YouDub-webui) | 5,848 | Apache-2.0 | Belge/konu → anlatımlı video (en yakın) | Open-source AI video localization and dubbing for YouTube/Bilibili: speech recognition, subtitle translation,  | altyazi |
| 45 | [remsky/Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) | 5,686 | Apache-2.0 | Seslendirme / TTS | Dockerized OpenAI-compatible wrapper for Kokoro-82M text-to-speech w/multiplatform CPU, AMD, NVIDIA GPU PyTorc | altyazi, kelime-zaman, ses-normalize, telaffuz |
| 46 | [geeklee/srt-whiteboard-animation](https://github.com/geeklee/srt-whiteboard-animation) | 5,616 | MIT | Altyazı / çeviri / dublaj | 将 SRT 字幕做成暖米黄纸张底的流式笔迹白板手绘动画 skill：mask 分区遮罩编排 + stream 连续笔迹（ink→color）。 | onizleme, altyazi |
| 47 | [darkzOGx/youtube-automation-agent](https://github.com/darkzOGx/youtube-automation-agent) | 5,226 | MIT | Kısa video / YouTube otomasyonu | 🎬 Open-source, self-hosted AI agent that runs a YouTube channel end to end: researches topics, writes scripts, | onizleme, altyazi, onbellek, kalite-denetim |
| 48 | [MoonInTheRiver/DiffSinger](https://github.com/MoonInTheRiver/DiffSinger) | 4,901 | MIT | Seslendirme / TTS | DiffSinger: Singing Voice Synthesis via Shallow Diffusion Mechanism (SVS & TTS); AAAI 2022; Official code | ses-normalize |
| 49 | [OpenMOSS/MOSS-TTS-Nano](https://github.com/OpenMOSS/MOSS-TTS-Nano) | 4,685 | Apache-2.0 | Seslendirme / TTS | A 100M-parameter multilingual TTS model for real-time CPU inference, voice cloning, and 48 kHz stereo generati | onbellek, telaffuz |
| 50 | [antgroup/echomimic_v2](https://github.com/antgroup/echomimic_v2) | 4,678 | Apache-2.0 | Konuşan yüz / avatar / dudak | [CVPR 2025] EchoMimicV2: Towards Striking, Simplified, and Semi-Body Human Animation | ses-normalize, telaffuz |
| 51 | [tmoroney/auto-subs](https://github.com/tmoroney/auto-subs) | 4,568 | MIT | Seslendirme / TTS | On-device subtitle generation that connects directly to DaVinci Resolve, Premiere, and After Effects. | onizleme, altyazi, kelime-zaman, ses-normalize |
| 52 | [OpenMOSS/MOSS-TTS](https://github.com/OpenMOSS/MOSS-TTS) | 4,330 | Apache-2.0 | Seslendirme / TTS | An open-source model family for long-form speech, dialogue synthesis, voice design, sound effects, and real-ti | onizleme, onbellek, telaffuz |
| 53 | [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills) | 4,295 | MIT | Kısa video / YouTube otomasyonu | AI 短剧与漫剧制作 skill 合集：小说改剧本、角色设定三视图、分镜脚本、生图/生视频提示词与成片审片，适配 Claude Code / Codex 等 ｜ Open-source agent skills for  | storyboard |
| 54 | [0xShug0/audio.cpp](https://github.com/0xShug0/audio.cpp) | 4,262 | NOASSERTION | Seslendirme / TTS | An all-in-one, pure C++ inference engine for audio models, powered by ggml. Supports TTS, STT, VAD, voice conv | onizleme, storyboard, altyazi, kelime-zaman, onbellek, kalite-denetim, ses-normalize |
| 55 | [metavoiceio/metavoice-src](https://github.com/metavoiceio/metavoice-src) | 4,201 | Apache-2.0 | Seslendirme / TTS | Foundational model for human-like, expressive TTS | altyazi, kalite-denetim |
| 56 | [GVCLab/PersonaLive](https://github.com/GVCLab/PersonaLive) | 4,156 | Apache-2.0 | Konuşan yüz / avatar / dudak | [CVPR 2026] PersonaLive! : Expressive Portrait Image Animation for Live Streaming | ses-normalize |
| 57 | [IAHispano/Applio](https://github.com/IAHispano/Applio) | 4,013 | MIT | Seslendirme / TTS | A simple, high-quality voice conversion tool focused on ease of use and performance. |  |
| 58 | [Vincentwei1021/anything2explainer](https://github.com/Vincentwei1021/anything2explainer) | 3,337 | NOASSERTION | Belge/konu → anlatımlı video (en yakın) | Topic in, narrated explainer video out. A Claude Code / Codex skill that turns any topic into a black-canvas m | onizleme, storyboard, altyazi, kelime-zaman, bolumler, kalite-denetim, telaffuz |
| 59 | [cporter202/automate-faceless-content](https://github.com/cporter202/automate-faceless-content) | 3,300 | — | Belge/konu → anlatımlı video (en yakın) | Learn how to automate faceless short-form + long-form video content and dominate YouTube, TikTok, Facebook & I |  |
| 60 | [NarratorAI-Studio/narrator-ai-cli-skill](https://github.com/NarratorAI-Studio/narrator-ai-cli-skill) | 3,296 | MIT | Kısa video / YouTube otomasyonu | AI 解说大师 — Agent skill；封装 narrator-ai-cli 供 Claude/Codex 等工具调用 | onizleme, kalite-denetim |
| 61 | [0xsline/OpenChatCut](https://github.com/0xsline/OpenChatCut) | 3,130 | AGPL-3.0 | Programatik animasyon / motion | Open-source, local-first conversational AI video editor with a professional multi-track timeline, Agent Skills | onizleme, altyazi, kelime-zaman, onbellek, kalite-denetim, telaffuz |
| 62 | [dmtrKovalenko/fframes](https://github.com/dmtrKovalenko/fframes) | 3,112 | MIT | Programatik animasyon / motion | programmatic video rendering framework that is actually fast | onizleme, altyazi, bolumler, onbellek |
| 63 | [oil-oil/oil-motion](https://github.com/oil-oil/oil-motion) | 2,918 | MIT | Programatik animasyon / motion | Web animation skill for Claude Code & Codex. 帮你做跟着滚动和鼠标动的网页动画。 |  |
| 64 | [Alisa0808/vox-director](https://github.com/Alisa0808/vox-director) | 2,871 | MIT | Belge/konu → anlatımlı video (en yakın) | Turn one topic into a finished Vox-style paper-collage explainer/ad video — automated end to end on Atlas Clou | onizleme, altyazi |
| 65 | [nateherkai/herk-edit-kit](https://github.com/nateherkai/herk-edit-kit) | 2,864 | NOASSERTION | Kısa video / YouTube otomasyonu | Herk Edit Kit by Nate Herk: edit videos, reels, and YouTube Shorts with Codex or Claude Code. 15 skills, trans | onizleme, storyboard, altyazi, kelime-zaman, bolumler, onbellek, kalite-denetim |
| 66 | [DanielSWolf/rhubarb-lip-sync](https://github.com/DanielSWolf/rhubarb-lip-sync) | 2,774 | NOASSERTION | Konuşan yüz / avatar / dudak | Rhubarb Lip Sync is a command-line tool that automatically creates 2D mouth animation from voice recordings. Y | telaffuz |
| 67 | [academa-labs/manimgx](https://github.com/academa-labs/manimgx) | 2,756 | MIT | Programatik animasyon / motion | The animation engine for agents: blazingly fast math and 3D videos with Manim's Python API, on a Rust GPU core | storyboard, telaffuz |
| 68 | [alchaincyf/huashu-motion](https://github.com/alchaincyf/huashu-motion) | 2,741 | MIT | Belge/konu → anlatımlı video (en yakın) | 让你的agent一键直出商业级产品宣传片：会作曲，能指着画面改。Commercial-grade launch films by your coding agent — point at the frame to cha |  |
| 69 | [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) | 2,584 | MIT | Kısa video / YouTube otomasyonu | Make videos with Claude Code: script, AI voiceover, music, video clips and render, on open-source models that  | onizleme, storyboard, altyazi, onbellek |
| 70 | [shinyobjectz/raea](https://github.com/shinyobjectz/raea) | 2,563 | NOASSERTION | Programatik animasyon / motion | Render Anything Engine: tell your AI what to make. Videos, motion graphics, 3D and games as React and TypeScri |  |
| 71 | [sarpstar/cinecode](https://github.com/sarpstar/cinecode) | 2,555 | MIT | Belge/konu → anlatımlı video (en yakın) | Films made with code. Short films, long YouTube videos, ads, explainers and music videos: an AI coding agent w | altyazi, ses-normalize |
| 72 | [xuanyustudio/LocalMiniDrama](https://github.com/xuanyustudio/LocalMiniDrama) | 2,452 | MIT | Kısa video / YouTube otomasyonu | 🎬 seedance2接入  开源本地 AI 短剧 & 漫剧生成工具 —— 从故事到成片一站式完成，数据不出本机，短剧工作流管理平台，高灵活度，AI真人剧，AI漫剧本地搞定。 Open-source local AI s | storyboard |
| 73 | [rushindrasinha/youtube-shorts-pipeline](https://github.com/rushindrasinha/youtube-shorts-pipeline) | 2,375 | MIT | Kısa video / YouTube otomasyonu | Automated YouTube Shorts pipeline: news → script → AI visuals → voiceover → captions → upload | altyazi, kelime-zaman, onbellek, telaffuz |
| 74 | [walterlow/freecut](https://github.com/walterlow/freecut) | 2,330 | MIT | Video düzenleme / ajan araçları | FreeCut is a professional-grade video editor that runs entirely in your browser. Professional video editing, z | onizleme, altyazi, onbellek, kalite-denetim |
| 75 | [Hao0321/video-autopilot-kit](https://github.com/Hao0321/video-autopilot-kit) | 2,320 | MIT | Kısa video / YouTube otomasyonu | Fill-in-your-own-data framework for YouTube / short-form video automation: CapCut JSON + ffmpeg tooling + an o | onizleme, altyazi, onbellek, ses-normalize |
| 76 | [trykimu/videoeditor](https://github.com/trykimu/videoeditor) | 2,304 | NOASSERTION | Programatik animasyon / motion | Your Creative Copilot for Video Editing | onizleme |
| 77 | [bangtutorial/bang-motion](https://github.com/bangtutorial/bang-motion) | 2,231 | MIT | Belge/konu → anlatımlı video (en yakın) | Agent skill for browser motion graphics — openers, promos, bumpers, kinetic typography, and five explainer sty | onizleme, altyazi, onbellek |
| 78 | [CaviraOSS/PageLM](https://github.com/CaviraOSS/PageLM) | 2,069 | NOASSERTION | Belge/konu → anlatımlı video (en yakın) | PageLM is a community driven version of NotebookLM & a education platform that transforms study materials into |  |
| 79 | [HKUDS/VideoAgent](https://github.com/HKUDS/VideoAgent) | 2,049 | MIT | Belge/konu → anlatımlı video (en yakın) | [EMNLP2026] "VideoAgent: All-in-One Agentic Framework for Video Understanding and Editing, and Remaking" | storyboard, altyazi, kalite-denetim |
| 80 | [nazdridoy/kokoro-tts](https://github.com/nazdridoy/kokoro-tts) | 2,019 | MIT | Belge/konu → anlatımlı video (en yakın) | A CLI text-to-speech tool using the Kokoro model, supporting multiple languages, voices (with blending), and v | onizleme, bolumler |
| 81 | [andyhuo520/digital-human-koubo](https://github.com/andyhuo520/digital-human-koubo) | 1,995 | MIT | Konuşan yüz / avatar / dudak | AI digital-human talking-head videos from one photo: Renoise MCP generation + 5 editing styles + 48 creator-gr | onizleme, altyazi, kelime-zaman, bolumler, onbellek, kalite-denetim, ses-normalize, telaffuz |
| 82 | [LingyiChen-AI/AIComicBuilder](https://github.com/LingyiChen-AI/AIComicBuilder) | 1,970 | Apache-2.0 | Video düzenleme / ajan araçları |   AI-powered animated comic generator — transform scripts into fully animated videos with AI-driven character  | onizleme, storyboard |
| 83 | [bugbakery/audapolis](https://github.com/bugbakery/audapolis) | 1,908 | AGPL-3.0 | Seslendirme / TTS | an editor for spoken-word audio with automatic transcription |  |
| 84 | [veedstudio/open-edit](https://github.com/veedstudio/open-edit) | 1,808 | Apache-2.0 | Programatik animasyon / motion | Open-source, agent-driven editing pipeline: create subtitles, motion graphics, slides, edit and render videos. | onizleme, storyboard, altyazi, kelime-zaman, onbellek, ses-normalize, telaffuz |
| 85 | [ThioJoe/Auto-Synced-Translated-Dubs](https://github.com/ThioJoe/Auto-Synced-Translated-Dubs) | 1,755 | AGPL-3.0 | Seslendirme / TTS | Automatically translates the text of a video based on a subtitle file, and then uses AI voice services to crea | altyazi, telaffuz |
| 86 | [Agents365-ai/video-podcast-maker](https://github.com/Agents365-ai/video-podcast-maker) | 1,723 | MIT | Belge/konu → anlatımlı video (en yakın) | Topic → 4K narrated video for coding agents. v5.3.0: local TTS (edge free + azure, no external engine), manife | onizleme, altyazi, bolumler, telaffuz |
| 87 | [DozenTwelve/Papermorph](https://github.com/DozenTwelve/Papermorph) | 1,720 | MIT | Belge/konu → anlatımlı video (en yakın) | An AI skill that turns books into animated, narrated, interactive web experiences | onizleme, storyboard, altyazi, bolumler |
| 88 | [met4citizen/TalkingHead](https://github.com/met4citizen/TalkingHead) | 1,676 | MIT | Konuşan yüz / avatar / dudak | Talking Head (3D): A JavaScript class for real-time lip-sync using full-body 3D avatars. | altyazi, kelime-zaman, ses-normalize, telaffuz |
| 89 | [iart-ai/motion-skills](https://github.com/iart-ai/motion-skills) | 1,587 | MIT | Belge/konu → anlatımlı video (en yakın) | 56 open-source skills that teach your AI coding agent to make motion graphics, animation & video — kinetic typ |  |
| 90 | [TIGER-AI-Lab/TheoremExplainAgent](https://github.com/TIGER-AI-Lab/TheoremExplainAgent) | 1,515 | MIT | Belge/konu → anlatımlı video (en yakın) | Official Repo for "TheoremExplainAgent: Towards Video-based Multimodal Explanations for LLM Theorem Understand | storyboard, altyazi |
| 91 | [vincentsch/explainroo](https://github.com/vincentsch/explainroo) | 1,322 | MIT | Belge/konu → anlatımlı video (en yakın) | Explainer videos and product demos made by your AI agent. Free and open source: a local voice (Kokoro), word t | altyazi, bolumler, onbellek, telaffuz |
| 92 | [haidrrrry/claude-remotion-skill](https://github.com/haidrrrry/claude-remotion-skill) | 1,036 | MIT | Kısa video / YouTube otomasyonu | Open-source Claude agent skill that teaches Claude Code, Claude Desktop & Claude AI to create and edit profess | altyazi |
| 93 | [jeertmans/manim-slides](https://github.com/jeertmans/manim-slides) | 988 | MIT | Programatik animasyon / motion | Tool for live presentations using manim |  |
| 94 | [FelippeChemello/podcast-maker](https://github.com/FelippeChemello/podcast-maker) | 712 | MIT | Belge/konu → anlatımlı video (en yakın) | Fully automated video maker using motion graphics and text-to-speech synthesis to turn newsletters into daily  |  |
| 95 | [lukaszliniewicz/Pandrator](https://github.com/lukaszliniewicz/Pandrator) | 649 | MIT | Belge/konu → anlatımlı video (en yakın) | Turn PDFs and EPUBs into audiobooks; subtitles or videos into dubbed videos (including translation), and more. | onizleme, altyazi, kelime-zaman, bolumler, onbellek, kalite-denetim, telaffuz |
| 96 | [kurbaitaev/ghost-editor](https://github.com/kurbaitaev/ghost-editor) | 558 | MIT | Kısa video / YouTube otomasyonu | Raw talking-head take in, finished reel out. Open-source AI video editor for Claude Code. | onizleme, altyazi, kalite-denetim |
| 97 | [sitor-ai/frametell](https://github.com/sitor-ai/frametell) | 504 | AGPL-3.0 | Belge/konu → anlatımlı video (en yakın) | Frametell: turn your ideas and material into vivid explainer videos with an AI director agent. Local-first, an | onizleme, storyboard, altyazi, kalite-denetim |
| 98 | [Wing900/ManimCat](https://github.com/Wing900/ManimCat) | 502 | AGPL-3.0 | Belge/konu → anlatımlı video (en yakın) | EN: ManimCat: AI-generated math animations from natural language. High-quality Manim rendering with LaTeX supp | onizleme, storyboard, altyazi, kalite-denetim |
| 99 | [hi-nikola/hand-drawn-explainer-video-nikola](https://github.com/hi-nikola/hand-drawn-explainer-video-nikola) | 487 | Apache-2.0 | Belge/konu → anlatımlı video (en yakın) | 中文手绘知识讲解视频 Codex Skill：逐笔故事、双语义岛、让怪诞小黑动起来与程序动画 | onizleme |
| 100 | [receptron/mulmocast-cli](https://github.com/receptron/mulmocast-cli) | 482 | AGPL-3.0 | Belge/konu → anlatımlı video (en yakın) | AI-powered podcast & video generator. | onizleme, altyazi, onbellek, kalite-denetim |
