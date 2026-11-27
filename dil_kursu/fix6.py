import sys; sys.path.insert(0,'/home/claude/kurs')
import en_ses, icerik, motor, birlestir
trd = birlestir.tr_dizini()
for m, v, h in [("That's out of scope for the MVP.", "am_michael", 1.0), ("we may not run out of solutions.", "am_michael", 0.95),
                ("If we make use of such methods, and take into account the full life cycle of products, we may not run out of solutions.", "am_michael", 1.0)]:
    y = en_ses.CACHE / f"{motor.anahtar(m, v, round(h, 3))}.wav"
    if y.exists(): y.unlink()
    en_ses.uret(m, v, h)
for i in ["BA-05", "YDS-06"]:
    for g in (False, True):
        mp3, s, b = birlestir.birlestir(icerik._ID[i], 0, trd, gunluk=g); print(mp3.name, f"{s/60:.1f}")
