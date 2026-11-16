#!/usr/bin/env python3
"""Aynı Türkçe paragrafı farklı açık kaynak TTS modelleriyle, aynı referans sesle seslendirir (kör karşılaştırma için).
Kullanım: python tts_karsilastir.py MODEL cikti_klasoru
MODEL: chatterbox_v2 | chatterbox_v3 | voxcpm2_klon | voxcpm2_tarif | fireredtts3"""
import json, sys, time
from pathlib import Path
import numpy as np
import soundfile as sf

METIN = [
    "Merhaba! Bugün iş görüşmelerinde en sık sorulan sorulardan birine bakacağız: Kendinizden bahseder misiniz?",
    "Bu soruda amaç, kısa ve net bir hikâye anlatmak.",
    "Önce şu anki işinizi, sonra en önemli başarınızı, en son da neden bu pozisyona başvurduğunuzu söyleyin.",
    "Mesela şöyle diyebilirsiniz: Yaklaşık beş yıldır iş analisti olarak çalışıyorum ve en büyük projemde "
    "müşteri bekleme süresini yüzde otuz azalttık.",
    "Gördüğünüz gibi, hepsi bu kadar basit.",
]
KOK = Path(__file__).resolve().parents[1]
REF = str(KOK / "ses" / "referans_fahrettin.wav")
REF_METIN = ("Merhaba, ben bugün size İngilizce öğrenmenin en etkili yollarını anlatacağım. "
             "Hazırsanız başlayalım, çünkü önümüzde gerçekten keyifli bir yol var.")
TARIF = "orta yaşlı erkek öğretmen, sıcak ve samimi, sakin tempoda, net anlatım"


def uretici(model):
    if model.startswith("chatterbox"):
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        m = (ChatterboxMultilingualTTS.from_pretrained(device="cpu") if model == "chatterbox_v2"   # 0.1.7 = V2
             else ChatterboxMultilingualTTS.from_pretrained(device="cpu", t3_model="v3"))
        return lambda t: (m.generate(t, language_id="tr", audio_prompt_path=REF).squeeze(0).numpy(), m.sr)
    if model.startswith("voxcpm2"):
        from voxcpm import VoxCPM
        m = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, device="cpu")
        sr = m.tts_model.sample_rate
        if model == "voxcpm2_klon":      # en sadık klon: referans ses + yazılı dökümü
            return lambda t: (m.generate(text=t, prompt_wav_path=REF, prompt_text=REF_METIN,
                                         reference_wav_path=REF, cfg_value=2.0, inference_timesteps=10), sr)
        return lambda t: (m.generate(text=f"({TARIF}){t}", reference_wav_path=REF,
                                     cfg_value=2.0, inference_timesteps=10), sr)
    if model == "fireredtts3":
        import torchaudio
        from fireredtts3.core import FireRedTTS3
        m = FireRedTTS3("pretrained_models", use_wetext=False, use_llm_tn=False)
        pa, psr = torchaudio.load(REF)
        def f(t):
            a, sr = m.generate(language=None, prompt_text=REF_METIN, prompt_audio=pa, prompt_audio_sr=psr,
                               text=t, do_tn=False)
            return a.squeeze(0).cpu().numpy(), sr
        return f
    raise SystemExit("bilinmeyen model " + model)


def main():
    model, cikti = sys.argv[1], Path(sys.argv[2]); cikti.mkdir(parents=True, exist_ok=True)
    t0 = time.time(); u = uretici(model); yukleme = time.time() - t0
    parcalar, sr, uretim, ses_sn = [], None, 0.0, 0.0
    for c in METIN:
        t1 = time.time(); x, sr = u(c); uretim += time.time() - t1
        x = np.asarray(x, np.float32).reshape(-1); ses_sn += len(x) / sr
        parcalar += [x, np.zeros(int(0.4 * sr), np.float32)]
        print(f"{time.time() - t1:6.1f} sn · {c[:50]}", flush=True)
    sf.write(cikti / f"{model}.wav", np.concatenate(parcalar), sr)
    bilgi = {"model": model, "yukleme_sn": round(yukleme, 1), "uretim_sn": round(uretim, 1),
             "ses_sn": round(ses_sn, 1), "gercek_zaman_orani": round(uretim / max(ses_sn, 0.1), 2)}
    (cikti / f"{model}.json").write_text(json.dumps(bilgi, ensure_ascii=False))
    print(bilgi)


if __name__ == "__main__":
    main()
