# Kalite ve denetim araştırması: 97 depo (Kasım 2026)

İlk araştırma ([benzer_projeler.md](benzer_projeler.md)) **video üreten** projelere bakıyordu. Bu araştırma işin
öbür yarısına bakar: **karar mercii, kalite test ekibi, ses kalitesi denetçisi, doğru anlatım ve bilgi kirliliği
kontrolü** yapan açık kaynak projeler.

**Yöntem.** 47 GitHub sorgusu (ör. *speech quality assessment, MOS prediction, DNSMOS, UTMOS, NISQA, TTS evaluation,
pronunciation assessment, hallucination detection, fact verification, claim verification, faithfulness, LLM as a
judge, LLM evaluation framework, guardrails, video quality, VMAF, forced alignment, readability*; konu etiketleri
`hallucination`, `llm-evaluation`, `fact-checking`, `speech-quality-assessment`) → 754 aday. Açıklama ve etiketlere
göre kategorilendi; güvenlik/pentest araçları, genel ajan çatıları ve "awesome" listeleri elendi; bilinen temel
araçlar (DNSMOS, VERSA, SelfCheckGPT, FActScore, MiniCheck, AlignScore, OpenAI evals, lm-eval-harness, Prometheus,
Multi-Agent Debate, LanguageTool, Zemberek…) elle eklendi → 97 depo. README'ler indirildi ve 8 özellik için
tarandı; ~20'si elle okundu.

## Ne öğrendik
| Ders | Kaynak | Bizim için anlamı |
|---|---|---|
| **Referanssız ses kalitesi puanı** CPU'da ölçülebilir; BAK = arka plan gürültüsü | microsoft/DNS-Challenge (DNSMOS P.835), SpeechMOS/UTMOS, NISQA-TTS, VERSA | "Hışırtı var mı?" sorusu artık kulakla değil sayıyla: cümle başına SIG/BAK/OVRL |
| **Uzun metni atomik iddialara böl, her birini kaynağa karşı doğrula** | FActScore, RefChecker, MiniCheck, FacTool, SelfCheckGPT | Senaryodaki her sayı ve İngilizce örnek belgede aranır; bulunamayan "uydurma" sayılır |
| **"Model önerir, araç karar verir"**: modelin kendi "doğru" demesi kanıt değildir | reverify, FactCircuit (kanıt zinciri) | Kapı deterministik; hakemin her bulgusu belge alıntısıyla gelmeli |
| **Eşikli onay kapısı (assert)**: CI'da geçti/kaldı | promptfoo, deepeval, giskard, Tracely | `kalite_kapisi.py`: KALDI ise teslim yok |
| **Kurallı hakem (1–5 puan) + kanıt** | Prometheus-Eval, deepeval G-Eval/DAG | SKILL 8b: 5 ölçütlü bağımsız hakem |
| **Üreteni değerlendirici yapma** | Multi-Agents-Debate, journalism fact-check-workflow, verification-before-completion | Hakem videoyu üretmemiş olmalı; "emin değilim" → kullanıcıya sorulur |
| Tutarlılıkla halüsinasyon tespiti | UQLM, SelfCheckGPT | İleride: açıklamayı birkaç kez ürettirip tutarsız olanı işaretlemek |
| Algısal video kalitesi | Netflix VMAF, ffmpeg-quality-metrics | Tahta animasyonunda gerek az; ileride sıkıştırma kontrolü için |

## Uyguladıklarımız (v2.2.0)
1. **`scripts/ses_puan.py`: DNSMOS ses denetçisi.** Microsoft'un ~1 MB ONNX modelleri (kod MIT, model CC-BY-4.0),
   yalnızca CPU. Her cümle için SIG/BAK/OVRL/P808; BAK < 3,5 ya da OVRL < 2,5 olan cümleler "yeniden üret" listesine
   girer. Seslendirme iş akışı artık her cümleyi puanlar ve `ses_puan.json`'u yayına ekler; önbellekten gelen
   cümleler tekrar puanlanmaz.
2. **`scripts/sadakat.py`: belgeye sadakat ve bilgi kirliliği.** EKSİK (belge satırı videoda yok), UYDURMA
   (belgede olmayan sayı/İngilizce örnek), TELAFFUZ (İngilizce okunacak öbeğe düşmüş Türkçe kelime), KONTROL
   (belgede geçmeyen özel ad), EKLENTİ (bizim eklediğimiz açıklamalar → hakeme).
3. **`scripts/kalite_kapisi.py`: karar mercii.** Senaryo şeması, okunmayan ekran metni, yerleşim/senkron,
   sadakat, ses puanı, Whisper telaffuz puanı ve video ses/sessizlik ölçümünü tek GEÇTİ/KALDI kararında toplar.
4. **SKILL.md 8a/8b:** kapı zorunlu; anlam doğruluğu için kanıtlı, 5 ölçütlü bağımsız hakem.

**İlk sonuç (B1 belgesi):** sadakat denetimi, teslim edilmiş eski senaryoda **57 yerde İngilizce okunacak öbeğin
içine Türkçe kelime düştüğünü** buldu (ör. "was/were ve ing takısı", "If ve present", "a work değil" tek parça
İngilizce olarak okunuyordu). Dönüştürücü düzeltildi: 57 → 0. Ayrıca okunmayan iki başlık (2B, O3), "on ve gün"
gibi Türkçe okunan İngilizce edatlar ve yazısı 30 px'in altına düşen iki tablo bulundu ve düzeltildi. Belge
kapsamı %99,4 (kalan satırlar bilerek çıkarılan kaynak bağlantıları).

## Bilerek almadıklarımız
- **API isteyen doğrulayıcılar** (Loki/OpenFactVerification, FacTool, RefChecker'ın GPT modu, promptfoo/deepeval'in
  LLM metrikleri): ücretli anahtar ister. Aynı işi kural tabanlı denetim + Claude hakem yapıyor.
- **Büyük yerel doğrulama modelleri** (MiniCheck-7B, AlignScore-large, Prometheus 8x7B): GPU/çok bellek ister,
  Türkçe desteği zayıf.
- **UTMOSv2 / NISQA**: torch + ağır modeller; DNSMOS aynı soruyu (gürültü/kalite) 1 MB'la cevaplıyor.
- **LanguageTool**: Türkçe desteği çok sınırlı; Zemberek Java ister. İleride yazım denetimi için aday.

## Tam liste (yıldıza göre)
Özellik sütunu README'de geçen anahtar kavramları gösterir (otomatik tarama).

| # | Depo | ⭐ | Lisans | Kategori | Açıklama | README'de |
|---|---|---|---|---|---|---|
| 1 | [microsoft/autogen](https://github.com/microsoft/autogen) | 61,859 | CC-BY-4.0 | LLM değerlendirme / hakem / kalite kapısı | A programming framework for agentic AI | cpu/yerel, coklu-ajan, api-gerekli |
| 2 | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | 39,077 | MIT | LLM değerlendirme / hakem / kalite kapısı | DSPy: The framework for programming—not prompting—language models | esik/assert |
| 3 | [langfuse/langfuse](https://github.com/langfuse/langfuse) | 37,455 | NOASSERTION | LLM değerlendirme / hakem / kalite kapısı | 🪢 Open source AI engineering platform: AI Gateway, agent observability, evals, and prompt/skill mana | cpu/yerel, llm-hakem, coklu-ajan |
| 4 | [mlflow/mlflow](https://github.com/mlflow/mlflow) | 28,822 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | The open source AI engineering platform for agents, LLMs, and ML models. MLflow enables teams of all | cpu/yerel, llm-hakem, coklu-ajan |
| 5 | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | 27,243 | MIT | LLM değerlendirme / hakem / kalite kapısı | Test your prompts, agents, and RAGs. Red teaming/pentesting/vulnerability scanning for AI. Compare p | cpu/yerel, esik/assert, api-gerekli |
| 6 | [m-bain/whisperX](https://github.com/m-bain/whisperX) | 25,340 | BSD-2-Clause | Ses kalitesi / konuşma değerlendirme | WhisperX:  Automatic Speech Recognition with Word-level Timestamps (& Diarization) | cpu/yerel |
| 7 | [comet-ml/opik](https://github.com/comet-ml/opik) | 23,439 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | Debug, evaluate, and monitor your LLM applications, RAG systems, and agentic workflows with comprehe | cpu/yerel, llm-hakem, esik/assert, api-gerekli |
| 8 | [openai/evals](https://github.com/openai/evals) | 19,747 | NOASSERTION | LLM değerlendirme / hakem / kalite kapısı | Evals is a framework for evaluating LLMs and LLM systems, and an open-source registry of benchmarks. | cpu/yerel, iddia-ayristirma, api-gerekli |
| 9 | [confident-ai/deepeval](https://github.com/confident-ai/deepeval) | 19,494 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | The LLM Evaluation Framework | cpu/yerel, llm-hakem, esik/assert, coklu-ajan, api-gerekli |
| 10 | [raga-ai-hub/RagaAI-Catalyst](https://github.com/raga-ai-hub/RagaAI-Catalyst) | 16,190 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | Python SDK for Agent AI Observability, Monitoring and Evaluation Framework. Includes features like a | esik/assert, api-gerekli |
| 11 | [languagetool-org/languagetool](https://github.com/languagetool-org/languagetool) | 15,262 | LGPL-2.1 | Metin / dil denetimi | Style and Grammar Checker for 25+ Languages |  |
| 12 | [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | 14,476 | MIT | LLM değerlendirme / hakem / kalite kapısı | A framework for few-shot evaluation of language models. | cpu/yerel, api-gerekli |
| 13 | [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) | 12,304 | NOASSERTION | LLM değerlendirme / hakem / kalite kapısı | AI Observability & Evaluation | cpu/yerel, coklu-ajan |
| 14 | [speechbrain/speechbrain](https://github.com/speechbrain/speechbrain) | 11,938 | Apache-2.0 | Ses kalitesi / konuşma değerlendirme | A PyTorch-based Speech Toolkit |  |
| 15 | [snakers4/silero-vad](https://github.com/snakers4/silero-vad) | 10,668 | MIT | Ses kalitesi / konuşma değerlendirme | Silero VAD: pre-trained enterprise-grade Voice Activity Detector | cpu/yerel |
| 16 | [open-mmlab/Amphion](https://github.com/open-mmlab/Amphion) | 10,343 | MIT | Ses kalitesi / konuşma değerlendirme | Amphion (/æmˈfaɪən/) is a toolkit for Audio, Music, and Speech Generation. Its purpose is to support | iddia-ayristirma |
| 17 | [NVIDIA/garak](https://github.com/NVIDIA/garak) | 10,038 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | the LLM vulnerability scanner | cpu/yerel, iddia-ayristirma, api-gerekli |
| 18 | [guardrails-ai/guardrails](https://github.com/guardrails-ai/guardrails) | 7,610 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | Adding guardrails to large language models. | cpu/yerel, esik/assert, api-gerekli |
| 19 | [open-compass/opencompass](https://github.com/open-compass/opencompass) | 7,595 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | OpenCompass is an LLM evaluation platform, supporting a wide range of models from OpenAI, Anthropic, | cpu/yerel, llm-hakem |
| 20 | [Helicone/helicone](https://github.com/Helicone/helicone) | 6,281 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | 🧊 Open source LLM observability platform. One line of code to monitor, evaluate, and experiment. YC  | cpu/yerel, coklu-ajan, api-gerekli |
| 21 | [Giskard-AI/giskard-oss](https://github.com/Giskard-AI/giskard-oss) | 5,953 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | 🐢 Open-Source Evaluation & Testing library for LLM Agents | llm-hakem, esik/assert, api-gerekli |
| 22 | [Netflix/vmaf](https://github.com/Netflix/vmaf) | 5,601 | NOASSERTION | Video / altyazı kalitesi | Perceptual video quality assessment based on multi-method fusion. |  |
| 23 | [Rikorose/DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) | 5,027 | NOASSERTION | Ses kalitesi / konuşma değerlendirme | Noise supression using deep filtering | cpu/yerel |
| 24 | [modelscope/ClearerVoice-Studio](https://github.com/modelscope/ClearerVoice-Studio) | 4,622 | Apache-2.0 | Ses kalitesi / konuşma değerlendirme | An AI-Powered Speech Processing Toolkit and Open Source SOTA Pretrained Models, Supporting Speech En | referanssiz |
| 25 | [EvolvingLMMs-Lab/lmms-eval](https://github.com/EvolvingLMMs-Lab/lmms-eval) | 4,497 | NOASSERTION | LLM değerlendirme / hakem / kalite kapısı | One-for-All Multimodal Evaluation Toolkit Across Text, Image, Video, and Audio Tasks | cpu/yerel, esik/assert, api-gerekli |
| 26 | [truera/trulens](https://github.com/truera/trulens) | 3,653 | MIT | LLM değerlendirme / hakem / kalite kapısı | Evaluation and Tracking for LLM Experiments and AI Agents | cpu/yerel, llm-hakem, esik/assert |
| 27 | [lmnr-ai/lmnr](https://github.com/lmnr-ai/lmnr) | 3,492 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | Laminar - open-source observability platform purpose-built for AI agents. YC S24. | cpu/yerel, iddia-ayristirma, esik/assert, api-gerekli |
| 28 | [vectara/hallucination-leaderboard](https://github.com/vectara/hallucination-leaderboard) | 3,329 | Apache-2.0 | Olgu doğrulama / halüsinasyon | Leaderboard Comparing LLM Performance at Producing Hallucinations when Summarizing Short Documents | iddia-ayristirma, kanit, llm-hakem |
| 29 | [confident-ai/deepteam](https://github.com/confident-ai/deepteam) | 3,103 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | DeepTeam is a framework to red team LLMs and AI agents. | cpu/yerel, iddia-ayristirma, llm-hakem, esik/assert, coklu-ajan, api-gerekli |
| 30 | [linto-ai/whisper-timestamped](https://github.com/linto-ai/whisper-timestamped) | 2,861 | AGPL-3.0 | Ses kalitesi / konuşma değerlendirme | Multilingual Automatic Speech Recognition with word-level timestamps and confidence | cpu/yerel, iddia-ayristirma, esik/assert |
| 31 | [huggingface/lighteval](https://github.com/huggingface/lighteval) | 2,586 | MIT | LLM değerlendirme / hakem / kalite kapısı | Lighteval is your all-in-one toolkit for evaluating LLMs across multiple backends | cpu/yerel |
| 32 | [resemble-ai/resemble-enhance](https://github.com/resemble-ai/resemble-enhance) | 2,501 | MIT | Ses kalitesi / konuşma değerlendirme | AI powered speech denoising and enhancement | cpu/yerel |
| 33 | [showlab/Paper2Video](https://github.com/showlab/Paper2Video) | 2,424 | MIT | Eğitim içeriği değerlendirme | Automatic Video Generation from Scientific Papers | cpu/yerel, kanit, llm-hakem, coklu-ajan, api-gerekli |
| 34 | [future-agi/future-agi](https://github.com/future-agi/future-agi) | 2,279 | Apache-2.0 | Olgu doğrulama / halüsinasyon | Open-source, end-to-end platform for evaluating, observing, and improving LLM and AI agent applicati | cpu/yerel, iddia-ayristirma, llm-hakem, api-gerekli |
| 35 | [Tiiiger/bert_score](https://github.com/Tiiiger/bert_score) | 1,924 | MIT | Metin / dil denetimi | BERT score for text generation |  |
| 36 | [PrithivirajDamodaran/Gramformer](https://github.com/PrithivirajDamodaran/Gramformer) | 1,583 | MIT | Metin / dil denetimi | A framework for detecting, highlighting and correcting grammatical errors on natural language text.  |  |
| 37 | [slhck/ffmpeg-normalize](https://github.com/slhck/ffmpeg-normalize) | 1,542 | NOASSERTION | Ses kalitesi / konuşma değerlendirme | Audio Normalization for Python/ffmpeg | esik/assert |
| 38 | [TIGER-AI-Lab/TheoremExplainAgent](https://github.com/TIGER-AI-Lab/TheoremExplainAgent) | 1,515 | MIT | Eğitim içeriği değerlendirme | Official Repo for "TheoremExplainAgent: Towards Video-based Multimodal Explanations for LLM Theorem  | cpu/yerel, iddia-ayristirma, api-gerekli |
| 39 | [microsoft/DNS-Challenge](https://github.com/microsoft/DNS-Challenge) | 1,479 | CC-BY-4.0 | Ses kalitesi / konuşma değerlendirme | This repo contains the scripts, models, and required files for the Deep Noise Suppression (DNS) Chal | cpu/yerel, referanssiz, iddia-ayristirma |
| 40 | [textstat/textstat](https://github.com/textstat/textstat) | 1,395 | MIT | Metin / dil denetimi | :memo: python package to calculate readability statistics of a text object - paragraphs, sentences,  |  |
| 41 | [ahmetaa/zemberek-nlp](https://github.com/ahmetaa/zemberek-nlp) | 1,379 | NOASSERTION | Metin / dil denetimi | NLP tools for Turkish. |  |
| 42 | [2akouwu/reverify](https://github.com/2akouwu/reverify) | 1,343 | MIT | Olgu doğrulama / halüsinasyon | Stop your AI from making things up — it proposes, deterministic tools decide, every claim checked ag | cpu/yerel, iddia-ayristirma, kanit, llm-hakem, esik/assert, api-gerekli |
| 43 | [Jwuthri/Tracely-ai](https://github.com/Jwuthri/Tracely-ai) | 1,299 | MIT | LLM değerlendirme / hakem / kalite kapısı | Trace-native CI/CD for AI agents — production failures become regression tests that block the PR. Au | cpu/yerel, iddia-ayristirma, llm-hakem, esik/assert, coklu-ajan, api-gerekli |
| 44 | [microsoft/prompty](https://github.com/microsoft/prompty) | 1,289 | MIT | LLM değerlendirme / hakem / kalite kapısı | Prompty makes it easy to create, manage, debug, and evaluate LLM prompts for your AI applications.   | cpu/yerel, api-gerekli |
| 45 | [cvs-health/uqlm](https://github.com/cvs-health/uqlm) | 1,217 | Apache-2.0 | Olgu doğrulama / halüsinasyon |  [JMLR 2026] UQLM: A Python package for LLM hallucination detection using uncertainty quantification | iddia-ayristirma, llm-hakem, esik/assert, api-gerekli |
| 46 | [Libr-AI/OpenFactVerification](https://github.com/Libr-AI/OpenFactVerification) | 1,164 | MIT | Olgu doğrulama / halüsinasyon | Loki: Open-source solution designed to automate the process of verifying factuality | iddia-ayristirma, kanit, api-gerekli |
| 47 | [prometheus-eval/prometheus-eval](https://github.com/prometheus-eval/prometheus-eval) | 1,122 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | Evaluate your LLM's response with Prometheus and GPT4 💯 | cpu/yerel, iddia-ayristirma, kanit, llm-hakem, coklu-ajan |
| 48 | [JudgmentLabs/judgeval](https://github.com/JudgmentLabs/judgeval) | 1,074 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | The Continuous-Improvement Stack for Agents. Our environment data and evals power agent improvement  | llm-hakem, api-gerekli |
| 49 | [aliutkus/speechmetrics](https://github.com/aliutkus/speechmetrics) | 1,059 | MIT | Ses kalitesi / konuşma değerlendirme | A wrapper around speech quality metrics MOSNet, BSSEval, STOI, PESQ, SRMR, SISDR | referanssiz, esik/assert |
| 50 | [gabrielmittag/NISQA](https://github.com/gabrielmittag/NISQA) | 988 | MIT | Ses kalitesi / konuşma değerlendirme | NISQA - Non-Intrusive Speech Quality and TTS Naturalness Assessment | referanssiz |
| 51 | [jitsi/jiwer](https://github.com/jitsi/jiwer) | 946 | Apache-2.0 | Ses kalitesi / konuşma değerlendirme | Evaluate your speech-to-text system with similarity measures such as word error rate (WER) | esik/assert |
| 52 | [GAIR-NLP/factool](https://github.com/GAIR-NLP/factool) | 937 | Apache-2.0 | Olgu doğrulama / halüsinasyon | FacTool: Factuality Detection in Generative AI | cpu/yerel, iddia-ayristirma, kanit, llm-hakem, api-gerekli |
| 53 | [superwesleyhys-ux/factcircuit](https://github.com/superwesleyhys-ux/factcircuit) | 927 | MIT | Olgu doğrulama / halüsinasyon | FactCircuit: an auditable claim-and-evidence verification loop with immutable provenance, staged che | cpu/yerel, iddia-ayristirma, kanit, llm-hakem, esik/assert, api-gerekli |
| 54 | [IncarnaMind/IncarnaMind](https://github.com/IncarnaMind/IncarnaMind) | 858 | Apache-2.0 | Olgu doğrulama / halüsinasyon | From messy files to a checked report. A free, open-source desktop app for macOS, Windows and Linux:  | cpu/yerel, llm-hakem, api-gerekli |
| 55 | [darkrishabh/agent-skills-eval](https://github.com/darkrishabh/agent-skills-eval) | 817 | MIT | LLM değerlendirme / hakem / kalite kapısı | A test runner for agentskills.io-style AI agent skills | cpu/yerel, kanit, llm-hakem, esik/assert, api-gerekli |
| 56 | [csteinmetz1/pyloudnorm](https://github.com/csteinmetz1/pyloudnorm) | 793 | MIT | Ses kalitesi / konuşma değerlendirme | Flexible audio loudness meter in Python with implementation of ITU-R BS.1770-4 loudness algorithm | esik/assert |
| 57 | [google-research/bleurt](https://github.com/google-research/bleurt) | 791 | Apache-2.0 | Metin / dil denetimi | BLEURT is a metric for Natural Language Generation based on transfer learning. | cpu/yerel, esik/assert |
| 58 | [facebookresearch/audiobox-aesthetics](https://github.com/facebookresearch/audiobox-aesthetics) | 783 | CC-BY-4.0 | Ses kalitesi / konuşma değerlendirme | Unified automatic quality assessment for speech, music, and sound. | cpu/yerel |
| 59 | [Continuum-AI-Corp/OrcaReplay](https://github.com/Continuum-AI-Corp/OrcaReplay) | 780 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | OrcaReplay — Time travel for AI agents. Record, replay, fork, and debug any agent run with any model | cpu/yerel, iddia-ayristirma, kanit, esik/assert, api-gerekli |
| 60 | [MigoXLab/dingo](https://github.com/MigoXLab/dingo) | 768 | Apache-2.0 | Olgu doğrulama / halüsinasyon | Dingo: A Comprehensive AI Data, Model and Application Quality Evaluation Tool | cpu/yerel, iddia-ayristirma, llm-hakem, coklu-ajan, api-gerekli |
| 61 | [overmind-core/overmind](https://github.com/overmind-core/overmind) | 760 | AGPL-3.0 | LLM değerlendirme / hakem / kalite kapısı | The platform for continuously improving AI agents. | cpu/yerel, llm-hakem, esik/assert, api-gerekli |
| 62 | [breizhn/DTLN](https://github.com/breizhn/DTLN) | 748 | MIT | Ses kalitesi / konuşma değerlendirme | Tensorflow 2.x implementation of the DTLN real time speech denoising model. With TF-lite, ONNX and r | cpu/yerel |
| 63 | [EverMind-AI/SkillCorpus](https://github.com/EverMind-AI/SkillCorpus) | 703 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | Open-source infrastructure that turns scattered SKILL.md files into curated, retrieval-ready agent-s | cpu/yerel, iddia-ayristirma, esik/assert, api-gerekli |
| 64 | [VITA-MLLM/Woodpecker](https://github.com/VITA-MLLM/Woodpecker) | 649 | — | Olgu doğrulama / halüsinasyon | ✨✨Woodpecker: Hallucination Correction for Multimodal Large Language Models | iddia-ayristirma, kanit |
| 65 | [ludlows/PESQ](https://github.com/ludlows/PESQ) | 637 | MIT | Ses kalitesi / konuşma değerlendirme | PESQ (Perceptual Evaluation of Speech Quality) Wrapper for Python Users (narrow band and wide band) |  |
| 66 | [HowieHwong/TrustLLM](https://github.com/HowieHwong/TrustLLM) | 636 | MIT | Olgu doğrulama / halüsinasyon | [ICML 2024] TrustLLM: LLM trustworthiness evaluation across truthfulness, safety, fairness, robustne | cpu/yerel, llm-hakem, esik/assert, api-gerekli |
| 67 | [potsawee/selfcheckgpt](https://github.com/potsawee/selfcheckgpt) | 635 | MIT | Olgu doğrulama / halüsinasyon | SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models | cpu/yerel, esik/assert, api-gerekli |
| 68 | [Skytliang/Multi-Agents-Debate](https://github.com/Skytliang/Multi-Agents-Debate) | 623 | GPL-3.0 | LLM değerlendirme / hakem / kalite kapısı | MAD: The first work to explore Multi-Agent Debate with Large Language Models :D | llm-hakem, coklu-ajan, api-gerekli |
| 69 | [slhck/ffmpeg-quality-metrics](https://github.com/slhck/ffmpeg-quality-metrics) | 563 | MIT | Video / altyazı kalitesi | Calculate quality metrics with FFmpeg (SSIM, PSNR, VMAF, VIF) | cpu/yerel, iddia-ayristirma, esik/assert |
| 70 | [jxmorris12/language_tool_python](https://github.com/jxmorris12/language_tool_python) | 534 | GPL-3.0 | Metin / dil denetimi | a free, non-AI python grammar checker 📝✅ | cpu/yerel |
| 71 | [anicolson/DeepXi](https://github.com/anicolson/DeepXi) | 526 | MPL-2.0 | Ses kalitesi / konuşma değerlendirme | Deep Xi: A deep learning approach to a priori SNR estimation implemented in TensorFlow 2/Keras. For  | cpu/yerel |
| 72 | [schmiph2/pysepm](https://github.com/schmiph2/pysepm) | 463 | GPL-3.0 | Ses kalitesi / konuşma değerlendirme | Python implementation of performance metrics in Loizou's Speech Enhancement book |  |
| 73 | [shmsw25/FActScore](https://github.com/shmsw25/FActScore) | 462 | MIT | Olgu doğrulama / halüsinasyon | A package to evaluate factuality of long-form generation. Original implementation of our EMNLP 2023  | cpu/yerel, iddia-ayristirma, kanit, api-gerekli |
| 74 | [jamditis/claude-skills-journalism](https://github.com/jamditis/claude-skills-journalism) | 453 | MIT | Olgu doğrulama / halüsinasyon | Claude Code skills for journalism, media, and academia - verification, FOIA, data journalism, academ | cpu/yerel, iddia-ayristirma, kanit, llm-hakem, coklu-ajan, api-gerekli |
| 75 | [wavlab-speech/versa](https://github.com/wavlab-speech/versa) | 438 | Apache-2.0 | Ses kalitesi / konuşma değerlendirme | Versatile Evaluation of Speech and Audio | cpu/yerel, referanssiz, esik/assert |
| 76 | [amazon-science/RefChecker](https://github.com/amazon-science/RefChecker) | 434 | Apache-2.0 | Olgu doğrulama / halüsinasyon | RefChecker provides automatic checking pipeline and benchmark dataset for detecting fine-grained hal | cpu/yerel, referanssiz, iddia-ayristirma, kanit, llm-hakem, esik/assert, api-gerekli |
| 77 | [sarulab-speech/UTMOSv2](https://github.com/sarulab-speech/UTMOSv2) | 380 | MIT | Ses kalitesi / konuşma değerlendirme | UTokyo-SaruLab MOS Prediction System |  |
| 78 | [tarepan/SpeechMOS](https://github.com/tarepan/SpeechMOS) | 372 | MIT | Ses kalitesi / konuşma değerlendirme | Easy-to-Use Speech MOS predictors |  |
| 79 | [NVIDIA/CleanUNet](https://github.com/NVIDIA/CleanUNet) | 355 | MIT | Ses kalitesi / konuşma değerlendirme | Official PyTorch Implementation of CleanUNet (ICASSP 2022) |  |
| 80 | [tianyi-lab/HallusionBench](https://github.com/tianyi-lab/HallusionBench) | 346 | BSD-3-Clause | Olgu doğrulama / halüsinasyon | [CVPR'24] HallusionBench: You See What You Think? Or You Think What You See? An Image-Context Reason | api-gerekli |
| 81 | [shahules786/mayavoz](https://github.com/shahules786/mayavoz) | 337 | MIT | Ses kalitesi / konuşma değerlendirme | Pytorch based speech enhancement toolkit. | esik/assert |
| 82 | [OpenBMB/UltraEval-Audio](https://github.com/OpenBMB/UltraEval-Audio) | 329 | Apache-2.0 | LLM değerlendirme / hakem / kalite kapısı | Your faithful, impartial partner for audio evaluation — know yourself, know your rivals. 真实评测，知己知彼。A | cpu/yerel, llm-hakem, api-gerekli |
| 83 | [sarulab-speech/UTMOS22](https://github.com/sarulab-speech/UTMOS22) | 318 | MIT | Ses kalitesi / konuşma değerlendirme | UT-Sarulab MOS prediction system using SSL models |  |
| 84 | [canberk7/ema-lightning](https://github.com/canberk7/ema-lightning) | 306 | Apache-2.0 | Ses kalitesi / konuşma değerlendirme | Tiny, fast and accurate Turkish text-to-speech. 8.6M parameters, 0.92% WER on Freya-TR-Eval, first a | cpu/yerel, esik/assert |
| 85 | [RookieJunChen/FullSubNet-plus](https://github.com/RookieJunChen/FullSubNet-plus) | 296 | Apache-2.0 | Ses kalitesi / konuşma değerlendirme | The official PyTorch implementation of "FullSubNet+: Channel Attention FullSubNet with Complex Spect | cpu/yerel |
| 86 | [Tencent/CenseoQoE](https://github.com/Tencent/CenseoQoE) | 240 | NOASSERTION | Video / altyazı kalitesi | image and video quality assessment |  |
| 87 | [boson-ai/EmergentTTS-Eval-public](https://github.com/boson-ai/EmergentTTS-Eval-public) | 237 | Apache-2.0 | Ses kalitesi / konuşma değerlendirme | [NeurIPS' 25] Benchmark for evaluating TTS models on complex prosodic, expressiveness, and linguisti | cpu/yerel, llm-hakem, api-gerekli |
| 88 | [Liyan06/MiniCheck](https://github.com/Liyan06/MiniCheck) | 235 | Apache-2.0 | Olgu doğrulama / halüsinasyon | MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents [EMNLP 2024] | cpu/yerel, iddia-ayristirma, kanit |
| 89 | [gdavila/easyVmaf](https://github.com/gdavila/easyVmaf) | 208 | MIT | Video / altyazı kalitesi | Python script to easily compute VMAF using FFmpeg. It allows to deinterlace, scale and sync Ref and  | cpu/yerel, esik/assert |
| 90 | [ceva-ip/DPDFNet](https://github.com/ceva-ip/DPDFNet) | 186 | Apache-2.0 | Ses kalitesi / konuşma değerlendirme | Clean up noisy speech in real time with DPDFNet - open-source streaming speech enhancement for resea | cpu/yerel, referanssiz |
| 91 | [IAAR-Shanghai/UHGEval](https://github.com/IAAR-Shanghai/UHGEval) | 183 | Apache-2.0 | Olgu doğrulama / halüsinasyon | [ACL 2024] User-friendly evaluation framework: Eval Suite & Benchmarks: UHGEval, HaluEval, HalluQA,  | cpu/yerel, api-gerekli |
| 92 | [AndreevP/wvmos](https://github.com/AndreevP/wvmos) | 179 | — | Ses kalitesi / konuşma değerlendirme | MOS score prediction by fine-tuned wav2vec2.0 model |  |
| 93 | [yuh-zha/AlignScore](https://github.com/yuh-zha/AlignScore) | 178 | MIT | Olgu doğrulama / halüsinasyon | ACL2023 - AlignScore, a metric for factual consistency evaluation. | iddia-ayristirma, llm-hakem |
| 94 | [aask1357/fastenhancer](https://github.com/aask1357/fastenhancer) | 165 | MIT | Ses kalitesi / konuşma değerlendirme | Speed-optimized streaming neural speech enhancement network | cpu/yerel |
| 95 | [SerhiiKorniienko/bullshit-detector](https://github.com/SerhiiKorniienko/bullshit-detector) | 163 | MIT | Olgu doğrulama / halüsinasyon | Agent skills that fact-check the internet: claim-by-claim verification with sources and a 0-10 BS sc | cpu/yerel, iddia-ayristirma, kanit, llm-hakem, api-gerekli |
| 96 | [zjunlp/Deco](https://github.com/zjunlp/Deco) | 151 | MIT | Olgu doğrulama / halüsinasyon | [ICLR 2025] MLLM can see? Dynamic Correction Decoding for Hallucination Mitigation | esik/assert |
| 97 | [obss/turkish-question-generation](https://github.com/obss/turkish-question-generation) | 47 | MIT | Eğitim içeriği değerlendirme | Automated question generation and question answering from Turkish texts using text-to-text transform |  |
