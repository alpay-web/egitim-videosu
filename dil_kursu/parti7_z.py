import sys, json; sys.path.insert(0,"/home/claude/kurs")
import icerik, motor, birlestir
trd=birlestir.tr_dizini(); yeni=[]
YENIDEN=["Bir ceket al.","Onu çöp kutusuna at.","reçel.","Bu ders, kıdemli iş analisti dizisi, on altıncı ders.","Bu ders, B1 seviyesi, on altıncı ders.",
 "Bu ders, C1 seviyesi, on altıncı ders.","gezip görmek.","kıl payı farkla."]
for d in icerik._A2g+icerik._Bg:
    for p in [motor.plan(d, icerik.isinma_icin(d)), motor.plan_gunluk(d)]:
        for c in motor.tr_cumleler(p):
            if (c in YENIDEN or (c not in trd and f"{birlestir.TASIYICI} {c}" not in trd)) and c not in yeni: yeni.append(c)
metin=[f"{birlestir.TASIYICI} {c}" if len(c.split())<=2 else c for c in yeni]
tel=json.load(open("/home/claude/egitim-videosu/senaryolar/dil_kursu/parti7_tr_kadin.json"))["telaffuz"]
sen={"baslik":"dil kursu parti 7 düzeltme","telaffuz":tel,"sahneler":[{"baslik":f"c{i+1}","tur":"metin","metin":m,"anlatim":m} for i,m in enumerate(metin)]}
json.dump(sen,open("/home/claude/egitim-videosu/senaryolar/dil_kursu/parti7_z1.json","w"),ensure_ascii=False,indent=0)
print(len(metin), metin)
