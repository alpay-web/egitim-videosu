"""Karakter yüzünü yerel olarak yeniden çizer (inpainting): ağız (gülümseme -> nötr) ve gözler.
Kullanım: python yuz_duzenle.py girdi.png yuz.json cikti_klasoru [aday_sayisi]
yuz.json: {"kirp": [x0, y0, boyut], "agiz": [cx, cy, rx, ry], "gozler": [[cx, cy, rx, ry], ...]}
"""
import json, sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFilter
from diffusers import StableDiffusionInpaintPipeline

girdi, cfg, cikti = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()), Path(sys.argv[3])
n = int(sys.argv[4]) if len(sys.argv) > 4 else 4
cikti.mkdir(parents=True, exist_ok=True)
torch.set_num_threads(4)

pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "Lykon/dreamshaper-8-inpainting", torch_dtype=torch.float32, safety_checker=None)
pipe.set_progress_bar_config(disable=True)

im = Image.open(girdi).convert("RGB")
x0, y0, b = cfg["kirp"]
S = 512
kirp = im.crop((x0, y0, x0 + b, y0 + b)).resize((S, S), Image.LANCZOS)
olc = S / b


def maske(elipsler, buyut=1.0, yumusak=6):
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    for cx, cy, rx, ry in elipsler:
        cx, cy, rx, ry = (cx - x0) * olc, (cy - y0) * olc, rx * olc * buyut, ry * olc * buyut
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    return m.filter(ImageFilter.GaussianBlur(yumusak))


STIL = "3d pixar style animated character, elderly professor, soft studio lighting, high quality render"
NEG = "deformed, blurry, ugly, extra teeth, distorted, low quality, realistic photo"
agiz_m = maske([cfg["agiz"]], 1.0, 9)
goz_m = maske(cfg["gozler"], 1.0, 5)


def uygula(resim, m, prompt, neg, tohum, guc):
    g = torch.Generator().manual_seed(tohum)
    out = pipe(prompt=f"{prompt}, {STIL}", negative_prompt=f"{neg}, {NEG}", image=resim, mask_image=m,
               num_inference_steps=30, guidance_scale=7.0, strength=guc, generator=g, height=S, width=S).images[0]
    # yalnızca maske içini al (kenarları orijinalle yumuşak birleştir)
    return Image.composite(out, resim, m)


sonuclar = []
for i in range(n):
    r = uygula(kirp, agiz_m,
               "serious thoughtful expression, mouth closed in a straight neutral line, relaxed cheeks, thick white mustache, no smile",
               "smile, smiling, grin, teeth, open mouth, laughing, raised cheeks, happy", 300 + i, 1.0)
    r = uygula(r, goz_m,
               "wise calm eyes, normal small size, slightly narrowed, relaxed upper eyelids, brown iris, looking straight at the viewer",
               "bulging eyes, big eyes, crazy eyes, wide open eyes, cross-eyed, staring, blue eyes", 400 + i, 0.95)
    tam = im.copy()
    tam.paste(r.resize((b, b), Image.LANCZOS), (x0, y0))
    tam.save(cikti / f"aday_{i + 1}.png")
    sonuclar.append(r)
    print("aday", i + 1, "hazır", flush=True)

# karşılaştırma görseli: orijinal + adaylar (yüz yakın plan)
kare = 384
sheet = Image.new("RGB", (kare * (n + 1), kare + 40), (30, 30, 30))
d = ImageDraw.Draw(sheet)
for j, r in enumerate([kirp] + sonuclar):
    sheet.paste(r.resize((kare, kare)), (j * kare, 40))
    d.text((j * kare + 10, 10), "orijinal" if j == 0 else f"aday {j}", fill=(255, 255, 255))
sheet.save(cikti / "karsilastirma.png")
