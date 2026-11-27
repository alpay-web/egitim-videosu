# -*- coding: utf-8 -*-
"""Kursun kelimeleri için Anki destesi (genanki, MIT). Ses: kurstaki İngilizce kliplerin aynısı.
Her not iki kart üretir: Türkçe → İngilizce (üretim) ve İngilizce ses → Türkçe (tanıma).
Tekrar zamanlamasını Anki'nin FSRS ayarı yapar (Deste seçenekleri → FSRS)."""
import subprocess, sys, hashlib
from pathlib import Path
sys.path.insert(0, "/home/claude/kurs")
import genanki, icerik, en_ses

CIKTI = Path("/home/claude/kurs/anki"); CIKTI.mkdir(exist_ok=True)
MEDYA = CIKTI / "medya"; MEDYA.mkdir(exist_ok=True)

model = genanki.Model(
    1607392319, "Sesli İngilizce Kursu",
    fields=[{"name": n} for n in ("Ingilizce", "Turkce", "Ornek", "OrnekTR", "SesKelime", "SesOrnek", "Ders")],
    templates=[
        {"name": "Türkçe → İngilizce",
         "qfmt": '<div class="tr">{{Turkce}}</div><div class="ip">İngilizcesini sesli söyleyin.</div>',
         "afmt": '{{FrontSide}}<hr id="answer"><div class="en">{{Ingilizce}}</div>{{SesKelime}}'
                 '<div class="ex">{{Ornek}}</div><div class="extr">{{OrnekTR}}</div>{{SesOrnek}}<div class="d">{{Ders}}</div>'},
        {"name": "İngilizce ses → Türkçe",
         "qfmt": '{{SesKelime}}<div class="ip">Dinleyin. Anlamını sesli söyleyin.</div>',
         "afmt": '{{FrontSide}}<hr id="answer"><div class="en">{{Ingilizce}}</div><div class="tr">{{Turkce}}</div>'
                 '<div class="ex">{{Ornek}}</div>{{SesOrnek}}<div class="d">{{Ders}}</div>'},
    ],
    css=".card{font-family:-apple-system,Segoe UI,Roboto,sans-serif;font-size:22px;text-align:center;color:#222;background:#fff}"
        ".en{font-size:30px;font-weight:600;margin:12px}.tr{font-size:24px;margin:10px}.ex{margin-top:16px;font-style:italic}"
        ".extr{color:#666;font-size:18px}.ip{color:#888;font-size:16px;margin-top:10px}.d{color:#aaa;font-size:13px;margin-top:18px}"
        ".nightMode .card{background:#1e1e1e;color:#eee}")


def mp3(metin, ses, hiz):
    wav = en_ses.uret(metin, ses, hiz)
    ad = "kurs_" + hashlib.sha1(f"{metin}|{ses}|{hiz}".encode()).hexdigest()[:12] + ".mp3"
    hedef = MEDYA / ad
    if not hedef.exists():
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-ac", "1", "-b:a", "48k", str(hedef)], check=True)
    return hedef


paket_dosyalar = []
ust = genanki.Deck(2059400110, "Sesli İngilizce Kursu")
desteler = [ust]
for dizi, ad in (("genel", "Genel İngilizce"), ("sinav_is", "Sınav ve İş")):
    alt = genanki.Deck(int(hashlib.sha1(dizi.encode()).hexdigest()[:8], 16), f"Sesli İngilizce Kursu::{ad}")
    desteler.append(alt)
    for x in icerik.DIZILER[dizi]:
        d = icerik._ID[x]; v1, v2 = d["sesler"]
        for k in d["kelimeler"]:
            a = mp3(k["en"], v2, d["en_hiz"]); b = mp3(k["ex"], v1, d["ornek_hiz"])
            paket_dosyalar += [str(a), str(b)]
            alt.add_note(genanki.Note(model=model, guid=genanki.guid_for(d["id"], k["en"]),
                fields=[k["en"], k["tr"].rstrip("."), k["ex"], k["ex_tr"], f"[sound:{a.name}]", f"[sound:{b.name}]",
                        f"{icerik.sira_no(d)} · {d['baslik']}"], tags=[dizi, d["id"]]))
pk = genanki.Package(desteler); pk.media_files = sorted(set(paket_dosyalar))
yol = CIKTI / "Sesli_Ingilizce_Kursu_kelimeler.apkg"; pk.write_to_file(str(yol))
print(yol, sum(len(dk.notes) for dk in desteler), "not")
