import sys, json; sys.path.insert(0,"/home/claude/kurs")
import icerik, motor, birlestir, sinama
trd=birlestir.tr_dizini(); yeni=[]; gor=set()
for d in icerik._A2d+icerik._Bd:
    pl = [d['_plan']] if '_plan' in d else [motor.plan(d, icerik.isinma_icin(d)), motor.plan_gunluk(d)]
    for c in [c for p in pl for c in motor.tr_cumleler(p)]:
        if c in trd or f"{birlestir.TASIYICI} {c}" in trd or c in gor: continue
        gor.add(c); yeni.append(c)
metin=[f"{birlestir.TASIYICI} {c}" if len(c.split())<=2 else c for c in yeni]
tel=json.load(open("/home/claude/egitim-videosu/senaryolar/dil_kursu/parti1_tr_kadin.json"))["telaffuz"]
tel.update({"Green": "Grin", "Kate": "Keyt", "Scrum": "Skram", "podcast'inden": "podkestinden", "Mr Brown": "Mister Braun", "Jack": "Cek", "Tom'un": "Tomun"})
sen={"baslik":"dil kursu parti 4 kadın ses","telaffuz":tel,
     "sahneler":[{"baslik":f"c{i+1}","tur":"metin","metin":m,"anlatim":m} for i,m in enumerate(metin)]}
json.dump(sen,open("/home/claude/egitim-videosu/senaryolar/dil_kursu/parti4_tr_kadin.json","w"),ensure_ascii=False,indent=0)
print(len(metin), sum(m.startswith("Türkçesi") for m in metin))
