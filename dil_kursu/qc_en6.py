import json, re, difflib, sys
import numpy as np, soundfile as sf
sys.path.insert(0,'/home/claude/kurs')
import icerik, motor, asr, en_ses
seen={}; kotu=[]
for d in icerik._A2e+icerik._Be:
    for x in motor.plan(d, icerik.isinma_icin(d))+motor.plan_gunluk(d):
        if x[0]=="E" and len(x[1].split())>3:
            seen[(x[1],x[2],x[3])]=1
SAY={"1773":"seventeen seventy three"}
def n(t):
    t=t.lower().replace("’","'").replace("-"," ")
    t=re.sub(r"\b(\d+)\b", lambda m: m.group(1), t)
    return re.sub(r"[^a-z0-9' ]+"," ",t).split()
for (m,v,h) in seen:
    y=en_ses.uret(m,v,h); x,sr=sf.read(y,dtype='float32'); hd=asr.duy(x)
    r=difflib.SequenceMatcher(None,n(m),n(hd)).ratio()
    if r<0.85: kotu.append((round(r,2),m,hd,v))
for k in sorted(kotu): print(k)
print(len(seen),'uzun klip,',len(kotu),'şüpheli')
