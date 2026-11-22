"""BA serisi senaryo yardımcıları (v02 ve sonrası). Sahne üreticileri, ortak telaffuz, kaydetme."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from video_uret import cumlelere_bol  # noqa: E402

S = []


def m(baslik, maddeler, anlatim, **k):
    S.append({"baslik": baslik, "maddeler": maddeler, "anlatim": anlatim, **k})


def t(baslik, basliklar, satirlar, anlatim, **k):
    S.append({"baslik": baslik, "tur": "tablo", "tablo": {"basliklar": basliklar, "satirlar": satirlar},
              "anlatim": anlatim, **k})


def dikkat(baslik, metin, anlatim, tip="uyari", **k):
    S.append({"baslik": baslik, "tur": "ipucu", "ipucu": {"tip": tip, "metin": metin}, "anlatim": anlatim, **k})


def g(baslik, dosya, odaklar, anlatim, **k):
    S.append({"baslik": baslik, "tur": "gorsel", "gorsel": f"gorseller/{dosya}",
              "odaklar": [{"kutu": b, "etiket": e} for b, e in odaklar], "anlatim": anlatim, **k})


def soru(baslik, metin, secenekler, dogru, anlatim, cevap, **k):
    S.append({"baslik": baslik, "tur": "soru", "soru": {"metin": metin, "secenekler": secenekler, "dogru": dogru,
              "cevap_cumle": len(cumlelere_bol(anlatim)), "bekle": 4}, "anlatim": anlatim + " " + cevap, **k})


TELAFFUZ = {
    "UML": "yu em el", "BPMN": "bi pi em en", "OMG": "o em ci", "CMMN": "si em em en", "DMN": "di em en",
    "KKB": "ka ka be", "KPS": "ka pe se", "MERNİS": "mernis", "MASAK": "masak", "KVKK": "ka ve ka ka",
    "BDDK": "be de de ka", "ÖBF": "ö be fe", "EFT": "e fe te", "OTP": "o te pe", "SMS": "es em es", "STP": "es ti pi",
    "XML": "eks em el", "BPMNDI": "bi pi em en di ay", "DMS": "di em es", "CRM": "si ar em", "ELK": "e le ka",
    "LTV": "el ti vi", "API": "ey pi ay", "SOAP": "soup", "GMY": "genel müdür yardımcısı", "KPI": "key pi ay",
    "XOR": "eks or", "Camunda": "kamunda", "Portal": "portal", "Portal'da": "portalda", "Portal'dan": "portaldan",
    "Portal'a": "portala", "Portal'ın": "portalın", "BA": "be a", "SoD": "es o di", "SQL": "es kyu el", "IAM": "ay ey em",
    "Postman": "post men", "Jira": "cira", "Confluence": "konfluens", "Miro": "miro", "Visio": "vizyo", "Agile": "ecayl",
    "draw.io": "dro ay o", "diagrams.net": "dayagrams nokta net", "PNG": "pi en ci", "SVG": "es vi ci", "PDF": "pi di ef",
    "VS Code": "vi es kod", "Notepad++": "notped artı artı", "ISO": "iso", "BR": "be re", "ID": "ay di",
    "MANUEL_INCELEME": "manuel inceleme", "Ctrl": "kontrol", "Ctrl+S": "kontrol es", "Ctrl+Z": "kontrol zed",
}


def kod_okunus(k):
    harf = {"P": "pe", "U": "u", "W": "dabılyu", "F": "fe", "S": "se", "B": "be", "D": "de", "I": "ı", "G": "ge", "L": "el"}
    rakam = "sıfır bir iki üç dört beş altı yedi sekiz dokuz".split()
    return harf[k[0]] + " " + " ".join(rakam[int(c)] for c in k[1:])


def kaydet(dosya, sen, ek_telaffuz=None):
    tel = {**TELAFFUZ, **(ek_telaffuz or {})}
    metin = " ".join(json.dumps(s, ensure_ascii=False) for s in S)
    for k in sorted(set(re.findall(r"\b([PUWFSBDIGL]\d\d?)\b", metin))):
        tel.setdefault(k, kod_okunus(k))
        for ek, ok in (("'de", "de"), ("'te", "te"), ("'deki", "deki"), ("'teki", "teki"), ("'ye", "ye"), ("'ya", "ya"),
                       ("'den", "den"), ("'ten", "ten"), ("'da", "da"), ("'ta", "ta")):
            tel.setdefault(k + ek, kod_okunus(k) + ok)
    sen = {**sen, "ingilizce_mod": "sozluk", "es": 1.0, "cumle_arasi": 0.7, "sahne_arasi": 1.6, "telaffuz": tel,
           "sahneler": S}
    Path(dosya).with_suffix(".json").write_text(json.dumps(sen, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(S), "sahne", sum(len(s["anlatim"].split()) for s in S), "kelime")
