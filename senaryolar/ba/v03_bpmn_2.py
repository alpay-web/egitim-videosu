#!/usr/bin/env python3
"""BA Teknik Rehberi · Video 3: BPMN 2 (ileri desenler, araçlar, menü rehberi, P01 laboratuvarı, uygulama paketi).
Belge satır 698–921. Çalıştır: python v03_bpmn_2.py"""
from ortak import m, t, dikkat, g, soru, kaydet

# ───────────────────────────── İleri desenler
m("İleri seviye BPMN: Firma desenleri", ["1. Telafi ve Saga", "2. Hata ile eskalasyonu ayırmak", "3. Mesaj korelasyonu",
                                         "4. Zaman ifadeleri (ISO 8601)", "5. BPMN + DMN ayrımı", "6–8. Seviyelendirme, denetim izi, anti-desenler"],
  "Önceki videoda BPMN'in sembollerini ve kapılarını gördük. Bu videoda ileri seviye desenlerle başlıyoruz; "
  "sonra araçları, menüleri, P01 laboratuvarını ve uygulama paketini çalışacağız. "
  "Sekiz desen var: telafi ve {Saga}; hata ile eskalasyonu ayırmak; mesaj korelasyonu; {ISO} sekiz bin altı yüz bir zaman ifadeleri; "
  "BPMN ile DMN ayrımı; ve son olarak seviyelendirme, denetim izi ve anti-desenler.",
  bolum="BPMN · İleri desenler", kanca="Diyagram düzgün görünür ama süreç takılır: bu videonun konusu bu.", ton="merakli")
t("1. Telafi (compensation) ve Saga", ["Adım", "Telafisi"],
  [["Bayiye EFT", "Bayiden iade al"], ["Rehin tescili", "Rehni kaldır"],
   ["Kasko poliçesi", "Poliçeyi iptal et, prim iadesi (P11)"], ["Kredi aktif", "Krediyi kapat"]],
  "Birinci desen telafi, yani {compensation}, ve {Saga}. Uzun süren işlemlerde veritabanındaki gibi bir geri al yoktur; "
  "her adımın tersini yapan bir telafi adımı tanımlanır. Firma örneği F04, cayma hakkı: kredi kullandırıldıktan sonra müşteri cayarsa ne olur? "
  "Bayiye EFT adımının telafisi bayiden iade almak. Rehin tescilinin telafisi rehni kaldırmak. "
  "Kasko poliçesinin telafisi poliçeyi iptal etmek ve prim iadesi; bu P11. Kredi aktif adımının telafisi de krediyi kapatmak. "
  "Çizimde her adımın yanına geri sar ikonlu bir telafi sınır olayı koyarsın ve ona {association} ile bağlı telafi görevini çizersin. "
  "Süreç bir telafi atan olayıyla bunları ters sırada çalıştırır.")
m("2. Hata ile eskalasyonu ayır", ["Hata: iş yapılamıyor, normal yolu keser (\"KKB servisi çalışmıyor\")",
                                   "Eskalasyon: iş sürüyor, üst seviye bilgilenmeli (\"limit aşımı, komiteye bildir\")",
                                   "Eskalasyonu hatayla çizmek süreci gereksiz yere keser"],
  "İkinci desen: hata ile eskalasyonu ayırmak. Hata, işin yapılamadığını söyler ve normal yolu keser; örneğin KKB servisi çalışmıyor. "
  "Eskalasyon ise işin devam ettiğini ama üst seviyenin bilgilenmesi gerektiğini söyler; "
  "örneğin kredi tutarı uzmanın limitini aşıyor, komiteye bildir. Eskalasyonu hata ile modellersen süreci gereksiz yere kesersin.")
m("3. Mesaj korelasyonu", ["Gelen mesaj hangi süreç örneğine ait?", "\"İmza geldi\" ↔ başvuru numarası",
                           "\"Poliçe numarası geldi\" ↔ teklif numarası", "Gereksinime yaz: korelasyon anahtarı: başvuruNo",
                           "U04'teki correlation-id: aynı fikir, loglamada"],
  "Üçüncü desen mesaj korelasyonu. Bir mesaj gelince hangi süreç örneğine ait olduğu bilinmelidir. "
  "İmza geldi mesajı başvuru numarasıyla, poliçe numarası geldi mesajı teklif numarasıyla eşleşir. "
  "İş analisti gereksinime şunu yazar: korelasyon anahtarı başvuru numarası. "
  "U04'teki {correlation-id} de aynı fikrin loglamadaki karşılığıdır; bunu ELK videosunda tekrar göreceğiz.")
t("4. Zaman ifadeleri (ISO 8601)", ["İfade", "Anlamı"],
  [["PT5S · PT4H", "5 saniye · 4 saat"], ["P1D · P30D", "1 gün · 30 gün"],
   ["R/2026-12-01T08:00/P1D", "Her gün 08:00"], ["R3/PT10M", "10 dakikada bir, 3 kez"]],
  "Dördüncü desen zaman ifadeleri. P T beş S beş saniye, P T dört H dört saat demek. "
  "P bir D bir gün, P otuz D otuz gün. "
  "R, iki bin yirmi altı, on iki, bir, T sekiz sıfır sıfır, P bir D: her gün sabah sekizde. "
  "R üç, P T on M: on dakikada bir, üç kez.")
dikkat("İş günü ISO'da yoktur", "\"2 iş günü\" yazamazsın. Tatile denk gelen vade gibi iş takvimi kuralı ayrı gereksinim olarak yazılır.",
       "Burada çok önemli bir tuzak var: iş günü kavramı {ISO} standardında yoktur. "
       "İki iş günü diye bir zamanlayıcı yazamazsın. Tatile denk gelen vadenin sonraki iş gününe kayması gibi iş takvimi kuralları "
       "ayrı bir gereksinim olarak yazılır.")
m("5. BPMN + DMN ayrımı", ["Süreçte kural yazma: kuralı DMN tablosuna koy", "Süreçte tek bir business rule task bırak",
                          "Adaylar: kredi/değer kademeleri, kampanya koşulları, ikinci el garanti",
                          "Kampanya değişince yalnız tablo güncellenir (B04 parametre ekranı)"],
  "Beşinci desen: BPMN ile DMN'i ayırmak. Süreçte kural yazma; kuralı DMN tablosuna koy ve süreçte tek bir {business rule task} bırak. "
  "Bireysel kredi değer kademeleri, kampanya koşulları ve ikinci el garanti uygunluğu kural tablosu adaylarıdır. "
  "Böylece kampanya değişince süreç değil yalnız tablo güncellenir; bu da B04 parametre ekranının işi.")
t("6. Seviyelendirme", ["Seviye", "Ne", "Firma örneği"],
  [["L0", "Değer zinciri", "Satış → Kredi → Operasyon → Tahsilat → Sigorta"], ["L1", "Süreç grubu", "Bireysel kredi yönetimi"],
   ["L2", "Uçtan uca süreç", "P01"], ["L3", "Alt süreç", "Belge kontrolü, Kasko poliçesi düzenle"], ["L4", "Ekran adımı", "D03–D07"]],
  "Altıncı desen seviyelendirme. L sıfır değer zinciri: satış, kredi, operasyon, tahsilat ve sigorta. "
  "L bir süreç grubu: bireysel kredi yönetimi. L iki uçtan uca süreç: P01. "
  "L üç alt süreç: belge kontrolü ya da kasko poliçesi düzenle. L dört ekran adımı: D03'ten D07'ye kadar. "
  "Kural: bir diyagram on beş yirmi akış nesnesini aşıyorsa bir alt seviyeye böl.")
m("7. Kontrol ve denetim izi", ["Dört göz: P01 kullandırım kontrolü ve checker onayı",
                                "SoD: ödemeyi giren ≠ onaylayan", "Log noktaları",
                                "Açıklama notu ya da grup ile işaretle", "Denetçi kontrolün yerini görebilmeli"],
  "Yedinci desen kontrol ve denetim izi. Dört göz kontrolü, örneğin P01'deki kullandırım kontrolü ve {checker} onayı; "
  "görevler ayrılığı, yani SoD: ödemeyi giren kişi onaylayan kişiyle aynı olamaz; ve log noktaları. "
  "Bunları diyagramda açıklama notu ya da grup ile işaretlersin. Denetçi diyagrama bakıp kontrolün nerede olduğunu görebilmelidir.")
m("8. Anti-desenler", ["Analitikte bayiyi şerit yapıp sequence flow ile bağlamak", "\"Bekle\" adlı user task",
                       "Ret, iptal, süre dolması için tek adsız bitiş", "Çakışan XOR koşulları (≥ 1500 ve ≤ 1500)",
                       "Dış servislerde (KKB, KPS, 3D Secure) hata yolu yok"],
  "Sekizinci desen, Firma'da sık göreceğin anti-desenler. Bir: analitik seviyede bayiyi Firma havuzunda şerit yapıp {sequence flow} ile bağlamak. "
  "İki: Bekle adlı bir {user task}. Üç: ret, iptal ve süresi dolma için tek bir adsız bitiş. "
  "Dört: {XOR} koşullarının çakışması; örneğin skor bin beş yüze eşit ya da büyük, ve skor bin beş yüze eşit ya da küçük; "
  "bin beş yüz iki koşula da girer. Beş: KKB, KPS, {3D Secure} gibi dış servislerde hiç hata yolu çizmemek.")
soru("Kendini sına 1/4", "\"Rehin fekki\" adımını P05'te nasıl çizersin?",
     ["Gömülü alt süreç", "Call activity", "Manual task", "Event alt süreci"], 1,
     "Kendini sınayalım; dört soru var. Birinci soru: rehin fekki adımını P05'te nasıl çizersin? "
     "A, gömülü alt süreç. B, {call activity}. C, {manual task}. D, olay alt süreci.",
     "Doğru cevap B: {call activity}. Erken kapama, son taksit, pert kapanışı ve kredi devri aynı süreci kullanır.",
     bolum="BPMN · Kendini sına")
soru("Kendini sına 2/4", "Kredi komitesinde 2 iş günü içinde karar çıkmazsa ne çizersin?",
     ["Kesen zamanlayıcı", "Kesmeyen zamanlayıcı + eskalasyon bildirimi", "Hata olayı", "Sonlandırma"], 1,
     "İkinci soru: kredi komitesine giden başvuruda iki iş günü içinde karar çıkmazsa ne çizersin? "
     "A, kesen zamanlayıcı. B, kesmeyen zamanlayıcı ve eskalasyon bildirimi. C, hata olayı. D, sonlandırma.",
     "Doğru cevap B. Kesmeyen zamanlayıcı ve eskalasyon bildirimi; komite kararı beklenmeye devam eder.")
soru("Kendini sına 3/4", "Sigorta şirketi ile Firma arasındaki poliçe iptal talebi hangi okla çizilir?",
     ["Sequence flow", "Association", "Message flow", "Data flow"], 2,
     "Üçüncü soru: sigorta şirketi ile Firma arasındaki poliçe iptal talebini hangi okla çizersin? "
     "A, {sequence flow}. B, {association}. C, {message flow}. D, {data flow}.",
     "Doğru cevap C: {message flow}. Sigorta şirketi ayrı bir havuzdur.")
soru("Kendini sına 4/4", "D06'da müşteri hiçbir isteğe bağlı sigorta seçmezse OR kapısı ne yapmalı?",
     ["Tüm kolları açmalı", "Varsayılan akışı (\"sigorta yok\") izlemeli", "Süreci sonlandırmalı", "Bekletmeli"], 1,
     "Dördüncü soru: D06'da müşteri hiçbir isteğe bağlı sigorta seçmezse {OR} kapısı ne yapmalı? "
     "A, tüm kolları açmalı. B, varsayılan akışı, yani sigorta yok yolunu izlemeli. C, süreci sonlandırmalı. D, bekletmeli.",
     "Doğru cevap B: varsayılan akış. Varsayılan akış yoksa süreç hata verir; bu yüzden {OR} kapısına mutlaka varsayılan akış konur.")

# ───────────────────────────── Araçlar ve menü
t("Hangi araçla çizilir?", ["Araç", "Ücret", "Ne zaman"],
  [["demo.bpmn.io", "Ücretsiz", "Öğrenme, hızlı deneme"],
   ["Camunda Modeler", "Ücretsiz", "BPMN + DMN, kural kontrolü"],
   ["draw.io / diagrams.net", "Ücretsiz", "Dokümantasyon çizimi"],
   ["Visio (BPMN şablonu)", "Lisanslı", "Kurumsal standart Microsoft"],
   ["Signavio, ARIS, Bizagi", "Kurumsal", "Kütüphane, simülasyon"]],
  "Araçlara geçelim. demo nokta bpmn nokta io tarayıcıda çalışır, ücretsiz ve kurulumsuzdur; öğrenme ve hızlı deneme için. Nokta bpmn olarak indirilir. "
  "{Camunda} {Modeler} ücretsiz bir masaüstü aracıdır: BPMN ve DMN, çalıştırılabilir model ve kural kontrolü. "
  "draw.io, diğer adıyla diagrams nokta net, ücretsizdir ve Confluence eklentisi var; dokümantasyon için çizim. "
  "Microsoft Visio'nun BPMN şablonu lisanslıdır; kurumsal standart Microsoft ise. "
  "{Signavio}, {ARIS} ve {Bizagi} kurumsal araçlardır: süreç kütüphanesi, simülasyon ve yönetişim. "
  "Firma çalışma setindeki P01'den P15'e kadar süreçleri yeniden çizmek için {Camunda} {Modeler} ya da bpmn nokta io kullanabilirsin.",
  bolum="BPMN · Araçlar ve menüler")
g("Modelleme aracının ekranı", "g12.png",
  [([0.0, 0.08, 1.0, 0.24], "Menü çubuğu ve sekmeler"), ([0.0, 0.24, 0.24, 0.85], "Palet: sürükle ve bırak"),
   ([0.24, 0.24, 0.7, 0.85], "Tuval ve bağlam menüsü"), ([0.7, 0.24, 1.0, 0.85], "Özellikler paneli"),
   ([0.0, 0.85, 1.0, 0.95], "Alt çubuk: Problems, Deploy")],
  "Bu araçların ekranı şöyle düzenlenmiştir. En üstte menü çubuğu: {File}, {Edit}, {Window}, {Help}. Altında sekmeler: açık nokta bpmn ve nokta dmn dosyaları; "
  "artıyla yeni dosya açılır. "
  "Solda palet, yani araç kutusu: el ve kement seçim araçları, boşluk aracı, global bağlantı, üç tip olay, kapı, görev ve alt süreç, "
  "{data object} ve {store}, {pool} ya da {participant}, ve {group}. Sürükleyip tuvale bırakırsın. "
  "Ortada tuval, yani {canvas}. Bir öğeye tıklayınca bağlam menüsü açılır: sonraki öğeyi ekle, anahtar ile tür değiştir, ok ile bağla, çöp kutusu ile sil. "
  "Çift tıklayınca etiket yazarsın, tekerlekle yakınlaştırırsın. "
  "Sağda özellikler paneli: {General} altında {Name} ve {ID}, {Documentation}, {Implementation}, {Assignment} yani atama, "
  "{Inputs} ve {Outputs}, akışlarda {Condition}, zaman olaylarında {Timer}. Panel seçili öğeye göre değişir. "
  "En altta {Problems}, yani kural hataları; {Deploy}, roket simgesi; ve {Start instance}, oynat simgesi.")
t("Menü rehberi (1/4)", ["Yapmak istediğin", "Nasıl"],
  [["Yeni BPMN dosyası", "File → New File → BPMN diagram (Camunda 7 / 8)"],
   ["Yeni DMN tablosu", "File → New File → DMN diagram; karar kutusunun tablo ikonu"],
   ["Öğe eklemek", "Paletten sürükle-bırak ya da öğeye tıkla → bağlam menüsü"],
   ["Görev türünü değiştirmek", "Göreve tıkla → anahtar (wrench) → User / Service / Business Rule Task"]],
  "Şimdi menü ve kontrol rehberi; {Camunda} {Modeler} ve bpmn nokta io için. "
  "Yeni BPMN dosyası: {File}, {New File}, {BPMN diagram}; {Camunda} yedi ya da sekiz seç. "
  "Yeni DMN tablosu: {File}, {New File}, {DMN diagram}; sonra tuvaldeki karar kutusunun sol üstündeki tablo ikonuna tıkla. "
  "Öğe eklemek için paletten sürükle bırak, ya da mevcut öğeye tıkla ve bağlam menüsünden görev, kapı ya da olay simgesine tıkla; ok otomatik bağlanır. "
  "Görev türünü değiştirmek için göreve tıkla, bağlam menüsündeki anahtara, yani {wrench}'e bas: {User Task}, {Service Task} ya da {Business Rule Task}.")
t("Menü rehberi (2/4)", ["Yapmak istediğin", "Nasıl"],
  [["Etiket yazmak", "Çift tıkla ya da seç + E"], ["Havuz eklemek", "Palette \"Create pool/participant\" → akışın etrafına tıkla"],
   ["Şerit eklemek", "Havuza tıkla → \"Add lane above / below\""],
   ["Akışa koşul", "Oka tıkla → Condition: C8 =approved = true · C7 ${approved}"]],
  "Etiket yazmak için öğeye çift tıkla ya da seçip E tuşuna bas. "
  "Havuz eklemek için paletteki {Create pool} ya da {participant} aracıyla mevcut akışın etrafına tıkla. "
  "Şerit eklemek için havuza tıkla, bağlam menüsünde {Add lane above} ya da {below}. "
  "Akışa koşul yazmak için kapıdan çıkan oka tıkla, özelliklerde {Condition}. "
  "İfade {Camunda} sekizde eşittir {approved} eşittir {true}; {Camunda} yedide dolar, süslü parantez içinde {approved}.")
t("Menü rehberi (3/4)", ["Yapmak istediğin", "Nasıl"],
  [["User task'ı gruba atamak", "Assignment → Candidate groups: kredi-tahsis"],
   ["Business rule task → DMN", "Implementation → DMN decision → Decision ID"],
   ["Zamanlayıcı sınır olayı", "Ara olayı kenara bırak → anahtar → Timer boundary → Duration PT48H"],
   ["Araç kısayolları", "H el · L kement · S boşluk · C bağlantı · Ctrl+Z geri al"]],
  "{User task}'ı bir gruba atamak: görev, özellikler, {Assignment}, {Candidate groups}: kredi tahsis. "
  "{Business rule task}'ı DMN'e bağlamak: görev, özellikler, {Implementation}, {DMN decision}, ardından {Decision ID}; yani DMN dosyasındaki karar kimliği. "
  "Zamanlayıcı sınır olayı: paletten ara olayı görevin kenarına bırak, anahtar, {Timer boundary event}, özelliklerde {Timer}, {Duration} P T kırk sekiz H; yani kırk sekiz saat. "
  "Araçlar arası hızlı geçiş: H el, L kement, S boşluk aracı, C global bağlantı; kontrol Z geri al.")
t("Menü rehberi (4/4)", ["Yapmak istediğin", "Nasıl"],
  [["Hataları görmek", "Alt çubukta Problems: bağlantısız öğe, adsız kapı"],
   ["Resim almak", "File → Export As Image (PNG / SVG)"], ["Kaydetmek", "Ctrl+S → .bpmn (XML), Git'te versiyonlanır"]],
  "Hataları görmek için alt çubuktaki {Problems}: bağlantısız öğe, adı boş kapı gibi uyarılar. "
  "Resim almak için {File}, {Export As Image}: PNG ya da SVG; Confluence ve Word için. "
  "Kaydetmek için kontrol S: nokta bpmn dosyası, yani XML; Git'te versiyonlanabilir.")

# ───────────────────────────── Laboratuvar
m("Laboratuvar: P01'i sıfırdan çiz (~45 dk)", ["1. demo.bpmn.io ya da New File → BPMN diagram",
                                              "Başlangıç olayının adı: \"Araç seçildi, kredi talebi\"",
                                              "2. Havuz \"Firma Kredi\" + Add lane below ile 6 şerit",
                                              "Müşteri · Bayi / Firma Temsilcisi · Sistem · Tahsis · Operasyon · Harici Sistemler"],
  "Şimdi laboratuvar: Firma'nın P01 kredi sürecini sıfırdan çiziyoruz; yaklaşık kırk beş dakika. "
  "Birinci adım: demo nokta bpmn nokta io'yu aç, ya da {Camunda} {Modeler}'da {File}, {New File}, {BPMN diagram}. "
  "Tuvalde hazır bir başlangıç olayı gelir; adını araç seçildi, kredi talebi yap. "
  "İkinci adım havuz ve şeritler: paletteki {participant} aracıyla havuz oluştur, adı Firma Kredi. "
  "Havuza tıkla ve {Add lane below} ile toplam altı şerit yap: müşteri; bayi ya da Firma temsilcisi; sistem, yani kural motoru; "
  "tahsis; operasyon; ve harici sistemler.", bolum="BPMN · Laboratuvar")
m("Laboratuvar: adım 3–6", ["3. Bayi: \"Başvuruyu Portal'a gir\" (User Task)",
                            "4. Sistem: \"KPS & KKB sorgula\" (Service) + \"Kural & skor değerlendir\" (Business Rule)",
                            "5. Zaman aşımı: KPS & KKB kenarına Timer boundary PT5S → Tahsis \"Manuel değerlendirme\"",
                            "6. \"Otomatik karar?\" XOR: onay, ret, manuel · Ret → bitiş \"Ret bildirimi\""],
  "Üçüncü adım: bayi şeridine başvuruyu Portal'a gir görevini ekle; bu bir {User Task}. "
  "Dördüncü adım: sistem şeridine KPS ve KKB sorgula görevini ekle, anahtardan {Service Task} yap; "
  "ardından kural ve skor değerlendir görevini ekle, anahtardan {Business Rule Task} yap. "
  "Beşinci adım zaman aşımı: KPS ve KKB sorgula görevinin kenarına bir ara olay bırak, anahtar, {Timer boundary event}, {Duration} P T beş S. "
  "Arkasından tahsis şeridindeki manuel değerlendirme görevine bir ok çiz; bu, U04'teki beş saniye kuralı. "
  "Altıncı adım: otomatik karar mı diye soran bir {XOR} kapısı ekle; üç çıkışı etiketle: onay, ret, manuel. "
  "Ret çıkışını ret bildirimi adlı bir bitiş olayına bağla.")
m("Laboratuvar: adım 7–10", ["7. Tahsis: \"Manuel değerlendirme\" + \"Karar?\" · ek belge → Bayi \"Ek belge yükle\" → geri (döngü)",
                             "8. Yetki limiti: \"limit dışı → Kredi komitesi\" (U08 Komitede)",
                             "9. Bayi: \"ÖBF ver, sözleşme bas\" · Müşteri: \"Kredi & rehin sözleşmesini imzala\"",
                             "10. 30 gün: event-based → \"Sözleşme imzalandı\" mesajı | P30D → \"Başvuru iptal / süresi doldu\""],
  "Yedinci adım: tahsis şeridine manuel değerlendirme, yani bir {User Task}, ve karar mı diye soran bir kapı ekle. "
  "Ek belge çıkışını bayi şeridindeki ek belge yükle görevine, oradan da geri manuel değerlendirmeye bağla; bu bir döngü. "
  "Sekizinci adım yetki limiti: karar kapısına limit dışı, kredi komitesi çıkışı ekle; bu U08'deki komitede durumu. "
  "Dokuzuncu adım: bayi şeridine ÖBF ver, sözleşme bas; müşteri şeridine de kredi ve rehin sözleşmesini imzala görevini ekle. "
  "Onuncu adım otuz gün kuralı: ÖBF'den sonra bir {event-based gateway} koy. Bir kol sözleşme imzalandı mesaj olayı; "
  "diğer kol P otuz D zamanlayıcısı, ardından başvuru iptal ya da süresi doldu bitişi.")
m("Laboratuvar: adım 11–12", ["11. Bayi: \"Evrak yükle, kullandırım talep et\" → AND kapısı",
                              "Harici: \"Rehin tescili (e-Devlet / Noter)\" ∥ Operasyon: \"Kullandırım kontrolü (4 göz)\"",
                              "İkinci AND ile birleştir (P01'de eksik olan)",
                              "12. \"Uygun mu?\" hayır → bayiye iade · evet → \"Ödeme emri (checker)\" → \"Bayiye EFT\"",
                              "→ \"Kredi aktif, plan SMS/e-posta\" → bitiş \"Araç teslim alındı\""],
  "On birinci adım: bayi şeridine evrak yükle, kullandırım talep et görevini ekle. Arkasına bir {AND} kapısı koy. "
  "Bir kol harici sistemler şeridinde rehin tescili; e-Devlet ya da noter üzerinden. "
  "Diğer kol operasyon şeridinde kullandırım kontrolü; dört göz. "
  "İki kolu ikinci bir {AND} kapısıyla birleştir; P01'de eksik olan bu birleştirmeyi sen ekliyorsun. "
  "On ikinci adım: uygun mu kapısı. Hayır ise bayiye iade, yani geri ok. Evet ise ödeme emri, {checker} onayıyla; "
  "sonra harici sistemlerde bayiye EFT; sonra sistemde kredi aktif, ödeme planı SMS ya da e-posta; "
  "en sonda müşteri şeridinde araç teslim alındı bitişi.")
m("Laboratuvar: adım 13–15", ["13. Atama: \"Manuel değerlendirme\" → kredi-tahsis · \"Ödeme emri\" → operasyon-checker",
                              "14. Doğrulama: Problems paneli; çıkışlar etiketli mi, her yol bitişe ulaşıyor mu?",
                              "15. Ctrl+S → .bpmn · Export As Image → PNG",
                              "Çalışma setindeki P01 ile karşılaştır: zaman aşımı, komite, 30 gün, AND birleştirme"],
  "On üçüncü adım atama: manuel değerlendirme görevi, özellikler, {Assignment}, {Candidate groups}: kredi tahsis. "
  "Ödeme emri görevi için {Candidate groups}: operasyon {checker}. "
  "On dördüncü adım doğrulama: {Problems} panelini kontrol et. Her kapının çıkışları etiketli mi? Her yol bir bitişe ulaşıyor mu? "
  "On beşinci adım: kontrol S ile nokta bpmn olarak kaydet, {File}, {Export As Image} ile PNG al. "
  "Çalışma setindeki P01 ile yan yana koy ve farkları bir paragrafla açıkla: eklenen zaman aşımı, komite, otuz gün kuralı ve {AND} birleştirme.")
dikkat("Laboratuvar kontrol listesi", "Her yol bir bitişe ulaşıyor mu? · Çıkışlar etiketli mi? · Şerit adları rol mü, kişi değil? · Görevler fiil + nesne mi?",
       "Bitirmeden önce dört soruyu kontrol et. Her yol bir bitişe ulaşıyor mu? Her kapının çıkışları etiketli mi? "
       "Şerit adları kişi değil rol mü? Görev adları fiil artı nesne mi? Dördüne de evet diyorsan çizimin teslime hazır.", tip="bilgi")

# ───────────────────────────── Uygulama paketi
m("Çizmeden önce 6 soru", ["Cevabı bulamıyorsan önce Çalışma Seti'ne bak", "Orada da yoksa varsayım yaz",
                           "Diyagramın yanına \"açık soru\" notu", "Gerçek projede bu notları iş birimine sorarsın"],
  "BPMN uygulama paketine geçiyoruz. Bir süreci çizmeye başlamadan önce altı sorunun cevabını yaz. "
  "Bir cevabı bulamıyorsan önce Firma çalışma setine bak. Orada da yoksa bir varsayım yaz ve diyagramın yanına açık soru olarak not et. "
  "Gerçek projede bu notları iş birimine sorarsın. Şimdi soruları P01'in cevaplarıyla görelim.", bolum="BPMN · Uygulama paketi")
t("6 soru, P01 cevapları (1/2)", ["Soru", "Neden", "P01 cevabı"],
  [["1. Süreci ne başlatır?", "Başlangıç türü", "Bayi portala girer → mesaj başlangıcı"],
   ["2. Kimler katılır?", "Pool ve lane sayısı", "Bayi (pool), Firma (Operasyon, Tahsis), KKB (kapalı)"],
   ["3. Her şey yolundaysa?", "Mutlu yol, önce çizilir", "Al → KKB → Skorla → Onayla → Sözleşme → Rehin + kasko → Kullandır"]],
  "Birinci soru: süreci ne başlatır? Başlangıç olayının türünü belirler: düz, mesaj ya da zamanlayıcı. "
  "P01'de bayi başvuruyu portala girer; yani mesaj başlangıç olayı. "
  "İkinci soru: kimler katılır? Havuz ve şerit sayısını belirler. P01'de bayi ayrı havuz; Firma havuzunda kredi operasyon ve kredi tahsis şeritleri; "
  "KKB ise kapalı havuz. "
  "Üçüncü soru: her şey yolunda giderse adımlar ne? Mutlu yolu, yani {happy path}'i verir; önce bu çizilir. "
  "P01'de: başvuru al, KKB sorgula, skorla, onayla, sözleşme, rehin ve kasko, kullandır.")
t("6 soru, P01 cevapları (2/2)", ["Soru", "Neden", "P01 cevabı"],
  [["4. Nerede, neye göre karar?", "Kapı türü, dal koşulları", "Belgeler tam mı? Kredi/değer limit içinde mi? Skor bandı?"],
   ["5. İşler nerede ters gider?", "Sınır olayları, istisnalar", "KKB 5 sn → MANUEL_INCELEME · 30 gün → iptal (U08)"],
   ["6. Kaç farklı şekilde biter?", "Ayrı bitiş olayları", "Kullandırıldı · Reddedildi · İptal edildi"]],
  "Dördüncü soru: nerede karar verilir, neye göre? Kapı türünü ve dal koşullarını verir. "
  "P01'de: belgeler tam mı, kredi değer oranı limit içinde mi, skor hangi bantta? "
  "Beşinci soru: işler nerede ters gider? Sınır olaylarını ve istisna dallarını verir. "
  "P01'de: KKB beş saniye içinde dönmezse MANUEL_INCELEME; taslakta otuz gün işlem yoksa ya da onaydan otuz gün geçerse iptal, bu U08. "
  "Altıncı soru: süreç kaç farklı şekilde biter? Ayrı bitiş olaylarını verir. "
  "P01'de üç: kredi kullandırıldı, başvuru reddedildi, başvuru iptal edildi.")
dikkat("As-Is ve To-Be ayrı dosya", "Bugünkü ve hedef süreci AYNI diyagrama koyma. İki dosya: \"AS-IS\" ve \"TO-BE\".",
       "Bir uyarı: bugünkü durum, yani {As-Is}, ile hedef durum, yani {To-Be}, sürecini aynı diyagrama koyma. "
       "İki ayrı dosya aç ve adlarına AS-IS ve TO-BE yaz. Aynı diyagramda karışınca hangi adımın bugün olduğu, hangisinin hedef olduğu kaybolur.")
t("Adlandırma kuralları", ["Öğe", "Kural", "Yanlış", "Doğru"],
  [["Görev", "Fiil + nesne, emir kipi", "\"Kontrol\"", "\"Belgeleri kontrol et\""],
   ["Kapı (XOR)", "Bir soru; her çıkış bir cevap", "\"Onay?\"", "\"Kredi/değer oranı limit içinde mi?\""],
   ["Kapıdan çıkan ok", "Sorunun cevabı", "(etiketsiz)", "\"Evet\" / \"Hayır\""],
   ["Bitiş olayı", "Sonuç durumu, geçmiş zaman", "\"Son\"", "\"Kredi kullandırıldı\""], ["Ara olay", "Olan şey", "\"Bekle\"", "\"KKB yanıtı alındı\""]],
  "Adlandırma kuralları. Görev: fiil artı nesne, emir kipinde. Yanlış: kontrol. Doğru: belgeleri kontrol et. "
  "{XOR} kapısı: bir soru; her çıkış oku bir cevap, yani evet ya da hayır, ya da bant adı. Yanlış: onay soru işareti. Doğru: kredi değer oranı limit içinde mi? "
  "Kapıdan çıkan ok: sorunun cevabı. Yanlış: etiketsiz ok. Doğru: evet ya da hayır. "
  "Bitiş olayı: sonuç durumu, geçmiş zamanla. Yanlış: son. Doğru: kredi kullandırıldı. "
  "Ara olay: olan şey. Yanlış: bekle. Doğru: KKB yanıtı alındı. "
  "Tek bir son bitiş olayı yerine her sonuç için ayrı bitiş çiz; diyagramı okuyan kişi sürecin kaç şekilde bittiğini ilk bakışta görür.")

# ───────────────────────────── Hata kataloğu
m("Kontrol akışı hata kataloğu", ["Araç bazılarını engeller: #8, #9, #11 çizilemez; #4–#6 uyarı",
                                  "#1, #2, #3, #7 GEÇERLİ dosya üretir: düzgün görünür, motorda takılır",
                                  "Kural: ayrım kapısı = birleşim kapısı (aynı tür)"],
  "Şimdi ileri seviye bir konu: kontrol akışı hata kataloğu; on bir hata var. Bazılarını araç zaten engeller: "
  "{Camunda} {Modeler} başlangıç olayına giren oku, yani sekiz numarayı; kapıya iliştirilen sınır olayını, yani dokuzu; "
  "ve aynı havuz içindeki mesaj akışını, yani on biri çizdirmez. Dört, beş ve altı için de yerleşik denetim uyarı verir. "
  "Ama bir, iki, üç ve yedi geçerli bir BPMN dosyası üretir: diyagram düzgün görünür, süreç motorunda çalıştırıldığında ise süreç takılır "
  "ya da bir adım iki kez çalışır. Kural: bir ayrım kapısı ile o dalları birleştiren kapı aynı türde olmalı.", bolum="BPMN · Hata kataloğu")
t("Hata kataloğu (1/4)", ["#", "Hata", "Yanlış çizim", "Ne olur → Düzeltme"],
  [["1", "XOR ayır, AND birleştir", "Müşteri tipi? → bireysel / kurumsal belge → AND → Skorla", "Kilitlenir → birleşimi XOR yap"],
   ["2", "AND ayır, XOR birleştir", "KKB sorgula ∥ kasko teklifi → XOR → Kredi kararı", "Karar 2 kez verilir → birleşimi AND yap"]],
  "Birinci hata: {XOR} ile ayır, {AND} ile birleştir. Firma'daki yanlış çizim: müşteri tipi mi diye soran bir {XOR}, "
  "bireysel belge kontrolü ya da kurumsal belge kontrolü, sonra {AND} birleşim, sonra skorla. "
  "{Token} yalnız bir daldan gelir ama {AND} iki dalı bekler: süreç kilitlenir. Düzeltme: birleşimi de {XOR} yap. "
  "İkinci hata: {AND} ile ayır, {XOR} ile birleştir. Yanlış çizim: {AND} ile KKB sorgula ve kasko teklifi al, sonra {XOR} birleşim, sonra kredi kararı ver. "
  "{XOR} gelen her {token}'ı geçirir: kredi kararı iki kez verilir. Düzeltme: birleşimi {AND} yap.")
t("Hata kataloğu (2/4)", ["#", "Hata", "Yanlış çizim", "Ne olur → Düzeltme"],
  [["3", "Koşullu XOR'da varsayılan yok", "Skor bandı? → [≥ 1500] Onay, [< 900] Red", "900–1499 takılır → varsayılan: Manuel inceleme"],
   ["4", "Ulaşılamayan adım", "\"Ekspertiz raporu iste\"ye ok gelmiyor", "Hiç çalışmaz → bağla ya da sil"],
   ["5", "Çıkmaz", "\"Red bildirimi gönder\"den ok çıkmıyor", "Süreç açık kalır → \"Başvuru reddedildi\" bitişi"]],
  "Üçüncü hata: koşullu {XOR}'da varsayılan dal yok. Yanlış çizim: skor bandı mı diye soran kapı; bin beş yüz ve üstü onay, dokuz yüzün altı red. "
  "Dokuz yüz ile bin dört yüz doksan dokuz arasındaki skorda hiçbir koşul doğru değil: {token} takılır. "
  "Düzeltme: bir dalı varsayılan yap, manuel inceleme. Varsayılan dal yoksa süreç motoru hata, yani {incident} üretir. "
  "Dördüncü hata: ulaşılamayan adım. Ekspertiz raporu iste görevine hiçbir ok gelmiyor; adım hiç çalışmaz. Düzeltme: bir akışa bağla ya da sil. "
  "Beşinci hata: çıkmaz. Red bildirimi gönder görevinden çıkan ok yok; {token} orada kaybolur, süreç açık kalır. "
  "Düzeltme: arkasına başvuru reddedildi bitiş olayı koy.")
t("Hata kataloğu (3/4)", ["#", "Hata", "Yanlış çizim", "Ne olur → Düzeltme"],
  [["6", "Başlangıç / bitiş eksik", "\"Başvuruyu al\" ile başlıyor", "Mesaj başlangıcı ekle"],
   ["7", "Örtük ayrım", "İmzalattan iki ok çıkıyor", "AND ile ayır, AND ile birleştir"],
   ["8", "Ters yönlü olay", "Ok başlangıç olayına dönüyor", "\"Belgeleri kontrol et\"e bağla"]],
  "Altıncı hata: başlangıç ya da bitiş eksik. Diyagram doğrudan başvuruyu al göreviyle başlıyor; süreci neyin tetiklediği belirsiz. "
  "Düzeltme: mesaj başlangıç olayı ekle. "
  "Yedinci hata: örtük ayrım. Sözleşmeyi imzalat görevinden iki ok çıkıyor: rehin tesis et ve kasko poliçesini doğrula. "
  "İki dal paralel çalışır ama bu diyagramda görünmez. Düzeltme: araya {AND} kapısı koy, sonra {AND} ile birleştir. "
  "Sekizinci hata: ters yönlü olay. Eksik belge tamamlandı sonrasındaki ok başlangıç olayına geri dönüyor. "
  "BPMN kuralına göre başlangıç olayına {sequence flow} bağlanamaz; döngü bir göreve dönmelidir. Düzeltme: oku belgeleri kontrol et görevine bağla.")
t("Hata kataloğu (4/4)", ["#", "Hata", "Yanlış çizim", "Ne olur → Düzeltme"],
  [["9", "Sınır olayı yanlış yerde", "5 sn zamanlayıcı \"Skor bandı?\" kapısında", "Yalnız aktiviteye → \"KKB sorgula\"ya iliştir"],
   ["10", "Lane dışında adım", "\"Rehin tesis et\" şeritlerin dışında", "Sahip belirsiz → Kredi Operasyon şeridine taşı"],
   ["11", "Aynı pool'da mesaj akışı", "Operasyon → Tahsis kesikli ok", "Yalnız pool'lar arası → sequence flow yap"]],
  "Dokuzuncu hata: sınır olayı yanlış yere iliştirilmiş. Beş saniyelik zamanlayıcı skor bandı kapısının kenarında. "
  "Sınır olayı yalnızca bir aktiviteye iliştirilebilir. Düzeltme: zamanlayıcıyı KKB sorgula servis görevine iliştir. "
  "Onuncu hata: şerit dışında kalan adım. Rehin tesis et görevi şeritlerin dışında; işin sahibi belirsiz. "
  "Düzeltme: görevi kredi operasyon şeridine taşı. "
  "On birinci hata: aynı havuz içinde mesaj akışı. Kredi operasyon şeridinden kredi tahsis şeridine kesikli ok. "
  "Mesaj akışı yalnızca havuzlar arasında kullanılır. Düzeltme: düz çizgili {sequence flow} yap.")
g("Kapı eşleştirme hataları: #1, #2, #3", "g13.png",
  [([0.0, 0.08, 1.0, 0.38], "1 · XOR → AND: kilitlenir"), ([0.0, 0.39, 1.0, 0.64], "2 · AND → XOR: iki kez çalışır"),
   ([0.0, 0.65, 1.0, 0.96], "3 · Varsayılan dal yok: takılır")],
  "Resmi soldan sağa oku: solda hatalı çizim ve sonucu kırmızıyla, sağda düzeltilmiş hali yeşille. "
  "İçinde çarpı olan elmas {XOR}, artı olan elmas {AND} kapısıdır. "
  "Birinci satır: {XOR} ile ayrılan bireysel ve kurumsal belge dalları {AND} ile birleşirse, {AND} hiç gelmeyecek dalı bekler; süreç kilitlenir. "
  "Sağda birleşim de {XOR}: devam eder. "
  "İkinci satır: {AND} ile ayrılan KKB sorgula ve kasko teklifi al dalları {XOR} ile birleşirse her {token} ayrı geçer; karar ver iki kez çalışır. "
  "Sağda birleşim {AND}: bir kez çalışır. "
  "Üçüncü satır: onay, skor bin beş yüz ve üstü; red, skor dokuz yüzün altı. Dokuz yüz ile bin dört yüz doksan dokuz arasında yol yok. "
  "Sağda manuel inceleme okunun başındaki kısa eğik çizgi, BPMN'de varsayılan dalın işaretidir.")
dikkat("Nasıl kontrol edilir?", "Her başlangıçtan token'ı parmağınla yürüt: \"Buradan kaç dal çıkar, ileride kaç dal beklenir?\" · Token Simulation anahtarı",
       "Bunu nasıl kontrol edersin? {Camunda} {Modeler}'da diyagramı aç ve her başlangıç olayından parmağınla {token}'ı yürüt. "
       "Her kapıda şunu sor: {token} buradan kaç daldan çıkar, ileride kaç dal bekleniyor? "
       "{Camunda} {Modeler}'ın yeni sürümlerinde sol üstteki {Token Simulation} anahtarı bu yürüyüşü ekranda canlandırır.", tip="bilgi")

# ───────────────────────────── İki katman
t("Bir .bpmn dosyasının iki katmanı", ["Katman", "Öğeler (XML)", "Ne işe yarar"],
  [["1. Anlam", "process · startEvent · serviceTask · sequenceFlow", "Motor bunu okur"],
   ["2. Çizim (BPMNDI)", "BPMNDiagram · BPMNPlane · BPMNShape · Bounds", "Yalnız resim"]],
  "{Camunda} {Modeler}'da kaydettiğin nokta bpmn dosyasını VS Code ya da Notepad artı artı ile açarsan iki bölüm görürsün. "
  "Birincisi anlam katmanı: süreç ne yapar. Örnekte {process} P01 kredi; içinde başvuru alındı adlı {startEvent}, KKB sorgula adlı {serviceTask} "
  "ve ikisini bağlayan bir {sequenceFlow}: {id} f1, {sourceRef} Basvuru_Alindi, {targetRef} KKB_Sorgula. "
  "İkincisi çizim katmanı, yani BPMNDI: şekiller ekranda nerede. {BPMNDiagram}, onun içinde {bpmnElement} P01_Kredi olan bir {BPMNPlane}, "
  "onun içinde {bpmnElement} KKB_Sorgula olan bir {BPMNShape}, "
  "ve {Bounds}: x iki yüz yetmiş, y seksen, {width} yüz, {height} seksen. "
  "Süreç motoru süreci ilk bölümden okur; ikinci bölüm yalnızca resimdir.", bolum="BPMN · Dosya katmanları")
dikkat("\"Şekil var ama süreçte yok\"", "İki katmandan birinde öğe eksik. Çizim katmanında karşılığı olmayan öğe ekranda görünmez; modelde yeniden çiz ya da bpmn-auto-layout.",
       "Bir araçta şekil var ama süreçte yok, ya da süreçte var ama ekranda görünmüyor sorunu yaşarsan, iki katman arasında bir öğe eksiktir. "
       "Çizim katmanında karşılığı olmayan bir öğe ekranda görünmez ve {Camunda} {Modeler} bu katmanı kendiliğinden üretmez. "
       "Öğeyi modelde yeniden çizmek ya da otomatik yerleşim aracı, örneğin {bpmn-auto-layout} kullanmak gerekir.")

# ───────────────────────────── Bağımsız görev
m("Bağımsız görev: hasar muvafakati", ["Kural: muvafakat için taksitler güncel olmalı",
                                       "Sigorta, servise ödemeden önce rehin alacaklısı Firma'dan muvafakat ister",
                                       "Güncel → yazı hazırlanır, sigortaya gönderilir",
                                       "Değil → müşteriye bildirim; ödeme gelirse yeniden kontrol, süre dolarsa kapat"],
  "Şimdi laboratuvardan farklı bir süreci kendi başına çizeceksin; çözümü bu videonun sonunda. "
  "Senaryo, Firma kuralına dayanıyor: hasar muvafakati için taksitler güncel olmalı. "
  "Kasko kapsamında hasar gören bir araç için sigorta şirketi, onarım ödemesini servise yapmadan önce rehin alacaklısı Firma'dan muvafakat yazısı ister. "
  "Firma, müşterinin taksitlerinin güncel olup olmadığını kontrol eder. Taksitler güncelse muvafakat yazısı hazırlanır ve sigorta şirketine gönderilir. "
  "Güncel değilse müşteriye ödeme yapması gerektiği bildirilir. Müşteri ödemeyi yaparsa kontrol yeniden yapılır; "
  "ödeme kurumun belirleyeceği süre içinde gelmezse talep kapatılır.", bolum="BPMN · Bağımsız görev")
m("Diyagramda olması gerekenler", ["1. İki pool: Sigorta (kapalı), Firma (açık, ≥ 2 lane)", "2. Mesaj başlangıcı + en az bir giden mesaj akışı",
                                   "3. Varsayılan dalı olan XOR", "4. Event-based: \"Ödeme alındı\" ↔ \"Bekleme süresi doldu\"",
                                   "5. En az iki bitiş · 6. 11 kontrolün hepsi"],
  "Diyagramda olması gerekenler altı madde. Bir: iki havuz; sigorta şirketi kapalı havuz, Firma açık havuz ve en az iki şerit. "
  "İki: bir mesaj başlangıç olayı ve en az bir giden mesaj akışı. Üç: varsayılan dalı olan bir {XOR} kapısı. "
  "Dört: ödemeyi beklemek için bir {event-based} kapı; ödeme alındı mesaj olayı ile bekleme süresi doldu zamanlayıcı olayı yarışır. "
  "Beş: en az iki ayrı bitiş olayı. Altı: hata kataloğundaki on bir kontrolün hepsinden geçmiş olmalı. "
  "Doğru yaptığını nasıl anlarsın? {Token}'ı üç yoldan yürüt: taksitler güncel, ödeme geldi, süre doldu. "
  "Her seferinde bir bitiş olayına ulaşıyor ve hiçbir kapıda takılmıyorsan doğru.")

# ───────────────────────────── Sorun giderme
t("Sorun giderme (1/2)", ["Belirti", "Olası neden", "Çözüm"],
  [["Ok şekle bağlanmıyor", "Hedef vurgulanmadan bırakıldı", "Kaynağa tıkla → ok simgesi → kenar mavi olunca bırak"],
   ["Lane eklenemiyor", "Henüz pool yok", "Create Pool/Participant → pool'a tıkla → Add Lane"],
   ["Sınır olayı yapışmıyor", "İçine ya da uzağa bırakıldı", "Kenar çizgisine sürükle, vurgulanınca bırak"],
   ["Kesikli ok çizilemiyor", "İki uç aynı pool'da", "Düz ok kullan; mesaj yalnız pool'lar arası"]],
  "Sorun giderme. Ok şekle bağlanmıyor, boşlukta kalıyorsa: ok sürüklenirken hedef şekil vurgulanmadan bırakılmıştır. "
  "Çözüm: kaynak şekle tıkla, bağlam menüsünde ok simgesini seç, hedef şeklin kenarı mavi olunca bırak. "
  "Şerit, yani {lane}, eklenemiyorsa: henüz havuz, yani {pool} ya da {participant}, yoktur. Önce paletten {Create Pool} ya da {Participant} ile havuz çiz, "
  "sonra havuza tıklayıp {Add Lane} seç. "
  "Sınır olayı göreve yapışmıyorsa: olay görevin içine ya da uzağına bırakılmıştır. Görevin kenar çizgisine sürükle, kenar vurgulanınca bırak. "
  "Kesikli ok, yani mesaj akışı, çizilemiyorsa: iki uç aynı havuzdadır. Aynı havuzda düz ok kullan; mesaj akışı yalnızca havuzlar arasıdır.",
  bolum="BPMN · Sorun giderme ve bilgi kontrolü")
t("Sorun giderme (2/2)", ["Belirti", "Olası neden", "Çözüm"],
  [["Token bir kapıda bekliyor", "Hata #1 (XOR → AND) ya da #3 (varsayılan yok)", "Kapıları eşleştir; varsayılan dal ekle"],
   ["Bir adım iki kez çalışıyor", "Hata #2 (AND → XOR) ya da #7 (örtük ayrım)", "Paralel dalları AND ile birleştir"],
   ["Dosya başka araçta boş", "Çizim katmanı (BPMNDI) eksik", "Yeniden çiz ya da otomatik yerleşim; \"no diagram to display\""]],
  "{Token} simülasyonunda {token} bir kapıda bekliyorsa: hata bir, yani {XOR}'dan {AND}'e, ya da hata üç, yani varsayılan dal yok. "
  "Çözüm: kapı türlerini eşleştir ve koşullu {XOR}'a varsayılan dal ekle. "
  "Bir adım simülasyonda iki kez çalışıyorsa: hata iki, yani {AND}'den {XOR}'a, ya da hata yedi, örtük ayrım. Çözüm: paralel dalları {AND} ile birleştir. "
  "Dosya başka bir araçta boş görünüyorsa: çizim katmanı, yani BPMNDI, eksiktir. Öğeyi modelde yeniden çiz ya da otomatik yerleşim aracı kullan. "
  "Hiç çizim katmanı yoksa modelleme aracı {no diagram to display} der.")

soru("Bilgi kontrolü 1/5", "XOR'un üç dalının da koşulu var, hiçbiri varsayılan değil. Başvuru hiçbir koşulu sağlamıyor. Ne olur?",
     ["Token ilk dala gider", "Token kapıda takılır", "Süreç hata verip baştan başlar", "Token üç dala da gider"], 1,
     "Beş soruluk bilgi kontrolü. Birinci soru: bir {XOR} kapısının üç çıkış dalının da koşulu var ve hiçbiri varsayılan değil. "
     "Gelen başvuru hiçbir koşulu sağlamıyor. Ne olur? A, {token} ilk dala gider. B, {token} kapıda takılır. "
     "C, süreç hata verip baştan başlar. D, {token} üç dala da gider.",
     "Doğru cevap B. Koşulu sağlanan dal yoksa {token} takılır; bu yüzden varsayılan dal gerekir.")
soru("Bilgi kontrolü 2/5", "KKB sorgusu ile kasko teklifi aynı anda başlıyor, ikisi bitince karar veriliyor. Birleşim kapısı?",
     ["XOR", "OR", "AND", "Event-based"], 2,
     "İkinci soru: KKB sorgusu ile kasko teklifi aynı anda başlatılıyor ve ikisi bitince kredi kararı veriliyor. Birleşim kapısı ne olmalı? "
     "A, {XOR}. B, {OR}. C, {AND}. D, {Event-based}.",
     "Doğru cevap C: {AND}. Paralel başlayan iki işi beklemek için {AND} kullanılır.")
soru("Bilgi kontrolü 3/5", "\"Bayi\" pool'u ile \"Firma\" pool'u arasındaki ok hangi türdür?",
     ["Sequence flow", "Message flow", "Association", "Data flow"], 1,
     "Üçüncü soru: bayi havuzu ile Firma havuzu arasındaki ok hangi türdür? "
     "A, {sequence flow}. B, {message flow}. C, {association}. D, {data flow}.",
     "Doğru cevap B: {message flow}. İki ayrı havuz arasındaki iletişim mesaj akışıdır.")
soru("Bilgi kontrolü 4/5", "5 saniyelik zamanlayıcı nereye iliştirilmeli?",
     ["Skor kapısına", "Başlangıç olayına", "KKB sorgula görevine", "Bitiş olayına"], 2,
     "Dördüncü soru: beş saniyelik zamanlayıcı nereye iliştirilmeli? "
     "A, skor kapısına. B, başlangıç olayına. C, KKB sorgula görevine. D, bitiş olayına.",
     "Doğru cevap C. Sınır olayı yalnızca bir aktiviteye iliştirilir; bekleme de KKB çağrısında olur.")
soru("Bilgi kontrolü 5/5", "Aynı kasko kontrol süreci hem P01'de hem P03'te kullanılıyor. Doğru gösterim?",
     ["İki yerde de gömülü alt süreç", "İki süreçte de call activity", "Mesaj akışıyla bağlamak", "Tek büyük diyagram"], 1,
     "Beşinci soru: aynı kasko kontrol süreci hem P01'de hem P03'te kullanılıyor. Doğru gösterim hangisi? "
     "A, iki yerde de gömülü alt süreç. B, iki süreçte de {call activity}. C, mesaj akışıyla bağlamak. D, tek büyük diyagram.",
     "Doğru cevap B: {call activity}. Yeniden kullanılan, ayrı tanımlı süreç {call activity} ile çağrılır.")

# ───────────────────────────── Kontrol listesi, çözüm
m("Teslim öncesi kontrol listesi (1/2)", ["6 sorunun cevabı diyagramda görünüyor", "Görev fiil + nesne · XOR bir soru · çıkış bir cevap",
                                         "Her ayrımın aynı türde birleşimi var", "Her koşullu XOR'da varsayılan dal",
                                         "Görev ve ara olaya tek ok girer, tek ok çıkar"],
  "Hızlı başvuru: teslim öncesi kontrol listesi; on madde. Bir: altı sorunun cevabı diyagramda görünüyor; "
  "tetikleyici, katılımcılar, mutlu yol, kararlar, istisnalar ve bitişler. "
  "İki: her görev fiil artı nesne, her {XOR} bir soru, her çıkış oku bir cevap. "
  "Üç: her ayrım kapısının aynı türde bir birleşim kapısı var. Dört: her koşullu {XOR}'da bir varsayılan dal var. "
  "Beş: her görev ve ara olaya tek ok giriyor ve tek ok çıkıyor; birleşme ve ayrılma yalnızca kapılarda yapılıyor, başlangıç ve bitiş hariç.",
  bolum="BPMN · Kontrol listesi ve çözümler")
m("Teslim öncesi kontrol listesi (2/2)", ["Görevlerden birden fazla ok çıkmıyor", "Sınır olayı yalnız görev, alt süreç, call activity üzerinde",
                                         "Her düğüm bir lane içinde", "Kesikli oklar yalnız pool'lar arası",
                                         "Token 3 senaryoyla yürütüldü, hep bitişe ulaştı"],
  "Altı: görevlerden birden fazla ok çıkmıyor; ayrımlar kapıyla yapılıyor. "
  "Yedi: sınır olayları yalnızca görev, alt süreç ya da {call activity} üzerinde. Sekiz: her düğüm bir şerit içinde. "
  "Dokuz: kesikli oklar yalnızca havuzlar arasında. "
  "On: {token} üç farklı senaryoyla yürütüldü ve her seferinde bir bitiş olayına ulaştı.")
m("Bağımsız görev: örnek çözüm (1/2)", ["Sigorta (kapalı) → \"Muvafakat talebi\" → mesaj başlangıcı \"Muvafakat talebi alındı\"",
                                        "Kredi Operasyon: \"Taksit durumunu kontrol et\" → XOR \"Taksitler güncel mi?\"",
                                        "Evet → \"Muvafakat yazısını hazırla\" → \"Yazıyı sigortaya gönder\" → \"Muvafakat verildi\"",
                                        "Hayır (varsayılan) → Tahsilat: \"Müşteriye ödeme bildirimi gönder\" → event-based"],
  "Ve bağımsız görevin örnek çözümü. Sigorta şirketi kapalı havuzdan muvafakat talebi adlı bir mesaj akışı gelir; "
  "Firma havuzunda muvafakat talebi alındı adlı mesaj başlangıç olayına düşer. "
  "Kredi operasyon şeridinde taksit durumunu kontrol et görevi, ardından taksitler güncel mi diye soran {XOR}. "
  "Evet ise muvafakat yazısını hazırla, sonra yazıyı sigorta şirketine gönder; bu sigorta havuzuna bir mesaj akışı. Ardından muvafakat verildi bitişi. "
  "Hayır, ki varsayılan dal budur, ise tahsilat şeridinde müşteriye ödeme bildirimi gönder görevi ve ardından bir {event-based} kapı.")
m("Bağımsız görev: örnek çözüm (2/2)", ["\"Ödeme alındı\" → görevin önündeki XOR birleşimi", "Başlangıç oku da bu kapıya",
                                        "\"Bekleme süresi doldu\" (P10D) → \"Talep kapatıldı\"",
                                        "Kontrol: #8 yok · #3 yok · iki bitiş"],
  "{Event-based} kapının bir kolunda ödeme alındı mesaj ara olayı var. Bu ok, taksit durumunu kontrol et görevinin önüne konan bir {XOR} birleşim kapısına döner. "
  "Başlangıç olayından gelen ok da bu kapıya bağlanır; böylece görevin tek giren oku olur. "
  "Diğer kolda bekleme süresi doldu zamanlayıcı ara olayı var. Süre çalışma setinde tanımlı değil; zamanlayıcıya örnek bir değer yaz, "
  "örneğin P on D, ve açık soru olarak işaretle. Ardından talebi kapat ve sigortaya bildir görevi, sigorta havuzuna mesaj akışıyla; "
  "sonra talep kapatıldı bitişi. "
  "Kontrol edelim: geri dönüş oku başlangıç olayına değil göreve gidiyor, yani hata sekiz yok. {XOR}'da varsayılan dal var, yani hata üç yok. "
  "{Event-based} kapının arkasında iki yakalayan olay var ve iki ayrı bitiş olayı var.")
m("Bu videoda neler gördük?", ["8 ileri desen: telafi, eskalasyon, korelasyon, ISO zaman, DMN, seviyeler, denetim, anti-desen",
                               "Araçlar, ekran ve menü rehberi", "P01 laboratuvarı (15 adım)", "6 soru, adlandırma, 11 hatalık katalog",
                               "İki katman, bağımsız görev, sorun giderme, kontrol listesi"],
  "Toparlayalım. Sekiz ileri deseni gördük: telafi, hata ile eskalasyon ayrımı, mesaj korelasyonu, {ISO} zaman ifadeleri, DMN ayrımı, "
  "seviyelendirme, denetim izi ve anti-desenler. Araçları, ekranı ve menü rehberini çalıştık. On beş adımda P01'i çizdik. "
  "Çizmeden önceki altı soruyu, adlandırma kurallarını ve on bir hatalık kataloğu öğrendik. "
  "Dosyanın iki katmanını, bağımsız görevi, sorun gidermeyi ve kontrol listesini tamamladık. "
  "Bir sonraki videoda süreç diyagramlama ile devam ediyoruz: {swimlane}, değer akışı ve israf.", ton="sakin")

kaydet(__file__, {
    "baslik": "Business Analyst Teknik Rehberi · 3: BPMN (2/2)",
    "alt_baslik": "İleri desenler · araçlar · P01 laboratuvarı · hata kataloğu · uygulama paketi",
    "kapanis": "Sıradaki video: Süreç diyagramlama",
    "tema": 3,
    "youtube_baslik": "Business Analyst Teknik Rehberi 3/14: BPMN 2 (ileri desenler, laboratuvar, 11 hata)",
    "etiketler": ["business analyst", "BPMN", "Camunda Modeler", "BPMN hataları", "compensation", "iş analisti"],
}, {"Saga": "saga", "P30D": "pe otuz de", "P10D": "pe on de", "PT5S": "pe te beş es", "PT48H": "pe te kırk sekiz eyç",
    "C7": "si yedi", "C8": "si sekiz", "f1": "ef bir", "Basvuru_Alindi": "başvuru alındı", "KKB_Sorgula": "ka ka be sorgula",
    "P01_Kredi": "pe sıfır bir kredi", "kredi-tahsis": "kredi tahsis", "operasyon-checker": "operasyon çekır", "e-Devlet": "e devlet"})
