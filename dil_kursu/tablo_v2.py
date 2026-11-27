import pandas as pd, json, sys
sys.path.insert(0,'.'); import icerik, ba_liste, motor
from wordfreq import zipf_frequency as zf
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
wb=Workbook(); H=PatternFill('solid',fgColor='EEEEEE')
def sayfa(ad,baslik,rows,ilk=False):
    ws=wb.active if ilk else wb.create_sheet(ad); ws.title=ad; ws.append(baslik)
    for c in ws[1]: c.font=Font(bold=True); c.fill=H
    for r in rows: ws.append(r)
    ws.freeze_panes='A2'
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width=min(55,max(9,max(len(str(c.value or '')) for c in col[:300])+2))
    return ws
wa=pd.read_csv('/home/claude/arastirma/designfuchen_word-atlas/data/word-atlas.csv',keep_default_na=False)
en_kol=lambda s: '' if not s else ' ; '.join(p.split('｜')[0].strip() for p in str(s).split(';'))
wa_map={w.lower():(t,c) for w,t,c in zip(wa.word,wa.topic,wa.cefr)}
d=pd.read_csv('/home/claude/kaynak/ox/data/oxford_5000.csv',keep_default_na=False); d['word']=d.word.str.strip()
o={'a1':1,'a2':2,'b1':3,'b2':4,'c1':5}; d['r']=d.cefr.map(o)
g=d.sort_values('r').groupby(d.word.str.lower(),sort=False).agg(word=('word','first'),cefr=('cefr','first'),type=('type',lambda s:', '.join(dict.fromkeys(s))),r=('r','first')).reset_index(drop=True)
g['zipf']=[zf(w,'en') for w in g.word]
g=g.sort_values(['r','zipf'],ascending=[True,False])
ox_cefr={w.lower():c.upper() for w,c in zip(g.word,g.cefr)}
awl=json.load(open('/home/claude/kaynak/academic-word-list-en-tr/words.json')); sub={x['en'].lower():x['sub'] for x in awl}
TR={'education':'eğitim','daily':'günlük yaşam','society':'toplum','thinking':'düşünce','nature':'doğa','work':'iş','health':'sağlık','emotion':'duygu','science':'bilim','travel':'seyahat','economy':'ekonomi','arts':'sanat','technology':'teknoloji','government':'yönetim','city':'şehir','environment':'çevre','history':'tarih','sport':'spor','media':'medya'}
rows=[]; sev={}
for lvl in ['a1','a2','b1','b2','c1']:
    ws=g[g.cefr==lvl].reset_index(drop=True); sev[lvl.upper()]=len(ws)
    for i,r in ws.iterrows():
        w=r.word.lower(); t=wa_map.get(w)
        rows.append([r.word,lvl.upper(),r.type,round(r.zipf,2),'evet' if t else '',TR.get(t[0],'') if t else '',('AWL '+str(sub[w])) if w in sub else '',f"{lvl.upper()}-{i//12+1:02d}"])
pil=[[dd['id'],dd['baslik'],k['en'],k['tr'].rstrip('.'),k['ex'],k['ex_tr'],dd['kaynak']] for dd in icerik.DERSLER for k in dd['kelimeler']]
sayfa('Pilot dersler',['Ders','Konu','İngilizce','Türkçe','Örnek cümle','Türkçesi','Kaynak listesi'],pil,ilk=True)
sayfa('Oxford 5000 (CEFR)',['Kelime','CEFR','Tür','Sıklık (Zipf)','IELTS listesinde','IELTS konusu','Akademik listede','Planlanan ders'],rows)
warows=[[r.word,r.cefr,TR.get(r.topic,r.topic),en_kol(r.synonyms),en_kol(r.antonyms),en_kol(r.collocations),en_kol(r.word_family),r.example2_en] for r in wa.sort_values(['topic','cefr','word']).itertuples()]
sayfa('IELTS (Word Atlas)',['Kelime','CEFR','IELTS konusu','Eş anlamlılar','Zıt anlamlılar','Eşdizimler','Kelime ailesi','IELTS tarzı örnek cümle'],warows)
awrows=[[x['en'],x['sub'],ox_cefr.get(x['en'].lower(),'listede yok'),f"AWL-{i//12+1:02d}"] for i,x in enumerate(sorted(awl,key=lambda x:(x['sub'],x['en'])))]
sayfa('AWL 570 (IELTS-YDS)',['Kelime (başkelime)','Alt liste','Oxford CEFR','Planlanan ders'],awrows)
barows=[]; n=0
for kat,lst in ba_liste.BA.items():
    for en,tr in lst:
        barows.append([en,tr,kat.split('. ',1)[1],round(zf(en.lower(),'en'),2) if ' ' not in en else '',f"BA-{n//12+1:02d}"]); n+=1
sayfa('Senior BA',['İngilizce','Türkçe','Kategori','Sıklık (Zipf)','Planlanan ders'],barows)
ar=motor.fsrs_araliklari()
muf=[[k,v,-(-v//12),'Oxford 3000/5000, kendi içinde sıklığa göre sıralı'] for k,v in sev.items()]
muf+= [['IELTS konu dizisi',len(wa),-(-len(wa)//12),'Word Atlas IELTS listesi; 19 IELTS konusu, eş anlamlı ve eşdizimlerle'],
       ['IELTS-AWL',570,48,'Academic Word List, alt liste 1–10'],
       ['YDS',None,None,'Bağlaçlar, edatlı fiiller, kalıplar; çıkmış soru analizinden derlenecek'],
       ['Senior BA',n,-(-n//12),'BABOK v3 kavramları, Scrum Guide, süreç, finans, toplantı kalıpları']]
ws=sayfa('Müfredat',['Seviye / dizi','Kelime sayısı','Ders sayısı (12 kelime/ders)','Kaynak'],muf)
ws.append([]); ws.append(['Her ders: 12 yeni kelime · ders içi aralıklı hatırlama · örnek cümle · kalıplar · dinleme metni veya diyalog · gölgeleme · sorular · IELTS konuşma, YDS boşluk doldurma ya da toplantı simülasyonu · son tekrar'])
ws.append(['Her dersin yanında: ertesi gün dinlenecek 4–6 dakikalık günlük tekrar kaydı'])
tk=[['Aynı ders (ders içinde)','0','Yeni kelimeden yaklaşık 25 saniye, 2 dakika, 5 dakika ve 15 dakika sonra (Pimsleur kademeli hatırlama)']]
tk+=[[f'{i+1}. tekrar',str(g_),('Günlük tekrar kaydı (ertesi gün)' if i==0 else 'Sonraki dersin başındaki ısınma bölümü' if i<4 else 'Haftalık genel tekrar kaydı')] for i,g_ in enumerate(ar)]
ws=sayfa('Tekrar takvimi',['Tekrar','Kaç ders/gün sonra','Nerede'],tk)
ws.append([]); ws.append(['Aralıklar FSRS algoritmasıyla (open-spaced-repetition/py-fsrs) hedef hatırlama oranı %95 alınarak hesaplandı.'])
gh=json.load(open('gh_tablo.json'))
sayfa('GitHub araştırması',['Depo','Lisans','Durum','Ne için'],gh)
kay=json.load(open('kaynak_tablo.json'))
sayfa('Kaynaklar',['Kaynak','Açıklama','Bağlantı'],kay)
wb.save('kelime_listeleri_v2.xlsx'); print(len(rows),len(warows),len(barows))
