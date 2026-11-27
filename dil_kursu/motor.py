# -*- coding: utf-8 -*-
"""Sesli ders motoru.
Yöntem: Pimsleur'un kademeli aralıklı hatırlama + beklenti ilkesi (sor → duraklama → doğru cevap),
aktif geri çağırma (TR→EN üretim, EN→TR tanıma), bağlam içinde örnek cümle, gölgeleme (shadowing),
anlaşılır girdi (seviyeye uygun hikâye), eşdizimler ve sınav formatında pratik (IELTS konuşma, YDS boşluk).

Olay listesi:
  ("T", metin)                     Türkçe anlatıcı (Chatterbox, Actions'ta üretilir)
  ("E", metin, ses, hiz)           İngilizce (Kokoro, yerel)
  ("S", saniye)                    sessizlik
  ("R", kat, taban)                tekrar duraklaması = kat × önceki klibin süresi + taban
  ("B",)                           sinyal sesi (boşluk)
  ("BOLUM", ad)                    bölüm işareti (ID3 bölüm/zaman çizelgesi için)
"""
import hashlib, json, random, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, "/home/claude/egitim-videosu/scripts")
from video_uret import cumlelere_bol  # noqa: E402  (senaryoyla aynı cümle bölme)

KOK = Path("/home/claude/kurs")
SR = 24000

SABIT = {
    "hosgeldin": "İngilizce sesli kursa hoş geldiniz.",
    "on_iki": "Bugün on iki yeni kelime öğreneceksiniz.",
    "kural1": "Kural basit: İngilizce bir kelime ya da cümle duyduğunuzda, duraklamada yüksek sesle tekrar edin.",
    "kural2": "Size bir soru sorduğumda cevabı duraklamada sesli söyleyin, sonra doğrusunu dinleyip kendinizi kontrol edin.",
    "kural3": "Hata yapmaktan korkmayın. Hatırlamaya çalışmak, öğrenmenin ta kendisidir.",
    "basla": "Hadi başlayalım.",
    "ilk": "İlk kelime.",
    "yeni": "Yeni kelime.",
    "sonraki": "Sıradaki kelime.",
    "ornek": "Örnek cümle.",
    "siz_tekrar": "Şimdi siz tekrar edin.",
    "hatirla": "Hatırlayalım.",
    "ingilizcesi": "İngilizcesi nedir?",
    "grup_tekrar": "Şimdi son öğrendiğimiz kelimeleri soruyorum. Türkçesini duyunca İngilizcesini sesli söyleyin.",
    "eski_tekrar": "Biraz daha önceki kelimelere dönelim.",
    "kalip_giris": "Şimdi bu kelimelerle sık kullanılan kalıplara bakalım. Kalıpları bir bütün olarak öğrenmek hem konuşmanızı hem de okumanızı hızlandırır.",
    "hikaye_tekrar": "Şimdi metni ikinci kez dinleyeceksiniz. Bu kez her bölümden sonra bir duraklama olacak.",
    "golge": "Konuşmacıyla aynı vurgu ve tonlamayla sesli tekrar edin. Bu tekniğe gölgeleme denir.",
    "soru_tr": "Şimdi metinle ilgili üç soru. Önce Türkçesini, sonra İngilizcesini duyacaksınız. Cevabı İngilizce söyleyin.",
    "soru_en": "Şimdi metinle ilgili üç soru. Soruları İngilizce dinleyin ve İngilizce cevap verin.",
    "secenekler": "Seçenekler.",
    "cevap_soyle": "Doğru seçeneği sesli söyleyin.",
    "karisik": "Şimdi bugünkü bütün kelimeleri karışık sırayla soruyorum. Türkçesini duyunca İngilizcesini sesli söyleyin.",
    "ters": "Şimdi tersini yapalım. İngilizce kelimeyi duyacaksınız; Türkçe anlamını sesli söyleyin.",
    "bitis1": "Harika bir iş çıkardınız. Bugünkü dersi tamamladınız.",
    "bitis2": "En iyi sonuç için bu dersi yarın bir kez daha dinleyin.",
    "bitis3": "Bu kelimeleri yarınki günlük tekrarda ve sonraki derslerin başında yeniden soracağım. Böylece kalıcı hafızanıza yerleşecekler.",
    "isinma": "Önce önceki derslerden bazı kelimeleri hatırlayalım. Türkçesini duyunca İngilizcesini sesli söyleyin.",
    "isinma_bitti": "Güzel. Şimdi bugünkü yeni kelimelere geçiyoruz.",
    "bitis4": "Görüşmek üzere.",
}
HARF = "ABCDE"


def T(m): return ("T", m)
def S(s): return ("S", s)
def R(k=1.6, t=0.8): return ("R", k, t)


def gruplar(d):
    n = d.get("gruplar") or [3] * (len(d["kelimeler"]) // 3)
    out, i = [], 0
    for g in n:
        out.append(list(range(i, i + g))); i += g
    assert i == len(d["kelimeler"])
    return out


def karisik(seq, tohum):
    s = list(seq); random.Random(tohum).shuffle(s); return s


def parcala(cumle, uzun=13):
    """Gölgeleme için uzun cümleyi noktalama yerlerinden makul parçalara böler."""
    if len(cumle.split()) <= uzun:
        return [cumle]
    parcalar = re.split(r"(?<=[,;:])\s+", cumle)
    out = []
    for p in parcalar:
        if out and (len(p.split()) < 4 or len(out[-1].split()) < 4):
            out[-1] += " " + p
        else:
            out.append(p)
    return out


def karma(seq, d, ses=0):
    """'T|..' / 'E|..' dizisini olaylara çevirir."""
    out = []
    for s in seq:
        tur, m = s.split("|", 1)
        if tur == "T":
            out.append(T(m))
        else:
            out.append(("E", m, d["sesler"][ses], d["ornek_hiz"]))
    return out


ON = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
ONLAR = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
SIRA_SON = {"bir": "birinci", "iki": "ikinci", "üç": "üçüncü", "dört": "dördüncü", "beş": "beşinci", "altı": "altıncı",
            "yedi": "yedinci", "sekiz": "sekizinci", "dokuz": "dokuzuncu", "on": "onuncu", "yirmi": "yirminci",
            "otuz": "otuzuncu", "kırk": "kırkıncı", "elli": "ellinci", "altmış": "altmışıncı", "yetmiş": "yetmişinci",
            "seksen": "sekseninci", "doksan": "doksanıncı", "yüz": "yüzüncü"}


def sira_tr(n):
    """1 → birinci, 13 → on üçüncü, 120 → yüz yirminci."""
    y, k = divmod(n, 100); o, b = divmod(k, 10)
    parca = ([(ON[y] + " " if y > 1 else "") + "yüz"] if y else []) + ([ONLAR[o]] if o else []) + ([ON[b]] if b else [])
    parca[-1] = SIRA_SON[parca[-1].split()[-1]] if " " not in parca[-1] else parca[-1].rsplit(" ", 1)[0] + " " + SIRA_SON[parca[-1].split()[-1]]
    return " ".join(parca)


def plan(d, isinma=None):
    v1, v2 = d["sesler"]
    hz, ohz, bek = d["en_hiz"], d["ornek_hiz"], d["bekle"]
    K = d["kelimeler"]
    ev = []
    e = lambda m, v=v1, h=hz: ("E", m, v, h)

    def hatirlat(i, soru=True):
        k = K[i]
        out = [T(k["tr"])]
        if soru:
            out += [S(0.2), T(SABIT["ingilizcesi"])]
        out += [S(bek), e(k["en"], v2), R(1.5, 0.9)]
        return out

    # --- giriş
    ev += [("BOLUM", "Giriş"), S(0.6), T(SABIT["hosgeldin"]), S(0.3),
           T(f"Bu ders, {d['seviye_ad']}, {sira_tr(d.get('ders_no', 1))} ders."), S(0.2), T(f"Konu: {d['konu_tr']}"), S(0.3),
           T(SABIT["on_iki"]), S(0.4), T(SABIT["kural1"]), S(0.2), T(SABIT["kural2"]), S(0.2),
           T(SABIT["kural3"]), S(0.4), T(SABIT["basla"]), S(1.0)]

    # --- ısınma: FSRS'ye göre vadesi gelen önceki derslerin kelimeleri (4, 12, 31 ders önce)
    if isinma:
        ev += [("BOLUM", "Isınma tekrarı"), T(SABIT["isinma"]), S(0.6)]
        eski = [k for od in isinma for k in od["kelimeler"]]
        for i in karisik(range(len(eski)), d["id"] + "isinma"):
            k = eski[i]
            ev += [T(k["tr"]), S(bek), ("E", k["en"], v2, hz), R(1.5, 0.9), S(0.4)]
        ev += [S(0.4), T(SABIT["isinma_bitti"]), S(1.0)]

    # --- yeni kelimeler (gruplar halinde, ders içi aralıklı hatırlama)
    gr = gruplar(d)
    soru_say = [0]

    def soru_ekle():
        soru_say[0] += 1
        return soru_say[0] <= 4          # ilk birkaç hatırlatmada "İngilizcesi nedir?" diye sor, sonra kısalt

    sayac = 0
    for gi, g in enumerate(gr):
        ev += [("BOLUM", f"Yeni kelimeler {gi + 1}")]
        if d.get("grup_basliklari"):
            ev += [T(d["grup_basliklari"][gi]), S(0.6)]
        for i in g:
            k = K[i]
            ev += [T(SABIT["ilk"] if sayac == 0 else SABIT["yeni"] if sayac % 2 else SABIT["sonraki"]), S(0.5),
                   e(k["en"], v1, hz), R(1.6, 1.0), e(k["en"], v2, hz), R(1.6, 1.0),
                   T(k["tr"]), S(0.4)]
            for n in k.get("not", []):
                ev += karma([n], d) + [S(0.3)]
            ev += [T(SABIT["ornek"]), S(0.3), e(k["ex"], v1, ohz), S(0.5), T(k["ex_tr"]), S(0.5),
                   T(SABIT["siz_tekrar"]), S(0.3), e(k["ex"], v2, ohz * 0.95), R(1.15, 1.2)]
            if sayac > 0 and i != g[0]:               # ~25 sn önceki kelimeyi geri çağır
                ev += [T(SABIT["hatirla"]), S(0.3)] + hatirlat(i - 1, soru_ekle()) + [S(0.6)]
            sayac += 1
            ev += [S(0.8)]
        # grup sonu: bu grubun kelimeleri (~2 dk), sonra daha eski grup (~5+ dk)
        ev += [T(SABIT["grup_tekrar"]), S(0.5)]
        for i in karisik(g, d["id"] + str(gi)):
            ev += hatirlat(i, soru_ekle()) + [S(0.5)]
        if gi >= 1:
            eski = gr[gi - 1] + (gr[0] if gi == 3 else [])
            ev += [S(0.5), T(SABIT["eski_tekrar"]), S(0.5)]
            for i in karisik(eski, d["id"] + "e" + str(gi)):
                ev += hatirlat(i, False) + [S(0.5)]
        ev += [S(1.0)]

    # --- kalıplar
    if d.get("kaliplar"):
        ev += [("BOLUM", "Kalıplar"), T(SABIT["kalip_giris"]), S(0.8)]
        for k in d["kaliplar"]:
            ev += [e(k["en"], v1, ohz), R(1.4, 1.0), T(k["tr"]), S(0.4), e(k["en"], v2, ohz), R(1.4, 1.0), S(0.4)]

    # --- dinleme (anlaşılır girdi) + gölgeleme + sorular
    hs = d["hikaye_sesi"]; hh = 0.92 if d["seviye"] in ("A1", "A2") else 1.0
    ev += [("BOLUM", "Dinleme"), T(d["hikaye_giris"]), S(1.0)]
    def konusmaci(c):            # diyalog satırı: "ses|metin" → o sesle; aksi halde anlatıcı sesi
        if "|" in c and c.split("|", 1)[0] in d.get("konusmacilar", {}):
            k, m = c.split("|", 1); return d["konusmacilar"][k], m
        return hs, c
    onceki = None
    for c in d["hikaye"]:
        v, m = konusmaci(c)
        ev += [S(0.35 if v != onceki and onceki else 0.0), ("E", m, v, hh), S(0.45)]; onceki = v
    ev += [S(1.2), T(SABIT["hikaye_tekrar"]), S(0.2), T(SABIT["golge"]), S(1.0)]
    for c in d["hikaye"]:
        v, m = konusmaci(c)
        for p in parcala(m):
            ev += [("E", p, v, hh * 0.95), R(1.15, 1.0)]
    ev += [S(0.8), ("BOLUM", "Sorular"), T(SABIT["soru_en"] if d.get("sorular_dil") == "en" else SABIT["soru_tr"]), S(0.8)]
    for q in d["sorular"]:
        if q.get("tr"):
            ev += [T(q["tr"]), S(0.4)]
        ev += [e(q["en"], v1, ohz), S(bek + 2.5), e(q["cevap"], v2, ohz), R(1.1, 1.0), S(0.4)]

    # --- sınav köşesi
    ev += [("BOLUM", "Sınav köşesi"), S(0.5)]
    for s in d.get("sinav_giris", []):
        ev += karma([s], d) + [S(0.4)]
    for s in d["sinav"]:
        for t in s["talimat"]:
            ev += karma([t], d) + [S(0.4)]
        if s["tur"] == "konusma":
            ev += [S(0.4), e(s["soru"], v1, ohz), S(0.6), ("B",), S(s["bekle"]), ("B",), S(0.8),
                   T(s["model_giris"]), S(0.6)]
            for m in s["model"]:
                ev += [e(m, v2, ohz), S(0.5)]
            ev += [S(1.0)]
        else:
            a, b = s["cumle"]
            if a:
                ev += [e(a, v1, ohz), S(0.15)]
            ev += [("B",), S(0.15)] + ([e(b, v1, ohz)] if any(ch.isalpha() for ch in b) else []) + [S(0.6), T(SABIT["secenekler"]), S(0.3)]
            for j, o in enumerate(s["secenekler"]):
                ev += [e(f"{HARF[j]}. {o}.", v2, hz), S(0.35)]
            ev += [S(0.3), T(SABIT["cevap_soyle"]), S(7.0)]
            ev += [e(f"{HARF[s['dogru']]}.", v2, hz), S(0.4)]
            ev += karma(s["aciklama"], d, 0) + [S(1.2)]

    # --- son tekrar (~10+ dk sonra) ve tanıma
    ev += [("BOLUM", "Son tekrar"), T(SABIT["karisik"]), S(0.6)]
    for i in karisik(range(len(K)), d["id"] + "son"):
        ev += hatirlat(i, False) + [S(0.5)]
    ev += [S(0.6), T(SABIT["ters"]), S(0.6)]
    for i in karisik(range(len(K)), d["id"] + "ters"):
        ev += [e(K[i]["en"], v1, hz), S(bek), T(K[i]["tr"]), S(0.8)]
    ev += [("BOLUM", "Kapanış"), S(0.6), T(SABIT["bitis1"]), S(0.3), T(SABIT["bitis2"]), S(0.3),
           T(SABIT["bitis3"]), S(0.3), T(SABIT["bitis4"]), S(1.5)]
    return ev


def tr_cumleler(ev):
    out = []
    for x in ev:
        if x[0] == "T":
            for c in cumlelere_bol(x[1]):
                out.append(c)
    return out


def anahtar(*a):
    return hashlib.sha1("|".join(map(str, a)).encode()).hexdigest()[:16]


# ---------------------------------------------------------------- aralıklı tekrar (FSRS) ve günlük tekrar kaydı
# FSRS (open-spaced-repetition/py-fsrs, MIT), hedef hatırlama %95, her tekrarda "iyi" varsayımıyla şu aralıkları verir:
# 1, 4, 12, 31, 74, 163 gün. Kursta: +1 gün = o dersin "günlük tekrar" kaydı; +4, +12, +31 = sonraki derslerin
# başındaki ısınma bölümü; +74 ve +163 = her yedinci dersten sonra gelen haftalık genel tekrar kaydı.
def fsrs_araliklari(hedef=0.95, adet=6):
    from datetime import datetime, timezone
    from fsrs import Scheduler, Card, Rating
    s = Scheduler(enable_fuzzing=False, desired_retention=hedef)
    t0 = datetime(2026, 1, 1, tzinfo=timezone.utc); c = Card()
    for r in (Rating.Good, Rating.Good):
        c, _ = s.review_card(c, r, t0)
    out = []
    for _ in range(adet):
        now = c.due; out.append(round((now - t0).total_seconds() / 86400)); c, _ = s.review_card(c, Rating.Good, now)
    return out


def isinma_dersleri(n, araliklar=None):
    """n. dersin (1'den başlar) ısınma bölümünde kelimeleri sorulacak önceki derslerin numaraları."""
    a = araliklar or fsrs_araliklari()
    return [n - g for g in a[1:4] if n - g >= 1]


SABIT.update({
    "gunluk1": "Bu, dünkü dersin günlük tekrar kaydı.",
    "gunluk2": "Türkçesini duyunca İngilizcesini söyleyin, sonra örnek cümleyi konuşmacıyla birlikte tekrar edin.",
    "gunluk3": "Şimdi dünkü metni bir kez daha, bu kez kesintisiz dinleyin.",
    "gunluk4": "Tekrar tamamlandı. Şimdi yeni derse geçebilirsiniz.",
})


def plan_gunluk(d):
    """Glossika/Natibo tarzı kısa günlük tekrar: ertesi gün dinlenir (FSRS'nin ilk aralığı: 1 gün)."""
    v1, v2 = d["sesler"]; bek = d["bekle"]; K = d["kelimeler"]
    ev = [("BOLUM", "Günlük tekrar"), S(0.5), T(SABIT["gunluk1"]), S(0.3), T(f"Ders: {d['baslik']}."), S(0.3),
          T(SABIT["gunluk2"]), S(1.0)]
    for i in karisik(range(len(K)), d["id"] + "gunluk"):
        k = K[i]
        ev += [T(k["tr"]), S(bek), ("E", k["en"], v2, d["en_hiz"]), S(0.6),
               ("E", k["ex"], v1, d["ornek_hiz"]), R(1.15, 1.0), S(0.4)]
    ev += [("BOLUM", "Metin"), S(0.6), T(SABIT["gunluk3"]), S(0.8)]
    for c in d["hikaye"]:
        if "|" in c and c.split("|", 1)[0] in d.get("konusmacilar", {}):
            k, m = c.split("|", 1); ev += [("E", m, d["konusmacilar"][k], 1.0), S(0.45)]
        else:
            ev += [("E", c, d["hikaye_sesi"], 1.0), S(0.45)]
    ev += [S(1.0), T(SABIT["gunluk4"]), S(1.2)]
    return ev
