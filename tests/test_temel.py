"""Hızlı birim testleri: ağır model gerektirmez (CI her push'ta çalıştırır)."""
import json, sys
from pathlib import Path

import numpy as np

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "scripts"))
import video_uret as v  # noqa: E402


def test_cumle_bolme_dur_isareti():
    c = v.cumlelere_bol("Birinci cümle. [dur] İkinci cümle? Üçüncü!")
    assert len(c) == 3 and c[0].endswith("[dur]")


def test_telaffuz_ve_sayi():
    m = v.seslendirme_metni("B1 için 30 dakika.", {"B1": "be bir"})
    assert "be bir" in m and "otuz" in m


def test_tum_senaryolar_gecerli():
    for f in list(KOK.glob("senaryolar/*.json")) + list(KOK.glob("ornek/*.json")):
        assert v.senaryo_dogrula(json.loads(f.read_text(encoding="utf-8"))) == [], f.name


def test_dogrulama_hatalari_yakalar():
    sen = {"sahneler": [{"baslik": "x", "tur": "tablolar", "anlatim": "a."},
                        {"baslik": "y", "anlatim": "Bir. İki.", "maddeler": ["a"], "goster": [0, 5]},
                        {"baslik": "z", "tur": "soru", "anlatim": "Soru. Cevap.",
                         "soru": {"metin": "?", "secenekler": ["a", "b"], "dogru": 3}}]}
    h = " | ".join(v.senaryo_dogrula(sen))
    assert "bilinmeyen tur" in h and "goster" in h and "dogru" in h


def test_ses_anahtari_metne_bagli():
    a = v.ses_anahtari("merhaba", None)
    assert a == v.ses_anahtari("merhaba", None)
    assert a != v.ses_anahtari("merhaba!", None) and a != v.ses_anahtari("merhaba", "sakin")


def test_ses_deposu_icerikle_bulur_eskiyi_reddeder(tmp_path):
    (tmp_path / "01_00.wav").write_bytes(b"x")
    (tmp_path / "dizin.json").write_text(json.dumps({"01_00": {"anahtar": "aaa", "metin": "eski"}}))
    d = v.SesDeposu(str(tmp_path))
    assert d.bul("05_03", "aaa") == tmp_path / "01_00.wav"   # sahne numarası değişse de bulunur
    assert d.bul("01_00", "bbb") is None                       # metin değişmişse eski ses kullanılmaz


def test_klip_temizle_nefes_kuyrugunu_keser():
    sr = v.SR; t = np.arange(int(sr * 1.0)) / sr
    konusma = (0.4 * np.sin(2 * np.pi * 180 * t)).astype(np.float32)
    nefes = (0.006 * np.random.RandomState(0).randn(int(sr * 0.8))).astype(np.float32)
    nefes = np.convolve(nefes, [1, -1], mode="same").astype(np.float32)   # tiz gürültü
    y, bas = v.klip_temizle(np.concatenate([konusma, nefes]))
    assert len(y) < len(konusma) + int(0.1 * sr) and bas == 0.0


def test_agiz_bicimleri_uc_tur_uretir():
    sr = v.SR; spf = sr // v.FPS; n = 60
    t = np.arange(spf * n) / sr
    ses = np.concatenate([0.3 * np.sin(2 * np.pi * 300 * t[:spf * 20]),          # alçak → o
                          0.3 * np.sin(2 * np.pi * 800 * t[:spf * 20]),          # orta → a
                          0.3 * np.sin(2 * np.pi * 2500 * t[:spf * 20])]).astype(np.float32)  # tiz → i
    b = v.agiz_bicimleri(ses, n, spf)
    assert set(b) == {"a", "o", "i"}


def test_ingilizce_parcalar_ve_bolme():
    c = v.cumlelere_bol("Soru: {I'm late, aren't I?} Doğru cevap B: {aren't I}. Bitti.")
    assert c == ["Soru: {I'm late, aren't I?}", "Doğru cevap B: {aren't I}.", "Bitti."]
    p = v.parcalara_ayir(v.seslendirme_metni(c[1], {"B": "be"}))
    assert p == [("tr", "Doğru cevap be: arnt ay.")]          # kısa öbek cümle içinde okunuşuyla
    assert v.temiz(c[1]) == "Doğru cevap B: aren't I."


def test_kapsam_okunmayani_bulur():
    sh = {"tur": "tablo", "anlatim": "Borrow ödünç almak demektir.",
          "tablo": {"satirlar": [["borrow", "ödünç almak"], ["lend", "ödünç vermek"]]}}
    assert v.okunmayanlar(sh) == ["lend ödünç vermek"]
    assert v.oto_goster(sh, ["Borrow ödünç almak.", "Lend ise ödünç vermek."]) == [0, 1]


def test_gomulu_ingilizce_okunusla_bagimsiz_alintiyla():
    t = v.seslendirme_metni("Had better kalıbından sonra {to} gelmez: {You'd better hurry up now}.", {})
    assert "{You'd better hurry up now}" in t and "{to}" not in t and "tu gelmez" in t


def test_onizleme_secimi_temsili_ve_kisa():
    sen = json.loads((KOK / "senaryolar/b1_tam_belge.json").read_text(encoding="utf-8"))
    sh = sen["sahneler"]
    idx = v.onizleme_sec(sh, 90, 0.9)
    assert idx[0] == 0 and idx == sorted(idx)
    turler = {sh[i].get("tur", "maddeler") for i in idx}
    assert {"soru", "tablo", "metin"} <= turler
    assert any("{" in sh[i]["anlatim"] for i in idx)
    sure = sum(v.sahne_suresi_tahmin(sh[i], 0.9) for i in idx)
    assert 45 <= sure <= 130


def test_genel_telaffuz_dosyasi_gecerli():
    g = json.loads((KOK / "telaffuz.json").read_text(encoding="utf-8"))
    assert g["telaffuz"]["B1"] == "be, bir"
    m = v.seslendirme_metni("vb. konular", g["telaffuz"])
    assert "ve benzeri" in m


def test_sadakat_uydurma_ve_telaffuz_yakalar():
    import sadakat
    belge = "## Zamanlar\n\nPast Simple: *I went home yesterday.* Sınav 45 dakika sürer ve 3 bölümden oluşur.\n"
    sen = {"sahneler": [{"baslik": "Zamanlar", "maddeler": ["Sınav 90 dakika"],
                         "anlatim": "Sınav 90 dakika sürer. {I went home yesterday.} {She is a doctor.} {If ve present}."}]}
    r = sadakat.denetle(sen, belge)
    assert any(u["deger"] == "90" for u in r["uydurma"])
    assert any("doctor" in u["deger"] for u in r["uydurma"])
    assert not any("went home" in u["deger"] for u in r["uydurma"])
    assert r["telaffuz"] and r["telaffuz"][0]["turkce"] == ["ve"]


def test_donusturucu_turkceyi_ingilizce_obekten_ayirir():
    import belge_senaryo as b
    t = b.anlatim("*was/were + V-ing* ve *a job, ~~a work~~*", {})
    import re
    for obek in re.findall(r"\{([^}]*)\}", t):
        assert not re.search(r"[çğıöşü]|\b(ve|değil)\b", obek), t
    assert "değil" in t and "ing" in t
