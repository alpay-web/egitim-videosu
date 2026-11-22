# Teknik terim telaffuzu: 100 depo araştırması (2026-11)

**Sorun:** BA serisi önizlemesinde *include, aggregation, sequence* gibi teknik terimler kötü okundu. Eski yöntem
`{terim}` → CMU sözlüğü (ARPAbet) → Türk harfleri idi: Amerikan ünlüleri (`opt → apt`, `backlog → beklag`,
`composition → kampızişın`) ve `W → v` (`sequence → sikvıns`, `query → kviri`) Türk BT ekiplerinin söylediğinden uzaktı.

GitHub'da G2P, fonem sözlüğü, metin normalleştirme, kod geçişi (code-switching) ve Türkçe TTS konularında 458 depo
tarandı; 253'ü ilgili çıktı, en çok yıldızlı 100'ü aşağıda.

## Uygulananlar (yalnız fikir; GPL/AGPL kod kopyalanmadı)
| Fikir | Kaynak | Bizde |
|---|---|---|
| Altın sözlük önce, G2P yedek | hexgrad/misaki (Apache), rhasspy/gruut (MIT) | `teknik_terimler.json` (~400 terim, Türk BT okunuşu) → bulunamazsa CMU |
| En uzun öbek eşleşmesi | NVIDIA/NeMo-text-processing (Apache) WFST sözlükleri | "state machine", "use case", "sequence diagram" tek parça aranır |
| ARPAbet eşleme düzeltmesi | Kyubyong/g2p, CharsiuG2P | yeni modda `W → u` (sikuıns, kuiri, uindou) |
| Aday üret + Whisper ile seç | petermg/Chatterbox-TTS-Extended (MIT) | zaten vardı (`kalite` girdisi, cümle başına 3 deneme) |
| Terimi ayrı dil parçası olarak söyletmek | Chatterbox kod geçişi tartışmaları, gentaiscool/code-switching-papers | `ingilizce_mod: "ayri"` seçeneği (A/B'de denendi) |
| Kısaltmayı harf harf açma | WeTextProcessing, NeMo TN | senaryo `telaffuz` sözlüğü (SQL → "es kyu el") |

Kullanım: senaryoda `"ingilizce_mod": "sozluk"` (yeni senaryolar), `"cmu"` (eski davranış, varsayılan; eski
videoların önbellek sesi bozulmasın diye), `"ayri"`. Senaryoya özel ek: `"teknik_terimler": {"terim": "okunuş"}`.

## A/B testi
`senaryolar/ab/telaffuz_{A,B,C}.json`: aynı 6 cümle; A = eski CMU, B = sözlük, C = ayrı İngilizce parça.

## En çok yıldızlı 100 ilgili depo
| # | Depo | ★ | Lisans | Ne işe yarar |
|---|---|---|---|---|
| 1 | [OpenBMB/VoxCPM](https://github.com/OpenBMB/VoxCPM) | 42873 | Apache-2.0 | VoxCPM2: Tokenizer-Free TTS for Multilingual Speech Generation, Creative Voice Design, and True-to-Life Clonin |
| 2 | [resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox) | 28033 | MIT | SoTA open-source TTS |
| 3 | [supertone-oss-archive/supertonic](https://github.com/supertone-oss-archive/supertonic) | 13752 | MIT | Lightning-Fast, On-Device, Multilingual TTS — running natively via ONNX. |
| 4 | [abus-aikorea/voice-pro](https://github.com/abus-aikorea/voice-pro) | 13465 | GPL-3.0 | Gradio WebUI for creators and developers, featuring key TTS (Edge-TTS, kokoro) and zero-shot Voice Cloning (E2 |
| 5 | [PaddlePaddle/PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech) | 12713 | Apache-2.0 | Easy-to-use Speech Toolkit including Self-Supervised Learning model, SOTA/Streaming ASR with punctuation, Stre |
| 6 | [Zyphra/Zonos](https://github.com/Zyphra/Zonos) | 7250 | Apache-2.0 | Zonos-v0.1 is a leading open-weight text-to-speech model trained on more than 200k hours of varied multilingua |
| 7 | [remsky/Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) | 5718 | Apache-2.0 | Dockerized OpenAI-compatible wrapper for Kokoro-82M text-to-speech w/multiplatform CPU, AMD, NVIDIA GPU PyTorc |
| 8 | [OpenMOSS/MOSS-TTS-Nano](https://github.com/OpenMOSS/MOSS-TTS-Nano) | 4709 | Apache-2.0 | A 100M-parameter multilingual TTS model for real-time CPU inference, voice cloning, and 48 kHz stereo generati |
| 9 | [jhaizhou-ops/S2Arm](https://github.com/jhaizhou-ops/S2Arm) | 3803 | Apache-2.0 | Run your own Switch games natively on iPhone, iPad and Mac: game code rewritten to ARM64, graphics direct to M |
| 10 | [havenicec/google-qr-sms-helper](https://github.com/havenicec/google-qr-sms-helper) | 2698 | MIT | Chrome Extension (MV3) to switch Google's mandatory QR code verification back to standard 6-digit SMS verifica |
| 11 | [antvis/G2Plot](https://github.com/antvis/G2Plot) | 2656 | MIT | :dango:  An interactive and responsive charting library based on G2. |
| 12 | [marytts/marytts](https://github.com/marytts/marytts) | 2580 | NOASSERTION | MARY TTS -- an open-source, multilingual text-to-speech synthesis system written in pure java |
| 13 | [FireRedTeam/FireRedTTS3](https://github.com/FireRedTeam/FireRedTTS3) | 1724 | Apache-2.0 | FireRedTTS3: Multilingual and Multi-Dialect Voice Cloning with Instruction-Guided Voice Design and Speech Edit |
| 14 | [bootphon/phonemizer](https://github.com/bootphon/phonemizer) | 1580 | GPL-3.0 | Simple text to phones converter for multiple languages |
| 15 | [devnen/Chatterbox-TTS-Server](https://github.com/devnen/Chatterbox-TTS-Server) | 1517 | MIT | Self-host the powerful Chatterbox TTS model. This server offers a user-friendly Web UI, flexible API endpoints |
| 16 | [OpenMOSS/MOSS-TTSD](https://github.com/OpenMOSS/MOSS-TTSD) | 1425 | Apache-2.0 | A multilingual model for long-form, multi-speaker dialogue synthesis with flexible speaker control and zero-sh |
| 17 | [diodiogod/TTS-Audio-Suite](https://github.com/diodiogod/TTS-Audio-Suite) | 1270 | NOASSERTION | A ComfyUI custom node integration for local multi-engine multi-language Text-to-Speech and Voice Conversion. S |
| 18 | [jfilter/clean-text](https://github.com/jfilter/clean-text) | 1031 | NOASSERTION | 🧹 Python package for text cleaning |
| 19 | [Kyubyong/g2p](https://github.com/Kyubyong/g2p) | 938 | Apache-2.0 | g2p: English Grapheme To Phoneme Conversion |
| 20 | [netease-youdao/Confucius4-TTS](https://github.com/netease-youdao/Confucius4-TTS) | 861 | NOASSERTION | Confucius4-TTS: a Multilingual and Cross-Lingual Zero-Shot TTS Engine |
| 21 | [Tomiinek/Multilingual_Text_to_Speech](https://github.com/Tomiinek/Multilingual_Text_to_Speech) | 843 | MIT | An implementation of Tacotron 2 that supports multilingual experiments with parameter-sharing, code-switching, |
| 22 | [wenet-e2e/WeTextProcessing](https://github.com/wenet-e2e/WeTextProcessing) | 843 | Apache-2.0 | Text Normalization & Inverse Text Normalization |
| 23 | [cmusphinx/cmudict](https://github.com/cmusphinx/cmudict) | 834 | NOASSERTION | CMU US English Dictionary |
| 24 | [open-dict-data/ipa-dict](https://github.com/open-dict-data/ipa-dict) | 827 | MIT | Monolingual wordlists with pronunciation information in IPA |
| 25 | [CrispStrobe/CrispASR](https://github.com/CrispStrobe/CrispASR) | 826 | MIT | C++ ggml runtime hub for multilingual ASR and TTS models: Cohere Transcribe, Parakeet TDT, Voxtral, Canary 1B  |
| 26 | [speechio/chinese_text_normalization](https://github.com/speechio/chinese_text_normalization) | 745 | MIT | Chinese text normalization for speech processing |
| 27 | [FireRedTeam/FireRedASR2S](https://github.com/FireRedTeam/FireRedASR2S) | 744 | Apache-2.0 | A SOTA Industrial-Grade All-in-One ASR system with ASR, VAD, LID, and Punc modules. FireRedASR2 supports Chine |
| 28 | [travisvn/chatterbox-tts-api](https://github.com/travisvn/chatterbox-tts-api) | 700 | AGPL-3.0 | Local, OpenAI-compatible text-to-speech (TTS) API using Chatterbox, enabling users to generate voice cloned sp |
| 29 | [cmusphinx/g2p-seq2seq](https://github.com/cmusphinx/g2p-seq2seq) | 682 | NOASSERTION | G2P with Tensorflow |
| 30 | [foreveryh/claude-code-switch](https://github.com/foreveryh/claude-code-switch) | 670 | MIT | One-command model switcher for Claude Code (Only for Anthropic API). |
| 31 | [inclusionAI/Ming-3.0-tts](https://github.com/inclusionAI/Ming-3.0-tts) | 622 | MIT | Ming-3.0-tts is an open-source TTS model family with 0.5B dense and 7.9B-A1.3B MoE variants, supporting multil |
| 32 | [PunithVT/ai-avatar-system](https://github.com/PunithVT/ai-avatar-system) | 587 | MIT | 🎭 AI Avatar / digital human platform — upload a photo, clone a voice, talk to any face in real time with lip-s |
| 33 | [petermg/Chatterbox-TTS-Extended](https://github.com/petermg/Chatterbox-TTS-Extended) | 581 | MIT | Modified version of Chatterbox that accepts text files as input and no character restrictions. I use it to mak |
| 34 | [Saganaki22/ComfyUI-OmniVoice-TTS](https://github.com/Saganaki22/ComfyUI-OmniVoice-TTS) | 567 | Apache-2.0 | OmniVoice TTS nodes for ComfyUI - Zero-shot multilingual text-to-speech with voice cloning, voice design, and  |
| 35 | [hexgrad/misaki](https://github.com/hexgrad/misaki) | 525 | Apache-2.0 | G2P |
| 36 | [AdolfVonKleist/Phonetisaurus](https://github.com/AdolfVonKleist/Phonetisaurus) | 521 | BSD-3-Clause | Phonetisaurus G2P |
| 37 | [NVIDIA/NeMo-text-processing](https://github.com/NVIDIA/NeMo-text-processing) | 518 | Apache-2.0 | NeMo text processing for ASR and TTS |
| 38 | [axelspringer/DeepPhonemizer](https://github.com/axelspringer/DeepPhonemizer) | 437 | MIT | Grapheme to phoneme conversion with deep learning. |
| 39 | [GitYCC/g2pW](https://github.com/GitYCC/g2pW) | 423 | Apache-2.0 | Chinese Mandarin Grapheme-to-Phoneme Converter. 中文轉注音或拼音 (INTERSPEECH 2022) |
| 40 | [alphacep/awesome-russian-speech](https://github.com/alphacep/awesome-russian-speech) | 418 | Apache-2.0 | Russian speech technology links |
| 41 | [open-speech/speech-aligner](https://github.com/open-speech/speech-aligner) | 411 | NOASSERTION | speech-aligner，是一个从“人声语音”及其“语言文本”，产生音素级别时间对齐标注的工具。speech-aligner, is a tool that generate phoneme-level alignm |
| 42 | [g2p/blocks](https://github.com/g2p/blocks) | 399 | GPL-3.0 | Enable bcache or LVM on existing block devices |
| 43 | [lingjzhu/CharsiuG2P](https://github.com/lingjzhu/CharsiuG2P) | 398 | MIT | Multilingual G2P in 100 languages |
| 44 | [vlomme/Multi-Tacotron-Voice-Cloning](https://github.com/vlomme/Multi-Tacotron-Voice-Cloning) | 396 | NOASSERTION | Phoneme multilingual(Russian-English) voice cloning based on |
| 45 | [randombk/chatterbox-vllm](https://github.com/randombk/chatterbox-vllm) | 386 | MIT | VLLM Port of the Chatterbox TTS model |
| 46 | [CUNY-CL/wikipron](https://github.com/CUNY-CL/wikipron) | 376 | Apache-2.0 | Massively multilingual pronunciation mining |
| 47 | [zszszszsz/.config](https://github.com/zszszszsz/.config) | 371 | MIT | # # Automatically generated file; DO NOT EDIT. # OpenWrt Configuration # CONFIG_MODULES=y CONFIG_HAVE_DOT_CONF |
| 48 | [kakaobrain/g2pm](https://github.com/kakaobrain/g2pm) | 369 | Apache-2.0 | A Neural Grapheme-to-Phoneme Conversion Package for Mandarin Chinese Based on a New Open Benchmark Dataset |
| 49 | [Xerophayze/TTS-Story](https://github.com/Xerophayze/TTS-Story) | 365 | NOASSERTION | TTS-Story is a web-based multi‑voice TTS studio for turning tagged scripts into audiobooks—featuring full spea |
| 50 | [VinAIResearch/XPhoneBERT](https://github.com/VinAIResearch/XPhoneBERT) | 358 | MIT | XPhoneBERT: A Pre-trained Multilingual Model for Phoneme Representations for Text-to-Speech (INTERSPEECH 2023) |
| 51 | [gentaiscool/code-switching-papers](https://github.com/gentaiscool/code-switching-papers) | 350 | Apache-2.0 | A curated list of research papers and resources on code-switching |
| 52 | [dmort27/panphon](https://github.com/dmort27/panphon) | 342 | MIT | Python package and data files for manipulating phonological segments (phones, phonemes) in terms of universal  |
| 53 | [rhasspy/gruut](https://github.com/rhasspy/gruut) | 332 | MIT | A tokenizer, text cleaner, and phonemizer for many human languages. |
| 54 | [g2p/bedup](https://github.com/g2p/bedup) | 328 | GPL-2.0 | Btrfs deduplication |
| 55 | [Aratako/T5Gemma-TTS](https://github.com/Aratako/T5Gemma-TTS) | 316 | MIT | Multilingual TTS model with voice cloning and duration control, based on T5Gemma encoder-decoder LLM |
| 56 | [canberk7/ema-lightning](https://github.com/canberk7/ema-lightning) | 308 | Apache-2.0 | Tiny, fast and accurate Turkish text-to-speech. 8.6M parameters, 0.92% WER on Freya-TR-Eval, first audio in ~4 |
| 57 | [ikegami-yukino/neologdn](https://github.com/ikegami-yukino/neologdn) | 290 | Apache-2.0 | Japanese text normalizer for mecab-neologd |
| 58 | [makerjackie/MTTS](https://github.com/makerjackie/MTTS) | 284 | MIT | A Demo of Mandarin/Chinese TTS frontend |
| 59 | [Kyubyong/g2pK](https://github.com/Kyubyong/g2pK) | 275 | Apache-2.0 | g2pK: g2p module for Korean |
| 60 | [yl4579/PL-BERT](https://github.com/yl4579/PL-BERT) | 270 | MIT | Phoneme-Level BERT for Enhanced Prosody of Text-to-Speech with Grapheme Predictions |
| 61 | [Alexir/CMUdict](https://github.com/Alexir/CMUdict) | 258 | BSD-3-Clause | CMUdict maintenance, and tools |
| 62 | [thousandlemons/English-words-pronunciation-mp3-audio-download](https://github.com/thousandlemons/English-words-pronunciation-mp3-audio-download) | 257 | Apache-2.0 | Download the pronunciation mp3 audio for 119,376 unique English words/terms |
| 63 | [Lyrcaxis/KokoroSharp](https://github.com/Lyrcaxis/KokoroSharp) | 253 | MIT | Fast local TTS inference engine in C# with ONNX runtime. Multi-speaker, multi-platform and multilingual.  Inte |
| 64 | [Kyubyong/g2pC](https://github.com/Kyubyong/g2pC) | 247 | Apache-2.0 | g2pC: A Context-aware Grapheme-to-Phoneme Conversion module for Chinese |
| 65 | [OpenPronounce/OpenPronounce](https://github.com/OpenPronounce/OpenPronounce) | 242 | AGPL-3.0 | Open-source, self-hosted pronunciation assessment: score a recording and find mispronounced words. English and |
| 66 | [ayutaz/piper-plus](https://github.com/ayutaz/piper-plus) | 242 | MIT | Multilingual neural TTS (6 languages: JA/EN/ZH/ES/FR/PT, code supports SV) — C++, C#, Rust, Go, Python, npm (W |
| 67 | [wannaphong/ttsmms](https://github.com/wannaphong/ttsmms) | 238 | MIT | TTS with The Massively Multilingual Speech (MMS) project |
| 68 | [g2p/git-fs](https://github.com/g2p/git-fs) | 237 | GPL-2.0 | A filesystem interface to git repositories |
| 69 | [YuanGongND/gopt](https://github.com/YuanGongND/gopt) | 234 | BSD-3-Clause | Code for the ICASSP 2022 paper "Transformer-Based Multi-Aspect Multi-Granularity Non-native English Speaker Pr |
| 70 | [thuhcsi/Crystal](https://github.com/thuhcsi/Crystal) | 233 | Apache-2.0 | Crystal - C++ implementation of a unified framework for multilingual TTS synthesis engine  with SSML specifica |
| 71 | [wayneclub/Apple-Dictionary](https://github.com/wayneclub/Apple-Dictionary) | 226 | MIT | Custom Apple Dictionary support dark mode and offline pronunciation |
| 72 | [sfortis/openai_tts](https://github.com/sfortis/openai_tts) | 223 | GPL-3.0 | Text-to-speech for Home Assistant from OpenAI, Mistral, Groq, Lemonfox, Kokoro, Chatterbox or any server that  |
| 73 | [rezkam/persian](https://github.com/rezkam/persian) | 206 | MIT | A fast Python toolkit for Persian (Farsi) text normalization, number/character conversion, and localization ut |
| 74 | [NRC-ILT/g2p](https://github.com/NRC-ILT/g2p) | 204 | NOASSERTION | Grapheme-to-Phoneme transductions that preserve input and output indices, and support cross-lingual g2p! |
| 75 | [cdcailf/cjkfold](https://github.com/cdcailf/cjkfold) | 201 | MIT | Fold look-alike CJK glyphs (Kangxi radicals, CJK radical supplements) so text extracted from PDFs matches agai |
| 76 | [davidmogar/cucco](https://github.com/davidmogar/cucco) | 200 | MIT | Text normalization library for Python |
| 77 | [keonlee9420/Cross-Speaker-Emotion-Transfer](https://github.com/keonlee9420/Cross-Speaker-Emotion-Transfer) | 193 | MIT | PyTorch Implementation of ByteDance's Cross-speaker Emotion Transfer Based on Speaker Condition Layer Normaliz |
| 78 | [freyavoiceai/FreyaTTS](https://github.com/freyavoiceai/FreyaTTS) | 192 | Apache-2.0 | An efficient 183M tokenizer-free non-autoregressive foundation model for Turkish speech synthesis |
| 79 | [nii-yamagishilab/ZMM-TTS](https://github.com/nii-yamagishilab/ZMM-TTS) | 186 | BSD-3-Clause | ZMM-TTS: Zero-shot Multilingual and Multispeaker Speech Synthesis Conditioned on Self-supervised Discrete Spee |
| 80 | [sequitur-g2p/sequitur-g2p](https://github.com/sequitur-g2p/sequitur-g2p) | 177 | GPL-2.0 | This is a github repository of the abandonware Sequitur G2P by Bisani & Ney |
| 81 | [lincwang123-bot/moonlit-stories](https://github.com/lincwang123-bot/moonlit-stories) | 177 | MIT | Reusable AI English picture-book workflow with consistent illustrations and local Chatterbox TTS. |
| 82 | [xinjli/transphone](https://github.com/xinjli/transphone) | 176 | MIT | phoneme tokenizer and grapheme-to-phoneme model for 8k languages |
| 83 | [speech-industry/bournemouth-forced-aligner](https://github.com/speech-industry/bournemouth-forced-aligner) | 175 | GPL-3.0 | Extract phoneme-level timestamps from speeh audio. |
| 84 | [microsoft/PhoneticMatching](https://github.com/microsoft/PhoneticMatching) | 169 | MIT | A phonetic matching library. Includes text utilities to do string comparisons on phonemes (the sound of the st |
| 85 | [snakers4/silero-stress](https://github.com/snakers4/silero-stress) | 168 | MIT | Silero Stress — pre-trained enterprise-grade automated stress and homograph disambiguation for the Russian lan |
| 86 | [persephone-tools/persephone](https://github.com/persephone-tools/persephone) | 160 | Apache-2.0 | A tool for automatic phoneme transcription |
| 87 | [NTT123/light-speed](https://github.com/NTT123/light-speed) | 155 | MIT | A modified VITS that utilizes phoneme duration's ground truth for better robustness |
| 88 | [hash2430/pitchtron](https://github.com/hash2430/pitchtron) | 155 | NOASSERTION | TTS for pitch-accented language. Korean dialect DB. |
| 89 | [uiuc-sst/g2ps](https://github.com/uiuc-sst/g2ps) | 153 | MIT | Data and code for grapheme-to-phoneme transducers in lots of languages |
| 90 | [felixkreuk/UnsupSeg](https://github.com/felixkreuk/UnsupSeg) | 148 | MIT | Self-Supervised Contrastive Learning for Unsupervised Phoneme Segmentation (INTERSPEECH 2020) |
| 91 | [rhasspy/piper-phonemize](https://github.com/rhasspy/piper-phonemize) | 143 | MIT | C++ library for converting text to phonemes for Piper |
| 92 | [nsu-ai/russian_g2p](https://github.com/nsu-ai/russian_g2p) | 141 | MIT | Accentor and transcriptor for Russian language |
| 93 | [open-data-plan/g2plot-vue](https://github.com/open-data-plan/g2plot-vue) | 138 | MIT | g2plot for vue |
| 94 | [VeteranXYZ/LuciaDictionary](https://github.com/VeteranXYZ/LuciaDictionary) | 136 | Apache-2.0 | A mobile-first English sentence learning tool for Chinese-speaking families, turning homework sentences into w |
| 95 | [SahandMalaei/ai-dictionary-koreader](https://github.com/SahandMalaei/ai-dictionary-koreader) | 134 | GPL-3.0 | Context-aware AI dictionary plugin for KOReader: instant definitions, explanations, deep dives, pronunciation, |
| 96 | [scarletcho/KoG2P](https://github.com/scarletcho/KoG2P) | 133 | GPL-3.0 | Korean grapheme-to-phone conversion in Python |
| 97 | [alexturkey/crisperwhisper-turkce-kelime-zamani](https://github.com/alexturkey/crisperwhisper-turkce-kelime-zamani) | 131 | Apache-2.0 | Verbatim speech-to-text with word timestamps on a 4 GB GPU: CrisperWhisper 2.0 Turbo (CT2 int8) + wav2vec2 CTC |
| 98 | [yl4579/AuxiliaryASR](https://github.com/yl4579/AuxiliaryASR) | 130 | MIT | Joint CTC-S2S Phoneme-level ASR for Voice Conversion and TTS (Text-Mel Alignment) |
| 99 | [mozi1924/Qwen3-TTS-EasyFinetuning](https://github.com/mozi1924/Qwen3-TTS-EasyFinetuning) | 130 | Apache-2.0 | Easy fine-tuning for Qwen3-TTS: Fast voice cloning and high-quality multilingual speech synthesis. |
| 100 | [carykh/videoToVoice](https://github.com/carykh/videoToVoice) | 128 | MIT | takes in a sequence of lip images, and predicts the phonemes being said. |