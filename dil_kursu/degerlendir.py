# -*- coding: utf-8 -*-
"""Kursun öğretim değerlendirmesi. Kullanılan açık kaynak araçlar:
spaCy (lemma, biçimbilim), cefrpy (kelime CEFR düzeyi), textstat (okunabilirlik), lexicalrichness (MTLD),
wordfreq (sıklık), py-fsrs (hafıza modeli / hatırlama tahmini), Kokoro klip süreleri (konuşma hızı)."""
import json, random, re, sys, collections
from datetime import datetime, timedelta, timezone
from pathlib import Path
import numpy as np, soundfile as sf
sys.path.insert(0, "/home/claude/kurs")
import icerik, motor, birlestir, en_ses
import spacy, textstat
from cefrpy import CEFRAnalyzer
from lexicalrichness import LexicalRichness

nlp = spacy.load("en_core_web_sm"); cefr = CEFRAnalyzer()
trd = birlestir.tr_dizini()
SURE = {}


def sure_en(m, v, h):
    k = (m, v, h)
    if k not in SURE:
        x, sr = sf.read(en_ses.uret(m, v, h), dtype="float32"); SURE[k] = len(birlestir.kirp(x)) / sr
    return SURE[k]


def sure_tr(c):
    if ("T", c) not in SURE:
        x = birlestir.tr_klip(c, trd); SURE[("T", c)] = len(birlestir.kirp(x)) / 24000
    return SURE[("T", c)]


def zaman_dokumu(ev):
    """Saniye: Türkçe anlatım, İngilizce dinleme, öğrencinin konuştuğu duraklamalar, diğer sessizlik."""
    t = collections.Counter(); son = 0.0; onceki = None
    for x in ev:
        if x[0] == "T":
            for c in motor.cumlelere_bol(x[1]):
                d = sure_tr(c); t["tr"] += d; son = d
        elif x[0] == "E":
            d = sure_en(x[1], x[2], x[3]); t["en"] += d; son = d
        elif x[0] == "R":
            t["ogrenci"] += min(12, x[1] * son + x[2])
        elif x[0] == "S":
            t["ogrenci" if x[1] >= 2.5 else "sessiz"] += x[1]
        elif x[0] == "B":
            t["sessiz"] += 0.32
    return t


FONKSIYON = set("""a an the and or but so if of to in on at for with from by up about into over after before
i you he she it we they me him her us them my your his its our their this that these those there here
be am is are was were been being have has had do does did not no yes can will would should could must
what who where when why how which some any all very too also just than then as""".split())


def lemmalar(metin):
    return [t for t in nlp(metin) if t.is_alpha]


def kelime_lemmalari(d):
    s = set()
    for k in d["kelimeler"]:
        for t in nlp(k["en"]):
            if t.is_alpha: s.add(t.lemma_.lower())
    return s


def kapsam(metinler, bilinen):
    tok = [t for m in metinler for t in lemmalar(m)]
    if not tok: return None, []
    ok = [t for t in tok if t.lemma_.lower() in bilinen or t.pos_ == "PROPN" or t.like_num]
    bilinmeyen = sorted({t.lemma_.lower() for t in tok if t not in ok and t.lemma_.lower() not in bilinen and t.pos_ != "PROPN" and not t.like_num})
    return len(ok) / len(tok), bilinmeyen


def yapi(sent):
    """Basit dilbilgisi yapısı etiketleri (spaCy etiketlerinden)."""
    doc = nlp(sent); y = set()
    for t in doc:
        if t.tag_ == "VBD": y.add("geçmiş zaman")
        if t.tag_ == "VBG" and any(c.lemma_ == "be" and c.dep_ == "aux" for c in t.children): y.add("şimdiki zaman (-ing)")
        if t.tag_ == "VBN" and any(c.lemma_ == "have" and c.dep_ == "aux" for c in t.children): y.add("present perfect")
        if t.dep_ in ("auxpass", "nsubjpass"): y.add("edilgen")
        if t.lemma_ == "will" and t.tag_ == "MD": y.add("gelecek (will)")
        if t.lemma_ in ("can", "could", "should", "must", "might", "may") and t.tag_ == "MD": y.add("kipler")
        if t.tag_ in ("JJR", "RBR", "JJS", "RBS"): y.add("karşılaştırma")
        if t.dep_ == "relcl": y.add("ilgi cümlesi")
        if t.dep_ == "mark" and t.lemma_ in ("if", "unless"): y.add("koşul")
        if t.tag_ in ("VBZ", "VBP") and t.lemma_ != "be": y.add("geniş zaman")
    if sent.strip().endswith("?"): y.add("soru")
    return y


def fsrs_simulasyon(gunler, n=4000, hedef_gunler=(30, 90, 180), adaptif=False):
    """Sabit takvim (sesli kurs: geri bildirim yok) ile FSRS hafıza modelinde ortalama hatırlama olasılığı.
    Hatırlanamayan tekrar 'Again' sayılır (ses doğru cevabı yine de verir = yeniden öğrenme)."""
    from fsrs import Scheduler, Card, Rating
    s = Scheduler(enable_fuzzing=False, desired_retention=0.9)
    t0 = datetime(2026, 1, 1, tzinfo=timezone.utc); rnd = random.Random(1)
    sonuc = {g: [] for g in hedef_gunler}
    for _ in range(n):
        c = Card(); c, _ = s.review_card(c, Rating.Good, t0); c, _ = s.review_card(c, Rating.Good, t0 + timedelta(minutes=10))
        olaylar = sorted([(g, "olc") for g in hedef_gunler] + ([] if adaptif else [(g, "tekrar") for g in gunler]),
                         key=lambda z: (z[0], z[1] == "tekrar"))
        sonraki = c.due if adaptif else None
        for g, tur in olaylar:
            now = t0 + timedelta(days=g)
            while adaptif and sonraki <= now:
                r = s.get_card_retrievability(c, sonraki)
                c, _ = s.review_card(c, Rating.Good if rnd.random() < r else Rating.Again, sonraki); sonraki = c.due
            if tur == "olc":
                sonuc[g].append(s.get_card_retrievability(c, now))
            else:
                r = s.get_card_retrievability(c, now)
                c, _ = s.review_card(c, Rating.Good if rnd.random() < r else Rating.Again, now)
    return {g: round(float(np.mean(v)), 3) for g, v in sonuc.items()}


if __name__ == "__main__":
    rapor = {"dersler": []}
    for dizi, ids in icerik.DIZILER.items():
        bilinen = set()
        for i, x in enumerate(ids, 1):
            d = icerik._ID[x]
            ev = motor.plan(d, icerik.isinma_icin(d)); gun = motor.plan_gunluk(d)
            z = zaman_dokumu(ev); toplam = sum(z.values())
            yeni = kelime_lemmalari(d); bilinen |= yeni
            hik = [c.split("|", 1)[1] if "|" in c else c for c in d["hikaye"]]
            k1, bil1 = kapsam(hik, bilinen)                       # yalnız derste öğretilenler
            k2, bil2 = kapsam(hik, bilinen | FONKSIYON)            # + temel işlev kelimeleri
            # sınav/iş dizisi: dersin seviyesinin altındaki CEFR kelimeleri bilindiği varsayılır
            sev = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "IELTS-AWL": 4, "YDS": 4, "BA": 4}[d["seviye"]]
            tok = [t for m in hik for t in lemmalar(m)]
            ustu = [t.lemma_.lower() for t in tok if t.pos_ != "PROPN" and (cefr.get_average_word_level_float(t.lemma_.lower()) or 0) > sev + 0.5 and t.lemma_.lower() not in yeni]
            # tekrar sayıları (yeni kelimeler)
            say_duy = collections.Counter(); say_cag = collections.Counter()
            for e in ev + gun:
                if e[0] == "E":
                    m = e[1].lower()
                    for k in d["kelimeler"]:
                        if re.search(r"\b" + re.escape(k["en"].lower()), m): say_duy[k["en"]] += 1
            for j, e in enumerate(ev + gun):
                if e[0] == "T":
                    for k in d["kelimeler"]:
                        if e[1] == k["tr"]:
                            nxt = (ev + gun)[j + 1:j + 4]
                            if any(n[0] == "S" and n[1] >= 3 for n in nxt): say_cag[k["en"]] += 1
            # konuşma hızı: hikâyenin ilk okunuşu
            hs = d["hikaye_sesi"]; kel = sum(len(m.split()) for m in hik)
            sn = sum(sure_en(m, d.get("konusmacilar", {}).get(c.split("|", 1)[0], hs) if "|" in c else hs, 0.92 if d["seviye"] in ("A1", "A2") else 1.0) for c, m in zip(d["hikaye"], hik))
            yapilar = set().union(*[yapi(m) for m in hik])
            metin = " ".join(hik)
            rapor["dersler"].append({
                "dizi": dizi, "sira": i, "id": d["id"], "dk": round(toplam / 60, 1),
                "tr_pay": round(z["tr"] / toplam, 3), "en_pay": round(z["en"] / toplam, 3), "ogrenci_pay": round(z["ogrenci"] / toplam, 3),
                "kapsam_ogretilen": round(k1, 3), "kapsam_islevli": round(k2, 3), "bilinmeyen_ornek": bil2[:12], "bilinmeyen_sayi": len(bil2),
                "seviye_ustu_oran": round(len(ustu) / max(1, len(tok)), 3), "seviye_ustu": sorted(set(ustu))[:10],
                "duyma_ort": round(np.mean([say_duy[k["en"]] for k in d["kelimeler"]]), 1),
                "duyma_min": min(say_duy[k["en"]] for k in d["kelimeler"]),
                "geri_cagirma_ort": round(np.mean([say_cag[k["en"]] for k in d["kelimeler"]]), 1),
                "wpm": round(kel / sn * 60), "wpm_duraklamali": round(kel / (sn + 0.45 * len(hik)) * 60), "fk_sinif": round(textstat.flesch_kincaid_grade(metin), 1),
                "mtld": round(LexicalRichness(metin).mtld(), 1) if len(metin.split()) > 60 else None,
                "yapilar": sorted(yapilar)})
            print(d["id"], rapor["dersler"][-1]["kapsam_islevli"], rapor["dersler"][-1]["wpm"], flush=True)
    ar = motor.fsrs_araliklari()
    rapor["fsrs"] = {
        "sabit_takvim_1_4_12_31": fsrs_simulasyon([1, 4, 12, 31]),
        "sabit_takvim_tam_1_4_12_31_74_163": fsrs_simulasyon([1, 4, 12, 31, 74, 163]),
        "yalniz_ders": fsrs_simulasyon([]),
        "adaptif_fsrs_anki": fsrs_simulasyon([], adaptif=True)}
    json.dump(rapor, open("/home/claude/kurs/degerlendirme.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(rapor["fsrs"], ensure_ascii=False))
