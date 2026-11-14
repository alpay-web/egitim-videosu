"""
Fotoğraf/görsel tabanlı konuşan karakter.

Tek bir portre görselinden (arka planı otomatik silinir) şu varyasyonları üretir:
  - ağız açıklığı 0..N (çene aşağı bükülür, ağız içi koyu renkle doldurulur)
  - göz kırpma (göz kapağı göz akının üstünden iner)
Yüz noktaları karakter.json içinde verilir (görsel pikseli cinsinden):
  {"agiz": [cx, cy, yari_genislik, gulus_egrisi], "cene_alt": y,
   "gozler": [[cx, cy, rx, ry], [cx, cy, rx, ry]], "kapak_renk": [r, g, b] (opsiyonel),
   "boyun": y (baş hareketinin döndüğü nokta)}
"""
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def arka_plan_sil(girdi, cikti):
    from rembg import new_session, remove
    im = Image.open(girdi).convert("RGB")
    out = remove(im, session=new_session("isnet-general-use"))
    out.save(cikti)
    return out


def _ornek_renk(arr, x, y, r=4):
    p = arr[max(0, y - r):y + r, max(0, x - r):x + r, :3].reshape(-1, 3)
    return tuple(int(v) for v in np.median(p, axis=0))


class FotoKarakter:
    def __init__(self, png_yolu, json_yolu, hedef_yukseklik):
        self.cfg = json.loads(Path(json_yolu).read_text(encoding="utf-8"))
        im = Image.open(png_yolu).convert("RGBA")
        s = hedef_yukseklik / im.height
        self.s = s
        self.im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        self.arr = np.asarray(self.im).astype(np.float32)
        c = self.cfg
        k = lambda v: v * s
        self.agiz = [k(c["agiz"][0]), k(c["agiz"][1]), k(c["agiz"][2]), k(c["agiz"][3])]
        self.cene = k(c["cene_alt"])
        self.gozler = [[k(v) for v in g] for g in c["gozler"]]
        self.boyun = k(c.get("boyun", c["cene_alt"] + 40))
        a8 = np.asarray(self.im)
        self.kapaklar = [tuple(c["kapak_renk"]) if "kapak_renk" in c else
                         _ornek_renk(a8, int(g[0]), int(g[1] - g[3] - 5 * s), r=max(2, int(3 * s)))
                         for g in self.gozler]
        self.cache = {}

    # ------------------------------------------------------------ ağız
    def _agiz_ac(self, arr, D):
        if D <= 0.5:
            return arr
        H, W, _ = arr.shape
        cx, cy, yg, egri = self.agiz
        x0, x1 = int(cx - yg - 4), int(cx + yg + 5)
        y_alt = int(min(H - 1, self.cene + (self.cene - cy) * 1.2))
        xs = np.arange(x0, x1)
        u = np.clip(1 - ((xs - cx) / yg) ** 2, 0, 1)
        d = D * u ** 0.9                                      # dudak açıklık profili
        y0 = cy - egri * (1 - u)                              # gülüş eğrisi (köşeler yukarıda)
        ys = np.arange(int(cy - egri - 2), y_alt)[:, None]
        # çeneye kadar tam, sonra boyuna doğru sönen kaydırma
        f = np.clip(1 - (ys - self.cene) / max(1, (y_alt - self.cene)), 0, 1)
        f = np.where(ys < self.cene, 1.0, f ** 1.5)
        kay = d[None, :] * f
        kaynak = ys - kay
        alt = (ys > y0[None, :])
        kaynak = np.where(alt, kaynak, ys)
        bosluk = alt & (kaynak < y0[None, :])               # ağzın içi
        kaynak_c = np.clip(kaynak, 0, H - 1)
        y_lo = np.floor(kaynak_c).astype(int)
        y_hi = np.minimum(y_lo + 1, H - 1)
        w = (kaynak_c - y_lo)[..., None]
        bolge = arr[y_lo, xs[None, :]] * (1 - w) + arr[y_hi, xs[None, :]] * w
        # ağız içi: koyu kırmızı -> alt kısımda dil
        derin = np.clip((ys - y0[None, :]) / np.maximum(kay, 1), 0, 1)[..., None]
        derin = derin ** 2.2
        ic = np.array([48, 14, 20, 255], np.float32) * (1 - derin) + np.array([150, 62, 72, 255], np.float32) * derin
        ic[..., :3] *= (0.75 + 0.25 * u[None, :, None])
        # kenar yumuşatma
        mask = Image.fromarray((bosluk * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
        m = (np.asarray(mask).astype(np.float32) / 255)[..., None]
        bolge = bolge * (1 - m) + ic * m
        out = arr.copy()
        out[ys[0, 0]:ys[-1, 0] + 1, x0:x1] = bolge
        return out

    # ------------------------------------------------------------ göz kırpma
    def _kirp(self, im, b):
        if b <= 0:
            return im
        im = im.copy()
        for (cx, cy, rx, ry), renk in zip(self.gozler, self.kapaklar):
            x0, y0, x1, y1 = int(cx - rx * 1.25), int(cy - ry * 1.3), int(cx + rx * 1.25) + 1, int(cy + ry * 1.3) + 1
            w, h = x1 - x0, y1 - y0
            ust = (cy - ry * 1.04) - y0
            kenar = ust + (2.08 * ry) * b
            yy = np.arange(h)[:, None].astype(np.float32)
            xx = np.arange(w)[None, :].astype(np.float32)
            elips = (((xx + x0 - cx) / (rx * 1.04)) ** 2 + ((yy + y0 - cy) / (ry * 1.06)) ** 2) <= 1
            # kapağın alt kenarı hafif kavisli (ortası daha aşağıda)
            kav = kenar + ry * 0.12 * b * (1 - ((xx + x0 - cx) / rx) ** 2)
            kapak = elips & (yy <= kav)
            m = Image.fromarray((kapak * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(0.8, rx * 0.04)))
            m = np.asarray(m).astype(np.float32)[..., None] / 255
            # dikey gradyan: üstte deri rengi, kenara yakın hafif koyu
            g = np.clip((yy - ust) / max(1, kav.max() - ust), 0, 1)[..., None]
            rk = np.array(renk, np.float32)[None, None, :]
            col = rk * (1.02 - 0.22 * g ** 2)
            parca = np.asarray(im.crop((x0, y0, x1, y1))).astype(np.float32)
            parca[..., :3] = parca[..., :3] * (1 - m) + col * m
            # kirpik çizgisi
            if b > 0.3:
                cizgi = elips & (np.abs(yy - kav) < max(1.0, ry * 0.07))
                cm = Image.fromarray((cizgi * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))
                cm = np.asarray(cm).astype(np.float32)[..., None] / 255 * 0.85
                parca[..., :3] = parca[..., :3] * (1 - cm) + np.array([60, 38, 32], np.float32) * cm
            im.paste(Image.fromarray(np.clip(parca, 0, 255).astype(np.uint8), "RGBA"), (x0, y0))
        return im

    def kare(self, agiz_seviye, kirp):
        """agiz_seviye: 0..1 (sürekli), kirp: 0..1"""
        a = round(agiz_seviye * 8) / 8
        b = round(kirp * 4) / 4
        k = (a, b)
        if k not in self.cache:
            D = a * self.agiz[2] * 0.5
            arr = self._agiz_ac(self.arr, D)
            im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
            self.cache[k] = self._kirp(im, b)
        return self.cache[k]

    def poz(self, im, t, konusuyor):
        """Hafif baş/gövde hareketi: nefes + yavaş salınım; konuşurken biraz daha canlı."""
        aci = 0.9 * math.sin(t * 0.7) + 0.5 * math.sin(t * 1.9 + 1) * konusuyor
        if abs(aci) < 0.05:
            return im, (0, 0)
        merkez = (im.width / 2, self.boyun)
        r = im.rotate(aci, resample=Image.BICUBIC, center=merkez)
        dy = 2.5 * math.sin(t * 1.3)
        return r, (0, dy)
