import sys; sys.path.insert(0, '/home/claude/kurs')
import birlestir, motor, icerik, sinama
trd = birlestir.tr_dizini()
L = icerik._A2e + icerik._Be
T = []
eksik = [c for d in L + T for p in ([d["_plan"]] if "_plan" in d else [motor.plan(d, icerik.isinma_icin(d)), motor.plan_gunluk(d)])
         for c in motor.tr_cumleler(p) if c not in trd and f"{birlestir.TASIYICI} {c}" not in trd]
print("eksik TR:", eksik, flush=True)
for d in L:
    for g in (False, True):
        mp3, s, b = birlestir.birlestir(d, 0, trd, gunluk=g); print(mp3.name, f"{s/60:.1f} dk", flush=True)
for d in T:
    mp3, s, b = birlestir.birlestir(d, 0, trd); print(mp3.name, f"{s/60:.1f} dk", flush=True)
