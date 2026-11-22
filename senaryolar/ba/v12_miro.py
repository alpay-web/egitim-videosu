#!/usr/bin/env python3
"""BA Teknik Rehberi · Video 12: Miro. Belge satır 3494–3732."""
from ortak import m, t, dikkat, g, soru, kaydet

m("Miro nedir?", ["Sonsuz tuval üzerinde eş zamanlı görsel iş birliği", "\"AI Innovation Workspace\": Sidekicks, Flows, Connectors",
                  "BA: workshop yönetmek, fikri görselleştirmek", "Paydaşları ortak resimde buluşturmak", "Dağınık bilgiyi gereksinime dönüştürmek"],
  "{Miro}, ekiplerin sonsuz bir tuval, yani {canvas} üzerinde eş zamanlı çalıştığı görsel iş birliği platformudur. "
  "Şirket kendisini artık {AI Innovation Workspace} olarak konumluyor: tuval üzerinde çalışan {Sidekicks}, yani yapay zeka ajanları; "
  "{Flows}, çok adımlı yapay zeka iş akışları; ve {Slack}, {Atlassian}, {GitHub} gibi araçlara {Connectors}. "
  "İş analisti için {Miro}; workshop yönetmek, fikirleri hızla görselleştirmek, paydaşları ortak bir resimde buluşturmak "
  "ve dağınık bilgiyi yapılandırılmış gereksinime dönüştürmek için kullanılır.",
  bolum="Miro: giriş ve hedefler", kanca="İyi bir workshop, iyi hazırlanmış bir panoyla başlar.", ton="merakli")
m("Bu bölümün hedefleri", ["Workshop panosu: frame'ler, renk kodları, zaman planı", "Bayi portalı story map: omurga, yürüyen iskelet, sürüm dilimleri",
                           "Kişisel verinin aktığı sistemleri gösteren DFD", "Workshop çıktısını Jira ve Confluence'a taşımak"],
  "Bu bölümü bitirdiğinde şunları yapabileceksin. Bir: bir gereksinim workshop'u için {frame}'leri, renk kodları ve zaman planı belli bir {Miro} panosu hazırlamak. "
  "İki: Firma bayi portalı için omurga, yürüyen iskelet ve sürüm dilimlerinden oluşan bir {user story map} çıkarmak. "
  "Üç: kişisel verinin hangi sisteme aktarıldığını gösteren bir veri akış diyagramı, yani DFD çizmek. "
  "Dört: workshop çıktısını Jira {story}'lerine ve Confluence sayfasına taşımak.")
t("Başlamadan önce gerekenler", ["Gereken", "Nereden", "Hazır olduğunu nasıl anlarsın"],
  [["Miro hesabı (ücretsiz plan)", "miro.com → Sign up", "\"+ New board\" düğmesi"], ["User story kalıbı", "Jira bölümü", "Rol, istek, fayda"],
   ["2–3 katılımcı", "—", "İki kişi aynı anda not ekleyebiliyor"]],
  "Başlamadan önce tablo üç sütun: gereken, nereden ve hazır olduğunu nasıl anlarsın. "
  "{Miro} hesabı; ücretsiz plan, sınırlı sayıda düzenlenebilir pano: miro nokta com, {Sign up}. {Dashboard}'da artı {New board} düğmesi varsa tamam. "
  "{User story} kalıbı: Jira bölümü; bir {story}'yi rol, istek ve fayda ile yazabiliyorsan tamam. "
  "Workshop'a katılacak iki üç kişi; deneme için arkadaş da olur. Aynı panoya iki kişi aynı anda yapışkan not ekleyebiliyorsa başlayabiliriz.")

# ───────────────────────────── Temel
m("Temel araçlar", ["Sticky note · şekil ve bağlayıcı · metin · frame", "Kart (Jira kartına dönüşür) · tablo · mind map",
                    "Şekil kütüphaneleri: BPMN, UML, AWS/Azure, flowchart", "Yorum · oylama · zamanlayıcı · şablon galerisi (Miroverse)"],
  "Temel seviye. Temel araçlar: yapışkan not, yani {sticky note}; şekiller ve bağlayıcılar; metin; {frame}, yani çerçeve, sunum ve gezinme bölümleri. "
  "Kart, Jira kartına dönüştürülebilir görev kartı; tablo; {mind map}; diyagram şekil kütüphaneleri, yani BPMN, UML, AWS ve {Azure}, {flowchart}. "
  "Yorum, oylama, zamanlayıcı ve şablon galerisi; {Miroverse} topluluk şablonları dahil.", bolum="Miro · Temel seviye")
m("İlk board'u düzenlemek", ["Soldan sağa frame'ler: Bağlam → Problem → Fikirler → Önceliklendirme → Aksiyonlar", "Her frame'in başında amaç ve talimat",
                             "Renk efsanesi: sarı fikir · kırmızı sorun · yeşil karar · mavi soru", "Katılımcı başına renk ya da isim etiketi"],
  "İlk {board}'unu düzenlerken: soldan sağa akışta {frame}'ler; bağlam, problem, fikirler, önceliklendirme, aksiyonlar. "
  "Her {frame}'in başında amaç ve talimat. Renk kodu efsanesi: sarı fikir, kırmızı sorun, yeşil karar, mavi soru. "
  "Ve katılımcı başına renk ya da isim etiketi.")
m("Kolaylaştırıcı özellikleri", ["\"Bring everyone to me\": herkesi kendi ekranına çek", "Takip modu (follow) · zamanlayıcı",
                                 "Gizli / anonim oylama", "Kilit (lock): sözleşilen alan bozulmasın", "Özel (private) mod: bağımsız fikir, sonra aç"],
  "Workshop için kolaylaştırıcı özellikleri: {Bring everyone to me}, yani herkesi bulunduğun ekrana çekme; takip modu, yani {follow}; zamanlayıcı; "
  "gizli ya da anonim oylama; katılımcıların sözleşmesi gereken alanı kilitleme, yani {lock}; "
  "ve özel, yani {private} mod ile bağımsız fikir üretip sonra açma.")

# ───────────────────────────── Orta
t("BA'nın Miro teknikleri (1/3)", ["Teknik", "Amaç", "Çıktı"],
  [["Paydaş haritası (güç/ilgi)", "Kimle nasıl iletişim", "Paydaş listesi, iletişim planı"], ["Customer journey map", "Uçtan uca deneyim, acı noktalar", "Fırsat listesi"],
   ["User story mapping", "Backbone altında story, MVP dilimi", "Sürüm planı, backlog"]],
  "Orta seviye: iş analistinin {Miro}'da yürütebileceği teknikler. Paydaş haritası, yani güç ilgi matrisi: kimlerle nasıl iletişim kurulacağını belirleme; "
  "çıktı paydaş listesi ve iletişim planı. {Customer journey map}: müşterinin uçtan uca deneyimini ve acı noktalarını görme; çıktı fırsat listesi. "
  "{User story mapping}: {backbone}, yani kullanıcı aktiviteleri altında {story}'leri dizip MVP ve sürüm dilimlerini çizme; "
  "çıktı sürüm planı ve önceliklendirilmiş {backlog}.", bolum="Miro · Orta seviye")
t("BA'nın Miro teknikleri (2/3)", ["Teknik", "Amaç", "Çıktı"],
  [["Event Storming", "Olay, komut, aktör, politika, dış sistem zaman çizgisinde", "Bounded context'ler"], ["As-is süreç haritalama", "Adımları ve sorunları keşfetmek", "Ham süreç → BPMN"],
   ["Affinity mapping", "Bulguları temalara gruplamak", "Tema listesi"], ["Dot voting / MoSCoW / değer–efor", "Önceliklendirme", "Öncelik sırası"]],
  "{Event Storming}: domain olaylarını turuncu, komutları mavi, aktörleri sarı, politikaları mor, dış sistemleri pembe notlarla zaman çizgisinde dizme; "
  "çıktı {bounded context}'ler, süreç ve entegrasyon resmi. "
  "{As-is} süreç haritalama: adımları ve sorunları ekipçe keşfetme; çıktı BPMN'e dönüştürülecek ham süreç. "
  "{Affinity mapping}: dağınık bulguları temalara gruplama; çıktı tema listesi. "
  "{Dot voting}, {MoSCoW} ya da değer efor matrisi: önceliklendirme; çıktı öncelik sırası.")
t("BA'nın Miro teknikleri (3/3)", ["Teknik", "Amaç", "Çıktı"],
  [["Impact mapping", "Hedef → aktör → etki → çıktı", "Hedefe bağlı backlog"], ["Retrospektif (Start/Stop/Continue, 4L, Sailboat)", "Ekip iyileştirmesi", "Aksiyon maddeleri"],
   ["Wireframe / low-fi prototip", "Ekran fikrini tartışmak", "Figma/Balsamiq'e taslak"]],
  "{Impact mapping}: hedef, aktör, etki, çıktı zinciri; çıktı hedefe bağlı {backlog}. "
  "Retrospektif, yani {Start Stop Continue}, 4L ya da {Sailboat}: ekip iyileştirmesi; çıktı aksiyon maddeleri. "
  "{Wireframe} ya da {low-fi} prototip: ekran fikrini hızla tartışmak; çıktı {Figma} ya da {Balsamiq}'e aktarılacak taslak.")
m("Story mapping adımları (bayi portalı)", ["1. Aktiviteler soldan sağa: Müşteri bul → Teklif hazırla → Başvuru yap → Sonucu takip et → Sözleşme imzalat → Araç teslim et",
                                           "2. Her aktivitenin altına story'leri öncelik sırasıyla diz", "3. Yatay çizgilerle sürüm dilimleri (MVP, Sürüm 2)",
                                           "4. Boşluk ve bağımlılıkları işaretle · 5. Kartları Jira'ya aktar"],
  "{Story mapping} adımları; örnek bayi portalı taşıt kredisi. Bir: kullanıcı aktivitelerini soldan sağa yaz: müşteri bul, teklif hazırla, başvuru yap, "
  "sonucu takip et, sözleşme imzalat, araç teslim et. İki: her aktivitenin altına görevleri, yani {story}'leri dikey olarak öncelik sırasıyla diz. "
  "Üç: yatay çizgilerle sürüm dilimlerini belirle; MVP ve sürüm iki. Dört: boşlukları ve bağımlılıkları işaretle. Beş: kartları Jira'ya aktar.")
m("Etkili workshop tasarımı", ["Amaç ve beklenen çıktı net · katılımcılarda karar yetkisi", "Zaman kutusu: ısınma 5 · keşif 20 · gruplama 15 · önceliklendirme 15 · aksiyon 10 dk",
                               "Önce sessiz bireysel üretim (groupthink ↓), sonra tartışma", "Park alanı (parking lot) · 24 saat içinde Confluence'a özet"],
  "Etkili workshop tasarımı. Amaç ve beklenen çıktı net olmalı; katılımcı listesi karar yetkisini içermeli. Gündem zaman kutulu olmalı: "
  "ısınma beş dakika, keşif yirmi dakika, gruplama on beş dakika, önceliklendirme on beş dakika, aksiyon on dakika. "
  "Önce sessiz bireysel üretim, ki bu {groupthink}'i azaltır; sonra tartışma. "
  "Park alanı, yani {parking lot} ile konu dışı tartışmaları ertele. Workshop sonrası yirmi dört saat içinde özet ve aksiyonları Confluence'a aktar.")

# ───────────────────────────── İleri
m("Entegrasyonlar ve yapay zeka", ["Jira, Confluence, Azure DevOps, Teams/Slack, Figma", "REST API ve SDK: notlar → CSV",
                                   "Miro AI: kümele, özetle, story ve AC taslağı", "Sidekicks ajan · Flows çok adımlı akış",
                                   "Enterprise/beta · insan kontrolü şart"],
  "İleri seviye: entegrasyonlar. Jira: kartları çift yönlü senkron Jira iş öğelerine çevirme, durumu {board}'da görme. Confluence: {board} gömme. "
  "{Azure DevOps}; {Microsoft Teams} ya da {Slack}, toplantı içinde {board}; {Figma}, tasarım gömme; {Google} ve {Microsoft} dosyaları. "
  "REST API ve SDK ile {board} içeriğini otomatik üretme ya da dışa aktarma; örneğin workshop notlarını CSV'ye alma. "
  "Yapay zeka, yani {Miro AI}, {Sidekicks} ve {Flows}: yapışkan notları temalara kümeleme, özet çıkarma, metinden {mind map} ya da diyagram üretme, "
  "notlardan {user story} ve kabul kriteri taslağı oluşturma, araştırma bulgularını sentezleme. "
  "{Sidekicks} tuvaldeki seçili bağlamı görerek ajan gibi çalışır; {Flows} ise tekrar eden çok adımlı işleri zincirler: "
  "mülakat notları, temalar, persona, gereksinim listesi. Özelliklerin bir kısmı {Enterprise} planlara ve beta durumuna bağlıdır; "
  "çıktı her zaman insan kontrolünden geçirilmelidir.", bolum="Miro · İleri seviye")
m("Kurumsal kullanım ve resmi modele geçiş", ["SSO ve SCIM · paylaşım politikası (dış link kapalı) · misafir denetimi",
                                             "Veri yerleşimi (data residency) · sınıflandırma etiketleri", "Müşteri ve kişisel veri board'a yazılmaz; ekran görüntüleri maskelenir",
                                             "Miro keşif aracı → süreç BPMN aracına, gereksinim Jira/Confluence'a · board \"arşiv\""],
  "Kurumsal kullanım ve güvenlik: SSO ve SCIM ile kullanıcı yönetimi; {board} paylaşım politikası, şirket dışı link kapalı; misafir erişimi denetimi; "
  "veri yerleşimi, yani {data residency} seçenekleri; sınıflandırma etiketleri. "
  "Müşteri verisi ve kişisel veri {board}'lara yazılmamalıdır; ekran görüntüleri maskelenmelidir. "
  "{Miro}'dan resmi modele geçiş: {Miro} keşif ve hizalama aracıdır. Onaylanan süreç BPMN aracına, yani Visio, {Signavio} ya da {Camunda} {Modeler}'a; "
  "gereksinim de Jira ve Confluence'a taşınır. {Board}, ilgili Confluence sayfasından linklenir ve arşiv olarak işaretlenir; böylece tek doğru kaynak karışmaz.")
m("Uzaktan ve hibrit workshop ipuçları", ["Hazırlık board'unu önceden paylaş, ısınma görevi ver", "Büyük grupta alt gruplara ayrı frame",
                                         "Kamera/ses kapalı katılımcı: oylama ve yorumla katılımı ölç", "Sonuç frame'ini toplantı bitmeden birlikte oku"],
  "Uzaktan ve hibrit workshop için ileri ipuçları: hazırlık {board}'unu önceden paylaşıp ısınma görevi ver; büyük gruplarda alt gruplara ayrı {frame}'ler aç; "
  "kamera ve sesi kapalı katılımcılar için oylama ve yorumla katılımı ölç; sonuç {frame}'ini toplantı bitmeden ekiple birlikte oku.")

# ───────────────────────────── Hatalar, mülakat
m("Sık yapılan hatalar", ["Amaçsız, yapısız \"boş board\"", "Board'u tek doğru kaynak yapmak", "Kilitlenmemiş yapı: çerçeve kayar",
                          "Sesi yüksek olanın domine etmesi", "Workshop sonrası takip yok"],
  "Sık yapılan hatalar. Amaçsız, yapısız bir boş {board} ile workshop başlatmak. {Board}'u tek doğru kaynak yapmak; kararları Confluence ve Jira'ya aktarmamak. "
  "Herkesin her şeyi düzenleyebildiği kilitlenmemiş yapı: çerçeveler kayar, şablon bozulur. "
  "Sesi yüksek kişilerin fikirlerinin domine etmesi; sessiz bireysel üretim ve anonim oylama kullan. Ve workshop sonrası takip yapmamak.",
  bolum="Miro · Hatalar ve mülakat")
m("Mülakat soruları ve ipuçları", ["1. Workshop tasarımı → amaç, zaman kutusu, sessiz üretim, park alanı", "2. Story mapping, MVP → uçtan uca en ince dilim",
                                   "3. Event Storming renkleri → turuncu olay, mavi komut, sarı aktör, mor politika, pembe dış sistem",
                                   "4. Uzaktan katılım → oylama, yorum, alt grup frame'i", "5. Resmi gereksinim → Jira kartı, Confluence notu"],
  "Mülakat soruları ve bölümden ipuçları. Bir: bir gereksinim workshop'unu nasıl tasarlar ve yönetirsiniz? Amaç, zaman kutusu, sessiz üretim, park alanı. "
  "İki: {user story mapping}'i anlatın; MVP'yi nasıl belirlersiniz? MVP uçtan uca çalışan en ince dilimdir. "
  "Üç: {Event Storming} ne işe yarar, hangi renkler neyi temsil eder? Turuncu olay, mavi komut, sarı aktör, mor politika, pembe dış sistem. "
  "Dört: uzaktan workshop'ta katılımı nasıl artırırsınız? Oylama, yorum ve alt grup {frame}'leri. "
  "Beş: {Miro}'daki çıktıları resmi gereksinime nasıl dönüştürürsünüz? Jira kartları ve Confluence toplantı notu.")

# ───────────────────────────── Görsel rehber
g("Miro board'u nasıl okunur?", "g32.png",
  [([0.02, 0.08, 0.37, 0.16], "1 · Ana menü, board adı"), ([0.57, 0.08, 1.0, 0.16], "2 · Kişiler, zamanlayıcı, Share, Present"),
   ([0.02, 0.17, 0.13, 0.95], "3 · Sol araç çubuğu"), ([0.13, 0.19, 0.85, 0.8], "4 · Frame'ler"),
   ([0.85, 0.17, 1.0, 0.8], "5 · Sağ panel"), ([0.13, 0.8, 1.0, 0.92], "6 · Alt çubuk")],
  "Görsel rehber: {Miro} {board} ekran yerleşimi ve workshop {frame} düzeni; şematik. Araçlar solda, iş {frame}'ler içinde soldan sağa. "
  "Bir, sol üst: ana menü ve {board} adı. {Board}'u yeniden adlandır, kopyala, dışa aktar; PDF, görsel ya da CSV; {board} ayarları. "
  "İki, sağ üst: katılımcı avatarları, tıklayınca o kişinin ekranını takip edersin; zamanlayıcı; oylama; {Share}, davet ve bağlantı erişimi; "
  "{Present}, {frame}'leri slayt gibi sunma. "
  "Üç, sol araç çubuğu: seç, şablonlar, metin, yapışkan not, şekiller, bağlantı çizgisi, kalem, yorum, {frame}, yükleme; "
  "üç noktada uygulamalar ve entegrasyonlar, yani Jira ve diyagram kütüphaneleri. "
  "Dört, {frame}'ler: workshop'un bölümleri. Örnekte bağlam ve kurallar, sessiz fikir üretimi, grupla ve oyla; mavi nokta oy demek. "
  "{Frame}'e bırakılan her öğe {frame} ile taşınır; {Present} modunda her {frame} bir slayt olur. "
  "Beş, sağ panel: {Frames} listesi, hızlı gezinme ve sıralama; yorumlar; yapay zeka paneli. "
  "Altı, alt çubuk: yakınlaştırma, {board} haritası yani küçük önizleme, geri al ve yinele.", bolum="Miro · Görsel rehber")
g("Story map nasıl okunur?", "g33.png",
  [([0.0, 0.12, 1.0, 0.27], "Backbone: kullanıcı yolculuğu"), ([0.0, 0.27, 1.0, 0.5], "MVP dilimi"),
   ([0.0, 0.5, 1.0, 0.75], "Sürüm 2"), ([0.0, 0.75, 1.0, 0.9], "Sonra")],
  "Story map; bayi portalı, üç sürüm dilimi. Üstte kullanıcı yolculuğu, çizgiler sürüm dilimlerini ayırır. "
  "Okunuşu: en üstteki mavi kartlar kullanıcının soldan sağa yolculuğudur; bunlara {backbone} denir: müşteri bul, teklif hazırla, başvuru yap, sonucu izle, sözleşme imzalat. "
  "Her aktivitenin altındaki kartlar o aktiviteyi gerçekleştiren {story}'lerdir; üstteki daha önemlidir. "
  "MVP diliminde: araç ve fiyat gir; ödeme planı hesapla ve teklifi PDF gönder; KVKK onayı al ve başvuruyu gönder; durumu listede gör; ıslak imza randevu. "
  "Kesikli yatay çizgiler sürüm dilimleridir. Sürüm ikide: kampanya seç, kasko teklifi ekle, belge fotoğrafı yükle, kefil ekle, SMS bildirimi, e-imza. "
  "Sonra: otomatik belge okuma ve mobil uygulama. "
  "MVP çizgisinin üstündeki kartlar, yolculuğun her adımını en basit haliyle uçtan uca çalıştırır. "
  "Bir aktivitenin altı MVP'de boşsa yolculuk kopuktur; bu, {story map}'in yakaladığı en değerli hatadır.")
t("Menü ve kısayol rehberi (1/2)", ["Yapmak istediğin", "Yol"],
  [["Yeni board", "Dashboard → + New board"], ["Şablon", "Templates → story map, retrospective, event storming…"],
   ["Yapışkan not · çoklu not", "N · not seçiliyken Tab"], ["Şekil / metin / frame", "T metin · F frame · L çizgi · C yorum"],
   ["Bağlamak · kilitlemek", "Kenar noktasından sürükle · sağ tık → Lock"]],
  "Menü ve kısayol rehberi; sütunlar yapmak istediğin ve yol. Yeni {board}: {Dashboard}, artı {New board}; ya da şablondan başla. "
  "Şablon eklemek: sol araç çubuğu, {Templates}; ara: {story map}, {retrospective}, {event storming}, {customer journey}, {flowchart}. "
  "Yapışkan not: N tuşu ya da araç çubuğu, {Sticky note}; renk seçmek için nota tıkla, üst bağlam menüsü. Çoklu not: not seçiliyken {Tab}, sağa yeni not. "
  "Şekil, metin, {frame}: T metin, F {frame}, L bağlantı çizgisi, C yorum. "
  "Bağlamak: şeklin kenarındaki noktadan sürükleyip diğer şekle bırak. Kilitlemek: öğeye sağ tık, {Lock}; katılımcılar yanlışlıkla taşımasın.")
t("Menü ve kısayol rehberi (2/2)", ["Yapmak istediğin", "Yol"],
  [["Oylama · zamanlayıcı", "Voting → alan, oy sayısı, süre · Timer"], ["Herkesi topla", "Avatar → Bring everyone to me"],
   ["Notları Jira'ya", "Seç → Jira kartına dönüştür"], ["AI ile grupla", "Seç → AI simgesi → kümele / özetle"], ["Dışa aktar", "Export → PDF, görsel, CSV"]],
  "Oylama: sağ üst, {Voting}; oylanacak alanı seç, kişi başı oy sayısı, süre, {Start}. Zamanlayıcı: sağ üst, {Timer}, süre, {Start}. "
  "Herkesi bir yere toplamak: kendi avatarına tıkla, {Bring everyone to me}. "
  "Notları Jira'ya aktarmak: notları seç, bağlam menüsü, Jira kartına dönüştür; Jira entegrasyonu kurulu olmalı. "
  "Yapay zeka ile gruplamak: notları seç, bağlam menüsünde AI simgesi; temalara göre kümele ya da özetle; plana ve yönetici ayarlarına bağlı. "
  "Dışa aktarmak: ana menü, {Export}; PDF ya da görsel; tablolar ve notlar için CSV.")

# ───────────────────────────── Laboratuvar
m("Laboratuvar: hazırlık (30 dk)", ["1. Yeni board: \"Bayi portalı – story mapping\"", "2. F ile 4 frame: 1 Bağlam · 2 Yolculuk · 3 Story'ler · 4 Sürüm dilimleri",
                                    "3. Bağlam: amaç, gündem, renk efsanesi, park alanı → kilitle", "4. Yolculuk: 5 boş mavi not",
                                    "5. Share → \"Can edit\" ile davet"],
  "Laboratuvar: altmış dakikalık bir {story mapping} workshop'u hazırla ve yönet. Hazırlık, otuz dakika, workshop'tan önce. "
  "Bir: yeni {board} aç; adı bayi portalı, {story mapping}. İki: F ile dört {frame} çiz ve sırala: bir bağlam, iki yolculuk yani {backbone}, "
  "üç {story}'ler, dört sürüm dilimleri ve aksiyonlar. "
  "Üç: bağlam {frame}'ine amaç, yani MVP kapsamında anlaşmak; gündem ve süreler; renk efsanesi, yani mavi aktivite, sarı {story}, pembe soru; ve park alanı kutusu. "
  "Bu {frame}'i kilitle. Dört: yolculuk {frame}'ine beş boş mavi not koy; katılımcılar dolduracak. "
  "Beş: {Share}, katılımcıları {Can edit} ile davet et.", bolum="Miro · Laboratuvar")
t("Workshop akışı (60 dk)", ["Süre", "Adım", "Miro'da ne yapılır"],
  [["5 dk", "Açılış", "Present: bağlam frame'i"], ["10 dk", "Yolculuğu kur", "5–7 aktivite soldan sağa"],
   ["15 dk", "Story üret", "Timer 8 dk sessiz yazım + 7 dk birleştirme"], ["10 dk", "Önceliklendir", "Önem sırası + Voting 5 oy"],
   ["10 dk · 10 dk", "Dilimle · kapanış", "MVP / Sürüm 2 çizgisi · pembe sorulara sahip"]],
  "Workshop akışı, altmış dakika. Beş dakika açılış: {Present} modunda bağlam {frame}'ini göster. "
  "On dakika yolculuğu kur: birlikte beş yedi aktiviteyi soldan sağa yazıp sırala. "
  "On beş dakika {story} üret: zamanlayıcı sekiz dakika; herkes sessizce sarı notları aktivitelerin altına yazar; sonra yedi dakika okuma ve tekrarı birleştirme. "
  "On dakika önceliklendir: her aktivite sütununda notları önem sırasına göre yukarıdan aşağıya diz; {Voting} ile kişi başı beş oy. "
  "On dakika dilimle: kesikli çizgiyle MVP ve sürüm iki dilimlerini çiz; her aktivitenin MVP'de en az bir {story}'si olmalı. "
  "On dakika kapanış: pembe soru notlarını sahiplere ata, et işaretiyle yorum; bir sonraki adımı yaz. "
  "Workshop sonrası, yirmi dört saat içinde: MVP {story}'lerini Jira'ya aktar, Jira entegrasyonu ya da CSV ile; "
  "{board}'un PDF'ini ve kararları Confluence'taki toplantı notuna koy; {board}'u arşiv olarak işaretle.")

# ───────────────────────────── Uygulama paketi
t("Pano düzeni kuralları (1/2)", ["Kural", "Neden", "Firma örneği"],
  [["Numaralı frame'ler soldan sağa", "Akış kendiliğinden okunur", "00 Amaç → 01 Mevcut → 02 Sorunlar → 03 Fikirler → 04 Öncelik → 05 Sonraki"],
   ["Her renk tek anlam", "Renk değişince anlam karışır", "Sarı adım · pembe sorun · mavi soru · yeşil fikir · turuncu kural"],
   ["Renk anahtarı ilk frame'de", "Yeni gelen bakar", "00 frame'inde liste"]],
  "Miro uygulama paketi. Pano düzeni kuralları: katılımcı panoya girdiğinde nereye bakacağını otuz saniyede anlamalı. "
  "Soldan sağa numaralı {frame}'ler; akışın sırası kendiliğinden okunur. Firma örneği: sıfır sıfır amaç ve kurallar, sıfır bir mevcut durum, sıfır iki sorunlar, "
  "sıfır üç fikirler, sıfır dört önceliklendirme, sıfır beş sonraki adımlar. "
  "Her renk tek anlam; renk değişince anlamı karışır. Sarı adım, pembe sorun, mavi soru, yeşil fikir, turuncu iş kuralı. "
  "Renk anahtarı ilk {frame}'de; yeni gelen katılımcı bakar.", bolum="Miro · Uygulama paketi")
t("Pano düzeni kuralları (2/2)", ["Kural", "Neden", "Firma örneği"],
  [["Kenarda park alanı", "Konu dışı fikir kaybolmaz", "\"Kasko yenileme\" kredi workshop'unda park alanına"],
   ["Her notta tek fikir", "Gruplama ve oylama mümkün", "\"Belge eksik ve KKB yavaş\" yerine iki not"], ["Frame başlığında süre", "Zaman görünür", "02 Sorunlar · 10 dk"]],
  "Kenarda park alanı: konu dışı ama önemli fikirler kaybolmaz; kasko yenileme fikri kredi workshop'unda park alanına. "
  "Her yapışkan notta tek fikir: gruplama ve oylama mümkün olur; belge eksik ve KKB yavaş yerine iki ayrı not. "
  "{Frame} başlığında süre: zaman yönetimi görünür; sıfır iki sorunlar, on dakika.")
m("Story map: üç katman", ["1. Omurga: Başvuru gir → Belge yükle → Kararı izle → Sözleşme hazırla → Kullandırımı tamamla",
                           "2. Yürüyen iskelet: tek araçlı bireysel başvuru · kimlik ve ruhsat · karar durumu · standart sözleşme · kullandırım durumu",
                           "3. Sürüm dilimleri: kurumsal, ortak araç ve kefil, ikinci el garanti",
                           "Yanlış: omurgaya sistem bileşeni (\"Veritabanı\", \"KKB servisi\")"],
  "{Story map}'in üç katmanı. Bir, omurga, yani {backbone}: kullanıcının baştan sona yaptığı büyük adımlar, soldan sağa. "
  "Bayi portalı için: başvuru gir, belge yükle, kararı izle, sözleşme hazırla, kullandırımı tamamla. "
  "İki, yürüyen iskelet, yani {walking skeleton}: her omurga adımının altındaki en basit {story}; hepsi birlikte uçtan uca çalışan en küçük ürünü oluşturur. "
  "Örnek: bireysel müşteri için tek araçlı başvuru gir; kimlik ve ruhsat yükle; karar durumunu gör; standart sözleşmeyi yazdır; kullandırım durumunu gör. "
  "Üç, sürüm dilimleri: yatay çizgilerle ayrılan satırlar. İlk dilim iskelettir; sonrakiler kurumsal müşteri, ortak araç ve kefil, ikinci el araç garantisi gibi zenginleştirmelerdir. "
  "Yanlış kullanım: omurgaya sistem bileşenlerini yazmak, örneğin veritabanı ya da KKB servisi. "
  "Omurga kullanıcının diliyle yazılır; sistem bileşenleri {story}'lerin teknik notlarına gider.")
t("DFD: KVKK için", ["Sembol", "Anlamı", "Firma örneği"],
  [["Dikdörtgen", "Dış varlık", "Müşteri, Bayi, KKB, Sigorta"], ["Yuvarlak köşeli kutu", "Süreç (veriyi dönüştürür)", "Başvuruyu değerlendir"],
   ["Açık uçlu dikdörtgen", "Veri deposu", "Başvuru veritabanı, Belge arşivi"], ["Etiketli ok", "Taşınan veri", "\"TCKN, gelir bilgisi\" → KKB"]],
  "Veri akış diyagramı, DFD, KVKK için. Dikdörtgen dış varlıktır: müşteri, bayi, KKB, sigorta şirketi. "
  "Yuvarlak köşeli kutu süreçtir, veriyi dönüştürür: başvuruyu değerlendir. Açık uçlu dikdörtgen veri deposudur: başvuru veritabanı, belge arşivi. "
  "Etiketli ok taşınan veridir: TCKN ve gelir bilgisi KKB'ye.")
dikkat("DFD seviyeleri ve kurallar", "Gane–Sarson (Yourdon'da süreç daire) · Seviye 0 tek süreç → Seviye 1: 4–6 alt süreç · ok etiketi veri adı · depo → depo ok yok · dış varlık → dış varlık ok yok",
       "Seviyeler: tablo {Gane-Sarson} notasyonunu kullanıyor; {Yourdon} notasyonunda süreç dairedir. Seviye sıfır, yani bağlam, tüm sistemi tek süreç olarak gösterir. "
       "Seviye bir bu süreci dört altı alt sürece açar. Her seviyede okların etiketi verinin adıdır, eylem değil. "
       "Kural: bir veri deposundan başka bir veri deposuna doğrudan ok çizilmez; araya veriyi taşıyan süreç konur. "
       "Dış varlıktan dış varlığa da ok çizilmez; bu iletişim senin sisteminin dışındadır.")
m("Workshop çıktısını taşımak", ["1. Oylananları bir frame'e topla", "2. Story kalıbına çevir → Jira kartı (ya da elle, numarayı nota yaz)",
                                 "3. Frame frame Export → Confluence toplantı notu + pano linki", "4. Kararlar, açık sorular, sahipler"],
  "Workshop çıktısını taşımak. Bir: oylama sonrası seçilen yapışkan notları bir {frame}'e topla. "
  "İki: her notu {story} kalıbına çevir; {Miro}'nun Jira entegrasyonu bağlıysa notu Jira kartına dönüştür, değilse Jira'da elle oluştur ve kart numarasını nota yaz. "
  "Üç: panoyu {frame} {frame} dışa aktar, {Export}, görsel ya da PDF; Confluence'taki toplantı notu sayfasına ekle ve panonun bağlantısını da koy. "
  "Dört: toplantı notu sayfasına kararları, açık soruları ve sahiplerini yaz.")
m("Bağımsız görev: hasar muvafakati workshop'u", ["45 dk uzaktan · kredi operasyon, tahsilat, sigorta operasyonu, bayi",
                                                 "1. 5–6 numaralı frame, başlıkta süre, toplam ≤ 45 dk", "2. Renk anahtarı ve park alanı",
                                                 "3. Mevcut durum: \"taksitler güncel olmalı\" turuncu not", "4. Hangi çıktı hangi araca?"],
  "Bağımsız görev: hasar muvafakati workshop'u. Süreci iyileştirmek için kırk beş dakikalık uzaktan bir workshop panosu hazırla. "
  "Katılımcılar: kredi operasyon, tahsilat, sigorta operasyonu ve bir bayi temsilcisi. "
  "Bir: beş altı numaralı {frame}; her birinin başlığında süre; toplam kırk beş dakikayı geçmesin. İki: renk anahtarı ve park alanı. "
  "Üç: mevcut durum {frame}'ine Firma kuralını, taksitler güncel olmalı, turuncu notla koy. Dört: workshop sonunda hangi çıktıların hangi araca gideceğini yaz.",
  bolum="Miro · Bağımsız görev ve sorun giderme")
t("Sorun giderme", ["Belirti", "Olası neden", "Çözüm"],
  [["Not eklenemiyor", "İzin \"can view\"", "Share → \"can edit\""], ["Pano yavaş", "Büyük görsel, eski frame", "Arşiv panosuna taşı"],
   ["Katılımcılar kayboluyor", "Odak yok", "Bring everyone to me"], ["Not anlamı karıştı", "Renk kuralsız", "Renk anahtarını 1 dk anlat"],
   ["Sonuç bulunamadı", "Çıktı Miro'da kaldı", "Aynı gün Confluence + Jira"]],
  "Sorun giderme. Katılımcılar not ekleyemiyorsa: paylaşım izni {can view}; {Share}'den izni {can edit} yap ya da katılımcıları panoya davet et. "
  "Pano açılışta yavaşsa: çok sayıda yüksek çözünürlüklü görsel ya da eski {frame} var; eski {frame}'leri ayrı bir arşiv panosuna taşı. "
  "Katılımcılar kayboluyor, farklı yerlere bakıyorsa: odak noktası yok; kolaylaştırıcı olarak herkesi kendi görünümüne çağır, {Bring everyone to me}. "
  "Notların anlamı karıştıysa: renkler kuralsız kullanılmış; sıfır sıfır {frame}'indeki renk anahtarını başta bir dakikada anlat. "
  "Workshop sonrası kimse sonucu bulamadıysa: çıktı {Miro}'da kalmış; aynı gün Confluence notu ve Jira kartları oluştur.")
soru("Bilgi kontrolü 1/5", "Story map'in omurgasına ne yazılır?", ["Kullanıcının büyük adımları", "Sistem bileşenleri", "Sprint numaraları", "Ekip üyeleri"], 0,
     "Beş soruluk bilgi kontrolü. Birinci soru: {story map}'in omurgasına ne yazılır? A, kullanıcının büyük adımları. B, sistem bileşenleri. C, sprint numaraları. D, ekip üyeleri.",
     "Doğru cevap A.", bolum="Miro · Bilgi kontrolü ve çözümler")
soru("Bilgi kontrolü 2/5", "DFD'de iki veri deposu arasında doğrudan ok neden yanlış?",
     ["Okun rengi yanlış olur", "Veriyi taşıyan bir süreç gösterilmeli", "Depolar birleştirilmeli", "Ok yerine çizgi kullanılır"], 1,
     "İkinci soru: DFD'de iki veri deposu arasında doğrudan ok neden yanlıştır? A, okun rengi yanlış olur. B, veriyi taşıyan bir süreç gösterilmelidir. "
     "C, depolar birleştirilmelidir. D, ok yerine çizgi kullanılır.",
     "Doğru cevap B.")
soru("Bilgi kontrolü 3/5", "\"Belge eksik ve KKB yavaş\" yazılı not neden sorunlu?",
     ["Fazla uzun", "Yanlış renkte", "İki fikir tek notta; ayrı oylanamaz", "İngilizce değil"], 2,
     "Üçüncü soru: belge eksik ve KKB yavaş yazılı bir yapışkan not neden sorunludur? A, fazla uzun. B, yanlış renkte. C, iki fikir tek notta; ayrı oylanamaz. D, İngilizce değil.",
     "Doğru cevap C.")
soru("Bilgi kontrolü 4/5", "Yürüyen iskelet neyi ifade eder?", ["Tüm özellikler", "Uçtan uca çalışan en küçük story seti", "Teknik mimari", "Test planı"], 1,
     "Dördüncü soru: yürüyen iskelet neyi ifade eder? A, tüm özellikler. B, uçtan uca çalışan en küçük {story} seti. C, teknik mimari. D, test planı.",
     "Doğru cevap B.")
soru("Bilgi kontrolü 5/5", "Konu dışı ama değerli bir fikir geldi. Ne yaparsın?", ["Hemen tartışırım", "Yok sayarım", "Toplantıyı uzatırım", "Park alanına koyarım"], 3,
     "Beşinci soru: konu dışı ama değerli bir fikir geldi. Ne yaparsın? A, hemen tartışırım. B, yok sayarım. C, toplantıyı uzatırım. D, park alanına koyarım.",
     "Doğru cevap D: park alanı.")
m("Hızlı başvuru: workshop öncesi", ["Amaç tek cümle, ilk frame'de", "Numaralı frame'ler, başlıkta süre", "Toplam süre takvimden 3–5 dk kısa",
                                     "Renk anahtarı, park alanı, izin testi", "Referans frame: P01, U04", "Çıktı yeri: Jira, Confluence"],
  "Hızlı başvuru: workshop öncesi kontrol listesi. Amaç tek cümle ve ilk {frame}'de. {Frame}'ler numaralı, başlıklarında süre var; "
  "toplam süre takvimdeki süreden üç beş dakika kısa. Renk anahtarı ve park alanı hazır. Katılımcıların düzenleme izni test edildi. "
  "Firma kuralları ve mevcut diyagramlar, yani P01, U04 ve diğerleri, referans {frame}'inde. "
  "Çıktıların gideceği yer belli: Jira projesi ve Confluence sayfası.")
t("Çözüm: örnek pano", ["Frame", "Süre", "İçerik"],
  [["00 Amaç ve kurallar", "3 dk", "Muvafakat süresini kısaltmak · renk anahtarı"], ["01 Mevcut durum", "10 dk", "Sarı adımlar · turuncu kural"],
   ["02 Sorunlar · 03 Fikirler", "8 dk · 10 dk", "Pembe notlar · yeşil notlar"], ["04 Önceliklendirme", "7 dk", "Etki/efor, kişi başı 3 oy"],
   ["05 Sonraki adımlar · park alanı", "4 dk · —", "Sahip ve tarih · konu dışı"]],
  "Bağımsız görevin örnek panosu. Sıfır sıfır amaç ve kurallar, üç dakika: sigortadan muvafakat talebinin gelmesinden yazının gönderilmesine kadar geçen süreyi kısaltmak; renk anahtarı. "
  "Sıfır bir mevcut durum, on dakika: sarı notlarla adımlar, turuncu notla taksitler güncel olmalı kuralı. "
  "Sıfır iki sorunlar, sekiz dakika: pembe notlar, her biri ilgili adımın altına. Sıfır üç fikirler, on dakika: yeşil notlar. "
  "Sıfır dört önceliklendirme, yedi dakika: etki efor matrisi, her kişiye üç oy. Sıfır beş sonraki adımlar, dört dakika: sahip ve tarih. "
  "Park alanı: konu dışı fikirler. Toplam kırk iki dakika; üç dakika tampon. "
  "Çıktılar: seçilen fikirler Jira'ya {story} olarak; kararlar ve açık sorular Confluence'ta kırk toplantı notları altına.")
m("Bu videoda neler gördük?", ["Temel araçlar, board düzeni, kolaylaştırıcı özellikleri", "On teknik, story mapping, workshop tasarımı",
                               "Entegrasyon, yapay zeka, güvenlik, resmi modele geçiş", "Ekran, story map okuma, menüler, laboratuvar",
                               "Pano kuralları, üç katman, DFD, çıktıyı taşımak"],
  "Toparlayalım. Temel araçları, {board} düzenini ve kolaylaştırıcı özelliklerini gördük. On tekniği, {story mapping}'i ve workshop tasarımını öğrendik. "
  "Entegrasyon, yapay zeka, güvenlik ve resmi modele geçişe baktık. Ekranı, {story map} okumayı, menüleri ve laboratuvarı çalıştık. "
  "Pano kuralları, üç katman, DFD ve çıktıyı taşımakla bitirdik. Bir sonraki videoda Microsoft Visio ile resmi diyagramlar çizeceğiz.", ton="sakin")

kaydet(__file__, {
    "baslik": "Business Analyst Teknik Rehberi · 12: Miro",
    "alt_baslik": "Workshop panosu · story mapping · Event Storming · DFD · çıktıyı taşımak",
    "kapanis": "Sıradaki video: Visio",
    "tema": 12,
    "youtube_baslik": "Business Analyst Teknik Rehberi 12/14: Miro (workshop, story map, Event Storming)",
    "etiketler": ["business analyst", "Miro", "workshop", "story mapping", "Event Storming", "iş analisti"],
}, {"MVP": "em vi pi", "DFD": "di ef di", "SDK": "es di key", "AWS": "ey dabılyu es", "AI": "ey ay", "4L": "dört el", "AC": "ey si",
    "miro.com": "miro nokta kom", "MoSCoW": "moskov"})
