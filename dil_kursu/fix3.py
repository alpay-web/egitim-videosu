import sys; sys.path.insert(0,'/home/claude/kurs')
import en_ses, icerik, motor, birlestir, asr, difflib, re, soundfile as sf
trd = birlestir.tr_dizini()
for x in ["A2-04", "A2-11", "BA-08"]:
    d = icerik._ID[x]
    for p in [motor.plan(d, icerik.isinma_icin(d)), motor.plan_gunluk(d)]:
        for e in p:
            if e[0] == "E": en_ses.uret(e[1], e[2], e[3])
for m, v in [("No, there aren't any onions.", "bm_lewis"), ("We prioritised the requirements using Moscow.", "am_michael")]:
    y = en_ses.uret(m, v, 1.0 if "Moscow" not in m else 0.9); a, _ = sf.read(y, dtype="float32"); print(m, "->", asr.duy(a))
for x in ["A2-04", "A2-11", "BA-08"]:
    for g in (False, True):
        mp3, s, b = birlestir.birlestir(icerik._ID[x], 0, trd, gunluk=g); print(mp3.name, f"{s/60:.1f}", flush=True)
