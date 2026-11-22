#!/usr/bin/env python3
"""BA Teknik Rehberi · Video 6: SQL. Belge satır 1387–1826. Kod satırları ekranda özetlenir, anlatımda açıklanır."""
from ortak import m, t, dikkat, g, soru, kaydet

# ───────────────────────────── Giriş
m("SQL nedir, BA için ne demek?", ["Standart dil (ISO/IEC 9075)", "Lehçe farklı, çekirdek aynı", "Gereksinimi veriyle doğrula, ölç", "Test verisi, rapor gereksinimi", "Veri kalitesini kanıtla"],
  "SQL, ilişkisel veritabanlarında veriyi sorgulamak ve yönetmek için kullanılan standart dildir; ISO standardı dokuz bin yetmiş beş. "
  "{Oracle}, {SQL Server}, {PostgreSQL} ve {MySQL} gibi ürünlerin kendi lehçeleri vardır ama çekirdek aynıdır. "
  "İş analisti için SQL şu demek: gereksinimi veriyle doğrulamak, mevcut durumu ölçmek, test verisi bulmak, "
  "rapor gereksinimini netleştirmek ve veri kalitesi sorunlarını kanıtlamak.",
  bolum="SQL: giriş ve hedefler", kanca="Başkasına sormadan veriye kendin bakabilmek.", ton="merakli")
m("Bu bölümün hedefleri", ["Başvuru, sözleşme, poliçe üzerinde JOIN, GROUP BY, alt sorgu; satır sayısını önceden tahmin",
                           "NULL'ın üç tuzağı: = NULL · NOT IN + NULL · LEFT JOIN'de WHERE", "JOIN çoğaltması (fan-out) ile şişen toplam",
                           "Veri kalitesi sorgusu → gereksinim"],
  "Bu bölümü bitirdiğinde şunları yapabileceksin. Bir: Firma başvuru, sözleşme ve poliçe tabloları üzerinde {JOIN}, {GROUP BY} ve alt sorgu yazmak; "
  "sonucun satır sayısını çalıştırmadan önce tahmin etmek. "
  "İki: {NULL}'ın yol açtığı üç tuzağı tanıyıp düzeltmek: eşittir {NULL}, {NOT IN} ile {NULL}, ve {LEFT JOIN}'de {WHERE} filtresi. "
  "Üç: JOIN çoğaltması, yani {fan-out} yüzünden şişen bir toplamı bulup düzeltmek. "
  "Dört: veri kalitesi kontrol sorguları yazıp bulguları bir gereksinime çevirmek.")
t("Başlamadan önce gerekenler", ["Gereken", "Nereden", "Hazır mısın?"],
  [["Tablo, satır, sütun, anahtar", "Temel seviye", "musteri_id neden yabancı anahtar?"],
   ["DBeaver Community", "dbeaver.io", "SQLite bağlantısı, vdf_lab.db"],
   ["Kurulum yoksa", "sqliteonline.com, DB Fiddle", "SELECT 1; → 1"],
   ["Laboratuvar betiği", "CREATE / INSERT", "COUNT(*) basvuru → 5"]],
  "Başlamadan önce dört hazırlık. Kavramlar: tablo, satır, sütun ve anahtar. Başvuru tablosundaki {musteri_id} neden yabancı anahtardır sorusunu cevaplayabiliyorsan hazırsın. "
  "Araç: {DBeaver} {Community}, ücretsiz; dbeaver nokta io'dan indirilir. "
  "{Database}, {New Database Connection}, {SQLite}; {Path} alanının yanındaki {Create} ile yeni bir dosya oluştur, örneğin {vdf_lab} nokta db; "
  "sonra {Finish}. Bağlantı solda görünüyorsa tamam. "
  "Kurulum yapamıyorsan tarayıcıda çalışan bir deneme ortamı: sqliteonline nokta com ya da {DB Fiddle}. {SELECT} bir sorgusu bir döndürüyorsa hazırsın. "
  "Son olarak laboratuvar betiği: bölümün laboratuvar kısmındaki {CREATE} ve {INSERT} betikleri. "
  "Başvuru tablosunda {COUNT} yıldız beş döndürüyorsa veri yüklenmiş demektir.")
t("Örnek şema", ["Tablo", "Sütunlar"],
  [["musteri", "musteri_id PK, tckn, ad, soyad, dogum_tarihi, sehir, segment"],
   ["basvuru", "basvuru_id PK, musteri_id FK, bayi_id FK, urun, tutar, vade, durum, kkb_skor, basvuru_tarihi"],
   ["sozlesme · taksit", "sozlesme_id PK, basvuru_id FK, ... · taksit_id PK, sozlesme_id FK, vade_tarihi, odeme_tarihi"],
   ["bayi · police", "bayi_id PK, bayi_adi, marka, bolge · police_id PK, sozlesme_id FK, tur, prim, durum"]],
  "Örnekler şu basit şemayı kullanıyor. musteri tablosu: birincil anahtar, yani PK, musteri_id; tckn, ad, soyad, dogum_tarihi, sehir ve segment. "
  "basvuru tablosu: PK basvuru_id; yabancı anahtar, yani FK, olarak musteri_id ve bayi_id; urun, tutar, vade, durum, kkb_skor ve basvuru_tarihi. "
  "sozlesme tablosu: PK sozlesme_id, FK basvuru_id; kullandirim_tarihi, faiz_orani ve anapara. "
  "taksit tablosu: PK taksit_id, FK sozlesme_id, taksit_no, vade_tarihi, tutar ve odeme_tarihi. "
  "bayi tablosu: PK bayi_id, bayi_adi, marka ve bolge. "
  "police tablosu: PK police_id, FK sozlesme_id; tur, prim, baslangic, bitis ve durum.")

# ───────────────────────────── Temel
t("Komut aileleri", ["Aile", "Komutlar"],
  [["DQL", "SELECT"], ["DML", "INSERT, UPDATE, DELETE, MERGE"], ["DDL", "CREATE, ALTER, DROP"],
   ["DCL", "GRANT, REVOKE"], ["TCL", "COMMIT, ROLLBACK, SAVEPOINT"]],
  "Temel seviyeye geçelim. Komutlar beş aileye ayrılır. DQL, sorgulama: {SELECT}. "
  "DML, veri değiştirme: {INSERT}, {UPDATE}, {DELETE}, {MERGE}. DDL, yapı tanımı: {CREATE}, {ALTER}, {DROP}. "
  "DCL, yetki: {GRANT}, {REVOKE}. TCL, işlem kontrolü: {COMMIT}, {ROLLBACK}, {SAVEPOINT}.", bolum="SQL · Temel seviye")
m("SELECT'in mantıksal çalışma sırası", ["FROM / JOIN → WHERE → GROUP BY → HAVING", "→ SELECT → DISTINCT → ORDER BY → LIMIT / FETCH",
                                         "Yazım sırasından farklı", "WHERE içinde SELECT'teki takma ad (alias) kullanılamaz"],
  "{SELECT}'in mantıksal çalışma sırası yazım sırasından farklıdır. Önce {FROM} ve {JOIN}, sonra {WHERE}, sonra {GROUP BY}, sonra {HAVING}; "
  "ardından {SELECT}, {DISTINCT}, {ORDER BY} ve en sonda {LIMIT} ya da {FETCH}. "
  "Bu yüzden {WHERE} içinde {SELECT}'te verdiğin takma adı, yani {alias}'ı kullanamazsın; o ad henüz oluşmamıştır.")
m("Örnek: son 30 gün, İstanbul, onaylı", ["basvuru b JOIN musteri m: musteri_id eşleşmesi", "WHERE durum = 'ONAY' ve sehir = 'ISTANBUL'",
                                          "basvuru_tarihi ≥ bugün − 30 gün", "Seçilen: basvuru_id, ad, soyad, tutar, vade · ORDER BY tutar DESC"],
  "İlk örnek: son otuz günde İstanbul'daki onaylanan başvurular. basvuru tablosuna b, musteri tablosuna m takma adı verilir "
  "ve musteri_id üzerinden {JOIN} yapılır. "
  "{WHERE} koşulları: durum eşittir ONAY ve sehir eşittir ISTANBUL; ve başvuru tarihi bugünden otuz gün öncesine eşit ya da büyük; "
  "bunu {CURRENT_DATE} eksi {INTERVAL} otuz {DAY} diye yazarsın. "
  "Seçilen sütunlar: basvuru_id, ad, soyad, tutar ve vade; sonuç tutara göre büyükten küçüğe, yani {ORDER BY} tutar {DESC} ile sıralanır.")
m("Filtre operatörleri ve toplama", ["=, <>, >, <, BETWEEN, IN, LIKE '%kasko%', IS NULL, IS NOT NULL, AND/OR/NOT",
                                     "NULL = NULL doğru dönmez → IS NULL", "NOT IN listesinde NULL → sonuç boş · NOT EXISTS daha güvenli",
                                     "COUNT(*), COUNT(DISTINCT x), SUM, AVG, MIN, MAX"],
  "Filtre operatörleri: eşittir, eşit değildir, büyüktür, küçüktür; {BETWEEN}, {IN}; içinde kasko geçen metin için {LIKE}; "
  "{IS NULL}, {IS NOT NULL}; ve {AND}, {OR}, {NOT}. "
  "Dikkat: {NULL} eşittir {NULL} doğru dönmez; boş değeri {IS NULL} ile ararsın. "
  "{NOT IN} listesinde {NULL} varsa sonuç boş döner; {NOT EXISTS} daha güvenlidir. Bunu birazdan tuzaklarda göreceğiz. "
  "Toplama fonksiyonları: {COUNT} yıldız, {COUNT} {DISTINCT}, {SUM}, {AVG}, {MIN} ve {MAX}.")
m("Örnek: bayi bazında onay oranı", ["basvuru JOIN bayi · GROUP BY bayi_adi", "COUNT(*) → basvuru_sayisi",
                                     "SUM(CASE WHEN durum = 'ONAY' THEN 1 ELSE 0 END) → onay_sayisi",
                                     "ROUND(100.0 × onay / toplam, 1) → onay_orani", "HAVING COUNT(*) ≥ 20 · ORDER BY onay_orani DESC"],
  "İkinci örnek: bayi bazında başvuru sayısı ve onay oranı, en az yirmi başvurusu olanlar. basvuru {JOIN} bayi; "
  "{GROUP BY} bayi_adi. {COUNT} yıldız, basvuru_sayisi olur. "
  "onay_sayisi için {SUM} içinde {CASE} {WHEN} durum ONAY ise bir, değilse sıfır yazarsın. "
  "onay_orani: yüz nokta sıfır çarpı onay sayısı bölü toplam, {ROUND} ile bir basamağa yuvarlanır. "
  "{HAVING} {COUNT} yıldız yirmiye eşit ya da büyük ile az başvurulu bayiler elenir; sonuç onay oranına göre azalan sıralanır.")
t("JOIN türleri", ["JOIN", "Sonuç", "BA kullanımı"],
  [["INNER", "İki tabloda eşleşenler", "Başvurusu olan müşteriler"], ["LEFT", "Sol tamamı + eşleşenler", "Tüm sözleşmeler ve varsa poliçeleri"],
   ["LEFT + IS NULL", "Sağda karşılığı yok (anti-join)", "Poliçesi olmayan sözleşmeler"], ["RIGHT", "Sağ tamamı", "Nadiren; LEFT ile yazılır"]],
  "{JOIN} türleri. {INNER}: her iki tabloda eşleşenler; örneğin başvurusu olan müşteriler. "
  "{LEFT}: sol tablonun tamamı ve eşleşenler; örneğin tüm sözleşmeler ve varsa poliçeleri. "
  "{LEFT} {JOIN} artı sağ tablonun id'si {IS NULL}: sağda karşılığı olmayanlar, yani {anti-join}; örneğin poliçesi olmayan sözleşmeler. "
  "{RIGHT}: sağ tablonun tamamı; nadiren kullanılır, {LEFT} ile yeniden yazılır.")
t("JOIN türleri (devam)", ["JOIN", "Sonuç", "BA kullanımı"],
  [["FULL OUTER", "İki tarafın tamamı", "İki sistem arasında mutabakat"], ["CROSS", "Kartezyen çarpım", "Takvim × bayi iskeleti"],
   ["SELF", "Tablonun kendisiyle", "Aynı TCKN ile farklı müşteri kayıtları"]],
  "{FULL OUTER}: iki tarafın tamamı; iki sistem arasında mutabakat. "
  "{CROSS}: kartezyen çarpım; takvim çarpı bayi gibi bir iskelet oluşturmak için. "
  "{SELF}: tablonun kendisiyle birleştirilmesi; örneğin aynı TCKN ile açılmış farklı müşteri kayıtlarını bulmak.")
g("JOIN'ler ve sorgu sırası bir bakışta", "g21.png",
  [([0.0, 0.1, 0.5, 0.66], "INNER ve LEFT JOIN"), ([0.5, 0.1, 1.0, 0.66], "LEFT + IS NULL ve FULL OUTER"),
   ([0.0, 0.66, 1.0, 0.96], "SELECT'in çalışma sırası")],
  "Görsel rehberdeki ilk çizim JOIN'leri ve sorgu sırasını bir arada gösteriyor; A müşteri, B başvuru, boyalı alan sonuçta dönen satırlar. "
  "{INNER} {JOIN}: iki tabloda eşleşenler, başvurusu olan müşteri. {LEFT} {JOIN}: A'nın tamamı ve eşleşen B; B yoksa B sütunları {NULL}. "
  "{LEFT} {JOIN} artı {IS NULL}: A'da olup B'de olmayan, yani hiç başvurusu olmayan müşteri. "
  "{FULL OUTER} {JOIN}: iki tarafın tamamı; sistemler arası mutabakat. "
  "Altta {SELECT}'in mantıksal çalışma sırası: bir {FROM} ve {JOIN}, iki {WHERE}, üç {GROUP BY}, dört {HAVING}, beş {SELECT}, altı {ORDER BY}, yedi {LIMIT}. "
  "Bu yüzden {SELECT}'te verilen takma ad {WHERE}'de kullanılamaz; toplama koşulları {WHERE}'e değil {HAVING}'e yazılır.")

# ───────────────────────────── Orta
m("Alt sorgu ve EXISTS: gecikmiş taksit", ["musteri m WHERE EXISTS (…)", "İçeride: basvuru → sozlesme → taksit",
                                           "Bağ: b.musteri_id = m.musteri_id", "odeme_tarihi IS NULL ve vade_tarihi < bugün"],
  "Orta seviye. Alt sorgu ve {EXISTS}: gecikmiş taksiti olan müşteriler. Müşteri tablosundan seçersin; {WHERE} {EXISTS} ile bir alt sorgu açarsın. "
  "İçeride basvuru, sozlesme ve taksit birleştirilir. Bağ: b nokta musteri_id eşittir m nokta musteri_id. "
  "Gecikme koşulu: ödeme tarihi boş, yani {IS NULL}, ve vade tarihi bugünden küçük. "
  "{EXISTS} yalnız var mı diye bakar; kaç tane olduğuyla ilgilenmez, bu yüzden satır çoğaltmaz.", bolum="SQL · Orta seviye")
m("CTE (WITH) ile okunabilir sorgu", ["WITH gecikme AS: sozlesme_id, MAX(bugün − vade) = gecikme_gun", "Yalnız ödenmemiş ve vadesi geçmiş taksitler",
                                      "CASE: ≤ 30 '1-30' · ≤ 60 '31-60' · ≤ 90 '61-90' · ELSE '90+'", "Kova başına COUNT(*) → sozlesme_sayisi"],
  "{CTE}, yani {WITH} ile okunabilir sorgu. Önce gecikme adlı bir ara tablo tanımlarsın: her sözleşme için bugün eksi vade tarihinin en büyüğü, "
  "yani en uzun gecikme günü; yalnız ödenmemiş ve vadesi geçmiş taksitler için. "
  "Sonra bu ara tablodan {CASE} ile kova üretirsin: otuza kadar bir ile otuz, altmışa kadar otuz bir ile altmış, "
  "doksana kadar altmış bir ile doksan, değilse doksan artı. Kova başına {COUNT} yıldız, sozlesme_sayisi olur. "
  "Bu, gecikme sürecindeki aksiyon kovalarının veri karşılığıdır.")
m("CASE, tarih, metin, set operatörleri", ["CASE WHEN · COALESCE(x, 0) · NULLIF(a, 0): sıfıra bölmeyi önler",
                                           "EXTRACT(YEAR FROM tarih) · DATE_TRUNC('month', …) PG / TRUNC(tarih, 'MM') Oracle",
                                           "UPPER, TRIM, SUBSTRING, CONCAT veya ||", "UNION · UNION ALL · INTERSECT · EXCEPT (Oracle: MINUS)"],
  "Fonksiyonlar. {CASE} {WHEN}; boşsa sıfır yazmak için {COALESCE}; sıfıra bölmeyi önlemek için {NULLIF}. "
  "Tarih: yılı almak için {EXTRACT} {YEAR} {FROM}; aya yuvarlamak için PostgreSQL'de {DATE_TRUNC} {month}, Oracle'da {TRUNC} ile {MM}. "
  "Metin: {UPPER}, {TRIM}, {SUBSTRING}, ve birleştirme için {CONCAT} ya da çift dikey çizgi. "
  "Set operatörleri: {UNION} tekrarsız; {UNION ALL} tekrarlı ve daha hızlı; {INTERSECT}; ve {EXCEPT}, Oracle'da {MINUS}. "
  "Mutabakatta çok kullanılır: ana sistemde olup raporlama tablosunda olmayan sözleşmeler gibi.")
m("DDL örneği: kampanya tablosu", ["kampanya_id INTEGER PRIMARY KEY", "kod VARCHAR(20) NOT NULL UNIQUE",
                                   "indirim_bp INTEGER CHECK (0–500)", "baslangic, bitis DATE NOT NULL · CHECK (bitis ≥ baslangic)"],
  "DDL örneği: kampanya tablosu. kampanya_id {INTEGER} {PRIMARY KEY}. Kod, yirmi karakterlik {VARCHAR}, boş olamaz ve tekil, yani {NOT NULL} {UNIQUE}. "
  "İndirim baz puanı tamsayı, {CHECK} ile sıfır ile beş yüz arasında. "
  "baslangic ve bitis {DATE} {NOT NULL}; bir de bitis baslangic'a eşit ya da büyük olmalı diye {CHECK} kuralı var. "
  "Gördüğün gibi iş kuralları tablonun kendisine de yazılabilir.")
m("DML örneği: süresi geçen onayları iptal et", ["UPDATE basvuru SET durum = 'IPTAL'", "WHERE durum = 'ONAY'",
                                                  "ve basvuru_tarihi < bugün − 15 gün", "ve sözleşmesi yok (NOT IN sozlesme)"],
  "DML örneği: {UPDATE} basvuru {SET} durum eşittir IPTAL. Koşullar: {WHERE} durum eşittir ONAY, başvuru tarihi bugünden on beş gün önceden eski, "
  "ve başvuru id sözleşme tablosunda yok. "
  "Bu sorguda bir tuzak var: {NOT IN} kullanılmış. Birazdan tuzak birde neden riskli olduğunu göreceğiz.")
dikkat("Canlıda UPDATE / DELETE kuralı", "Önce aynı WHERE ile SELECT COUNT(*) · değişiklik onay akışından (CR) geçer · rollback planı olur.",
       "İş analisti kuralı: canlıda {UPDATE} ya da {DELETE} çalıştırmadan önce aynı {WHERE} ile {SELECT} {COUNT} yıldız yaparsın; "
       "kaç satırın etkileneceğini görürsün. Değişiklik onay akışından, yani {change request}'ten geçmeli ve bir geri alma, yani {rollback} planı olmalıdır.")
m("Normalizasyon özeti", ["1NF: atomik değerler, tekrar eden grup yok", "2NF: bileşik anahtarın bir kısmına bağımlılık yok",
                          "3NF: anahtar olmayan alanlar arası bağımlılık yok", "Raporlamada bilinçli denormalizasyon: star schema (fact + dimension)"],
  "Normalizasyon özeti. Birinci normal form: atomik değerler, tekrar eden grup yok. "
  "İkinci normal form: bileşik anahtarın bir kısmına bağımlılık yok. Üçüncü normal form: anahtar olmayan alanlar arasında bağımlılık yok. "
  "Raporlama ve veri ambarı tarafında ise bilinçli denormalizasyon yapılır: {star schema}, yani {fact} ve {dimension} tabloları.")

# ───────────────────────────── İleri
m("Window fonksiyonları: en son başvuru", ["Satırları gruplayıp kaybetmeden hesaplar", "ROW_NUMBER() OVER (PARTITION BY musteri_id ORDER BY basvuru_tarihi DESC) AS rn",
                                           "Dış sorguda WHERE rn = 1"],
  "İleri seviye: pencere fonksiyonları, yani {window} fonksiyonları. Satırları gruplayıp kaybetmeden hesaplama yaparlar. "
  "Örnek: her müşterinin en son başvurusu. İç sorguda {ROW_NUMBER} {OVER}, {PARTITION BY} musteri_id, {ORDER BY} basvuru_tarihi {DESC}; "
  "bu numaraya rn de, {AS} rn. Dış sorguda rn eşittir bir olanları al.", bolum="SQL · İleri seviye")
m("Aylık hacim, kümülatif, değişim", ["WITH aylik: DATE_TRUNC('month', kullandirim_tarihi), SUM(anapara) AS hacim",
                                      "SUM(hacim) OVER (ORDER BY ay) → kumulatif", "hacim − LAG(hacim) → aylik_degisim",
                                      "100 × değişim / NULLIF(LAG(hacim), 0) → degisim_yuzde"],
  "İkinci örnek: aylık kullandırım, kümülatif toplam ve önceki aya göre değişim. Önce aylik adlı {CTE}: kullandırım tarihini aya yuvarla, anaparaları topla; buna hacim de. "
  "Sonra {SUM} hacim {OVER} aya göre sıralı: kümülatif toplam. Hacim eksi {LAG} hacim: önceki aya göre değişim. "
  "Yüzde değişim için 100.0 çarpı değişim, bölü {LAG} hacim; ama sıfıra bölmemek için {NULLIF} ile sarılır.")
m("Diğer pencere fonksiyonları", ["RANK, DENSE_RANK", "NTILE(10): skor desilleri", "LEAD, FIRST_VALUE",
                                  "AVG(...) OVER (ORDER BY ay ROWS BETWEEN 2 PRECEDING AND CURRENT ROW): 3 aylık hareketli ortalama"],
  "Diğer pencere fonksiyonları: {RANK} ve {DENSE_RANK}; skor desilleri için {NTILE} on; {LEAD} ve {FIRST_VALUE}. "
  "Bir de üç aylık hareketli ortalama: {AVG} {OVER} aya göre sıralı, {ROWS BETWEEN} iki {PRECEDING} {AND} {CURRENT ROW}.")
m("Recursive CTE: takvim", ["Hiyerarşi (bayi → bölge → genel müdürlük, onay zinciri) ya da tarih serisi",
                            "WITH RECURSIVE takvim(gun): 2026-01-01'den başla, gun + 1, 2026-01-31'e kadar",
                            "takvim LEFT JOIN basvuru → her gün için başvuru sayısı (boş günler 0)"],
  "Özyinelemeli, yani {recursive} {CTE}: hiyerarşiler için, örneğin bayi, bölge, genel müdürlük ya da onay yetki zinciri; ya da tarih serisi üretmek için. "
  "Örnek: takvim adlı {CTE} bir Ocak iki bin yirmi altıdan başlar, her adımda gün artı bir, otuz bir Ocak'a kadar. "
  "Sonra takvimi başvurularla {LEFT JOIN} yaparsın; böylece hiç başvuru olmayan günler de sıfırla görünür.")
m("Transaction ve izolasyon", ["ACID: Atomicity, Consistency, Isolation, Durability",
                               "Read Uncommitted · Read Committed · Repeatable Read · Serializable",
                               "Anomaliler: dirty read, non-repeatable read, phantom read",
                               "BA: \"İki kullanıcı aynı başvuruyu onaylarsa?\" → optimistic locking (versiyon kolonu)"],
  "İşlem ve izolasyon. {ACID}: {Atomicity}, {Consistency}, {Isolation}, {Durability}. "
  "İzolasyon seviyeleri: {Read Uncommitted}, {Read Committed}, {Repeatable Read} ve {Serializable}. "
  "Anomaliler: {dirty read}, {non-repeatable read} ve {phantom read}. "
  "İş analisti açısından önemi: aynı anda iki kullanıcı aynı başvuruyu onaylarsa ne olur gibi eşzamanlılık gereksinimlerini yazmak. "
  "Çözüm genellikle iyimser kilitleme, yani {optimistic locking}: bir versiyon kolonu.")
m("Performans", ["Index (B-tree) seçici kolonlarda · bileşik index'te kolon sırası", "WHERE UPPER(kolon): index devre dışı",
                 "SELECT * yerine gereken kolonlar", "EXPLAIN / EXPLAIN ANALYZE (PG) · EXPLAIN PLAN (Oracle)",
                 "Plan: full table scan, index scan, nested loop, hash join"],
  "Performans. {Index}, yani dizin, {B-tree} yapısındadır ve seçici kolonlarda işe yarar; bileşik dizinde kolon sırası önemlidir. "
  "{WHERE} içinde {UPPER} gibi bir fonksiyonla kolonu sararsan dizin devre dışı kalır. {SELECT} yıldız yerine gereken kolonları seç. "
  "Planı okumak için PostgreSQL'de {EXPLAIN} ya da {EXPLAIN ANALYZE}, Oracle'da {EXPLAIN PLAN}. "
  "Planda göreceklerin: {full table scan}, {index scan}, {nested loop} ve {hash join}.")
t("Veri kalitesi kontrolleri", ["Boyut", "Kontrol sorgusu fikri"],
  [["Tamamlık", "musteri WHERE tckn IS NULL → COUNT(*)"], ["Teklik", "GROUP BY tckn HAVING COUNT(*) > 1"],
   ["Geçerlilik", "Yaş < 18 kredi müşterisi; TCKN 11 hane değil"], ["Tutarlılık", "Taksit toplamı ≠ anapara + faiz"],
   ["Referans bütünlüğü · güncellik", "Sahipsiz (orphan) poliçe · son 24 saatte güncellenmeyen kur tablosu"]],
  "Ve bir iş analistinin en değerli SQL kullanımı: veri kalitesi kontrolleri. Tabloda her boyut için bir kontrol sorgusu fikri var. Tamamlık: TCKN'si boş olan müşteri sayısı. "
  "Teklik: TCKN'ye göre grupla, {HAVING} {COUNT} birden büyük olanlar; yani mükerrer kayıtlar. "
  "Geçerlilik: yaşı on sekizden küçük kredi müşterisi; on bir hane olmayan TCKN. "
  "Tutarlılık: taksit toplamı sözleşme anapara artı faize eşit değil. "
  "Referans bütünlüğü: sahibi olmayan, yani {orphan} poliçe kayıtları; {LEFT JOIN} ve {IS NULL} ile bulunur. "
  "Güncellik: son yirmi dört saatte güncellenmeyen kur tablosu.")
dikkat("KVKK ve güvenlik", "En az yetki · kişisel veri maskelenmiş view'dan · test ortamına anonimleştirmeden veri yok · parametreli sorgu (SQL injection)",
       "KVKK ve güvenlik. Üretim verisinde sorgu yetkisi en az yetki ilkesiyle verilir; kişisel veriler maskelenmiş {view}'lardan okunur. "
       "Test ortamına üretim verisi anonimleştirmeden taşınmaz. "
       "Uygulamalarda {SQL injection} riskine karşı parametreli sorgu gereksinimi yazılır.")

# ───────────────────────────── Hatalar, mülakat
m("Sık yapılan hatalar", ["JOIN fan-out ile SUM şişer → önce alt kırılımda topla", "LEFT JOIN + sağ tabloya WHERE = INNER JOIN (koşul ON'a)",
                          "NULL'ı unutmak: AVG yok sayar, COUNT(kolon) saymaz", "Tarih: ≤ '2026-03-31' 00:00'da biter → < '2026-04-01'",
                          "Tamsayı bölmesi 0 → 100.0 × ile ondalığa çevir"],
  "Sık yapılan hatalar. Bir: {JOIN} sonrası satır çoğalması yüzünden {SUM}'ın şişmesi; önce alt kırılımda toplayıp sonra birleştirmek gerekir. "
  "İki: {LEFT JOIN} yapıp sağ tabloya {WHERE} koşulu koyarak onu {INNER JOIN}'e dönüştürmek; koşul {ON} içine yazılmalı. "
  "Üç: {NULL}'ları hesaba katmamak; {AVG} {NULL}'ları yok sayar, {COUNT} kolon {NULL} saymaz. "
  "Dört: tarih aralığında saat bileşenini unutmak. Küçük eşit 2026-03-31, günün 00:00'ında biter. Küçüktür 2026-04-01 kullan. "
  "Beş: tamsayı bölmesiyle oranın sıfır çıkması; yüz nokta sıfır ile çarparak ondalığa çevir.", bolum="SQL · Hatalar ve mülakat")
m("Mülakat soruları", ["1. WHERE ile HAVING farkı?", "2. Poliçesi olmayan sözleşmeler sorgusu", "3. Her bayinin en yüksek 3 başvurusu (ROW_NUMBER / DENSE_RANK)",
                       "4. UNION ile UNION ALL farkı?", "5. Rapor sayısı kaynakla tutmuyor: analiz?", "6. Index her zaman hızlandırır mı?"],
  "Mülakat soruları. Bir: {WHERE} ile {HAVING} farkı nedir? İki: poliçesi olmayan sözleşmeleri bulan sorguyu yazın. "
  "Üç: her bayinin en yüksek tutarlı üç başvurusunu nasıl getirirsiniz? İpucu: {ROW_NUMBER} ya da {DENSE_RANK}. "
  "Dört: {UNION} ile {UNION ALL} farkı. Beş: bir rapor sayısı kaynak sistemle tutmuyor; nasıl analiz edersiniz? "
  "Altı: dizin her zaman hızlandırır mı, neden?")
m("Cevap ipuçları", ["WHERE gruplamadan önce satırı, HAVING sonra grubu süzer", "sozlesme + NOT EXISTS (police) ya da LEFT JOIN + IS NULL",
                     "ROW_NUMBER() OVER (PARTITION BY bayi_id ORDER BY tutar DESC) ≤ 3", "UNION tekrarı atar; UNION ALL atmaz, daha hızlı",
                     "Satır sayısı, fan-out, NULL, tarih sınırı · index yazmayı yavaşlatır, fonksiyonla devre dışı"],
  "İpuçları, bölümün içeriğinden. {WHERE} gruplamadan önce satırı, {HAVING} gruplamadan sonra grubu süzer. "
  "Poliçesiz sözleşme: {NOT EXISTS} ya da {LEFT JOIN} artı {IS NULL}. "
  "İlk üç: {ROW_NUMBER} {OVER}, {PARTITION BY} bayi_id, {ORDER BY} tutar {DESC}; üçe eşit ya da küçük olanlar. "
  "{UNION} tekrarı atar; {UNION ALL} atmaz ve daha hızlıdır. "
  "Tutmayan rapor için satır sayısına, {JOIN} çoğaltmasına, {NULL} davranışına ve tarih sınırına bakarsın. "
  "Dizin ise yazma işlemlerini yavaşlatır, seçici olmayan kolonda işe yaramaz ve fonksiyonla sarılınca devre dışı kalır.")

# ───────────────────────────── Görsel rehber
g("Şemayı okumak: ER diyagramı", "g22.png",
  [([0.0, 0.08, 1.0, 0.48], "musteri — basvuru — bayi"), ([0.35, 0.4, 0.65, 0.65], "basvuru — sozlesme: sıfır veya bir"),
   ([0.0, 0.6, 1.0, 0.92], "taksit — sozlesme — police"), ([0.0, 0.9, 1.0, 1.0], "Çift çizgi, halka, kaz ayağı")],
  "Sorgu yazmadan önce tabloların nasıl bağlı olduğunu görmen gerekir. Bu ER diyagramı, bölümdeki örneklerin kullandığı şemayı gösteriyor; "
  "altı tablo, {crow's foot} notasyonu. "
  "Çizginin müşteri ucunda çift çizgi, başvuru ucunda kaz ayağı var: bir müşterinin çok sayıda başvurusu olabilir, her başvuru tek bir müşteriye aittir. "
  "Yani musteri, basvuru ve bayi; başvuru ile bayi arasında da aynı ilişki var. "
  "basvuru ile sozlesme arasındaki halka sıfır veya bir demektir: her başvurunun sözleşmesi olmak zorunda değil. "
  "Altta taksit, sozlesme ve police: taksitler ve poliçeler sözleşmeye çok tarafından bağlı. "
  "Alttaki açıklama: çift çizgi tam bir; halka artı çizgi sıfır ya da bir; kaz ayağı, yani üç çizgi, çok; PK birincil anahtar, FK yabancı anahtar. "
  "{JOIN} yazarken yabancı anahtar eşittir birincil anahtar eşleştirmesini bu çizgilerden okursun: başvurunun müşteri id'si eşittir müşterinin müşteri id'si.",
  bolum="SQL · Görsel rehber ve araçlar")
t("Araç menü rehberi (1/3)", ["Yapmak istediğin", "DBeaver", "SSMS", "Oracle SQL Developer"],
  [["Bağlantı", "New Database Connection", "Connect to Server", "Connections → +"],
   ["Sorgu penceresi", "New SQL script (Ctrl+])", "New Query (Ctrl+N)", "Open SQL Worksheet"],
   ["İmleçteki sorgu", "Ctrl+Enter", "Seç + F5", "Ctrl+Enter / F9"]],
  "Araç menü rehberi: {DBeaver}, ücretsiz ve çok veritabanlı; {SQL Server Management Studio}; ve {Oracle SQL Developer}. "
  "Bağlantı kurmak: {DBeaver}'da {Database}, {New Database Connection}, veritabanı türü, sonra host, port ve kullanıcı. "
  "{SSMS}'te başlangıçta {Connect to Server}: {Server name} ve {Authentication}. {Oracle}'da sol panelde {Connections}, artı, bilgileri gir, {Test}, {Connect}. "
  "Sorgu penceresi: {DBeaver}'da {SQL Editor}, {New SQL script}, kontrol köşeli parantez. {SSMS}'te {New Query}, kontrol N. "
  "{Oracle}'da bağlantıya sağ tık, {Open SQL Worksheet}. "
  "İmlecin olduğu sorguyu çalıştırmak: {DBeaver}'da kontrol {Enter}; {SSMS}'te sorguyu seç ve F5; {Oracle}'da kontrol {Enter} ya da F9.")
t("Araç menü rehberi (2/3)", ["Yapmak istediğin", "DBeaver", "SSMS", "Oracle SQL Developer"],
  [["Tüm betik", "Alt+X", "F5 (seçimsiz)", "F5 (Run Script)"], ["Çalıştırma planı", "Ctrl+Shift+E", "Ctrl+L / Ctrl+M", "F10 (Explain Plan)"],
   ["Tablo yapısı", "Çift tık → Columns, Keys", "Object Explorer → Columns", "Columns, Constraints"]],
  "Tüm betiği çalıştırmak: {DBeaver}'da alt X; {SSMS}'te seçim yoksa F5; {Oracle}'da F5, yani {Run Script}. "
  "Çalıştırma planı: {DBeaver}'da kontrol shift E, {Explain execution plan}; {SSMS}'te kontrol L tahmini, kontrol M gerçek plan; {Oracle}'da F10, {Explain Plan}. "
  "Tablo yapısını görmek: {DBeaver}'da {Navigator}'da tabloya çift tık, {Columns}, {Keys} ve {ER Diagram} sekmeleri. "
  "{SSMS}'te {Object Explorer}, {Tables}, tablo, {Columns}. {Oracle}'da tabloya tıkla, {Columns} ve {Constraints} sekmeleri.")
t("Araç menü rehberi (3/3)", ["Yapmak istediğin", "DBeaver", "SSMS", "Oracle SQL Developer"],
  [["ER diyagramı", "View Diagram", "New Database Diagram", "Data Modeler → Import"], ["Excel'e al", "Export data → XLSX/CSV", "Save Results As", "Export"],
   ["Auto-commit kapat", "Auto-Commit → Manual", "BEGIN TRAN", "Preferences → Autocommit"]],
  "ER diyagramı üretmek: {DBeaver}'da şemaya sağ tık, {View Diagram}; {SSMS}'te {Database Diagrams}, {New Database Diagram}; "
  "{Oracle}'da {File}, {Data Modeler}, {Import}, {Data Dictionary}. "
  "Sonucu Excel'e almak: {DBeaver}'da sonuç tablosuna sağ tık, {Export data}, XLSX ya da CSV; {SSMS}'te sonuç ızgarasına sağ tık, {Save Results As}, CSV; "
  "{Oracle}'da sonuca sağ tık, {Export}. "
  "Otomatik {commit}'i kapatmak: {DBeaver}'da araç çubuğundaki {Auto-Commit} düğmesi, {Manual}. "
  "{SSMS}'te varsayılan {autocommit}; işlemi {BEGIN TRAN} ile başlatırsın. {Oracle}'da {Tools}, {Preferences}, {Database}, {Advanced}, {Autocommit}.")
dikkat("Güvenlik alışkanlığı", "Üretim bağlantısını farklı renkle işaretle (Connection type: Production) · DML'den önce aynı WHERE ile SELECT COUNT(*)",
       "Bir güvenlik alışkanlığı: üretim bağlantısını farklı renkte işaretle. {DBeaver}'da bağlantı ayarları, {General}, {Connection type}: {Production}. "
       "Ve DML çalıştırmadan önce aynı {WHERE} ile {SELECT} {COUNT} yıldız yap.")

# ───────────────────────────── Laboratuvar
m("Laboratuvar: veri (~45 dk)", ["4 tablo: musteri, basvuru, sozlesme, police", "musteri: 1 Ayse · 2 Mehmet · 3 Zeynep · 4 Can",
                                 "basvuru: 101 · 102 · 103 · 104 · 105", "sozlesme: 9001 → 101 · 9002 → 103", "police: 7001 → 9001 KASKO"],
  "Laboratuvar: küçük veriyle {JOIN} ve toplama alıştırması; yaklaşık kırk beş dakika. "
  "Betiği {DBeaver}'da bir {SQLite} ya da {PostgreSQL} bağlantısında, ya da tarayıcıdaki bir deneme ortamında çalıştır. "
  "Beklenen sonuçlar bu betikle çalıştırılarak doğrulanmıştır. "
  "Dört tablo oluşturulur: musteri, basvuru, sozlesme ve police. {INSERT} {INTO} musteri {VALUES}: 1 Ayse ISTANBUL; 2 Mehmet ANKARA; 3 Zeynep ISTANBUL; 4 Can IZMIR. "
  "{INSERT} {INTO} basvuru {VALUES}: 101, 1, B1, 800000, ONAY; 102, 1, B2, 300000, RED; 103, 2, B1, 500000, ONAY; "
  "104, 3, B1, 1200000, MANUEL; 105, 2, B2, 450000, ONAY. "
  "{INSERT} {INTO} sozlesme {VALUES}: 9001, 101; 9002, 103. {INSERT} {INTO} police {VALUES}: 7001, 9001, KASKO.",
  bolum="SQL · Laboratuvar")
t("Laboratuvar görevleri (1/2)", ["#", "Görev", "İpucu", "Beklenen"],
  [["1", "Müşteri adıyla tüm başvurular", "musteri JOIN basvuru", "5 satır; Can yok"], ["2", "Hiç başvurusu olmayan müşteri", "LEFT JOIN + IS NULL", "Can"],
   ["3", "Şehir bazında sayı ve toplam", "LEFT JOIN + GROUP BY, COUNT(b.basvuru_id)", "İST 3 / 2.300.000 · ANK 2 / 950.000 · İZM 0 / NULL"],
   ["4", "Onaylı ama sözleşmesiz", "ONAY + anti-join", "105"]],
  "Görevler. Bir: müşteri adıyla birlikte tüm başvuruları listele; müşteri {JOIN} başvuru. Beklenen: beş satır, Can listede yok. "
  "İki: hiç başvurusu olmayan müşteriyi bul; {LEFT JOIN} ve {IS NULL}. Beklenen: Can. "
  "Üç: şehir bazında başvuru sayısı ve toplam tutar; {LEFT JOIN}, şehre göre {GROUP BY} ve {COUNT} başvuru id. "
  "Beklenen: İstanbul üç başvuru, iki milyon üç yüz bin; Ankara iki, dokuz yüz elli bin; İzmir sıfır ve {NULL}. "
  "Dört: onaylanmış ama sözleşmesi olmayan başvuru; durum ONAY ve {anti-join}. Beklenen: yüz beş.")
t("Laboratuvar görevleri (2/2)", ["#", "Görev", "İpucu", "Beklenen"],
  [["5", "Poliçesi olmayan sözleşme", "sözleşme LEFT JOIN poliçe", "9002"],
   ["6", "Her müşterinin en yüksek başvurusu", "ROW_NUMBER() … ORDER BY tutar DESC", "(1, 101, 800.000) · (2, 103, 500.000) · (3, 104, 1.200.000)"],
   ["7", "Bayi onay oranı (≥ 2 başvuru)", "SUM(CASE …) + HAVING", "B1: 3, %66,7 · B2: 2, %50,0"]],
  "Beş: poliçesi olmayan sözleşme; sözleşme {LEFT JOIN} poliçe. Beklenen: dokuz bin iki. "
  "Altı: her müşterinin en yüksek tutarlı başvurusu; {ROW_NUMBER} {OVER}, müşteri id'ye göre bölümlü, tutara göre azalan. "
  "Beklenen: Ayşe yüz bir, sekiz yüz bin; Mehmet yüz üç, beş yüz bin; Zeynep yüz dört, bir milyon iki yüz bin. "
  "Yedi: bayi bazında onay oranı, en az iki başvuru; {SUM} {CASE} ve {HAVING}. Beklenen: B1 üç başvuru, yüzde altmış altı virgül yedi; "
  "B2 iki başvuru, yüzde elli.")
dikkat("COUNT(*) mı, COUNT(kolon) mu?", "3. görevde COUNT(*) → İZMİR 1 (NULL dolu satır). COUNT(b.basvuru_id) NULL saymaz → 0.",
       "Üçüncü görevde dikkat: {COUNT} yıldız yazarsan İzmir için bir çıkar, çünkü {LEFT JOIN} Can için {NULL} dolu bir satır üretir. "
       "{COUNT} başvuru id ise {NULL}'ları saymaz ve sıfır verir. Bu fark raporlarda en sık yapılan hatalardan biridir. "
       "Kendi sonucunu kontrol etme yöntemi: her sorgudan sonra satır sayısını tahmin et, sonra çalıştır. "
       "Tahminin tutmuyorsa {JOIN} çoğaltması ya da {NULL} davranışı vardır.")

# ───────────────────────────── Uygulama paketi
m("Hazırlık: veriye iki kusur ekle", ["INSERT sozlesme (9003, NULL): başvurusuz sözleşme", "INSERT police (7002, 9001, 'TRAFIK'): 9001'e ikinci poliçe",
                                      "Artık 5. görevin sonucu: 9002 ve 9003", "Sonuçlar SQLite'ta doğrulandı; PostgreSQL'de de aynı"],
  "SQL uygulama paketi: tuzaklar, veri kalitesi ve hata ayıklama. Hazırlık olarak veriye iki kusur ekle. "
  "Gerçek sistemlerde sık görülen iki kusuru temsil ederler. Birincisi dokuz bin üç numaralı sözleşme, başvurusu boş, yani {NULL}: bir veri kalitesi hatası. "
  "İkincisi yedi bin iki numaralı poliçe, dokuz bin bir'e bağlı ikinci bir poliçe; türü TRAFIK. "
  "Bu iki satırdan sonra laboratuvardaki beşinci görevin sonucu dokuz bin iki ve dokuz bin üç olur. "
  "Aşağıdaki sonuçlar bu veriyle {SQLite} üzerinde doğrulanmıştır; {PostgreSQL}'de de aynısı çıkar.", bolum="SQL · Tuzaklar")
m("Tuzak 1: NOT IN ve NULL", ["Soru: onaylı ama sözleşmesiz başvuru?", "YANLIŞ: basvuru_id NOT IN (SELECT basvuru_id FROM sozlesme) → 0 satır",
                              "Listede NULL var (9003): 105 ≠ NULL → \"bilinmiyor\" → WHERE'den geçmez",
                              "DOĞRU: NOT EXISTS (… s.basvuru_id = b.basvuru_id) → 105"],
  "Tuzak bir: {NOT IN} ve {NULL}. Soru: onaylanmış ama sözleşmesi olmayan başvuru hangisi? "
  "Yanlış sorgu: durum ONAY ve basvuru_id {NOT IN}, parantez içinde {SELECT} basvuru_id {FROM} sozlesme. Sıfır satır döner. "
  "Neden yanlış? Alt sorgu listesinde bir {NULL} var; dokuz bin üç. Yüz beş {NOT IN} yüz bir, yüz üç, {NULL} ifadesi şunu da sorar: "
  "yüz beş {NULL}'a eşit değil mi? Cevap bilinmiyordur. Bilinmeyen sonuç {WHERE}'den geçemez; bu yüzden hiçbir satır dönmez. "
  "Dakikalarca veri yok sanabilirsin. "
  "Doğru sorgu: {NOT EXISTS}, sözleşmenin başvuru id'si eşittir başvurunun id'si. Sonuç: yüz beş.")
m("Tuzak 2: LEFT JOIN'den sonra WHERE", ["Soru: her müşterinin onaylı başvuru sayısı, onayı olmayan 0 görünsün",
                                         "YANLIŞ: LEFT JOIN … WHERE b.durum = 'ONAY' → yalnız Ayse ve Mehmet",
                                         "Can'ın NULL satırı ve Zeynep'in MANUEL satırı elenir → INNER'a döner",
                                         "DOĞRU: koşulu ON içine taşı + COALESCE(SUM(tutar), 0)"],
  "Tuzak iki: {LEFT JOIN}'den sonra {WHERE} filtresi. Soru: her müşterinin onaylanmış başvuru sayısı ve tutarı; hiç onayı olmayan müşteri sıfır görünsün. "
  "Yanlış sorgu: müşteri {LEFT JOIN} başvuru, sonra {WHERE} durum eşittir ONAY. Yalnız Ayşe ve Mehmet döner. "
  "Neden? {LEFT JOIN} başvurusu olmayan Can için {NULL} dolu bir satır üretir. {WHERE} durum ONAY bu satırı ve Zeynep'in MANUEL satırını eler. "
  "Sonuçta {LEFT JOIN}, {INNER JOIN}'e dönüşmüş olur. "
  "Doğru sorgu: koşulu {ON} içine taşı; {LEFT JOIN} başvuru {ON} müşteri id eşleşmesi {AND} durum ONAY. Tutar için {COALESCE} {SUM} tutar, sıfır.")
t("Tuzak 2: doğru sonuç", ["ad", "onay_sayisi", "onay_tutari"],
  [["Ayse", "1", "800000"], ["Mehmet", "2", "950000"], ["Zeynep", "0", "0"], ["Can", "0", "0"]],
  "Doğru sorgunun sonucu: Ayşe bir onay, sekiz yüz bin. Mehmet iki onay, dokuz yüz elli bin. Zeynep sıfır, sıfır. Can sıfır, sıfır. "
  "Dört müşterinin dördü de listede.")
m("Tuzak 3: JOIN çoğaltması (fan-out)", ["Soru: poliçesi olan sözleşmelerin başvuru tutarı toplamı?",
                                         "YANLIŞ: basvuru JOIN sozlesme JOIN police → SUM = 1.600.000",
                                         "9001'in iki poliçesi var (KASKO, TRAFIK): 101 iki satır, 800.000 iki kez",
                                         "DOĞRU: WHERE EXISTS (sozlesme JOIN police …) → 800.000"],
  "Tuzak üç: {JOIN} çoğaltması, yani {fan-out}. Soru: poliçesi olan sözleşmelere ait başvuruların toplam tutarı nedir? "
  "Yanlış sorgu: başvuru {JOIN} sözleşme {JOIN} poliçe, sonra {SUM} tutar. Bir milyon altı yüz bin döner. "
  "Neden? Dokuz bin bir numaralı sözleşmenin iki poliçesi var, KASKO ve TRAFIK. {JOIN} yüz bir numaralı başvuruyu iki satıra çoğaltır "
  "ve sekiz yüz bin iki kez toplanır. Toplam bir olma sorusunun cevabıysa {JOIN} yerine {EXISTS} kullan. "
  "Doğru sorgu: {WHERE} {EXISTS}, sözleşme {JOIN} poliçe, başvuruya bağlı. Sonuç sekiz yüz bin.")
dikkat("Kontrol alışkanlığı", "JOIN'den önce ve sonra COUNT(*) ile COUNT(DISTINCT b.basvuru_id) karşılaştır. Farklıysa satırlar çoğalmıştır.",
       "Kontrol alışkanlığı: {JOIN}'den önce ve sonra {COUNT} yıldız ile {COUNT} {DISTINCT} başvuru id değerlerini karşılaştır. "
       "İkisi farklıysa satırlar çoğalmıştır.")
m("Veri kalitesi ve CTE + sıralama", ["sozlesme WHERE basvuru_id IS NULL → 9003",
                                      "WITH bayi_onay: ONAY'ları bayiye göre topla", "RANK() OVER (ORDER BY toplam DESC) → sira",
                                      "Sonuç: B1 1300000 sıra 1 · B2 450000 sıra 2"],
  "Veri kalitesi kontrolü ve {CTE} ile sıralama. sozlesme {WHERE} basvuru_id {IS NULL}: dokuz bin üç. "
  "Bayi bazlı onaylanan tutar: bayi onay adlı {CTE}, durumu ONAY olanların tutarını bayiye göre toplar. "
  "Sonra {RANK} {OVER}, toplama göre azalan; buna sıra de. Sonuç: B1 1300000, sıra 1; B2 450000, sıra 2.")
dikkat("Bulgu → gereksinim", "EARS (istenmeyen davranış): \"Sözleşme oluşturulurken basvuru_id boşsa, sistem kaydı oluşturmamalı ve 'Sözleşme bir başvuruya bağlı olmalıdır' göstermeli.\" Doğrulama: Test.",
       "Bir veri kalitesi bulgusu tek başına iş değildir; bir gereksinime dönüşmelidir. "
       "Örnek, {EARS}'ın istenmeyen davranış kalıbıyla: sözleşme kaydı oluşturulurken başvuru id alanı boşsa, sistem kaydı oluşturmamalı "
       "ve sözleşme bir başvuruya bağlı olmalıdır mesajını göstermelidir. Doğrulama yöntemi: test.", tip="bilgi")
t("Veritabanına göre yazım farkları", ["İşlem", "PostgreSQL / SQLite", "SQL Server", "Oracle"],
  [["İlk 10 satır", "LIMIT 10", "TOP 10", "FETCH FIRST"], ["Bugün", "CURRENT_DATE", "GETDATE()", "SYSDATE"],
   ["NULL yerine", "COALESCE", "ISNULL", "NVL"], ["Birleştirme", "a || b", "a + b", "a || b"], ["Fark", "EXCEPT", "EXCEPT", "MINUS"]],
  "Veritabanına göre yazım farkları. İlk on satır: {PostgreSQL} ve {SQLite}'ta {LIMIT} on; {SQL Server}'da {SELECT} {TOP} on; {Oracle}'da {FETCH FIRST} on {ROWS ONLY}. "
  "Bugünün tarihi: {CURRENT_DATE}; {SQL Server}'da {CAST} {GETDATE} {AS DATE}; {Oracle}'da {TRUNC} {SYSDATE}. "
  "{NULL} yerine değer: {COALESCE}; {SQL Server}'da {ISNULL}, {Oracle}'da {NVL} de olur. "
  "Metin birleştirme: çift dikey çizgi; {SQL Server}'da artı ya da {CONCAT}. "
  "Fark kümesi: {EXCEPT}; {Oracle}'da {MINUS}.")
m("Bağımsız görev", ["1. Her bayi için onaylı ama sözleşmesiz başvuru sayısı (yoksa 0)", "Ayrı bayi tablosu yok: en az bir başvurusu olanlar",
                     "2. Poliçesiz sözleşmeler + müşteri adı; müşterisi bulunamayan da kalsın", "Doğruysa: ilki 2 satır, ikincisi 2 satır, birinde ad boş"],
  "Bağımsız görev; aynı veriyle iki soru. Bir: her bayi için onaylanmış ama sözleşmesi olmayan başvuru sayısını listele. "
  "Hiç böyle başvurusu olmayan bayi de sıfırla görünsün; şemada ayrı bayi tablosu olmadığı için yalnız en az bir başvurusu olan bayiler listelenir. "
  "İki: poliçesi olmayan sözleşmeleri müşteri adıyla birlikte listele; müşterisi bulunamayan sözleşme de listede kalsın. "
  "Doğru yaptığını nasıl anlarsın? İlk sorguda iki satır, ikinci sorguda iki satır dönüyor ve ikinci sorgunun bir satırında ad boş. "
  "Çözüm videonun sonunda.", bolum="SQL · Bağımsız görev ve sorun giderme")
t("Sorun giderme (1/2)", ["Belirti", "Olası neden", "Çözüm"],
  [["ambiguous column name", "Sütun iki tabloda var", "b.basvuru_id gibi kısaltma yaz"],
   ["must appear in the GROUP BY", "Gruplanmayan, toplanmayan sütun", "GROUP BY'a ekle ya da MAX()"],
   ["0 satır ama veri var", "NOT IN + NULL ya da = NULL", "NOT EXISTS, IS NULL"]],
  "Sorun giderme. {ambiguous column name}, başvuru id hatası: aynı sütun iki tabloda var. Sütunun önüne tablo kısaltmasını yaz; b nokta başvuru id gibi. "
  "{PostgreSQL}'de {must appear in the GROUP BY clause} hatası: {SELECT}'te gruplanmayan ve toplanmayan bir sütun var. "
  "Sütunu {GROUP BY}'a ekle ya da {MAX} gibi bir toplama fonksiyonuna al. "
  "Sorgu sıfır satır döndü ama veri olduğunu biliyorsun: {NOT IN} ile {NULL} ya da eşittir {NULL}. {NOT EXISTS} ve {IS NULL} kullan.")
t("Sorun giderme (2/2)", ["Belirti", "Olası neden", "Çözüm"],
  [["Toplam beklenenden büyük", "JOIN çoğaltması", "Satır sayısını karşılaştır; EXISTS"], ["LEFT JOIN'de müşteriler eksik", "Sağ koşulu WHERE'de", "ON içine taşı"],
   ["UPPER(sehir) = 'IZMIR' eşleşmiyor", "Türkçe yerelde i → İ", "Saklı yazımla karşılaştır ya da collation sor"]],
  "Toplamlar beklenenden büyük: {JOIN} çoğaltması. {JOIN} öncesi ve sonrası satır sayısını karşılaştır; {EXISTS} kullan ya da önce grupla sonra birleştir. "
  "{LEFT JOIN} yaptım ama bazı müşteriler yok: sağ tablo için yazılan koşul {WHERE}'de; {ON} içine taşı. "
  "{UPPER} şehir eşittir IZMIR Türkçe veride eşleşmiyor: Türkçe yerel ayarda küçük i büyük harfe noktalı İ olarak çevrilir. "
  "Karşılaştırmayı saklı değerin yazımıyla yap ya da veritabanının harmanlama, yani {collation} ayarını sor.")

soru("Bilgi kontrolü 1/5", "WHERE kefil_id = NULL kaç satır döner?",
     ["Kefili olmayan tüm satırlar", "Hiçbir satır", "Tüm satırlar", "Hata verir"], 1,
     "Beş soruluk bilgi kontrolü. Birinci soru: {WHERE} kefil id eşittir {NULL} kaç satır döner? "
     "A, kefili olmayan tüm satırlar. B, hiçbir satır. C, tüm satırlar. D, hata verir.",
     "Doğru cevap B: hiçbir satır. {NULL} eşitlikle karşılaştırılamaz; {IS NULL} kullanılır.", bolum="SQL · Bilgi kontrolü ve çözümler")
soru("Bilgi kontrolü 2/5", "Alt sorgu listesinde NULL varsa NOT IN ne döndürür?",
     ["NULL'u yok sayar", "Hiçbir satır", "Yalnız NULL satırları", "Hata verir"], 1,
     "İkinci soru: alt sorgu listesinde {NULL} varsa {NOT IN} ne döndürür? A, {NULL}'u yok sayar. B, hiçbir satır. C, yalnız {NULL} satırları. D, hata verir.",
     "Doğru cevap B: hiçbir satır.")
soru("Bilgi kontrolü 3/5", "Bir sözleşmenin iki poliçesi varken başvuru tutarını poliçeyle JOIN edip toplarsan?",
     ["Tutar iki kez sayılır", "Tutar sıfırlanır", "Sonuç değişmez", "Sorgu hata verir"], 0,
     "Üçüncü soru: bir sözleşmenin iki poliçesi varken başvuru tutarını poliçe tablosuyla {JOIN} edip toplarsan ne olur? "
     "A, tutar iki kez sayılır. B, tutar sıfırlanır. C, sonuç değişmez. D, sorgu hata verir.",
     "Doğru cevap A: tutar iki kez sayılır; {fan-out}.")
soru("Bilgi kontrolü 4/5", "LEFT JOIN'de sol tablonun tüm satırları kalsın diye sağ tabloya ait koşul nereye yazılır?",
     ["WHERE", "HAVING", "ON", "ORDER BY"], 2,
     "Dördüncü soru: {LEFT JOIN}'de sağ tabloya ait koşul nereye yazılmalı ki sol tablonun tüm satırları kalsın? "
     "A, {WHERE}. B, {HAVING}. C, {ON}. D, {ORDER BY}.",
     "Doğru cevap C: {ON}.")
soru("Bilgi kontrolü 5/5", "Oracle'da EXCEPT yerine geleneksel olarak (21c öncesi) hangisi kullanılır?",
     ["DIFF", "MINUS", "EXCLUDE", "NOT UNION"], 1,
     "Beşinci soru: {Oracle}'da {EXCEPT} yerine geleneksel olarak, yirmi bir c öncesi sürümlerde, hangi anahtar kelime kullanılır? "
     "A, {DIFF}. B, {MINUS}. C, {EXCLUDE}. D, {NOT UNION}.",
     "Doğru cevap B: {MINUS}.")
t("Hızlı başvuru: \"olmayan\" kayıtları bulma", ["Soru", "Güvenli kalıp"],
  [["A'da olup B'de olmayan", "NOT EXISTS"], ["A'nın hepsi + eşleşen B", "LEFT JOIN … ON … AND koşul"],
   ["B'de eşleşmesi olan A", "EXISTS"], ["Boş değer · boşsa 0", "IS NULL · COALESCE(SUM(x), 0)"],
   ["Sayım, NULL hariç", "COUNT(sutun) · COUNT(*)"]],
  "Hızlı başvuru: olmayan kayıtları bulma kalıpları. A'da olup B'de olmayan: {WHERE} {NOT EXISTS}, B'de A'nın anahtarı. "
  "A'nın hepsi, B'den eşleşen varsa: A {LEFT JOIN} B, {ON} anahtar eşitliği {AND} B koşulu. "
  "B'de en az bir eşleşmesi olan A, çoğaltmadan: {WHERE} {EXISTS}. Boş değer: {IS NULL} ya da {IS NOT NULL}. Boşsa sıfır göster: {COALESCE} {SUM}. "
  "Sayım, {NULL} hariç: {COUNT} sütun; tüm satırlar için {COUNT} yıldız.")
m("Çözüm 1: bayi bazlı sözleşmesiz onay", ["SELECT bayi_id, SUM(CASE WHEN durum = 'ONAY' AND NOT EXISTS (sozlesme …) THEN 1 ELSE 0 END)",
                                          "FROM basvuru GROUP BY bayi_id", "Sonuç: B1 0 · B2 1"],
  "Bağımsız görevin çözümü. Bir: bayi id ve {SUM} {CASE} {WHEN} durum ONAY {AND} {NOT EXISTS} sözleşme ise bir, değilse sıfır; "
  "{FROM} basvuru {GROUP BY} bayi_id. Sonuç: B1 sıfır, B2 bir.")
m("Çözüm 2: poliçesiz sözleşme ve ad", ["sozlesme LEFT JOIN basvuru LEFT JOIN musteri", "WHERE NOT EXISTS (police …)",
                                        "Sonuç: 9002 Mehmet · 9003 NULL", "JOIN yazarsan 9003 düşer → veri kalitesi sorunu görünmez"],
  "İki: sozlesme {LEFT JOIN} basvuru {LEFT JOIN} musteri; {WHERE} {NOT EXISTS} poliçe. Sonuç: dokuz bin iki Mehmet, dokuz bin üç {NULL}. "
  "İkinci sorguda {LEFT JOIN} yerine {JOIN} yazarsan dokuz bin üç listeden düşer ve veri kalitesi sorunu görünmez olur. "
  "Bir iş analisti için bu satır en değerli satırdır.")
m("Bu videoda neler gördük?", ["Komut aileleri, çalışma sırası, filtre, toplama, JOIN türleri", "EXISTS, CTE, fonksiyonlar, set, DDL/DML, normalizasyon",
                               "Window, recursive CTE, transaction, performans, veri kalitesi", "Araçlar, laboratuvar, 3 tuzak, bulgu → gereksinim",
                               "Yazım farkları, sorun giderme, kalıplar"],
  "Toparlayalım. Komut ailelerini, {SELECT}'in çalışma sırasını, filtreleri, toplamayı ve {JOIN} türlerini gördük. "
  "{EXISTS}, {CTE}, fonksiyonlar, set operatörleri, DDL ve DML ile normalizasyonu çalıştık. "
  "Pencere fonksiyonları, {recursive} {CTE}, işlem izolasyonu, performans ve veri kalitesi kontrollerine geçtik. "
  "Araçları, laboratuvarı, üç tuzağı ve bulgudan gereksinim yazmayı öğrendik; yazım farklarına, sorun gidermeye ve kalıplara baktık. "
  "Bir sonraki videoda ELK ile loglardan bir hatanın izini süreceğiz.", ton="sakin")

kaydet(__file__, {
    "baslik": "Business Analyst Teknik Rehberi · 6: SQL",
    "alt_baslik": "JOIN · GROUP BY · CTE · window · NULL tuzakları · veri kalitesi",
    "kapanis": "Sıradaki video: ELK",
    "tema": 6,
    "youtube_baslik": "Business Analyst Teknik Rehberi 6/14: SQL (JOIN, NULL tuzakları, fan-out, veri kalitesi)",
    "etiketler": ["business analyst", "SQL", "JOIN", "veri kalitesi", "DBeaver", "iş analisti"],
}, {"DQL": "di kyu el", "DML": "di em el", "DDL": "di di el", "DCL": "di si el", "TCL": "ti si el", "TCKN": "te ce ka en",
    "ISO/IEC": "iso", "PK": "pi key", "FK": "ef key", "SSMS": "es es em es", "XLSX": "eks el es eks", "CSV": "si es vi",
    "EARS": "iırs", "1NF": "birinci normal form", "2NF": "ikinci normal form", "3NF": "üçüncü normal form",
    "ISTANBUL": "istanbul", "IZMIR": "izmir", "ANKARA": "ankara", "ONAY": "onay", "RED": "red", "MANUEL": "manuel", "IPTAL": "iptal",
    "KASKO": "kasko", "TRAFIK": "trafik", "Ayse": "ayşe", "dbeaver.io": "dibiver nokta io", "sqliteonline.com": "es kyu layt onlayn nokta kom",
    "B1": "be bir", "B2": "be iki", "21c": "yirmi bir si",
    **{k: v for k, v in {"musteri": "müşteri", "basvuru": "başvuru", "sozlesme": "sözleşme", "police": "poliçe", "sehir": "şehir", "tckn": "te ce ka en", "dogum_tarihi": "doğum tarihi", "musteri_id": "müşteri ay di", "basvuru_id": "başvuru ay di", "sozlesme_id": "sözleşme ay di", "taksit_id": "taksit ay di", "bayi_id": "bayi ay di", "police_id": "poliçe ay di", "kampanya_id": "kampanya ay di", "urun": "ürün", "kkb_skor": "ka ka be skor", "basvuru_tarihi": "başvuru tarihi", "kullandirim_tarihi": "kullandırım tarihi", "faiz_orani": "faiz oranı", "taksit_no": "taksit no", "vade_tarihi": "vade tarihi", "odeme_tarihi": "ödeme tarihi", "bayi_adi": "bayi adı", "bolge": "bölge", "tur": "tür", "baslangic": "başlangıç", "baslangic'a": "başlangıca", "bitis": "bitiş", "basvuru_sayisi": "başvuru sayısı", "onay_sayisi": "onay sayısı", "onay_orani": "onay oranı", "sozlesme_sayisi": "sözleşme sayısı", "rn": "ar en", "ISTANBUL": "istanbul", "IPTAL": "iptal"}.items()}})
