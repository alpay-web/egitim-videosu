"""Seslendirmeyi Whisper ile yazıya döküp senaryoyla karşılaştırır; yanlış okunan kelimeleri raporlar.
Kullanım: python denetle.py senaryo.json ses_klasoru rapor.txt [model]"""
import difflib, json, re, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from video_uret import cumlelere_bol  # noqa

def norm(t):
    t = unicodedata.normalize("NFC", t).replace("İ", "i").replace("I", "ı").lower()
    t = re.sub(r"[^\wçğıöşü' ]+", " ", t)
    return t.split()

sen = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
klasor, rapor = Path(sys.argv[2]), Path(sys.argv[3])
model_adi = sys.argv[4] if len(sys.argv) > 4 else "medium"
from faster_whisper import WhisperModel
m = WhisperModel(model_adi, device="cpu", compute_type="int8")
satirlar, sorunlar = [], []
for si, sh in enumerate(sen["sahneler"]):
    for ci, c in enumerate(cumlelere_bol(sh["anlatim"])):
        dosya = next(iter(sorted(klasor.glob(f"{si + 1:02d}_{ci:02d}.*"))), None)
        if not dosya:
            continue
        segs, _ = m.transcribe(str(dosya), language="tr", beam_size=5, initial_prompt=None)
        duyulan = " ".join(s.text.strip() for s in segs)
        a, b = norm(c), norm(duyulan)
        sm = difflib.SequenceMatcher(a=a, b=b)
        farklar = [f"'{' '.join(a[i1:i2])}' → '{' '.join(b[j1:j2])}'" for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
        oran = sm.ratio()
        satirlar.append(f"{dosya.stem}\t{oran:.2f}\tMETİN: {c}\n\t\tDUYULAN: {duyulan}\n\t\tFARK: {'; '.join(farklar)}\n")
        if farklar:
            sorunlar.append((oran, dosya.stem, farklar))
        print(dosya.stem, f"{oran:.2f}", "; ".join(farklar), flush=True)
sorunlar.sort()
ozet = ["EN SORUNLU CÜMLELER (benzerlik düşükten yükseğe):"] + [f"{s}\t{o:.2f}\t{'; '.join(f)}" for o, s, f in sorunlar]
rapor.write_text("\n".join(ozet) + "\n\n=== AYRINTI ===\n" + "\n".join(satirlar), encoding="utf-8")
