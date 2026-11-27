import sys, re; sys.path.insert(0,'/home/claude/kurs')
import en_ses, icerik, motor, birlestir, motor, asr, soundfile as sf
d = icerik._ID["A2-23"]; trd = birlestir.tr_dizini()
for p in [motor.plan(d, icerik.isinma_icin(d)), motor.plan_gunluk(d)]:
    for e in p:
        if e[0] == "E" and ("Ayşe" in e[1] or re.search(r"\bCan(?=( was| is|,| isn't| good))", e[1])):
            y = en_ses.CACHE / f"{motor.anahtar(e[1], e[2], round(e[3], 3))}.wav"
            if y.exists(): y.unlink()
            y = en_ses.uret(e[1], e[2], e[3]); a, _ = sf.read(y, dtype="float32"); print(e[1], "->", asr.duy(a))
for g in (False, True):
    mp3, s, b = birlestir.birlestir(d, 0, trd, gunluk=g); print(mp3.name, f"{s/60:.1f}")
