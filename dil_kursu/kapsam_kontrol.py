"""A1 hikâye ve İngilizce dinleme kapsamı: bilinen = önceki + bugünkü kelimeler + yapı kelimeleri + temel işlev kelimeleri (spaCy lemma)."""
import sys, spacy
sys.path.insert(0, "/home/claude/kurs")
import parti1_a, parti2_a, icerik
from degerlendir import FONKSIYON
nlp = spacy.load("en_core_web_sm")
def lem(m): return [t for t in nlp(m) if t.is_alpha]
dersler = [icerik._ID["A1-01"]] + parti1_a.A1 + parti2_a.A1
bil = set(FONKSIYON); hedef = float(sys.argv[1]) if len(sys.argv) > 1 else 0.95
for d in dersler:
    for k in d["kelimeler"]:
        bil |= {t.lemma_.lower() for t in nlp(k["en"]) if t.is_alpha} | {k["en"].lower()}
    bil |= set((d.get("yapi") or {}).get("bilinen", []))
    if d.get("ders_no", 1) < 14: continue
    for ad, ml in (("hikaye", d["hikaye"]), ("dinleme_en", d.get("dinleme_en", []))):
        ml = [c.split("|", 1)[1] if "|" in c and c.split("|",1)[0].isupper() else c for c in ml]
        tok = [t for m in ml for t in lem(m)]
        ok = [t for t in tok if t.lemma_.lower() in bil or t.text.lower() in bil or t.pos_ == "PROPN" or t.like_num]
        bilm = sorted({t.lemma_.lower() for t in tok if t not in ok})
        k = len(ok) / len(tok)
        print(f"{d['id']} {ad:10s} {k:.3f} {'OK ' if k >= hedef else 'DÜŞÜK'} {len(tok)} kelime | {', '.join(bilm)}")
