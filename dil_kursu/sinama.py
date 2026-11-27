# -*- coding: utf-8 -*-
"""Kendini sınama kayıtları: önceki derslerden rastgele 40 kelime (Türkçe → İngilizce üretim) ve 10 cümle (İngilizce → Türkçe anlama).
Cevap hemen verilmez; dinleyen puanını kendisi tutar. Sonda puan rehberi."""
import sys; sys.path.insert(0, "/home/claude/kurs")
import icerik, motor
from motor import T, S, karisik

GIRIS = ["Kendini sınama kaydına hoş geldiniz.",
         "Bu kayıt bir sınav gibi. Önce kırk kelime soracağım. Türkçesini duyunca İngilizcesini sesli söyleyin.",
         "Beş saniye düşünme süreniz olacak. Sonra doğru cevabı duyacaksınız.",
         "Doğru bildiğiniz her cevap için kendinize bir puan verin. Bir kâğıt ve kalem hazırlayın.",
         "Sonra on cümle dinleyeceksiniz. Her cümlenin Türkçe anlamını söyleyin. Anlamı doğru verdiyseniz yine bir puan.",
         "Toplam elli puan. Hazırsanız başlayalım."]
BOL2 = "Şimdi ikinci bölüm. İngilizce cümleyi dinleyin ve Türkçe anlamını sesli söyleyin."
PUAN = ["Sınama bitti. Şimdi puanınızı toplayın.",
        "Kırk ve üzeri: harika. Kelimeler kalıcı hafızanıza yerleşmiş. Yeni derslere devam edin.",
        "Otuz ile kırk arası: iyi. Günlük tekrarları atlamadan devam edin.",
        "Otuzun altında kaldıysanız, son on dersin günlük tekrarlarını bir kez daha dinleyin. Sonra bu sınamayı tekrarlayın.",
        "Bilemediğiniz kelimeler, unutmanın normal bir parçası. Hatırlamaya çalışmak öğrenmenin ta kendisidir. Görüşmek üzere."]


def plan_sinama(ids, tohum, n=40, m=10):
    havuz = [(icerik._ID[x], k) for x in ids for k in icerik._ID[x]["kelimeler"]]
    sec = [havuz[i] for i in karisik(range(len(havuz)), tohum)]
    kel, cum = sec[:n], sec[n:n + m]
    ev = [("BOLUM", "Giriş"), S(0.6)] + [x for g in GIRIS for x in (T(g), S(0.4))] + [S(0.8), ("BOLUM", "Kelimeler")]
    for i, (d, k) in enumerate(kel, 1):
        ev += [T(k["tr"]), S(5.0), ("E", k["en"], d["sesler"][1], d["en_hiz"]), S(1.6)]
        if i % 10 == 0 and i < n:
            ev += [S(0.5), T("On soru daha tamam. Devam ediyoruz."), S(0.8)]
    ev += [S(1.0), ("BOLUM", "Cümleler"), T(BOL2), S(0.8)]
    for d, k in cum:
        ev += [("E", k["ex"], d["sesler"][0], d["ornek_hiz"]), S(6.0), T(k["ex_tr"]), S(1.4)]
    ev += [S(1.0), ("BOLUM", "Puan")] + [x for g in PUAN for x in (T(g), S(0.5))] + [S(1.5)]
    return ev


def dersler():
    g = icerik.DIZILER["genel"]; s = icerik.DIZILER["sinav_is"]
    a = {"id": "SINAMA-1", "baslik": "Kendini sınama 1 · Genel İngilizce A1", "sira": "X002", "sesler": ["bf_emma", "am_michael"], "kelimeler": []}
    b = {"id": "SINAMA-2", "baslik": "Kendini sınama 2 · Sınav ve İş 1-32", "sira": "X003", "sesler": ["am_michael", "bf_emma"], "kelimeler": []}
    a["_plan"] = plan_sinama(g[:g.index("A1-25") + 1], "sinama1")
    b["_plan"] = plan_sinama(s[:s.index("YDS-06") + 1], "sinama2")
    return [a, b]
