import sys; sys.path.insert(0,'/home/claude/kurs')
import en_ses, icerik, motor, birlestir
trd = birlestir.tr_dizini()
for x in ["B2-09", "B2-11", "B2-12", "C1-13"]:
    d = icerik._ID[x]
    for p in [motor.plan(d, icerik.isinma_icin(d)), motor.plan_gunluk(d)]:
        for e in p:
            if e[0] == "E": en_ses.uret(e[1], e[2], e[3])
    for g in (False, True):
        mp3, s, b = birlestir.birlestir(d, 0, trd, gunluk=g); print(mp3.name, f"{s/60:.1f}", flush=True)
