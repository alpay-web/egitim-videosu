#!/usr/bin/env python3
"""BA Teknik Rehberi · Video 13: Microsoft Visio. Belge satır 3733–3954."""
from ortak import m, t, dikkat, g, soru, kaydet

m("Microsoft Visio", ["Microsoft'un profesyonel diyagram aracı", "Microsoft 365 ekosistemiyle yaygın", "Süreç, organizasyon, ağ, UML/ER diyagramları",
                      "Dosya formatı .vsdx (eski .vsd yalnız ücretli planlarda)"],
  "{Visio}, Microsoft'un profesyonel diyagram aracıdır. Finans kurumlarında {Microsoft 365} ekosistemiyle birlikte yaygın olarak kullanılır; "
  "süreç, organizasyon, ağ ve UML ya da ER diyagramları için kurumsal standart olabilir. "
  "Dosya formatı nokta {vsdx}'tir; eski nokta {vsd} sadece ücretli planlarda açılır.",
  bolum="Visio: giriş ve hedefler", kanca="Miro'da keşfettiğimizi şimdi resmi diyagrama çeviriyoruz.", ton="merakli")
m("Bu bölümün hedefleri", ["Cross-Functional Flowchart ve BPMN şablonlarıyla Firma süreçleri", "Check Diagram + Issues: neyi yakalar, neyi yakalamaz",
                           "Shape Data (sahip, süre, sistem) → diyagram veri kaynağı olur", "Lisans yoksa aynı iş draw.io'da"],
  "Bu bölümü bitirdiğinde şunları yapabileceksin. Bir: {Visio}'da {Cross-Functional Flowchart} ve BPMN şablonlarıyla Firma süreçlerini çizmek. "
  "İki: {Check Diagram} ile diyagramı doğrulayıp {Issues} penceresindeki hataları düzeltmek ve bu kontrolün neyi yakalamadığını bilmek. "
  "Üç: şekillere {Shape Data} alanları, yani sahip, süre ve sistem ekleyip diyagramı bir veri kaynağına dönüştürmek. "
  "Dört: {Visio} lisansın yoksa aynı işi {draw.io}'da yapmak.")
t("Başlamadan önce gerekenler", ["Gereken", "Nereden", "Hazır olduğunu nasıl anlarsın"],
  [["Visio masaüstü (Professional / Plan 2)", "Kurumun Microsoft 365 lisansı", "Şeritte Process sekmesi"],
   ["Lisans yoksa draw.io", "app.diagrams.net", "More Shapes → BPMN General"], ["Swimlane ve BPMN kavramları", "Process Diagramming, BPMN bölümleri", "Pool, lane, gateway farkı"]],
  "Başlamadan önce tablo üç sütun: gereken, nereden ve hazır olduğunu nasıl anlarsın. "
  "{Visio} masaüstü, {Professional} ya da {Visio Plan 2}: kurumun {Microsoft 365} lisansı; şeritte {Process} sekmesi görünüyorsa tamam. "
  "Lisans yoksa ücretsiz {draw.io}: {app.diagrams.net}; artı {More Shapes}, {BPMN General} işaretlenebiliyorsa tamam. "
  "{Swimlane} ve BPMN kavramları: bu rehberin {Process Diagramming} ve BPMN bölümleri; {pool}, {lane} ve {gateway} farkını söyleyebiliyorsan hazırsın.")

# ───────────────────────────── Temel
t("Sürümler ve lisanslar (1/2)", ["Seçenek", "Uygulama", "Kapsam"],
  [["Visio in Microsoft 365", "Hafif web uygulaması", "Temel akış, blok, organizasyon; görüntüleme"],
   ["Visio Plan 1", "Web uygulaması", "Cross-functional, BPMN, UML, ER; katman, shape data, Power BI"]],
  "Temel seviye: sürümler ve lisanslar, güncel yapı. Tablo seçenek, uygulama ve kapsam. "
  "{Visio in Microsoft 365}: hafif web uygulaması; {Microsoft 365} ticari planlarına dahil; temel akış şeması, blok ve organizasyon diyagramları; "
  "görüntüleme ve temel düzenleme. "
  "{Visio Plan 1}: web uygulaması; daha geniş şablon ve şekil seti; {cross-functional flowchart}, BPMN, UML, ER; katmanlar, kapsayıcılar, "
  "{shape data} ve {Power BI} entegrasyonu.", bolum="Visio · Temel seviye")
t("Sürümler ve lisanslar (2/2)", ["Seçenek", "Uygulama", "Kapsam"],
  [["Visio Plan 2", "Web + masaüstü", "Plan 1 + çevrimdışı, veri bağlantısı, kural doğrulama"],
   ["Visio Standard / Professional 2024", "Kalıcı lisanslı masaüstü", "Abonelik istemeyen kurumlar"]],
  "{Visio Plan 2}: web artı masaüstü uygulaması; {Plan 1}'in tamamı artı masaüstü, çevrimdışı çalışma, gelişmiş şablonlar, "
  "veri bağlantılı diyagramlar ve kural doğrulama. "
  "{Visio Standard} ya da {Professional} 2024: kalıcı lisanslı masaüstü; abonelik istemeyen kurumlar için. "
  "Lisans kapsamı değişebilir; kurumunuzda hangi planın olduğunu IT'den teyit edin.")
m("Temel kavramlar", ["Stencil: şekil kütüphanesi · master shape", "Template: diyagram türü + stencil seti",
                      "Connector: dinamik bağlayıcı, şekil taşınınca yeniden yönlenir", "Glue: yapışma noktaları", "Sayfa, arka plan sayfası, tema"],
  "Temel kavramlar. {Stencil}, şekil kütüphanesi; {master shape}; {template}, yani önceden ayarlanmış diyagram türü ve {stencil} seti; "
  "{connector}, yani dinamik bağlayıcı: şekil taşınınca kendini yeniden yönlendirir; {glue}, yani yapışma noktaları; "
  "sayfa ve arka plan sayfası; ve tema.")
m("Temel kullanım ipuçları", ["Mavi oklar (AutoConnect): sonraki adım tek tıkla", "Ctrl + sürükle: kopyala",
                              "Position → Auto Align & Space · Format Painter · F2 metin", "Ctrl + Shift + sol tık yakınlaş · sağ tık uzaklaş (ya da Ctrl + tekerlek)"],
  "Temel kullanım ipuçları: şekil üzerindeki mavi oklarla, yani {AutoConnect} ile sonraki adımı tek tıkla ekleme; "
  "{Ctrl} ile sürükleyerek kopyalama; hizalama ve dağıtma: {Align}, {Position}, {Auto Align and Space}; {Format Painter}; "
  "F2 ile metin düzenleme; {Ctrl} artı {Shift} artı sol tık ile yakınlaştırma, {Ctrl} artı {Shift} artı sağ tık ile uzaklaştırma; "
  "ya da {Ctrl} artı fare tekerleği.")

# ───────────────────────────── Orta
m("Cross-Functional Flowchart (swimlane)", ["Lane ve phase (dikey aşama ayırıcı) ekle", "Lane başlığı = rol adı",
                                           "Lane içine bırakılan şekil otomatik ait olur", "As-is ve to-be ayrı sayfa, aynı lane sırası"],
  "Orta seviye. {Cross-Functional Flowchart}, yani {swimlane}: {lane} ve {phase}, yani dikey aşama ayırıcı ekleme; "
  "{lane} başlıklarını rol adıyla doldurma; şekilleri {lane} içine bırakınca otomatik ait olma. "
  "{As-is} ve {to-be} için ayrı sayfalar; karşılaştırma için aynı {lane} sırası.", bolum="Visio · Orta seviye")
m("BPMN şablonu ve doğrulama", ["BPMN Basic Shapes: event, activity, gateway, pool/lane, message flow",
                                "Plan 2 masaüstü: Process → Check Diagram", "Bağlantısız şekil, başlangıçsız akış, pool'lar arası sequence flow",
                                "Create from Selection: alt süreci yeni sayfaya taşı, linkle"],
  "BPMN şablonu: {BPMN Basic Shapes} {stencil}'i ile {event}, {activity}, {gateway}, {pool} ve {lane}, {message flow}. "
  "{Plan 2} masaüstünde {Process} sekmesindeki {Check Diagram} ile BPMN kural doğrulaması yapılır: bağlantısız şekiller, başlangıcı olmayan akış, "
  "{pool}'lar arası hatalı {sequence flow} gibi hatalar listelenir. "
  "Alt süreçler için {Create from Selection} ile seçili adımları yeni sayfaya taşıyıp link verme.")
dikkat("Visio çizim aracıdır, modelleme aracı değil", "UML 2.5 şablonları: class, use case, sequence, activity, state, component, deployment · Crow's Foot ER · tutarlılık elle sağlanır",
       "UML ve veri tabanı diyagramları: UML 2.5 şablonları, yani {class}, {use case}, {sequence}, {activity}, {state}, {component}, {deployment}; "
       "ve {Crow's Foot} notasyonlu ER diyagramı. Dikkat: {Visio} modelleme aracı değil, çizim aracıdır. "
       "Tutarlılık, yani aynı sınıfın her diyagramda aynı olması, elle sağlanır.")
m("Katmanlar, kapsayıcılar, çağrı notları", ["Layers: \"Sistem adımları\", \"Kontroller\", \"KPI'lar\" aç/kapa",
                                            "Denetim sunumunda yalnız kontrol katmanı", "Container: ilgili adımları grupla, başlıkla", "Callout: çağrı notu"],
  "Katmanlar, yani {layers}; kapsayıcılar, yani {containers}; çağrı notları, yani {callouts}. Katmanlarla aynı diyagramda farklı görünümler açılıp kapatılabilir; "
  "örneğin sistem adımları, kontroller, KPI'lar. Denetim sunumunda sadece kontrol katmanını göstermek gibi. "
  "{Container} ile ilgili adımları gruplayıp başlıklandırma.")
m("Shape Data (şekil verisi)", ["Adım ID · Sorumlu · Ortalama süre", "Sistem · Kontrol ID · Risk seviyesi",
                                "Review → Shape Reports · Excel'e aktar", "Diyagram = süreç envanterinin veri kaynağı"],
  "{Shape Data}, yani şekil verisi: her şekle özellik ekleme. Adım ID, sorumlu, ortalama süre, sistem, kontrol ID, risk seviyesi. "
  "Bu veriler raporlanabilir, {Review}, {Shape Reports}; ve Excel'e aktarılabilir. Böylece diyagram, süreç envanterinin veri kaynağı olur.")

# ───────────────────────────── İleri
m("Data Visualizer: Excel'den diyagram", ["Excel'deki adımlar → otomatik cross-functional flowchart ya da organizasyon şeması",
                                          "Sütunlar: Process Step ID, Description, Next Step ID, Connector Label, Shape Type, Function, Phase",
                                          "Excel güncellenince diyagram yenilenir", "Büyük süreç envanterinde büyük zaman kazancı"],
  "İleri seviye. {Data Visualizer}, yani Excel'den diyagram üretme. Excel tablosundaki adımlarla otomatik {cross-functional flowchart} "
  "ya da organizasyon şeması oluşturulur. Tablonun sütunları: {Process Step ID}, {Process Step Description}, {Next Step ID}, {Connector Label}, "
  "{Shape Type}, {Function}, {Phase}; yani adım ID, açıklama, sonraki adım ID, bağlantı etiketi, şekil tipi, fonksiyon ya da {lane}, ve aşama. "
  "Excel güncellenince diyagram yenilenir. Büyük süreç envanterlerinde çok zaman kazandırır.", bolum="Visio · İleri seviye")
t("Data Visualizer örnek tablosu (1/2)", ["Adım", "Açıklama → sonraki", "Şekil · lane · aşama"],
  [["P1", "Başvuru alınır → P2", "Start · Bayi · Başvuru"], ["P2", "KKB sorgusu yapılır → P3", "Process · Sistem · Değerlendirme"],
   ["P3", "Skor yeterli mi? → P4 Evet, P5 Hayır", "Decision · Sistem · Değerlendirme"]],
  "Örnek tablo. P1: başvuru alınır; sonraki adım P2; şekil tipi {Start}; fonksiyon bayi; aşama başvuru. "
  "P2: KKB sorgusu yapılır; sonraki P3; {Process}; sistem; değerlendirme. "
  "P3: skor yeterli mi; sonraki P4 ve P5; bağlantı etiketleri evet ve hayır; {Decision}; sistem; değerlendirme.")
t("Data Visualizer örnek tablosu (2/2)", ["Adım", "Açıklama → sonraki", "Şekil · lane · aşama"],
  [["P4", "Otomatik onay → P6", "Process · Sistem · Karar"], ["P5", "Manuel inceleme → P6", "Process · Kredi Tahsis · Karar"],
   ["P6", "Sonuç bildirilir", "End · Bayi · Bildirim"]],
  "P4: otomatik onay; sonraki P6; {Process}; sistem; karar. P5: manuel inceleme; sonraki P6; {Process}; kredi tahsis; karar. "
  "P6: sonuç bildirilir; sonraki adım yok; {End}; bayi; bildirim.")
m("Veri bağlantısı, Power BI, Power Automate", ["Link Data to Shapes: Excel, SQL Server, SharePoint listesi",
                                                "Data Graphics: SLA'i aşan adım kırmızı, kuyruk sayısı çubuk", "Periyodik yenileme → canlı operasyon haritası",
                                                "Power BI'a göm, KPI ile renklendir", "Masaüstünde akış → Power Automate (sürümde kontrol et)"],
  "{Data Graphics} ve veri bağlantısı, yani {Link Data to Shapes}: şekilleri Excel, {SQL Server}, {SharePoint} listesi gibi kaynaklara bağlayıp "
  "değerleri ikon, renk ve çubuklarla gösterme; örneğin SLA'i aşan adım kırmızı, kuyruk sayısı çubuk. "
  "Veriler periyodik olarak yenilenebilir; canlı operasyon haritası oluşturulabilir. "
  "{Power BI} ve {Power Automate}: {Visio} diyagramı {Power BI} raporuna gömülüp verilerle eşleştirilebilir; süreç adımlarını KPI'larla renklendirme. "
  "Masaüstünde {Visio} akışı {Power Automate} akışına dönüştürülebilir; özellik desteğini sürümünüzde kontrol edin.")
m("Standart, iş birliği ve yönetişim", ["Kurumsal .vssx stencil ve .vstx şablon", "ShapeSheet: formül, koşullu biçim · VBA / Office JavaScript API",
                                       "OneDrive/SharePoint eş zamanlı düzenleme, yorum, versiyon geçmişi", "Teams sekmesi · Confluence'a gömme · PDF/SVG",
                                       "Onaylı diyagram: kontrollü SharePoint kütüphanesi, sürüm ve onay meta verisi"],
  "Şablon ve {stencil} standardı: kurumsal renk, yazı tipi ve şekil seti içeren özel nokta {vssx} {stencil} ve nokta {vstx} şablon hazırlanarak "
  "tüm süreç ekiplerine dağıtılır. {ShapeSheet} ile şekillere formül, koşullu biçim ve davranış eklenebilir; ileri düzey. "
  "VBA ya da {Office JavaScript API} ile toplu işlemler otomatikleştirilebilir. "
  "İş birliği ve yönetişim: {OneDrive} ya da {SharePoint} üzerinde eş zamanlı düzenleme ve yorum, versiyon geçmişi; {Teams}'de sekme olarak paylaşım; "
  "Confluence'a gömme, eklentiyle; ya da PDF veya SVG dışa aktarımı. "
  "Onaylı süreç diyagramları kontrol edilen bir {SharePoint} kütüphanesinde, sürüm numarası ve onay meta verisiyle tutulur.")
m("Alternatiflerle karşılaştırma", ["draw.io / diagrams.net: ücretsiz, Confluence entegre", "Lucidchart: bulut iş birliği",
                                    "Signavio / ARIS / Bizagi: süreç yönetimi, simülasyon, repository", "Enterprise Architect / Visual Paradigm: gerçek UML modelleme",
                                    "Visio: Microsoft ekosistemi + veri · zayıf: model deposu, kurallar"],
  "Alternatiflerle karşılaştırma: {draw.io} ya da {diagrams.net}, ücretsiz, Confluence entegre; {Lucidchart}, bulut iş birliği; "
  "{Signavio}, {ARIS} ya da {Bizagi}: süreç yönetimi, simülasyon, {repository}; {Enterprise Architect} ya da {Visual Paradigm}: "
  "gerçek UML modelleme ve izlenebilirlik. {Visio}'nun gücü Microsoft ekosistemi ve veri bağlantılarıdır; "
  "zayıf tarafı model deposu ve kuralların sınırlı olmasıdır.")

# ───────────────────────────── Hatalar, mülakat
m("Sık yapılan hatalar", ["Bağlayıcıyı yapıştırmamak (glue yok): oklar kopar", "Basic Flowchart ile \"BPMN gibi görünen\" diyagram",
                          "Tüm süreç tek sayfada, alt süreç sayfası yok", "Shape data yok: yalnız görsel", "Lisans farkı: web sürümünde düzenleyememe"],
  "Sık yapılan hatalar. Bağlayıcıları şekillere yapıştırmamak, yani {glue} yok; şekil taşınınca oklar kopar. "
  "{Basic Flowchart} şekilleriyle BPMN gibi görünen ama standart dışı diyagram çizmek. Tüm süreci tek sayfaya sığdırmak, alt süreç sayfaları kullanmamak. "
  "{Shape data} kullanmamak; diyagramı sadece görsel olarak bırakmak. "
  "Lisans farkını bilmemek: paydaşın web sürümünde diyagramı düzenleyememesi.", bolum="Visio · Hatalar ve mülakat")
m("Mülakat soruları", ["1. Cross-functional flowchart nasıl, nelere dikkat?", "2. Excel envanterinden otomatik diyagram?",
                       "3. Katman ve shape data hangi amaçla?", "4. Visio, draw.io, BPM aracı: nasıl seçim?", "5. BPMN uygunluğu nasıl kontrol?"],
  "Mülakat soruları. Bir: {Visio}'da {cross-functional flowchart} nasıl oluşturulur ve nelere dikkat edersiniz? "
  "İki: Excel'deki süreç envanterinden diyagramı nasıl otomatik üretirsiniz? Cevap: {Data Visualizer}. "
  "Üç: katman ve {shape data}'yı hangi amaçlarla kullanırsınız? Dört: {Visio}, {draw.io} ve gerçek bir BPM aracı arasında nasıl seçim yaparsınız? "
  "Beş: bir diyagramın BPMN kurallarına uygunluğunu nasıl kontrol edersiniz? {Check Diagram} ve elle hata kataloğu.")

# ───────────────────────────── Görsel rehber
g("Visio ekranı nasıl okunur?", "g34.png",
  [([0.03, 0.09, 0.98, 0.16], "1 · Sekmeler"), ([0.03, 0.16, 0.98, 0.28], "2 · Şerit"), ([0.03, 0.29, 0.25, 0.92], "3 · Shapes paneli"),
   ([0.26, 0.29, 0.75, 0.92], "4 · Çizim sayfası"), ([0.76, 0.29, 0.98, 0.92], "5 · Shape Data"), ([0.02, 0.92, 0.6, 0.98], "6 · Alt çubuk")],
  "Görsel rehber: {Visio} masaüstü ekran yerleşimi; şematik, numaralı bölgeler. Üstte şerit, solda şekiller, sağda şekil verisi. Tablo numara, bölge ve ne yaparsın. "
  "Bir, sekmeler: komut grupları; {File}, {Home}, {Insert}, {Draw}, {Design}, {Data}, {Process}, {Review}, {View}. "
  "{Cross-Functional Flowchart} sekmesi yalnızca {swimlane} diyagramı açıkken görünür; bağlamsal sekme. "
  "İki, şerit, yani {ribbon}: seçili sekmenin komutları; {Home} sekmesi açıkken {Clipboard}, {Font}, {Paragraph}, {Tools}, {Shape Styles}, {Arrange}, {Editing}. "
  "{Home}, {Tools}'taki {Connector} aracı bağlayıcı çizer; {Arrange} hizalama ve dağıtma yapar. "
  "Üç, {Shapes} paneli: şablonun {stencil}'leri; {Search shapes} ile ara, {More Shapes} ile başka {stencil} aç, örneğin BPMN, UML. "
  "Örnekte {CFF Shapes}, {Basic Flowchart}, {BPMN Basic Shapes}; şekli sürükle bırak. "
  "Dört, çizim sayfası: şekilleri sürükle bırak. Şeklin üzerine gelince çıkan mavi oklar, {AutoConnect}, sonraki şekli bağlı olarak ekler. "
  "Bağlayıcı ucunun yeşil olması şekle yapıştığını gösterir, yani {glue}. Örnekte bayi, sistem, tahsis şeritleri; başvuru gir ve kontrol. "
  "Beş, {Shape Data} penceresi: seçili şeklin veri alanları; örnekte adım ID P1, sorumlu bayi, süre on beş dakika, sistem Portal, kontrol ID K yedi. "
  "{Data}, {Shape Data Window} ile açılır; raporlar ve veri grafikleri bu alanlardan beslenir. "
  "Altı, alt çubuk: sayfa sekmeleri, {Page} bir ve artı; {as-is} ve {to-be} için ayrı sayfa; yakınlaştırma; {Fit to window}.",
  bolum="Visio · Görsel rehber")
t("Menü rehberi (1/3)", ["Sekme", "BA'nın en çok kullandığı komutlar"],
  [["File", "New → Cross-Functional Flowchart, BPMN Diagram, UML Class, Database Crow's Foot, Data Visualizer · Export → PDF/PNG/SVG"],
   ["Home", "Pointer Ctrl+1 · Connector Ctrl+3 · Text Ctrl+2 · Align · Auto Align & Space · Group Ctrl+G · Layers"],
   ["Insert", "Pages · Container · Callout · Connectors · Hyperlink Ctrl+K · Text box"]],
  "Sekme sekme menü rehberi; {Visio Plan 2} masaüstü, web sürümünde bazı komutlar yoktur. Tablo sekme ve BA'nın en çok kullandığı komutlar. "
  "{File}: {New}, şablon ara: {Cross-Functional Flowchart}, {BPMN Diagram}, {UML Class}, {Database Crow's Foot}, {Data Visualizer}. {Export}: PDF, PNG, SVG. "
  "{Home}: {Tools}: {Pointer}, {Ctrl} bir; {Connector}, {Ctrl} üç; {Text}, {Ctrl} iki. {Arrange}: {Align}, {Position}, {Auto Align and Space}, "
  "{Group}, {Ctrl} G. {Editing}: {Layers}, {Layer Properties}. "
  "{Insert}: {Pages}, yeni sayfa; {Container}, adımları çerçeveleme; {Callout}, not balonu; {Connectors}; {Hyperlink}, {Ctrl} K; {Text box}.")
t("Menü rehberi (2/3)", ["Sekme", "BA'nın en çok kullandığı komutlar"],
  [["Design", "Themes, Variants · Backgrounds · Borders & Titles · Re-Layout Page · Connectors → Right-Angle"],
   ["Data", "Link Data to Shapes · Data Graphics · Shape Data Window · Define Shape Data"],
   ["Process", "Create from Selection · Check Diagram · Rules to Check → BPMN"]],
  "{Design}: {Themes} ve {Variants}, kurumsal renk; {Backgrounds}; {Borders and Titles}; {Re-Layout Page}, otomatik yerleşim; {Connectors}, {Right-Angle}. "
  "{Data}: {Link Data to Shapes}, Excel, SQL ya da {SharePoint} verisi bağla; {Data Graphics}, veriye göre ikon ve renk; {Shape Data Window}; {Define Shape Data}. "
  "{Process}: {Subprocess}, {Create from Selection}, seçili adımları alt sürece taşır ve linkler; {Check Diagram}, BPMN ve akış kurallarını doğrular; "
  "{Rules to Check}, BPMN.")
t("Menü rehberi (3/3)", ["Sekme", "BA'nın en çok kullandığı komutlar"],
  [["Review", "New Comment · Shape Reports (Excel raporu)"], ["View", "Ruler, Grid, Guides · Task Panes → Shape Data, Size & Position, Pan & Zoom"],
   ["Cross-Functional Flowchart", "Swimlane · Separator (aşama) · Orientation"]],
  "{Review}: {Comments}, {New Comment}; {Shape Reports}, {shape data}'dan Excel raporu. "
  "{View}: {Ruler}, {Grid}, {Guides}; {Task Panes}: {Shape Data}, {Size and Position}, {Pan and Zoom}. "
  "{Cross-Functional Flowchart}: {Insert}, {Swimlane}; {Separator}, yani aşama; {Orientation}, yatay ya da dikey.")

# ───────────────────────────── Laboratuvar 1
m("Laboratuvar 1: swimlane (1–4)", ["1. File → New → Cross-Functional Flowchart → Horizontal → Create", "2. Swimlane ile 4 şerit: Bayi, Sistem, Kredi Tahsis, Operasyon",
                                     "3. Separator: \"Başvuru\", \"Karar ve kullandırım\"", "4. Basic Flowchart: Start/End, Process, Decision · swimlane çizimini birebir kur"],
  "Laboratuvar: {swimlane}'i {Visio}'da çiz ve veriyle zenginleştir; yaklaşık altmış dakika. "
  "Bir, şablon: {File}, {New}, {Cross-Functional Flowchart}, {Horizontal}, {Create}. İki şerit hazır gelir. "
  "İki, şeritler: {Cross-Functional Flowchart} sekmesi, {Swimlane} ile toplam dört şerit yap. Şerit başlıklarına çift tıkla: bayi, sistem, kredi tahsis, operasyon. "
  "Üç, aşamalar: {Separator} ile iki aşama ekle: başvuru, karar ve kullandırım. "
  "Dört, şekiller: {Basic Flowchart} {stencil}'inden {Start} ve {End}, {Process} ve {Decision} şekillerini sürükle. "
  "{Process Diagramming} bölümündeki {swimlane} çizimini, yani süreç diyagramı görsel rehberini, birebir kur.", bolum="Visio · Laboratuvarlar")
m("Laboratuvar 1: bağla, düzenle, veri (5–8)", ["5. Mavi oklar / Connector · uçlar yeşil · karar çıkışları \"evet\"/\"hayır\"",
                                                "6. Ctrl+A → Auto Align & Space · Design → Connectors → Right-Angle",
                                                "7. Define Shape Data: \"Süre (dk)\", \"Sorumlu\", \"Kontrol ID\"", "8. Review → Shape Reports → New → Excel"],
  "Beş, bağlantı: şekle gelince çıkan mavi oklarla ya da {Home}, {Connector} ile bağla. Uçların yeşil olduğunu kontrol et. "
  "Karar şeklinin çıkış oklarına çift tıklayıp evet ve hayır yaz. "
  "Altı, düzen: tümünü seç, {Ctrl} A; {Home}, {Position}, {Auto Align and Space}. {Design}, {Connectors}, {Right-Angle}. "
  "Yedi, {shape data}: manuel inceleme şeklini seç; {Data}, {Shape Data Window}. Sağ tık, {Data}, {Define Shape Data} ile "
  "süre dakika, sorumlu ve kontrol ID alanlarını ekle ve doldur. Aynısını diğer adımlar için yap. "
  "Sekiz, rapor: {Review}, {Shape Reports}, {New}; {shape data} alanlarını seç, Excel'e çıkart; süreç envanteri tablon hazır.")
m("Laboratuvar 1: katman, alt süreç, teslim (9–13)", ["9. Layers → New → \"Kontroller\" · Callout → Assign to Layer · gizle/aç",
                                                      "10. Process → Create from Selection", "11. Check Diagram → Issues'ı düzelt",
                                                      "12. (İsteğe bağlı) Data Visualizer: P1–P6 → Data → Refresh", "13. Export → PDF + .vsdx Confluence'a"],
  "Dokuz, katman: {Home}, {Layers}, {Layer Properties}, {New}, kontroller, {OK}. Kontrol notlarını, {Insert}, {Callout}, seç; "
  "{Home}, {Layers}, {Assign to Layer}, kontrolleri işaretle. Katmanı gizleyip açarak denetim görünümünü dene. "
  "On, alt süreç: manuel inceleme adımlarını ayrı sayfaya taşımak için onları seç; {Process}, {Create from Selection}. "
  "On bir, doğrulama: {Process}, {Check Diagram}; {Issues} penceresindeki uyarıları düzelt: bağlantısız şekil, etiketsiz karar çıkışı ve benzeri. "
  "On iki, Excel'den otomatik çizim, isteğe bağlı: {File}, {New}, {Data Visualizer}, {Cross-Functional Flowchart}; örnek Excel şablonunu aç; "
  "bu bölümün ileri seviye kısmındaki {Data Visualizer} tablosunu, P1'den P6'ya, doldur; {Visio}'ya dönüp diyagramı oluştur. "
  "Excel'i değiştirip {Data}, {Refresh} ile güncelle. "
  "On üç, teslim: {File}, {Export}, PDF; ve nokta {vsdx} dosyasını Confluence'taki süreç sayfasına ekle.")

# ───────────────────────────── Uygulama paketi
m("Check Diagram nasıl çalışır?", ["Basic Flowchart, Cross-Functional Flowchart, BPMN: kendi kural setleri",
                                   "Process → Diagram Validation → Check Diagram", "Bulgular Issues penceresinde · tıkla → şekil seçilir"],
  "{Visio} uygulama paketi. {Check Diagram}: ne yakalar, ne yakalamaz? {Visio}'nun {Basic Flowchart}, {Cross-Functional Flowchart} ve BPMN şablonları "
  "kendi kural setleriyle gelir. {Process} sekmesi, {Diagram Validation} grubu, {Check Diagram} tıklanınca {Visio} diyagramı bu kurallara göre tarar "
  "ve bulguları {Issues} penceresinde listeler. Bir bulguya tıklayınca ilgili şekil seçilir.", bolum="Visio · Uygulama paketi")
t("Yakaladıkları ve yakalayamadıkları", ["Yakaladıkları (örnekler)", "Yakalayamadıkları"],
  [["Hiçbir şekle bağlı olmayan bağlayıcı", "\"Kredi/değer limit içinde mi?\" iş açısından doğru mu"],
   ["Girişi ya da çıkışı olmayan şekil", "XOR ayırıp AND birleştirme: kilitlenme"], ["Başlangıç ya da bitiş olayı eksik", "Firma kuralı: 72 ay yazılmış; kural 6–60 ay"],
   ["BPMN'e aykırı bağlantı", "Eksik istisna dalı (KKB zaman aşımı)"]],
  "Tablo iki sütun: yakaladıkları, örnekler; ve yakalayamadıkları. Yakaladıkları: hiçbir şekle bağlı olmayan bağlayıcı; girişi ya da çıkışı olmayan şekiller; "
  "başlangıç ya da bitiş olayı eksikliği; BPMN notasyonuna aykırı bağlantılar. "
  "Yakalayamadıkları: kredi değer limit içinde mi sorusunun iş açısından doğru olup olmadığı; "
  "XOR ile ayırıp AND ile birleştirmenin yol açtığı kilitlenme gibi davranış hataları; "
  "Firma kurallarıyla çelişki, örneğin azami vade yetmiş iki ay yazılmış, kural altı ile altmış ay; "
  "ve eksik istisna dalları, örneğin KKB zaman aşımı çizilmemiş.")
dikkat("Check Diagram temiz ≠ süreç doğru", "Yalnız grafik söz dizimi · BPMN 11 maddelik hata kataloğu + Firma kuralları elle · Rules to Check · Import Rules From",
       "Microsoft'un açıklamasına göre doğrulama yalnızca diyagramın grafik söz dizimini kontrol eder. "
       "Bu yüzden {Check Diagram} temiz çıksa bile BPMN bölümündeki on bir maddelik hata kataloğunu ve Firma kurallarını elle kontrol et. "
       "Dosyada hangi kural setlerinin açık olduğunu görmek için {Check Diagram}'ın yanındaki oka tıkla, {Rules to Check}. "
       "Başka bir şablonla başlamış bir dosyaya kural seti eklemek için aynı menüden {Import Rules From} seç.")
m("Laboratuvar 2: bilerek hatalı çiz (1–3)", ["1. File → New → BPMN Diagram · beklenen: BPMN Basic Shapes", "2. Start Event · \"Başvuruyu al\", \"KKB sorgula\" · Gateway · End Event",
                                              "3. Üç hata: boşta ok · gateway'den tek çıkış · bağlanmamış End Event"],
  "Laboratuvar: bilerek hatalı çiz, {Visio}'ya buldur. Bir: {File}, {New}, arama kutusuna {BPMN Diagram} yaz, şablonu aç. "
  "Beklenen: solda {BPMN Basic Shapes} {stencil}'i. "
  "İki: bir {Start Event}, iki {Task}, yani başvuruyu al ve KKB sorgula; bir {Gateway} ve bir {End Event} bırak. "
  "Üç: bilerek üç hata yap: KKB sorgula görevinden çıkan oku boşlukta bırak; {gateway}'den yalnızca bir çıkış oku çiz; {End Event}'i hiçbir şeye bağlama.")
m("Laboratuvar 2: buldur ve düzelt (4–6)", ["4. Check Diagram → Issues birden fazla bulgu", "5. Tıkla, düzelt, tekrar → \"No issues were found\"",
                                            "6. İki çıkışı Conditional yap, varsayılan dal yok → hata #3 yakalanıyor mu?"],
  "Dört: {Process}, {Check Diagram}. Beklenen: {Issues} penceresi açılır ve birden fazla bulgu listeler. "
  "Beş: her bulguya tıkla, seçilen şekli düzelt, yeniden {Check Diagram} de. Beklenen: {No issues were found} benzeri bir bildirim. "
  "Altı: şimdi {gateway}'in iki çıkış bağlayıcısını da koşullu yap; bağlayıcıya sağ tık, {Flow Type}, {Conditional}; menü adı sürüme göre değişebilir. "
  "Ama varsayılan dal tanımlama. {Check Diagram}'ı yeniden çalıştır ve sonucu not et. Bu, hata kataloğundaki üç numaralı hatadır; "
  "{Visio}'nun bunu yakalayıp yakalamadığını kendi sürümünde gör. Yakalamıyorsa elle kontrol listesine güven.")
t("Visio ve draw.io karşılıkları (1/2)", ["İş", "Visio", "draw.io"],
  [["BPMN şablonu", "New → \"BPMN Diagram\"", "More Shapes → BPMN General"], ["Swimlane", "New → \"Cross-Functional Flowchart\"", "pool ara → Horizontal Pool"],
   ["Şekle veri alanı", "Sağ tık → Define Shape Data", "Edit Data (Ctrl+M)"]],
  "{Visio} ile {draw.io} karşılıkları; tablo iş, {Visio} ve {draw.io}. BPMN şablonu: {Visio}'da {File}, {New}, {BPMN Diagram}; "
  "{draw.io}'da artı {More Shapes}, {BPMN General}, {Apply}. "
  "{Swimlane}: {Visio}'da {File}, {New}, {Cross-Functional Flowchart}; {draw.io}'da arama kutusuna {pool} yaz, {Horizontal Pool}. "
  "Şekle veri alanı: {Visio}'da şekle sağ tık, {Data}, {Define Shape Data}; {draw.io}'da şekle sağ tık, {Edit Data}, {Ctrl} M, özellik ekle.")
t("Visio ve draw.io karşılıkları (2/2)", ["İş", "Visio", "draw.io"],
  [["Doğrulama", "Process → Check Diagram", "Yok; kontrol listesi elle"], ["Dışa aktarma", "Export → PDF/PNG", "Export as → PDF/PNG"],
   ["Paylaşma", "OneDrive/SharePoint → Share", ".drawio · Confluence'a göm"]],
  "Diyagramı doğrulama: {Visio}'da {Process}, {Check Diagram}; {draw.io}'da yerleşik doğrulama yok; kontrol listesini elle uygula. "
  "Dışa aktarma: {Visio}'da {File}, {Export}, PDF ya da PNG; {draw.io}'da {File}, {Export as}, PDF ya da PNG. "
  "Başkasıyla paylaşma: {Visio}'da {OneDrive} ya da {SharePoint}'e kaydet, {Share}; "
  "{draw.io}'da dosyayı nokta {drawio} olarak kaydet; Confluence için {draw.io} uygulaması varsa sayfaya göm.")
m("Bağımsız görev: U04 swimlane'i Visio'da", ["Çalışma Seti U04: bayi başvurusu ve otomatik karar", "1. Şeritler: Bayi, Başvuru API, Karar Motoru, KKB",
                                             "2. \"Yanıt 5 sn içinde geldi mi?\" → Hayır → MANUEL_INCELEME", "3. Shape Data: Sahip, Sistem, Hedef süre (\"?\")",
                                             "4. Check Diagram + hata kataloğu #1–#7, #10 · 5. PDF"],
  "Bağımsız görev: U04 {swimlane}'i {Visio}'da. Firma Çalışma Seti'ndeki U04, yani bayi başvurusu ve otomatik karar diyagramını "
  "{Visio}'da {Cross-Functional Flowchart} olarak yeniden çiz. Bir: şeritler bayi, başvuru API, karar motoru, KKB. "
  "İki: KKB beş saniye kuralını karar şekliyle göster: yanıt beş saniye içinde geldi mi; hayır ise {MANUEL_INCELEME}. "
  "Üç: her görev şekline üç {Shape Data} alanı ekle: sahip, sistem, hedef süre; bilinmiyorsa soru işareti yaz. "
  "Dört: {Check Diagram}'ı temiz geçir; sonra BPMN hata kataloğunun bu diyagrama uyan maddelerini, yani bir ile yedi arası ve on, elle uygula. "
  "Beş: PDF olarak dışa aktar. Doğru yaptığını nasıl anlarsın: {Issues} penceresi boş; her karar şeklinin her çıkışı etiketli; "
  "{Shape Data} penceresinde, {View}, {Task Panes}, {Shape Data}, herhangi bir göreve tıklayınca üç alan görünüyor.",
  bolum="Visio · Bağımsız görev ve sorun giderme")
t("Sorun giderme (1/2)", ["Belirti", "Olası neden", "Çözüm"],
  [["Process sekmesi yok", "Web ya da Standard sürüm", "Professional / Plan 2; yoksa draw.io"], ["\"Kural seti yok\"", "Boş çizimden başlatıldı", "Import Rules From → Flowchart/BPMN"],
   ["Bağlayıcı taşınmıyor", "Uç yapışmamış", "Ucu bağlantı noktasına sürükle"]],
  "Sorun giderme; belirti, olası neden, çözüm. Şeritte {Process} sekmesi yok: {Visio}'nun web sürümü ya da {Standard} sürümü kullanılıyor; "
  "masaüstü {Professional} ya da {Plan 2} gerekir; yoksa {draw.io} ve elle kontrol. "
  "{Check Diagram} kural seti yok gibi davranıyor: dosya boş çizimden başlatılmış; {Check Diagram} oku, {Import Rules From}, {Flowchart} ya da BPMN kural seti. "
  "Bağlayıcı şekille birlikte taşınmıyor: uç şekle yapışmamış; bağlayıcının ucunu şeklin bağlantı noktasına sürükle, uç işaretinin renginin değiştiğini gör.")
t("Sorun giderme (2/2)", ["Belirti", "Olası neden", "Çözüm"],
  [["Şerit değişince sahip değişmiyor", "Şekil şerit dışına bırakıldı", "Şerit vurgulanana kadar sürükle"],
   ["Temiz ama mantık yanlış", "Yalnız grafik söz dizimi", "Hata kataloğu + Firma kuralları elle"]],
  "Şekil şerit değiştirince sahibi değişmiyor: şekil şerit kutusunun dışına bırakılmış; şekli şeridin içine, şerit vurgulanana kadar sürükle. "
  "{Check Diagram} temiz ama süreç mantığı yanlış: doğrulama yalnızca grafik söz dizimine bakar; BPMN hata kataloğunu ve Firma kurallarını elle uygula.")
soru("Bilgi kontrolü 1/5", "Visio'da diyagram doğrulama hangi sekmededir?", ["Design", "Review", "Process", "Data"], 2,
     "Beş soruluk bilgi kontrolü. Birinci soru: {Visio}'da diyagram doğrulama hangi sekmededir? A, {Design}. B, {Review}. C, {Process}. D, {Data}.",
     "Doğru cevap C: {Process}.", bolum="Visio · Bilgi kontrolü ve çözümler")
soru("Bilgi kontrolü 2/5", "Check Diagram temiz çıktı. Hangisinden emin olabilirsin?",
     ["Süreç Firma kurallarına uygun", "Hiçbir kapı kilitlenmiyor", "Tüm istisnalar çizildi", "Bağlantılar kural setine göre biçimsel olarak doğru"], 3,
     "İkinci soru: {Check Diagram} temiz çıktı. Hangisinden emin olabilirsin? A, süreç Firma kurallarına uygun. B, hiçbir kapının kilitlenmediği. "
     "C, tüm istisnaların çizildiği. D, bağlantıların kural setine göre biçimsel olarak doğru olduğu.",
     "Doğru cevap D.")
soru("Bilgi kontrolü 3/5", "Boş bir çizime BPMN kurallarını eklemek için?", ["Import Rules From", "Rules to Check", "Shape Data", "Layers"], 0,
     "Üçüncü soru: boş bir çizime BPMN kurallarını eklemek için? A, {Import Rules From}. B, {Rules to Check}. C, {Shape Data}. D, {Layers}.",
     "Doğru cevap A.")
soru("Bilgi kontrolü 4/5", "Görevlere \"Sahip\" ve \"Hedef süre\" eklemek için hangi özellik?", ["Layers", "Shape Data", "Comments", "Containers"], 1,
     "Dördüncü soru: görev şekillerine sahip ve hedef süre bilgisi eklemek için hangi özellik kullanılır? A, {Layers}. B, {Shape Data}. C, {Comments}. D, {Containers}.",
     "Doğru cevap B.")
soru("Bilgi kontrolü 5/5", "Lisansı olmayan ekip arkadaşı diyagramı düzenleyecek. En pratik çözüm?",
     ["Ekran görüntüsü göndermek", "PowerPoint'e kopyalamak", "draw.io'da çizip .drawio paylaşmak", "Excel'e dökmek"], 2,
     "Beşinci soru: {Visio} lisansı olmayan bir ekip arkadaşı diyagramı düzenleyecek. En pratik çözüm? A, ekran görüntüsü göndermek. "
     "B, {PowerPoint}'e kopyalamak. C, {draw.io}'da çizip nokta {drawio} paylaşmak. D, Excel'e dökmek.",
     "Doğru cevap C. Cevaplar: bir C, iki D, üç A, dört B, beş C.")
m("Hızlı başvuru: teslim öncesi", ["Doğru şablon (CFF ya da BPMN Diagram) · Check Diagram temiz", "BPMN hata kataloğu elle uygulandı",
                                   "Her karar çıkışı etiketli · her şeritte görev", "Shape Data dolu ya da \"?\"",
                                   "Başlık bloğu: süreç kodu (P01, U04), sürüm, tarih", "PDF → Confluence süreç sayfası"],
  "Hızlı başvuru: {Visio}'da bir süreç diyagramını teslim etmeden önce. Doğru şablonla başladım: {Cross-Functional Flowchart} ya da {BPMN Diagram}. "
  "{Check Diagram} temiz. BPMN hata kataloğu elle uygulandı. Her karar çıkışı etiketli; her şeritte en az bir görev var. "
  "Görevlerde {Shape Data} alanları dolu ya da soru işaretiyle işaretli. Başlık bloğunda süreç kodu, P01, U04; sürüm ve tarih var. "
  "PDF olarak dışa aktarıldı ve Confluence'taki süreç sayfasına eklendi.")
m("Çözüm: bağımsız görev kontrol noktaları", ["Başvuruyu gir → kaydet → KKB sorgula → Skor döndür", "Yanıt 5 sn içinde? Evet → Otomatik karar → ONAY/RED",
                                              "Hayır → MANUEL_INCELEME · Bayi: Sonucu gör", "KKB sorgula: Karar motoru ekibi · ≤ 5 sn"],
  "Çözümler; bağımsız görev, kontrol noktaları. Bayi şeridi: başvuruyu gir; başvuru API şeridi: başvuruyu kaydet; karar motoru şeridi: KKB sorgula; "
  "KKB şeridi: skor döndür. Karar motoru şeridinde, KKB sorgula adımından hemen sonra karar şekli: yanıt beş saniye içinde geldi mi? "
  "KKB'nin skor döndür adımı yalnızca evet dalını besler. Evet: otomatik karar ver; onay ya da red. Hayır: başvuruyu {MANUEL_INCELEME}'ye al. "
  "Sonuç bayiye geri döner: bayi şeridinde sonucu gör adımı. "
  "{Shape Data} örneği, KKB sorgula: sahip karar motoru ekibi; sistem karar motoru; hedef süre en fazla beş saniye, yani U04 zaman aşımı eşiği.")
m("Bu videoda neler gördük?", ["Sürümler, temel kavramlar, kullanım ipuçları", "Swimlane, BPMN, UML/ER, katman, Shape Data",
                               "Data Visualizer, veri bağlantısı, Power BI, yönetişim, alternatifler", "Ekran, menüler, iki laboratuvar",
                               "Check Diagram sınırları, draw.io karşılıkları, U04"],
  "Toparlayalım. Sürümleri, temel kavramları ve kullanım ipuçlarını gördük. {Swimlane}, BPMN, UML ve ER, katmanlar ve {Shape Data}'yı öğrendik. "
  "{Data Visualizer}, veri bağlantısı, {Power BI}, yönetişim ve alternatiflere baktık. Ekranı, menüleri ve iki laboratuvarı çalıştık. "
  "{Check Diagram}'ın sınırları, {draw.io} karşılıkları ve U04 göreviyle bitirdik. "
  "Son videoda {Agile} çalışma biçimini ve kaynakları ele alacağız.", ton="sakin")

kaydet(__file__, {
    "baslik": "Business Analyst Teknik Rehberi · 13: Visio",
    "alt_baslik": "Swimlane · BPMN · Check Diagram · Shape Data · Data Visualizer · draw.io",
    "kapanis": "Sıradaki video: Agile ve kaynaklar",
    "tema": 13,
    "youtube_baslik": "Business Analyst Teknik Rehberi 13/14: Microsoft Visio (swimlane, BPMN, Check Diagram)",
    "etiketler": ["business analyst", "Visio", "swimlane", "BPMN", "draw.io", "iş analisti"],
}, {"ER": "e re", "SLA": "es el ey", "KPI": "key pi ay", "VBA": "vi bi ey", "SVG": "es vi ci", "PNG": "pi en ci", "XOR": "eks or", "AND": "end",
    "IT": "ay ti", "API": "ey pi ay", "Ctrl": "kontrol"})
