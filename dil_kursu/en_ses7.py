import sys, json; sys.path.insert(0, "/home/claude/kurs")
import en_ses, icerik, motor, sinama
L = icerik._A2g + icerik._Bg
for d in L:
    pl = [d["_plan"]] if "_plan" in d else [motor.plan(d, icerik.isinma_icin(d)), motor.plan_gunluk(d)]
    for x in [x for p in pl for x in p]:
        if x[0] == "E": en_ses.uret(x[1], x[2], x[3])
    json.dump(en_ses.secim, open(en_ses.SECIM, "w"), ensure_ascii=False, indent=0)
    print(d["id"], "tamam", flush=True)
