#!/usr/bin/env python3
"""BA Teknik Rehberi · Video 5: Diyagram okuma atölyesi (P01, U04, U07, U08, D05, envanter, kendini sına).
Belge satır 1175–1386. Firma adları genelleştirildi (vdf → Firma, Zebra → Portal)."""
from ortak import m, t, dikkat, g, soru, kaydet

# ───────────────────────────── Giriş ve 7 adım
m("Diyagram okuma atölyesi", ["Çalışma Seti'ndeki gerçek akışlar", "P01 kredi süreci (BPMN) · U04 bayi başvurusu (sequence)",
                              "U07 alan modeli (class) · U08 yaşam döngüsü (state)", "D05 Portal kredi ve kampanya ekranı (wireframe)",
                              "Her görselde kırmızı numaralar → tablo → okunuş → sorular"],
  "Bu videoda okuma pratiği yapıyoruz. Firma çalışma setindeki gerçek akışları kullanacağız: P01 kredi süreci, bir BPMN; "
  "U04 bayi başvurusu, bir {sequence}; U07 alan modeli, bir {class}; U08 başvuru yaşam döngüsü, bir {state} diyagramı; "
  "ve D05 Portal kredi ve kampanya ekranı, bir {wireframe}. "
  "Her görselin üzerinde kırmızı numaralar var. Her numaranın ne olduğunu ve ne anlama geldiğini göreceğiz; "
  "ardından diyagramın cümle cümle okunuşu, Firma iş kurallarıyla bağlantısı ve bir iş analistinin soracağı sorular gelecek.",
  bolum="Atölye: okuma yöntemi", kanca="Bir diyagramı okumak, onu çizmek kadar önemli bir beceri.", ton="merakli")
m("7 adımlı okuma yöntemi (1/2)", ["1. Türü tanı", "Kulvar + eşkenar dörtgen = BPMN · kutular + inen kesikli çizgi = sequence",
                                   "Üç bölmeli kutu + uçta sayılar = class · yuvarlak durum + etiketli ok = state",
                                   "Tarayıcı çerçevesi + form = wireframe", "2. Çerçeveyi oku: kimler var, hangi kanal?"],
  "Her diyagram için yedi adımlı bir okuma yöntemi var. Birinci adım: türü tanı. Kulvarlı akış ve eşkenar dörtgen kapılar görüyorsan BPMN. "
  "Üstte kutular ve aşağı inen kesikli çizgiler görüyorsan {sequence}. Üç bölmeli kutular ve çizgi uçlarında sayılar görüyorsan {class}. "
  "Yuvarlak köşeli durum kutuları ve etiketli oklar görüyorsan {state machine}. Tarayıcı çerçevesi ve form alanları görüyorsan {wireframe}. "
  "İkinci adım: çerçeveyi oku. Başlık, alt başlık, kulvar ya da katılımcı adları; kimler var, hangi kanal?")
m("7 adımlı okuma yöntemi (2/2)", ["3. Başlangıcı bul", "4. Mutlu yolu sonuna kadar izle",
                                   "5. Alternatifler: ret, manuel, ek belge, zaman aşımı, bayiye iade",
                                   "6. Simgeleri oku: ikonlar, alt/opt, elmas, üçgen, renkler, pasif alanlar",
                                   "7. Firma kuralıyla karşılaştır"],
  "Üçüncü adım: başlangıcı bul; başlangıç olayı, ilk mesaj, ilk durum noktası ya da ekrandaki adım göstergesi. "
  "Dördüncü adım: mutlu yolu izle; onay yolunu sonuna kadar takip et. "
  "Beşinci adım: alternatif yolları izle; ret, manuel inceleme, ek belge, zaman aşımı, bayiye iade. "
  "Altıncı adım: simgeleri oku; görev ikonları, {alt} ve {opt} kutuları, elmas ve üçgen uçlar, kırmızı ve yeşil durumlar, pasif alanlar. "
  "Yedinci adım: Firma kuralıyla karşılaştır.")
t("Adım 7: Firma kuralları", ["Kural", "Değer"],
  [["Vade", "6–60 ay"], ["Bireysel kredi/değer", "400.000 ₺'ye kadar %70 … 2.000.000 ₺'ye kadar %20; üstü finanse edilmez"],
   ["Kurumsal", "Fatura bedelinin %90'ı"], ["Belgeler tamsa", "Aynı gün onay"],
   ["Teminat · erken kapama", "Rehin + kasko · rehin yaklaşık 1 saatte kalkar"]],
  "Karşılaştıracağın Firma kuralları şunlar. Vade altı ile altmış ay. Bireyselde kademeli kredi değer oranı: dört yüz bin liraya kadar yüzde yetmiş, "
  "kademeler düşerek iki milyon liraya kadar yüzde yirmi; iki milyonun üstü finanse edilmez. "
  "Kurumsalda fatura bedelinin yüzde doksanı. Belgeler tamsa aynı gün onay. Teminat rehin ve kasko. "
  "Erken kapamada da rehin yaklaşık bir saatte kalkar. Her diyagramda şunu sor: bu kuralları nerede uyguluyor?")

# ───────────────────────────── Görsel 1: P01
g("Görsel 1 · P01: kulvarlar ve başlangıç", "g16.png",
  [([0.0, 0.0, 1.0, 1.0], "P01: bayide başvurudan kullandırıma"),
   ([0.0, 0.08, 0.06, 0.95], "1 · Kulvarlar"), ([0.02, 0.08, 0.2, 0.36], "2 · Başlangıç: araç seçildi"),
   ([0.06, 0.22, 0.22, 0.4], "3 · Başvuruyu Portal'a gir")],
  "Birinci görsel: P01 kredi başvurusundan kullandırıma, numaralı. Bayide başlayan başvurunun otomatik ya da manuel kararla sözleşmeye, rehne ve bayiye ödemeye kadar uçtan uca akışı. "
  "Bir numara kulvarlar: müşteri, bayi ya da Firma temsilcisi, sistem yani kural motoru, tahsis, operasyon ve harici sistemler. "
  "Her bant bir rol ya da sistem; adımı kimin yaptığını bulunduğu bant söyler. "
  "İki numara başlangıç olayı: araç seçildi, kredi talebi. İnce kenarlı yeşil daire; süreci müşterinin araç seçmesi tetikler. "
  "Üç numara: başvuruyu Portal'a gir; müşteri, araç ve kampanya. Bayi temsilcisinin Portal'da yaptığı iş; D03'ten D07'ye ekranlar.",
  bolum="Görsel 1 · P01 (BPMN)")
g("P01: sistem ve otomatik karar", "g16.png",
  [([0.12, 0.38, 0.28, 0.95], "4–5 · KPS & KKB sorgula, SOAP"), ([0.2, 0.36, 0.33, 0.52], "6 · Kural & skor değerlendir"),
   ([0.26, 0.25, 0.36, 0.52], "7 · XOR: otomatik karar"), ([0.26, 0.25, 0.36, 0.45], "8 · Ret bildirimi")],
  "Dört numara bir {service task}: KPS ve KKB sorgula. Sol üstteki dişli, işi sistemin otomatik yaptığını söyler. "
  "KPS kimlik ve adres, KKB kredi raporu verir. "
  "Beş numara kesikli ok, üstünde SOAP yazıyor: harici sistemlere giden mesaj. KPS ve KKB entegrasyonu SOAP ile; U04'teki {sequence} bu oku ayrıntılandırır. "
  "Altı numara kural ve skor değerlendir: kural motoru kredi değer oranını, vadeyi, kampanya uygunluğunu ve skoru değerlendirir. "
  "Yedi numara otomatik karar mı diye soran {XOR} kapısı. Üç çıkışı var: onay, doğrudan ÖBF'ye; ret; ve manuel. Yalnız biri seçilir. "
  "Sekiz numara ret bildirimi adlı bitiş olayı: kalın kırmızı daire, bu yol burada biter.")
g("P01: manuel karar ve sözleşme", "g16.png",
  [([0.3, 0.45, 0.45, 0.68], "9 · Manuel değerlendirme"), ([0.38, 0.45, 0.48, 0.68], "10 · XOR: karar"),
   ([0.36, 0.2, 0.47, 0.6], "11 · Ek belge yükle, geri dönüş"), ([0.48, 0.2, 0.58, 0.36], "12 · ÖBF ver, sözleşme bas"),
   ([0.54, 0.08, 0.64, 0.22], "13 · Sözleşmeyi imzala")],
  "Dokuz numara tahsis kulvarında manuel değerlendirme. Kural motorunun karar veremediği başvurular kredi tahsis uzmanına düşer; B01 ve B02 ekranları. "
  "On numara karar mı diye soran {XOR}. Üç çıkış: onay ya da şartlı onay ÖBF'ye gider; ek belge bayiye döner. "
  "On bir numara ek belge yükle ve geri dönüş: bayi eksik belgeyi yükler, başvuru tekrar manuel değerlendirmeye girer; bu bir döngü. "
  "On iki numara ÖBF ver, sözleşme bas. Tüketici kredisinde ön bilgilendirme formu sözleşmeden önce verilir; bu yasal bir zorunluluk. "
  "On üç numara müşteri kulvarında kredi ve rehin sözleşmesini imzala. Müşteri kulvarına çıkan ok, işin müşteriye geçtiğini gösterir.")
g("P01: kullandırım", "g16.png",
  [([0.6, 0.22, 0.7, 0.36], "14 · Evrak yükle: iki ok"), ([0.6, 0.78, 0.7, 0.93], "15 · Rehin tescili"),
   ([0.66, 0.66, 0.75, 0.8], "16 · Kullandırım kontrolü"), ([0.74, 0.66, 0.79, 0.82], "17 · Uygun mu?")],
  "On dört numara: evrak yükle, kullandırım talep et. Bayi imzalı evrakı yükler; bu D09. Buradan iki ok çıkar. "
  "On beş numara harici sistemlerde rehin tescili; e-Devlet ya da noter. Teminatın tesisi budur. "
  "On altı numara operasyonda kullandırım kontrolü, dört göz. Dört göz ilkesi, yani {maker-checker}; B03 ekranı. "
  "On yedi numara uygun mu diye soran {XOR}. Hayır ise bayiye iade: evrak eksiği bayiye geri döner.")
g("P01: ödeme ve bitiş", "g16.png",
  [([0.78, 0.66, 0.86, 0.8], "18 · Ödeme emri, checker"), ([0.78, 0.8, 0.86, 0.93], "19 · Bayiye EFT"),
   ([0.84, 0.38, 0.92, 0.5], "20 · Kredi aktif, plan"), ([0.9, 0.08, 0.98, 0.22], "21 · Araç teslim alındı")],
  "On sekiz numara ödeme emri, {checker} onayıyla. Ödemeyi giren ve onaylayan farklı kişidir; bu SoD, yani görevler ayrılığı. "
  "On dokuz numara bayiye EFT: kredi tutarı bayiye ödenir. "
  "Yirmi numara kredi aktif, plan SMS ya da e-posta: ana sistem, yani {core system}, krediyi aktif eder ve ödeme planı müşteriye gider. "
  "Yirmi bir numara araç teslim alındı bitişi: olumlu sonuç.")
m("P01 cümle cümle (1/2)", ["Müşteri aracı seçer (2) → bayi Portal'a girer (3)", "Sistem KPS/KKB'yi SOAP ile sorgular (4–5), kural ve skor (6)",
                           "Otomatik karar (7): ret → bitiş (8) · manuel → uzman (9–11) · onay → ÖBF (12)",
                           "Müşteri imzalar (13) → bayi evrak + kullandırım talebi (14)"],
  "Şimdi P01'i cümle cümle okuyalım. Müşteri aracını seçer, iki numara; bayi temsilcisi başvuruyu Portal'a girer, üç numara. "
  "Sistem KPS ve KKB'yi SOAP ile sorgular, dört ve beş; kuralları ve skoru değerlendirir, altı. "
  "Otomatik karar üç yoldan birine gider, yedi: ret ise süreç ret bildirimiyle biter, sekiz; "
  "manuel ise tahsis uzmanı inceler ve onaylar, şartlı onaylar ya da ek belge ister, dokuz ile on bir arası; "
  "onay ise doğrudan ÖBF ve sözleşme adımına geçilir, on iki. "
  "Müşteri sözleşmeleri imzalar, on üç; bayi evrakı yükleyip kullandırım talep eder, on dört.")
m("P01 cümle cümle (2/2)", ["Rehin tescili başlar (15) · operasyon 4 göz kontrolü (16)", "Uygun değilse bayiye iade (17)",
                           "Uygunsa checker onayı (18) → bayiye EFT (19) → kredi aktif, plan (20)", "Müşteri aracı teslim alır (21)"],
  "Bu noktada rehin tescili harici sistemde başlatılır, on beş; operasyon dört göz kontrolü yapar, on altı. "
  "Evrak uygun değilse bayiye iade edilir, on yedi; uygunsa ödeme emri {checker} tarafından onaylanır, on sekiz; "
  "bayiye EFT yapılır, on dokuz; kredi aktifleşir ve plan müşteriye gönderilir, yirmi. Müşteri aracı teslim alır, yirmi bir.")
m("P01: BA olarak soracağın sorular (1/2)", ["14'ten çıkan iki ok paralel mi? → AND kapısı; EFT'den önce rehin bekleniyor mu?",
                                             "KKB 5 sn'de dönmezse? → 4'e hata / zaman aşımı sınır olayı",
                                             "\"Aynı gün onay\" nasıl ölçülüyor? → 9'a zamanlayıcı ve eskalasyon"],
  "Bir iş analisti olarak bu diyagrama hangi soruları sorarsın? "
  "Bir: on dört numaralı görevden çıkan iki ok paralel mi çalışıyor? Paralelse bir {AND} kapısıyla gösterilmeli. "
  "Ayrıca EFT'den önce rehin tescilinin tamamlanması bekleniyor mu? Diyagramda birleştirme kapısı yok. "
  "İki: KKB beş saniyede yanıt vermezse ne olur? U04'te bu durum manuel incelemeye düşürülüyor; "
  "P01'de dört numaralı göreve bir hata ya da zaman aşımı sınır olayı eklenmeli. "
  "Üç: belgeler eksiksizse aynı gün onay kuralı nasıl ölçülüyor? Manuel değerlendirme için bir zamanlayıcı ve eskalasyon yok.")
m("P01: BA olarak soracağın sorular (2/2)", ["Onaydan 30 gün sonra imza yoksa? → event-based: imza geldi / 30 gün doldu",
                                             "Kasko ve isteğe bağlı sigortalar (D06) nerede? Dain-i mürtehin kullandırım koşulu mu?",
                                             "Ret bildirimi müşteriye de gidiyor mu? Gerekçe kodu bayiye nasıl?"],
  "Dört: onaydan sonra otuz gün içinde imza gelmezse ne olur? U08'deki bu kural P01'de görünmüyor; "
  "{event-based} kapıyla imza geldi ya da otuz gün doldu ayrımı eklenmeli. "
  "Beş: kasko ve isteğe bağlı sigortalar, yani D06, bu akışta nerede? Teminatın parçası olan kasko poliçesinin "
  "dain-i mürtehin Firma olarak kesilmesi bir kullandırım koşulu mu? "
  "Altı: ret bildirimi müşteriye de gidiyor mu, gerekçe kodu bayiye nasıl gösteriliyor?")
dikkat("Bu soruları neden soruyorsun?", "Her soru bir eksik gereksinimdir: paralellik, zaman aşımı, SLA, 30 gün kuralı, teminat koşulu, bildirim.",
       "Bu altı sorunun ortak noktası şu: her biri bir eksik gereksinimdir. Paralellik, zaman aşımı, ölçülebilir hizmet süresi, otuz gün kuralı, "
       "teminat koşulu ve bildirim. Diyagram okumanın asıl amacı buldukların değil, eksik olanları fark etmektir.", tip="bilgi")

# ───────────────────────────── Görsel 2: U04
g("Görsel 2 · U04: katılımcılar ve ilk mesajlar", "g17.png",
  [([0.0, 0.0, 1.0, 1.0], "U04: P01'in 3–7. adımları, mesaj mesaj"),
   ([0.02, 0.09, 0.98, 0.18], "1 · Katılımcılar (lifeline)"), ([0.37, 0.09, 0.6, 0.18], "2 · «ext» KPS (SOAP)"),
   ([0.05, 0.15, 0.35, 0.23], "3 · POST /applications"), ([0.3, 0.23, 0.48, 0.32], "4 · Kendine mesaj")],
  "İkinci görsel U04, bayi başvurusu ve otomatik karar. P01'deki üç ile yedi arasındaki adımların sistemler arasında hangi mesajlarla gerçekleştiğini gösterir. "
  "Geliştirici bunu {API} tasarımı, test uzmanı entegrasyon testi olarak kullanır. "
  "Bir numara katılımcılar, yani {lifeline}'lar. Kutu katılımcı, altındaki kesikli çizgi zamandır. Soldan sağa: bayi Portal arayüzü, "
  "{API Gateway}, başvuru servisi, KPS, KKB, kural ve skor motoru, {core system} ve ELK. "
  "İki numara: ext KPS, SOAP. ext {stereotype}'ı Firma dışı sistem demek; gri kutular harici, mavi kutular Firma sistemleri. "
  "Üç numara ilk mesaj: POST bölü {applications}, JWT ve {correlation-id} ile. Düz ok senkron çağrıdır. "
  "JWT kimliği taşır; {correlation-id} tüm logları birbirine bağlar. "
  "Dört numara kendine mesaj, yani {self-call}: zorunlu alan ve belge kontrolü. Servis kendi içinde kontrol yapar; ok aynı çizgiye geri döner.",
  bolum="Görsel 2 · U04 (sequence)")
g("U04: alt, evaluate, opt", "g17.png",
  [([0.3, 0.32, 0.5, 0.4], "5 · Dönüş: kimlik + adres"), ([0.24, 0.37, 0.62, 0.5], "6 · alt [KKB yanıt verdi]"),
   ([0.24, 0.48, 0.62, 0.55], "7 · [timeout > 5 sn]"), ([0.3, 0.53, 0.7, 0.61], "8 · evaluate(...)"),
   ([0.24, 0.6, 0.86, 0.72], "9–10 · opt [ONAY] · createDraftLoan")],
  "Beş numara dönüş mesajı: kimlik ve adres. Kesikli ok yanıttır. "
  "Altı numara bir {alt} kutusu; üst bölmesinde koşul: KKB yanıt verdi. Bu bir {if} {else}: KKB yanıt verirse rapor ve skor alınır. "
  "Yedi numara {alt} kutusunun alt bölmesi: {timeout} beş saniyeden büyük. "
  "{Else} yolu: KKB beş saniyede dönmezse durum MANUEL_INCELEME olur. İki bölmeden yalnızca biri çalışır. "
  "Sekiz numara {evaluate}: başvuru, KKB, LTV ve kampanya parametreleriyle kural motoruna gider; LTV kredi değer oranıdır. "
  "Dokuz numara bir {opt} kutusu, koşulu karar eşittir ONAY. Tek dallı koşul: yalnızca onayda çalışır. "
  "On numara {createDraftLoan}, {core system}'e: onaylanan başvuru için ana sistemde taslak kredi açılır ve {loanId} döner.")
g("U04: log, yanıt, not", "g17.png",
  [([0.3, 0.72, 0.92, 0.79], "11 · log(...) → ELK, asenkron"), ([0.18, 0.77, 0.34, 0.85], "12 · 201 Created"),
   ([0.68, 0.8, 0.9, 0.93], "13 · Not: correlation-id, Postman")],
  "On bir numara: log, istek ve yanıt, PII maskeli, ELK'ya. Açık uçlu ok asenkron mesajdır; yanıt beklenmez. Kişisel veriler maskelenir. "
  "On iki numara: iki yüz bir {Created}, numara ve durum. {API} yanıtı; HTTP iki yüz bir, kayıt oluşturuldu demek. "
  "On üç numara bir not: tüm SOAP çağrıları ELK'da {correlation-id} ile aranabilir; Postman koleksiyonuyla tekrar oynatılabilir.")
m("U04 okunuşu ve bağlantılar", ["Bayi gönderir → gateway kimliği doğrular → başvuru servisi", "Zorunlu alanlar · KPS'den kimlik ve adres",
                                 "KKB yanıt → rapor + skor · 5 sn aşılırsa manuel", "Kural motoru karar · onayda core'da taslak kredi",
                                 "Her istek/yanıt maskeli ELK'ya · bayiye no + durum"],
  "U04'ün okunuşu: bayi başvuruyu gönderir; {gateway} kimliği doğrulayıp başvuru servisine iletir. "
  "Servis zorunlu alanları kontrol eder, KPS'den kimlik ve adresi alır. KKB yanıt verirse rapor ve skor alınır; "
  "beş saniyeyi aşarsa başvuru manuel incelemeye işaretlenir. Ardından kural motoru karar verir; karar onaysa {core system}'de taslak kredi açılır. "
  "Her istek ve yanıt maskelenerek ELK'ya yazılır; bayiye başvuru numarası ve durum döner. "
  "Rehberin diğer konularıyla bağlantısı: {correlation-id} ile Kibana'da arama ELK bölümünde; JWT ve kimlik IAM bölümünde; "
  "POST {applications} isteğinin Postman testi ve SOAP KPS, KKB çağrıları da Postman bölümünde.")
m("U04: soracağın sorular", ["KKB timeout olunca başvuru yine de kural motoruna gidiyor mu? (diyagramda evet)",
                             "Kural motoru KKB skoru olmadan nasıl karar veriyor?", "KPS hata verirse ne olur? (alt kutusu yok)",
                             "Ret ve manuel durumlarında bayiye hangi mesaj dönüyor?"],
  "U04 için soracağın sorular: KKB {timeout} olunca başvuru yine de kural motoruna gidiyor mu? Diyagramda evet. "
  "Peki kural motoru KKB skoru olmadan nasıl karar veriyor? KPS hata verirse ne olur? Bunun için bir {alt} kutusu yok. "
  "Ret ve manuel durumlarında bayiye hangi mesaj dönüyor?")

# ───────────────────────────── Görsel 3: U07
g("Görsel 3 · U07: Basvuru sınıfı", "g18.png",
  [([0.0, 0.0, 1.0, 1.0], "U07: Firma'nın çekirdek varlıkları"),
   ([0.19, 0.07, 0.37, 0.25], "1–2 · Basvuru: ad ve nitelikler"), ([0.19, 0.18, 0.37, 0.27], "3 · Operasyonlar"),
   ([0.02, 0.07, 0.24, 0.22], "4 · Musteri–Basvuru: 1 borçlu — 0..*")],
  "Üçüncü görsel: U07 alan modeli, numaralı. Yani başvurudan krediye, teminattan sigortaya ve IAM'e Firma'nın çekirdek varlıkları. "
  "Bir numara sınıf adı: Basvuru. Kutunun üst bölmesi varlıktır. "
  "İki numara nitelikler: kanal bayi, web ya da mobil; alanın alabileceği değerler. Ayrıca talep tutarı, para; vade, tamsayı; ödeme tipi. "
  "Üç numara operasyonlar: {simuleEt}, ödeme planı döndürür; ve {degerlendirmeyeGonder}. "
  "Dört numara Musteri ile Basvuru arası: bir borçlu, sıfır ya da çok. Bir müşteri sıfır ya da çok başvurunun borçlusu olabilir; "
  "her başvurunun bir borçlusu var. Borçlu bir rol adıdır; kefil ayrı bir rol ve Kefalet sınıfında.", bolum="Görsel 3 · U07 (class)")
g("U07: belge, karar, kampanya, bayi", "g18.png",
  [([0.02, 0.2, 0.24, 0.38], "5 · Belge ◆ Basvuru"), ([0.21, 0.24, 0.36, 0.42], "6 · KararKaydi ◆ Basvuru"),
   ([0.27, 0.03, 0.72, 0.12], "7 · Basvuru–Kampanya: 0..1"), ([0.52, 0.1, 0.72, 0.2], "8 · Bayi–Kampanya: çoktan çoğa"),
   ([0.35, 0.3, 0.9, 0.4], "9 · KararKaydi–Kullanici")],
  "Beş numara Belge'den Basvuru'ya dolu elmas, bir ve sıfır ya da çok. {Composition}: belgeler başvuruya aittir; başvuru silinirse belgeler de anlamını yitirir. "
  "Altı numara KararKaydi'dan Basvuru'ya dolu elmas: her başvurunun sıfır ya da çok karar kaydı olur; otomatik, manuel, şartlı ya da ek belge. "
  "Yedi numara Basvuru ile Kampanya arası: sıfır ya da çok, sıfır ya da bir. Bir başvuruda en fazla bir kampanya kullanılır; kampanya opsiyoneldir. "
  "Sekiz numara Bayi ile Kampanya arası: iki uçta da sıfır ya da çok, kapsam. Çoktan çoğa: bir kampanya birçok bayide geçerli, "
  "bir bayinin birçok kampanyası olur. "
  "Dokuz numara KararKaydi ile Kullanici arası: sıfır ya da çok karar veren, bir. Her karar kaydı tek bir kullanıcıya bağlı; bu denetim izidir.")
g("U07: kredi, teminat, plan", "g18.png",
  [([0.21, 0.4, 0.36, 0.5], "10 · onay → dönüşür 0..1"), ([0.0, 0.52, 0.2, 0.7], "11–12 · «abstract» Teminat, kalıtım"),
   ([0.34, 0.48, 0.54, 0.6], "13 · Kredi ◆ OdemePlani"), ([0.52, 0.47, 0.72, 0.6], "14 · OdemePlani ◆ Taksit")],
  "On numara KararKaydi'dan Kredi'ye: onay, dönüşür, sıfır ya da bir. Onaylanan başvuru en fazla bir krediye, yani sözleşmeye dönüşür. "
  "On bir numara boş üçgen, yani kalıtım: Rehin ve Kefalet birer Teminat'tır. "
  "On iki numara {abstract} Teminat: soyut sınıf; tek başına nesnesi olmaz, ancak Rehin ya da Kefalet olarak var olur. "
  "On üç numara Kredi ile OdemePlani arası dolu elmas, bir ve bir ya da çok, versiyon. Bir kredinin birden çok ödeme planı versiyonu olur: "
  "vade değişikliği ya da ara ödeme gibi. On altı numaralı not bunu açıklar. "
  "On dört numara OdemePlani ile Taksit arası dolu elmas, bir ve bir ya da çok: taksitler plana aittir. Durum: ödendi, bekliyor ya da gecikmede.")
g("U07: IAM, not, kredi operasyonları", "g18.png",
  [([0.75, 0.3, 0.9, 0.68], "15 · Kullanici → Rol → Yetki"), ([0.75, 0.68, 0.95, 0.8], "16 · Not: Para, versiyon"),
   ([0.2, 0.55, 0.36, 0.62], "17 · kapamaTutari(tarih), kapat()")],
  "On beş numara Kullanici, Rol ve Yetki: iki ilişkide de sıfır ya da çok. IAM modeli: kullanıcıya rol, role yetki verilir. "
  "Rolün {sodGrubu} alanı görevler ayrılığını tutar. "
  "On altı numara not: para, tutar artı para birimidir. Plan değişikliğinde yeni versiyon oluşur; eski versiyon pasifleşir, silinmez. "
  "On yedi numara kredi operasyonları: {kapamaTutari}, tarih alır ve para döndürür; erken kapama hesabı, yani W08. Bir de {kapat}.")
m("U07'den çıkan iş kuralları", ["Başvuruda en fazla bir kampanya", "Her kararın bir sahibi var",
                                 "Plan değişikliği tarihçeyi silmez", "Teminat: rehin ya da kefalet (ortak araçta biri borçlu biri kefil, çapraz kefalet yok)",
                                 "Kredinin 0..* poliçesi; dainiMurtehin: Boolean"],
  "Bu modelden çıkan iş kuralları: başvuruda en fazla bir kampanya; her kararın bir sahibi var; ödeme planı değişikliği tarihçeyi silmez. "
  "Teminat rehin ya da kefalet olabilir. Firma kuralı: ortak alınan araçta biri borçlu diğeri kefil olur, çapraz kefalet yok. "
  "Bir kredinin sıfır ya da çok sigorta poliçesi olur; {dainiMurtehin} adlı {Boolean} alan, kaskoda Firma'nın rehin alacaklısı olduğunu tutar.")
m("U07: BA incelemesi", ["Arac: faturaBedeli ve kaskoDegeri → kredi/değer hangisine göre?",
                         "Kampanya.maxLTV var; bireysel kademe tablosu (400.000 / 2.000.000 ₺) nerede?",
                         "Kurumsal %90 kuralı Musteri.tip'e mi bağlı?", "Kefalet'teki kefil: Musteri ilişkisi çizgi olarak yok"],
  "İş analisti incelemesi: Arac sınıfında {faturaBedeli} ve {kaskoDegeri} var; kredi değer kuralı hangisine göre hesaplanıyor? "
  "Kampanya'da {maxLTV} var ama bireysel kademeli LTV tablosu, yani dört yüz bin ve iki milyon lira eşikleri, hangi varlıkta tutuluyor? "
  "Kurumsal müşteri için yüzde doksan kuralı Musteri tip alanına mı bağlı? "
  "Ve Kefalet'teki kefil, Musteri tipinde bir alan ama bu ilişki çizgi olarak çizilmemiş.")

# ───────────────────────────── Görsel 4: U08
g("Görsel 4 · U08: başlangıç ve değerlendirme", "g19.png",
  [([0.0, 0.0, 1.0, 1.0], "U08: başvurunun tüm durumları"),
   ([0.02, 0.1, 0.3, 0.22], "1–2 · Başlangıç, gönder()"), ([0.27, 0.1, 0.42, 0.22], "3 · Değerlendirmede"),
   ([0.22, 0.19, 0.42, 0.38], "4 · Ek Belge Bekleniyor"), ([0.38, 0.09, 0.6, 0.22], "5–6 · Manuel İnceleme")],
  "Dördüncü görsel: U08 başvuru yaşam döngüsü, numaralı. Yani bir başvurunun alabileceği tüm durumlar ve aralarındaki geçişler. "
  "Portal'daki D08 başvurularım ekranı ve {back-office}'teki B01 tahsis kuyruğu bu durumları gösterir. "
  "Bir numara dolu siyah nokta: ilk durum noktası. "
  "İki numara geçiş etiketi: gönder, köşeli parantezde zorunlu belgeler tam. Olay gönder; koşul köşeli parantezde; belgeler tam değilse gönderilemez. "
  "Üç numara değerlendirmede durumu: kural motoru çalışıyor. "
  "Dört numara ek belge bekleniyor ve gidiş dönüş okları: ek belge iste ile girilir, belge yüklendi ile değerlendirmede durumuna dönülür. "
  "Beş numara: kural uyarısı ya da KKB {timeout}. Manuel incelemeye düşme nedenleri; U04'teki zaman aşımıyla aynı. "
  "Altı numara manuel inceleme: tahsis uzmanının kuyruğunda.", bolum="Görsel 4 · U08 (state)")
g("U08: komite, ret, onay", "g19.png",
  [([0.58, 0.09, 0.8, 0.22], "7 · [limit dışı] → Komitede"), ([0.55, 0.25, 0.8, 0.42], "8 · Şartlı Onay"),
   ([0.8, 0.09, 1.0, 0.32], "9 · Reddedildi"), ([0.37, 0.22, 0.5, 0.42], "10 · otomatik onay"),
   ([0.44, 0.42, 0.6, 0.55], "11 · Onaylandı")],
  "Yedi numara: köşeli parantezde limit dışı, komitede. Uzmanın yetki limitini aşan başvuru kredi komitesine gider. "
  "Sekiz numara şartlı onay: manuel incelemeden ya da komiteden gelinir. Şartlar kabul edilip plan yeniden hesaplanınca onaylandı durumuna geçer. "
  "Dokuz numara reddedildi, pembe, ve son durum. Manuel incelemeden ya da komiteden ret. Pembe olumsuz son demek. "
  "On numara otomatik onay: değerlendirmede durumundan doğrudan onaylandı durumuna; manuel adım atlanır. "
  "On bir numara onaylandı: ÖBF ve sözleşme aşaması.")
g("U08: iptal, sözleşme, kullandırım", "g19.png",
  [([0.02, 0.42, 0.25, 0.55], "12 · İptal / Süresi Doldu"), ([0.1, 0.22, 0.22, 0.45], "13 · 30 gün işlem yok"),
   ([0.45, 0.58, 0.6, 0.7], "14 · Sözleşme İmzalandı"), ([0.44, 0.68, 0.62, 0.86], "15 · Kullandırım Kontrolde"),
   ([0.6, 0.72, 0.92, 0.86], "16–17 · Kullandırıldı, checker")],
  "On iki numara iptal ya da süresi doldu: onaydan sonra otuz gün geçerse ya da müşteri vazgeçerse. "
  "On üç numara otuz gün işlem yok: taslakta otuz gün bekleyen başvuru da iptal olur; bu bir zaman olayı. "
  "On dört numara sözleşme imzalandı: imza ve evrak ile girilir. "
  "On beş numara kullandırım kontrolde ve bayiye iade, eksik evrak: P01'deki on altı ve on yedinci adımların durum karşılığı. "
  "On altı numara kullandırıldı, yeşil: başarılı son. "
  "On yedi numara ödeme emri onay, {checker}: kullandırımı tetikleyen olay; dört göz.")
m("U08 okunuşu", ["Taslak → belgeler tamsa değerlendirme", "Otomatik onay · ek belge · manuel",
                  "Manuel: onay, şartlı, ret, komite", "Onaylandı → İmzalandı → Kontrolde",
                  "İade ya da checker → Kullandırıldı"],
  "U08'in okunuşu: başvuru taslak olarak doğar; zorunlu belgeler tamsa gönderilip değerlendirmeye girer. "
  "Kural motoru onaylarsa doğrudan onaylandı durumuna geçer; eksik belge varsa ek belge bekleniyor durumunda bekler; "
  "kural uyarısı ya da KKB zaman aşımında manuel incelemeye düşer. "
  "Manuel incelemede başvuru onaylanır, şartlı onaylanır, reddedilir ya da uzmanın limitini aşıyorsa komiteye gider. "
  "Onaylanan başvuru imza ve evrakla sözleşme imzalandı durumuna, kullandırım talebiyle kullandırım kontrolde durumuna geçer. "
  "Evrak eksikse bayiye iade edilir; {checker} ödeme emrini onaylayınca kullandırıldı olur.")
dikkat("Diyagramdan test senaryosu", "Her ok = pozitif test · ok olmayan her geçiş = negatif test. Reddedildi → Onaylandı ✗ · Taslak → Manuel İnceleme ✗ · Kullandırıldı'dan dönüş ✗",
       "Bu diyagramdan test senaryosu yazmanın kolay yolu: her ok bir pozitif testtir; ok olmayan her geçiş bir negatif testtir. "
       "Örnek negatif testler: reddedildi durumundan onaylandı durumuna geçilememeli; taslaktan doğrudan manuel incelemeye geçilememeli; "
       "kullandırıldı durumundan geri dönülememeli. "
       "Soracağın sorular da şunlar: reddedilen başvuruya itiraz ya da yeniden başvuru nasıl işliyor? "
       "Ek belge bekleniyor durumunda bir süre sınırı var mı? Komite kararı için SLA ne?", tip="bilgi")

# ───────────────────────────── Görsel 5: D05
g("Görsel 5 · D05: ekran bağlamı", "g20.png",
  [([0.0, 0.0, 1.0, 1.0], "D05: yeni başvuru, adım 3"),
   ([0.0, 0.0, 0.5, 0.05], "1 · Adres: hangi sayfa"), ([0.6, 0.03, 1.0, 0.09], "2 · Bildirim, bayi, kullanıcı"),
   ([0.0, 0.09, 0.2, 0.45], "3 · Sol menü: Yeni Başvuru"), ([0.17, 0.1, 0.65, 0.24], "4–5 · Taslak, adım göstergesi")],
  "Beşinci görsel D05: Portal'da yeni başvurunun üçüncü adımı, kredi ve kampanya; bir {wireframe}. "
  "Bir ekran taslağı da diyagram gibi okunur: amaç, alanlar, kurallar, aksiyonlar ve mesajlar. "
  "Bir numara adres: portal nokta firma nokta com nokta tr, başvuru, yeni, kredi. Hangi kanal ve sayfa: yetkili satıcı portalı. "
  "İki numara bildirim, bayi, yani Örnek Oto Kadıköy, ve kullanıcı. Oturum bağlamı: kullanıcı yalnız kendi bayisinin verisini görür; bu IAM. "
  "Üç numara sol menü, yeni başvuru seçili. Portalın ana işlevleri; raporlar altında satış performansı ve penetrasyon. "
  "Dört numara: taslak B tire yüz on sekiz bin yedi yüz doksan. Başvuru henüz taslak durumunda; U08'deki ilk durum. "
  "Beş numara adım göstergesi, adım üç: müşteri tamam, araç tamam, kredi ve kampanya; sonra sigorta, belgeler ve gönder.",
  bolum="Görsel 5 · D05 (wireframe)")
g("D05: kredi parametreleri", "g20.png",
  [([0.19, 0.27, 0.58, 0.35], "6 · Kampanya"), ([0.19, 0.35, 0.58, 0.42], "7 · Ödeme tipi: Balon"),
   ([0.19, 0.42, 0.58, 0.49], "8 · Kredi tutarı, vade"), ([0.19, 0.49, 0.58, 0.56], "9 · Balon tutarı (%30)"),
   ([0.19, 0.56, 0.58, 0.63], "10 · Faiz: gri alan")],
  "Altı numara kampanya: Model X yüzde sıfır faiz, on iki ay. Bayi kapsamındaki geçerli kampanyalar listelenir. "
  "Yedi numara ödeme tipi: balon ödemeli. Firma ürünlerinden biri; diğerleri eşit, kademeli artan, ara ödemeli ve değişken. "
  "Sekiz numara kredi tutarı dört yüz otuz bin lira, vade yirmi dört ay. Vade Firma kuralıyla altı ile altmış ay arasında seçilebilir. "
  "Dokuz numara balon tutarı, yüzde otuz: yüz yirmi dokuz bin lira. Son taksitte ödenecek tutar; planın son satırında "
  "yüz kırk üç bin yüz yirmi lira kırk kuruş olarak görünür. "
  "On numara aylık faiz, gri alan. Pasif alan: kullanıcı değiştiremez; kampanya ya da fiyat tablosundan gelir.")
g("D05: hesap, ihlal, plan", "g20.png",
  [([0.19, 0.63, 0.58, 0.7], "11 · Ödeme Planını Hesapla"), ([0.19, 0.7, 0.58, 0.81], "12 · Kural ihlali"),
   ([0.59, 0.25, 1.0, 0.5], "13 · Ödeme planı önizleme"), ([0.59, 0.5, 1.0, 0.6], "14 · Özet"),
   ([0.59, 0.64, 1.0, 0.71], "15–16 · ÖBF yazdır, Devam")],
  "On bir numara ödeme planını hesapla: kural motorunu ve plan hesabını tetikler; U07'deki {simuleEt}. "
  "On iki numara kırmızı kural ihlali kutusu: seçilen kampanya balon ödemeli tip ile kullanılamaz; kampanya koşulları eşit ödemeli, on iki ay, "
  "en fazla yüzde elli kredi değer. Mesaj hangi kuralın ihlal edildiğini söylüyor; iyi bir hata mesajı budur. "
  "On üç numara ödeme planı önizleme: taksit numarası, vade tarihi, taksit ve kalan anapara. "
  "On dört numara özet: toplam geri ödeme, yıllık maliyet oranı, toplam faiz ve kredi değer; müşteriye gösterilmesi gereken maliyet bilgileri. "
  "On beş numara ön bilgi formu yazdır. Yasal: ÖBF sözleşmeden önce verilir, teslim kaydı başvuruya bağlanır. "
  "On altı numara devam: sigorta adımına, yani D06'ya geçer.")
m("D05: tutarlılık kontrolü", ["İhlal varken plan görünüyor → önizleme gizlenmeli mi, Devam pasif mi?",
                               "Kampanya \"%0 faiz\" ama alan %1,99 · kampanya 12 ay, vade 24 ay",
                               "Kredi/değer %20 → araç ≈ 2.150.000 ₺ → bireysel üst sınır 2.000.000 ₺ aşılır"],
  "Ekrandaki tutarlılık kontrolü; iş analistinin yapması gereken iş. Kural ihlali varken ekranda yine de bir ödeme planı görünüyor. "
  "İhlal varken önizleme gizlenmeli mi, devam düğmesi pasif mi olmalı? "
  "Kampanya yüzde sıfır faiz diyor ama faiz alanı yüzde bir virgül doksan dokuz gösteriyor; kampanyada on iki ay koşulu varken vade yirmi dört ay seçili. "
  "Ekran hangi değerin geçerli olduğunu açıkça göstermeli. "
  "Kredi değer yüzde yirmi görünüyor; dört yüz otuz bin lira kredi için bu, araç bedelinin yaklaşık iki milyon yüz elli bin lira olduğu anlamına gelir. "
  "Bu da bireysel kuralın üst sınırı olan iki milyon lirayı aşar. Bu örnek değerler, taslağın tutarlılığını sorgulamak için iyi bir alıştırma.")
m("D05'ten kabul kriteri", ["Senaryo: Kampanya ödeme tipiyle uyumsuz", "Diyelim ki kampanya yalnız Eşit Ödemeli tipte geçerli",
                            "Eğer ki bayi \"Balon Ödemeli\" seçip Hesapla'ya basarsa", "O zaman ihlal edilen kural ve koşullar gösterilmeli",
                            "Ve önizleme gösterilmemeli · Ve \"Devam\" pasif olmalı"],
  "Bu ekrandan yazılacak bir kabul kriteri örneği. Senaryo: kampanya ödeme tipiyle uyumsuz. "
  "Diyelim ki Model X yüzde sıfır faiz, on iki ay kampanyası yalnızca eşit ödemeli tipte geçerli. "
  "Eğer ki bayi bu kampanyayla balon ödemeli tipi seçip ödeme planını hesapla düğmesine basarsa, "
  "o zaman sistem ihlal edilen kuralı ve kampanya koşullarını gösteren hata mesajını göstermeli. "
  "Ve ödeme planı önizlemesi gösterilmemeli. Ve devam düğmesi pasif olmalı.")

# ───────────────────────────── Envanter
m("Diyagram envanteri: nasıl çalışmalı?", ["Çalışma Seti'ndeki diyagramları rehber konularıyla eşleştir",
                                           "Her birini 7 adımla oku", "Sonra ilgili bölümün laboratuvarında kendin çiz"],
  "Son olarak Firma diyagram envanteri: hangi konuyu hangi dosyayla çalışmalısın? "
  "Çalışma setindeki diyagramları rehberin konularıyla eşleştirerek çalış. Her birini yedi adımla oku, "
  "sonra ilgili bölümün laboratuvarında kendin yeniden çiz.", bolum="Atölye · Envanter ve kendini sına")
t("Envanter (1/3): UML", ["Rehber konusu", "Çalışma setindeki karşılığı"],
  [["UML – use case", "U01 kanallar, U02 back-office ve IAM, U14 Sigorta"], ["UML – activity", "U03 değerlendirme ve otomatik karar"],
   ["UML – sequence", "U04, U05 (3D Secure), U06 erken kapama, U11, U16 IAM"], ["UML – class", "U07 alan modeli, U15 sigorta alan modeli"],
   ["UML – state machine", "U08 başvuru, U09 kredi hesabı, U12 poliçe, U13 hasar"]],
  "UML {use case}: U01 müşteri ve bayi kanalları, U02 {back-office} ve IAM, U14 Firma sigorta. "
  "UML {activity}: U03 başvuru değerlendirme ve otomatik karar. "
  "UML {sequence}: U04 bayi başvurusu, U05 online taksit ödeme, yani {3D Secure}, U06 erken kapama ve rehin fekki, "
  "U11 sigorta teklif karşılaştırma, U16 IAM erişim talebi. "
  "UML {class}: U07 alan modeli ve U15 sigorta alan modeli. "
  "UML {state machine}: U08 başvuru, U09 kredi hesabı, U12 sigorta poliçesi ve U13 hasar dosyası.")
t("Envanter (2/3): mimari, veri, BPMN", ["Rehber konusu", "Çalışma setindeki karşılığı"],
  [["UML – component / deployment", "U10 mimari ve entegrasyonlar, U18 ağ bölgeleri"], ["Süreç – veri akışı", "U17 kredi ve sigorta veri akışı"],
   ["BPMN – kredi ve tahsilat", "P01, P02 gecikme, P04 vade değişikliği, P05 erken kapama, P13 kredi devri"],
   ["BPMN – sigorta", "P03 kasko yenileme, P09, P10 hasar, P11 iptal, P12 kredi koruma"]],
  "UML {component} ve {deployment}: U10 sistem mimarisi ve entegrasyonlar, U18 ağ bölgeleri ve dağıtım. "
  "Süreç diyagramlama, veri akışı: U17 kredi ve sigorta veri akışı. "
  "BPMN kredi ve tahsilat: P01 başvurudan kullandırıma, P02 gecikme ve tahsilat, P04 vade değişikliği talebi, "
  "P05 erken kapama ve rehin fekki, P13 kredi devri. "
  "BPMN sigorta: P03 kasko yenileme takibi, ki on beş gün kuralı burada; P09 tekliften poliçeye; P10 kasko hasar ihbarından ödemeye; "
  "P11 poliçe iptali ve prim iadesi; P12 kredi koruma tazminatı.")
t("Envanter (3/3): IAM, Agile, yönetişim, ekranlar", ["Rehber konusu", "Çalışma setindeki karşılığı"],
  [["IAM", "P06 Joiner-Mover-Leaver, U16, I01–I03 ekranları"], ["Agile, Jira, Confluence", "P08 BA teslimat, P15 test ve UAT, US-01…US-10"],
   ["IT yönetişimi · şikayet", "P07 ITIL değişiklik (CR), I04 · P14 şikayet ve kök neden"],
   ["Wireframe okuma", "W01–W12 web, M01–M08 mobil, D01–D09 Portal, B01–B08, S01–S15, F01–F11"]],
  "IAM: P06 {Joiner-Mover-Leaver} ve yetki gözden geçirme, U16, ve I01 ile I03 arası ekranlar; erişim talebi, rol ve yetki matrisi, yetki gözden geçirme. "
  "Agile, Jira ve Confluence: P08 BA teslimat süreci, P15 sistem testi ve UAT, ve çalışma setindeki US sıfır birden US ona kadar {user story}'ler. "
  "IT yönetişimi: P07 ITIL değişiklik yönetimi, yani CR, ve I04 değişiklik talebi ekranı. Şikayet ve kök neden: P14. "
  "{Wireframe} okuma: W01'den W12'ye web self servis, M01'den M08'e mobil, D01'den D09'a Portal, "
  "B01'den B08'e {back-office}, S01'den S15'e sigorta, F01'den F11'e ek senaryolar.")

# ───────────────────────────── Kendini sına
soru("Kendini sına 1/5", "P01'de 7 numaralı kapı XOR yerine AND olsaydı ne olurdu?",
     ["Yalnız onay yolu çalışırdı", "Üç yol birden başlardı", "Süreç kilitlenirdi", "Hiçbir şey değişmezdi"], 1,
     "Kendini sınayalım. Birinci soru: P01'de yedi numaralı kapı {XOR} yerine {AND} olsaydı ne olurdu? "
     "A, yalnız onay yolu çalışırdı. B, üç yol birden başlardı. C, süreç kilitlenirdi. D, hiçbir şey değişmezdi.",
     "Doğru cevap B. Onay, ret ve manuel yolların üçü birden başlardı; aynı başvuru hem reddedilir hem sözleşmeye giderdi.")
soru("Kendini sına 2/5", "U04'te KKB 6 saniyede yanıt verirse başvurunun durumu ne olur?",
     ["ONAY", "RET", "MANUEL_INCELEME", "Taslak"], 2,
     "İkinci soru: U04'te KKB altı saniyede yanıt verirse başvurunun durumu ne olur? A, ONAY. B, RET. C, MANUEL_INCELEME. D, taslak.",
     "Doğru cevap C. Köşeli parantezde {timeout} beş saniyeden büyük dalı çalışır; durum MANUEL_INCELEME olur.")
soru("Kendini sına 3/5", "U07'ye göre bir başvuruda iki kampanya kullanılabilir mi?",
     ["Evet", "Hayır, kampanya ucu 0..1", "Yalnız kurumsalda", "Bayiye bağlı"], 1,
     "Üçüncü soru: U07'ye göre bir başvuruda iki kampanya kullanılabilir mi? A, evet. B, hayır, kampanya ucu sıfır ya da bir. "
     "C, yalnız kurumsalda. D, bayiye bağlı.",
     "Doğru cevap B. İlişkinin kampanya ucu sıfır ya da bir.")
soru("Kendini sına 4/5", "U08'e göre Komitede durumundaki başvuru hangi durumlara geçebilir?",
     ["Onaylandı veya Taslak", "Reddedildi veya Şartlı Onay", "Kullandırıldı", "Ek Belge Bekleniyor"], 1,
     "Dördüncü soru: U08'e göre komitede durumundaki bir başvuru hangi durumlara geçebilir? "
     "A, onaylandı ya da taslak. B, reddedildi ya da şartlı onay. C, kullandırıldı. D, ek belge bekleniyor.",
     "Doğru cevap B: reddedildi ya da şartlı onay.")
soru("Kendini sına 5/5", "D05'te faiz alanı neden gri?",
     ["Hata var", "Pasif alan: kampanyadan / fiyat tablosundan gelir", "Kampanya seçilmedi", "Vade geçersiz"], 1,
     "Beşinci soru: D05'te faiz alanı neden gri? A, hata var. B, pasif alan; kampanyadan ya da fiyat tablosundan gelir. "
     "C, kampanya seçilmedi. D, vade geçersiz.",
     "Doğru cevap B. Pasif alan: faiz kullanıcı tarafından girilmez, kampanyadan ya da fiyat tablosundan gelir.")
m("Bu videoda neler gördük?", ["7 adımlı okuma yöntemi", "P01 BPMN: 21 numara, okunuş, 6 soru", "U04 sequence: alt, opt, asenkron log",
                               "U07 class: çokluk, composition, kalıtım · U08 state: test senaryoları", "D05 wireframe: tutarlılık, kabul kriteri · envanter"],
  "Toparlayalım. Yedi adımlı okuma yöntemini öğrendik. P01 BPMN diyagramını yirmi bir numarasıyla okuduk ve altı soru çıkardık. "
  "U04'te {alt}, {opt} ve asenkron logu; U07'de çokluk, {composition} ve kalıtımı; U08'de durumları ve test senaryolarını gördük. "
  "D05 ekranında tutarlılık kontrolü yapıp bir kabul kriteri yazdık ve diyagram envanterini çıkardık. "
  "Bir sonraki videoda SQL ile veriyi kendimiz sorgulamaya başlıyoruz.", ton="sakin")

kaydet(__file__, {
    "baslik": "Business Analyst Teknik Rehberi · 5: Diyagram okuma atölyesi",
    "alt_baslik": "BPMN · sequence · class · state · wireframe: numara numara okuma",
    "kapanis": "Sıradaki video: SQL",
    "tema": 5,
    "youtube_baslik": "Business Analyst Teknik Rehberi 5/14: Diyagram okuma atölyesi (BPMN, sequence, class, state, wireframe)",
    "etiketler": ["business analyst", "diyagram okuma", "BPMN", "sequence diagram", "class diagram", "wireframe", "iş analisti"],
}, {"JWT": "cey dabılyu ti", "PII": "pi ay ay", "HTTP": "eyç ti ti pi", "ITIL": "itil", "CR": "si ar", "UAT": "yu ey ti",
    "US-01": "yu es sıfır bir", "US-10": "yu es on", "MANUEL_INCELEME": "manuel inceleme", "B-118790": "be, yüz on sekiz bin yedi yüz doksan",
    "Basvuru": "başvuru", "Musteri": "müşteri", "KararKaydi": "karar kaydı", "Kullanici": "kullanıcı", "OdemePlani": "ödeme planı",
    "Arac": "araç", "Kampanya": "kampanya", "Rehin": "rehin", "Kefalet": "kefalet", "Teminat": "teminat", "Taksit": "taksit",
    "Rol": "rol", "Yetki": "yetki", "Belge": "belge", "Kredi": "kredi"})
