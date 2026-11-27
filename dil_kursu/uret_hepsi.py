import sys; sys.path.insert(0,'/home/claude/kurs')
import birlestir, motor, icerik
trd=birlestir.tr_dizini()
eksik=[]
for d in icerik.DERSLER:
    for c in motor.tr_cumleler(motor.plan(d, icerik.isinma_icin(d)))+motor.tr_cumleler(motor.plan_gunluk(d)):
        if c not in trd and f"{birlestir.TASIYICI} {c}" not in trd: eksik.append(c)
print('eksik TR:', eksik, flush=True)
sec=sys.argv[1:] or [d['id'] for d in icerik.DERSLER]
for d in icerik.DERSLER:
    if d['id'] not in sec: continue
    for g in (False, True):
        mp3,s,b=birlestir.birlestir(d,0,trd,gunluk=g); print(mp3.name, f"{s/60:.1f} dk", flush=True)
