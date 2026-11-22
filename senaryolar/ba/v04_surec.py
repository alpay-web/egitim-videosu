#!/usr/bin/env python3
"""BA Teknik Rehberi · Video 4: Süreç diyagramlama (Process Diagramming). Belge satır 922–1174."""
from ortak import m, t, dikkat, g, soru, kaydet

# ───────────────────────────── Giriş ve hedefler
m("Süreç diyagramlama bir disiplindir", ["Doğru soruya doğru görünümü seçmek", "Bilgiyi doğru kişilerden toplamak",
                                         "Modeli karar almaya yarar hale getirmek", "BPMN güçlü ama tek seçenek değil"],
  "Süreç diyagramlama tek bir notasyon değil, bir disiplindir. Üç şeyi kapsar: doğru soruya doğru görünümü seçmek, "
  "bilgiyi doğru kişilerden toplamak ve modeli karar almaya yarayacak hale getirmek. "
  "BPMN bu disiplinin en güçlü notasyonlarından biri, ama tek seçenek değil. Bu videoda diğerlerini ve süreci sayıyla iyileştirmeyi öğreneceğiz.",
  bolum="Süreç diyagramlama: giriş", kanca="Altmış dakikalık iş neden üç gün sürer?", ton="merakli")
m("Bu bölümün hedefleri", ["Bir Firma süreci için SIPOC ve 4–5 şeritli swimlane", "Adımları sınıflamak: değer katan · gerekli · israf",
                           "İşlem süresi, toplam süre, aktivite oranı, zincirleme %C/A, devir sayısı",
                           "Darboğazı sayıyla gösterip tek iyileştirme önermek"],
  "Bu bölümün sonunda dört şey yapabileceksin. Bir: bir Firma süreci için SIPOC tablosu ve dört beş şeritli bir {swimlane} diyagramı hazırlamak. "
  "İki: her adımı değer katan, gerekli ama değer katmayan ve israf diye sınıflandırmak. "
  "Üç: bir değer akışı için işlem süresini, toplam süreyi, aktivite oranını, zincirleme ilk seferde doğru oranını ve devir sayısını hesaplamak. "
  "Dört: sürecin darboğazını sayıyla gösterip tek bir iyileştirme önermek.")
t("Başlamadan önce gerekenler", ["Gereken", "Nereden", "Hazır mısın?"],
  [["Adımları bilen 1–2 kişi", "Bayi satış temsilcisi, operasyon uzmanı", "20 dk görüşme ayarladın"],
   ["draw.io (ücretsiz)", "app.diagrams.net", "Aramada pool yazınca havuz çıkıyor"],
   ["Hesap tablosu", "Excel / Google Sheets", "Toplam ve oran alabiliyorsun"],
   ["Kavramlar", "Temel ve Orta seviye", "İşlem ile bekleme farkını anlatabiliyorsun"]],
  "Başlamadan önce dört şey gerekli. Sürecin adımlarını bilen bir iki kişi; örneğin bayi satış temsilcisi ve operasyon uzmanı. "
  "Yirmi dakikalık bir görüşme ayarladıysan hazırsın. "
  "Ücretsiz draw.io; adres app nokta diagrams nokta net. Arama kutusuna {pool} yazınca havuz şekli çıkıyorsa tamam. "
  "Bir hesap tablosu: Excel ya da Google Sheets. Bir sütunun toplamını ve iki hücrenin oranını alabiliyorsan yeterli. "
  "Ve kavramlar: bu bölümün temel ve orta seviyesi. İşlem süresi ile bekleme süresi farkını bir cümleyle anlatabiliyorsan başlayabiliriz.")

# ───────────────────────────── Temel seviye
t("Hangi soru, hangi diyagram? (1/2)", ["Soru", "Uygun teknik"],
  [["Sınırlar, girdi / çıktılar?", "SIPOC"], ["Adımlar hangi sırayla, hangi kararlarla?", "Basit akış şeması (flowchart)"],
   ["Kim ne yapıyor, devir teslimler nerede?", "Swimlane (cross-functional)"], ["Zaman ve israf nerede?", "Value Stream Map (VSM)"]],
  "Temel soru şu: hangi soruya hangi diyagram? Sürecin sınırları, girdileri ve çıktıları neler diye soruyorsan: SIPOC. "
  "Adımlar hangi sırayla ve hangi kararlarla ilerliyor diye soruyorsan: basit akış şeması, yani {flowchart}. "
  "Kim ne yapıyor, devir teslimler nerede diye soruyorsan: {swimlane}, diğer adıyla {cross-functional} diyagram. "
  "Zaman ve israf nerede diye soruyorsan: değer akış haritası, yani {Value Stream Map}, kısaca VSM.", bolum="Süreç · Temel seviye")
t("Hangi soru, hangi diyagram? (2/2)", ["Soru", "Uygun teknik"],
  [["Veri nereden nereye gidiyor?", "Data Flow Diagram (DFD)"], ["Kurumlar arası standart, çalıştırılabilir model", "BPMN 2.0"],
   ["Hiyerarşik süreç mimarisi", "Process map / L0–L4, EPC (ARIS)"], ["Sistem durum değişikliği", "UML state machine"]],
  "Veri nereden gelip nereye gidiyor diye soruyorsan: veri akış diyagramı, yani {Data Flow Diagram}, kısaca DFD. "
  "Sistem ve kurumlar arası standart ve çalıştırılabilir bir model istiyorsan: BPMN iki nokta sıfır. "
  "Hiyerarşik bir süreç mimarisi istiyorsan: süreç haritası, yani {process map}, L sıfırdan L dörde seviyeler, ya da {ARIS} dünyasındaki EPC. "
  "Bir sistemin durum değişikliğini anlatacaksan: UML {state machine}.")
t("Akış şeması sembolleri (ANSI/ISO 5807)", ["Sembol", "Şekil"],
  [["Terminal (başla / bitir)", "Oval"], ["İşlem", "Dikdörtgen"], ["Karar (Evet / Hayır)", "Eşkenar dörtgen"],
   ["Belge", "Altı dalgalı dikdörtgen"], ["Veri giriş / çıkış · Veri tabanı", "Paralelkenar · Silindir"],
   ["Sayfa bağlayıcı · Önceden tanımlı işlem", "Daire · Yanları çift çizgili dikdörtgen"]],
  "Klasik akış şeması sembolleri ANSI ve ISO beş bin sekiz yüz yedi standardına dayanır. "
  "Terminal, yani başla ve bitir, ovaldir. İşlem dikdörtgendir. Karar eşkenar dörtgendir ve evet ile hayır çıkışları vardır. "
  "Belge, altı dalgalı bir dikdörtgendir. Veri giriş ve çıkışı paralelkenar, veri tabanı silindirdir. "
  "Sayfa bağlayıcı bir dairedir; önceden tanımlı işlem ise yanları çift çizgili bir dikdörtgendir.")
t("SIPOC: kasko poliçesi tanzimi", ["Sütun", "İçerik"],
  [["Suppliers", "Müşteri, Bayi, Sigorta şirketi, SBM/TRAMER"], ["Inputs", "Ruhsat, kimlik, hasar geçmişi, teminat tercihi"],
   ["Process", "Teklif al → Karşılaştır → Onay → Tahsilat → Poliçe üret → Gönder"],
   ["Outputs", "Poliçe PDF, tahsilat kaydı, komisyon kaydı"], ["Customers", "Müşteri, Finans, Sigorta şirketi"]],
  "SIPOC örneği: kasko poliçesi tanzimi. Tedarikçiler, yani {Suppliers}: müşteri, bayi, sigorta şirketi, SBM ve TRAMER. "
  "Girdiler, yani {Inputs}: araç ruhsatı, kimlik, hasar geçmişi ve teminat tercihi. "
  "Süreç, yani {Process}: teklif al, karşılaştır, onay, tahsilat, poliçe üret, gönder. "
  "Çıktılar, yani {Outputs}: poliçe PDF'i, tahsilat kaydı ve komisyon kaydı. "
  "Müşteriler, yani {Customers}: müşteri, finans ve sigorta şirketi.")
m("Bilgi toplama teknikleri", ["Doküman incelemesi: prosedür, talimat", "Mülakat", "İş başında gözlem (shadowing / gemba)",
                               "Workshop, anket", "Sistem log ve rapor analizi"],
  "Bilgiyi nasıl toplarsın? Doküman incelemesi: prosedürler ve talimatlar. Mülakat. İş başında gözlem, yani {shadowing}, "
  "yalın dünyadaki adıyla {gemba}. Çalıştay, yani {workshop}. Anket. Ve sistem log ve rapor analizi.")
dikkat("Prosedür ≠ gerçek", "Prosedür \"olması gereken\"i, gözlem \"gerçekte olan\"ı anlatır. As-is modeli gerçeğe dayanmalı.",
       "Buradaki ilke çok önemli. Prosedür dokümanı olması gerekeni anlatır; gözlem ise gerçekte olanı. "
       "Mevcut durum modeli, yani {as-is}, gerçeğe dayanmalıdır. Prosedürü kopyalayıp {as-is} diye sunarsan, "
       "sorunların asıl kaynağını hiç görmezsin.")

# ───────────────────────────── Orta seviye
m("Swimlane çizerken kurallar", ["Her lane bir rol veya sistem (kişi adı değil)", "Lane değiştiren ok = devir teslim (handoff): gecikme ve hata riski",
                                 "Adım adı fiil + nesne (\"Belgeleri kontrol et\")", "Her kararın çıkışları etiketli, her yol bir bitişe",
                                 "Sistem adımları ayrı lane'de → otomasyon fırsatı görünür"],
  "Orta seviyede {swimlane} çizim kuralları. Bir: her şerit bir rol ya da sistemdir, kişi adı değil. "
  "İki: şerit değiştiren her ok bir devir tesliminin, yani {handoff}'un işaretidir; gecikme ve hata riski buralarda yoğunlaşır. "
  "Üç: adım isimleri fiil artı nesne; örneğin belgeleri kontrol et. "
  "Dört: her kararın tüm çıkışları etiketlidir ve her yol bir bitişe ulaşır. "
  "Beş: sistem adımları ayrı bir şeritte tutulursa otomasyon fırsatları görünür olur.", bolum="Süreç · Orta seviye")
t("Süreç seviyeleri", ["Seviye", "İçerik", "Örnek"],
  [["L0", "Değer zinciri", "Satış → Kredi → Operasyon → Tahsilat → Sigorta"], ["L1", "Süreç grubu", "Bireysel kredi yönetimi"],
   ["L2", "Süreç", "Taşıt kredisi başvuru ve tahsis"], ["L3", "Alt süreç / aktivite akışı", "Belge kontrolü ve manuel inceleme"],
   ["L4", "Talimat / ekran adımı", "\"Ruhsat fotokopisini sisteme yükle\""]],
  "Süreç seviyeleri, yani süreç mimarisi. L sıfır değer zinciri: satış, kredi, operasyon, tahsilat, sigorta. "
  "L bir süreç grubu: bireysel kredi yönetimi. L iki süreç: taşıt kredisi başvuru ve tahsis. "
  "L üç alt süreç ya da aktivite akışı: belge kontrolü ve manuel inceleme. "
  "L dört talimat ya da ekran adımı: ruhsat fotokopisini sisteme yükle. "
  "APQC'nin süreç sınıflandırma çerçevesi, yani {Process Classification Framework}, kısaca PCF, gibi referans modeller "
  "L bir ile L üç arasındaki sınıflandırma için iyi bir başlangıç noktasıdır.")
m("Value Stream Mapping (VSM)", ["Her adım için:", "İşlem süresi (process time)", "Bekleme süresi (wait time)",
                                 "%C/A: complete & accurate, ilk seferde doğru oranı", "Kuyruk miktarı"],
  "Değer akış haritası, yani VSM. Her adım için dört şey yazılır: işlem süresi, yani {process time}; bekleme süresi, yani {wait time}; "
  "yüzde C bölü A, yani {complete} {and} {accurate}, ilk seferde doğru ve eksiksiz oranı; ve kuyruk miktarı.")
t("VSM metrikleri", ["Metrik", "Formül", "Örnek"],
  [["Toplam lead time", "Σ (işlem + bekleme)", "3 gün 4 saat"], ["Toplam işlem süresi", "Σ işlem", "52 dakika"],
   ["Process cycle efficiency", "işlem / lead time", "%1,1"], ["Rolled %C/A", "Π (%C/A)", "0,9 × 0,8 × 0,95 = %68"]],
  "Dört metrik var. Toplam süre, yani {lead time}: işlem ve bekleme sürelerinin toplamı; örnekte üç gün dört saat. "
  "Toplam işlem süresi: yalnız işlem sürelerinin toplamı; örnekte elli iki dakika. "
  "Süreç verimliliği, yani {process cycle efficiency}: işlem süresinin toplam süreye oranı; örnekte yüzde bir virgül bir. "
  "Zincirleme ilk seferde doğru, yani {rolled} yüzde C bölü A: adımların oranlarının çarpımı. "
  "Örnekte sıfır virgül dokuz çarpı sıfır virgül sekiz çarpı sıfır virgül doksan beş; yaklaşık yüzde altmış sekiz.")
dikkat("Şikayeti bulguya çevir", "\"Süreç yavaş\" → \"Bekleme süresinin %90'ı belge eksikliğinden geri dönmede\"",
       "Bu tablonun gücü şurada: süreç yavaş şikayetini ölçülebilir bir bulguya çevirir. "
       "Örneğin: bekleme süresinin yüzde doksanı belge eksikliğinden geri dönmede. "
       "Böyle bir cümleyle yönetime gidersen, iyileştirmenin nereye yapılacağı tartışma konusu olmaktan çıkar.", tip="bilgi")
t("Lean israf türleri: TIMWOODS", ["Harf", "İsraf"],
  [["T · I · M", "Transport · Inventory · Motion"], ["W · O · O", "Waiting · Overproduction · Over-processing"],
   ["D · S", "Defects · Skills (kullanılmayan yetenek)"], ["Örnek", "Aynı belgeyi bayi, operasyon, tahsis 3 kez kontrol = over-processing"]],
  "Yalın üretimdeki israf türleri TIMWOODS kısaltmasıyla hatırlanır. T taşıma, yani {Transport}. I stok, yani {Inventory}. "
  "M hareket, yani {Motion}. W bekleme, yani {Waiting}. O fazla üretim, yani {Overproduction}. "
  "İkinci O fazla işlem, yani {Over-processing}. D hata, yani {Defects}. S de kullanılmayan yetenek, yani {Skills}. "
  "Örnek: aynı belgeyi bayi, operasyon ve tahsis ekibinin üç kez kontrol etmesi; bu {over-processing}.")
m("DFD (Data Flow Diagram)", ["Harici varlık: kare · Süreç: daire / yuvarlak dikdörtgen", "Veri deposu: açık uçlu dikdörtgen · Veri akışı: etiketli ok",
                              "Seviye 0 (context diagram) → Seviye 1 → Seviye 2",
                              "KVKK veri envanteri: hangi veri, hangi sisteme, hangi amaçla, hangi üçüncü tarafa?"],
  "Veri akış diyagramı, yani DFD. Harici varlık kare, süreç daire ya da yuvarlak köşeli dikdörtgen, veri deposu açık uçlu dikdörtgen, "
  "veri akışı ise etiketli bir oktur. Seviye sıfır, yani bağlam diyagramı, {context diagram}; ardından seviye bir ve seviye iki. "
  "KVKK veri envanteri ve veri akış haritası için çok değerlidir: kişisel veri hangi sisteme, hangi amaçla, hangi üçüncü tarafa aktarılıyor?")

# ───────────────────────────── İleri seviye
m("As-is → to-be dönüşümü", ["As-is'te sorun noktaları (pain point) kırmızı", "Kök neden: 5 Neden, balık kılçığı (Ishikawa), Pareto",
                             "To-be'de her değişiklik → bir gereksinim + bir KPI hedefi",
                             "Gap analizi: As-is | To-be | Fark | Etki | Gereksinim ID"],
  "İleri seviyeye geçiyoruz. {As-is}'ten {to-be}'ye dönüşümde önce {as-is} diyagramındaki sorun noktaları, yani {pain point}'ler kırmızıyla işaretlenir. "
  "Sonra kök neden analizi yapılır: beş neden, balık kılçığı yani Ishikawa, ve Pareto. "
  "{To-be} diyagramında her değişiklik bir gereksinime ve bir KPI hedefine bağlanır. "
  "Bunu bir fark, yani gap analizi tablosunda toplarsın: {as-is}, {to-be}, fark, etki ve gereksinim ID'si.", bolum="Süreç · İleri seviye")
m("Process mining", ["Sistem loglarından gerçek süreç: case ID, aktivite, zaman damgası", "Celonis, Signavio Process Intelligence, Disco, PM4Py",
                     "Varyantlar, döngüler (rework), SLA ihlalleri", "Conformance checking: modelden sapma"],
  "Süreç madenciliği, yani {process mining}: sistem loglarından vaka kimliği, aktivite ve zaman damgasıyla gerçek süreç keşfedilir. "
  "{Celonis}, {Signavio} {Process Intelligence}, {Disco} ya da açık kaynak {PM4Py} ile varyantlar, döngüler yani yeniden işleme, {rework}, "
  "ve SLA ihlalleri bulunur. Uygunluk denetimi, yani {conformance checking}, modelden sapmayı gösterir.")
t("Gereken log yapısı", ["case_id", "activity", "timestamp", "resource"],
  [["BSV-1001", "Başvuru alındı", "2026-03-02 09:14", "bayi_17"], ["BSV-1001", "KKB sorgusu", "2026-03-02 09:14", "system"],
   ["BSV-1001", "Manuel inceleme", "2026-03-02 13:40", "tahsis_04"], ["BSV-1001", "Ek belge istendi", "2026-03-02 13:52", "tahsis_04"],
   ["BSV-1001", "Manuel inceleme", "2026-03-04 10:05", "tahsis_02"], ["BSV-1001", "Onaylandı", "2026-03-04 10:20", "tahsis_02"]],
  "Gereken log yapısı dört alan: {case_id}, {activity}, {timestamp} ve {resource}. Örnek vaka BSV bin bir. "
  "İki Mart sabah dokuz on dörtte başvuru alındı, kaynak bayi on yedi. Aynı dakikada KKB sorgusu, kaynak {system}. "
  "On üç kırkta manuel inceleme, tahsis sıfır dört. On üç elli ikide ek belge istendi, yine tahsis sıfır dört. "
  "Dört Mart saat on sıfır beşte tekrar manuel inceleme, bu kez tahsis sıfır iki. On yirmide onaylandı, tahsis sıfır iki. "
  "Bu altı satırdan bile bir döngü görüyorsun: manuel inceleme iki kez yapılmış ve arada iki gün beklenmiş.")
m("EPC, kontroller, yönetişim", ["EPC: ARIS'te olay → fonksiyon → olay; AND/OR/XOR bağlaçları",
                                 "Kritik adıma kontrol noktası (önleyici/tespit edici, manuel/otomatik) + RACI",
                                 "BDDK denetimi için süreç – risk – kontrol matrisi (RCM)",
                                 "Yönetişim: sahip, versiyon, geçerlilik, onay akışı, merkezi depo, ortak alt süreç kütüphanesi"],
  "Olay güdümlü süreç zinciri, yani {Event-driven Process Chain}, kısaca EPC: {ARIS} dünyasında olay, fonksiyon, olay zinciri; "
  "{AND}, {OR} ve {XOR} bağlaçlarıyla. Bazı kurumsal süreç kütüphaneleri hâlâ EPC kullanır. "
  "Süreç kontrolleri ve risk: her kritik adıma bir kontrol noktası eklenir; önleyici ya da tespit edici, manuel ya da otomatik; ve RACI. "
  "BDDK bilgi sistemleri denetimi ve iç kontrol için süreç, risk, kontrol matrisi, yani RCM üretilir. "
  "Model yönetişimi: süreç sahibi, versiyon, geçerlilik tarihi, onay akışı ve merkezi depo. "
  "Model tekrarını önlemek için ortak bir alt süreç kütüphanesi tutulur; örneğin kimlik doğrulama ya da müşteri onayı al.")
m("Otomasyon fırsat analizi", ["Kural tabanlı, yüksek hacimli, yapılandırılmış veri → RPA / BPM / API adayı",
                               "Yargı gerektiren adım → karar destek ya da insan-döngüde (human-in-the-loop) yapay zeka"],
  "Otomasyon fırsat analizi: kural tabanlı, yüksek hacimli ve yapılandırılmış veri kullanan adımlar RPA, BPM ya da {API} entegrasyonu için adaydır. "
  "Yargı gerektiren adımlar ise karar destek ya da insan döngüde, yani {human-in-the-loop} yapay zeka için adaydır.")

# ───────────────────────────── Hatalar ve mülakat
m("Sık yapılan hatalar", ["Sadece mutlu yol (istisnalar işin %30–50'si olabilir)", "As-is'i prosedürden kopyalamak",
                          "Tek diyagrama her şey; seviye ayrımı yok", "Kişi adlarını lane yapmak",
                          "Tetikleyici ve sonuç tanımsız · diyagramı güncellememek"],
  "Sık yapılan hatalar. Sadece mutlu yolu çizmek; oysa istisnalar gerçek işin yüzde otuz ile elli arasını oluşturabilir. "
  "{As-is}'i prosedürden kopyalamak, sahada doğrulamamak. Tek diyagrama her şeyi sığdırmak, seviye ayrımı yapmamak. "
  "Kişi adlarını şerit yapmak, rol yerine. Başlangıç tetikleyicisini ve bitiş sonucunu tanımlamamak. "
  "Ve diyagramı güncellememek: değişen süreç, eski diyagramla güvenilirliğini kaybeder.", bolum="Süreç · Hatalar ve mülakat")
m("Mülakat soruları", ["1. As-is için kaynaklar; çelişki olursa?", "2. Swimlane'de darboğaz nasıl bulunur?",
                       "3. SIPOC ne zaman?", "4. Process mining için hangi alanlar?", "5. İyileştirme başarısı hangi metriklerle?"],
  "Mülakat soruları. Bir: {as-is} sürecini çıkarırken hangi kaynakları kullanırsınız, çelişki olursa ne yaparsınız? "
  "İki: {swimlane} diyagramında darboğazı nasıl tespit edersiniz? Üç: SIPOC ne zaman kullanılır? "
  "Dört: {process mining} için hangi veri alanları gerekir? Beş: bir süreç iyileştirmesinin başarısını hangi metriklerle ölçersiniz?")
m("Cevap ipuçları", ["Doküman + mülakat + gözlem + log; çelişkide gözlem ve log kazanır, farkı yaz",
                     "Şerit değiştiren oklar, kuyruk biriken insan adımı, bekleme süresi", "Kapsam ve sınırı netleştirmek için, çizimden önce",
                     "case_id, activity, timestamp (+ resource)", "Lead time, aktivite oranı, zincirleme %C/A, devir sayısı"],
  "Kısa ipuçları, bu bölümün içeriğinden. Bir: doküman, mülakat, gözlem ve log; çelişkide gerçekte olanı gösteren gözlem ve log esas alınır, "
  "fark ayrıca not edilir. İki: şerit değiştiren oklara, kuyruğun biriktiği insan adımlarına ve bekleme sürelerine bakarsın. "
  "Üç: SIPOC, kapsamı ve sınırları netleştirmek için çizimden önce kullanılır. "
  "Dört: {case_id}, {activity}, {timestamp}; ve varsa {resource}. "
  "Beş: toplam süre, aktivite oranı, zincirleme ilk seferde doğru oranı ve devir sayısı; birazdan metrik kartında hepsini göreceğiz.")

# ───────────────────────────── Görsel rehber
g("Swimlane nasıl okunur?", "g14.png",
  [([0.0, 0.1, 0.2, 0.88], "1 · Şerit adları: kimler var?"), ([0.15, 0.13, 0.75, 0.5], "2 · Başlangıçtan okları izle"),
   ([0.45, 0.5, 0.75, 0.68], "Darboğaz adayı: manuel inceleme"), ([0.0, 0.88, 1.0, 0.97], "5 devir teslim")],
  "Görsel rehbere geçiyoruz. {Swimlane} diyagramı şöyle okunur. Bir: soldaki şerit adlarını oku; kimler var? Burada bayi, sistem, kredi tahsis ve operasyon. "
  "İki: başlangıç dairesini bul ve okları takip et. Bayi başvuru girer, sistem kontrolleri yapar, skor yeterli mi diye sorar. "
  "Üç: her ok bir şeritten diğerine geçtiğinde dur; burada iş el değiştiriyor. Bilgi eksiksiz geçiyor mu, ne kadar bekliyor diye sor. "
  "Dört: karar noktasının iki çıkışını ayrı ayrı izle. Evet ise otomatik onay ve sözleşme imzalat; hayır ise kredi tahsiste manuel inceleme. "
  "Beş: aynı şeritte arka arkaya çok adım varsa o rolün yüküne bak. "
  "Vurgulu manuel inceleme kutusu insan iş gücüne bağlı olduğu için tipik darboğaz adayıdır; kuyruk burada birikir. "
  "Alttaki not: bu akışta beş devir teslim var: bayiden sisteme, sistemden tahsise, tahsisten bayiye, sistemden bayiye ve bayiden operasyona.",
  bolum="Süreç · Görsel rehber")
dikkat("Bu çizim bilerek sade", "Ret yolu yok; \"Sözleşme imzalat\"a iki ok doğrudan giriyor. BPMN'de: ret yolunu ekle, iki oku XOR birleşiminde topla.",
       "Bir not: bu çizim sade tutuldu. Manuel incelemenin ret yolu gösterilmedi ve sözleşme imzalat adımına iki ok doğrudan giriyor. "
       "Aynı süreci BPMN'de çizerken ret yolunu eklersin ve iki oku önce bir {XOR} birleşim kapısında toplarsın; "
       "bunu BPMN uygulama paketindeki hata kataloğunda görmüştük.", tip="bilgi")
g("Value Stream Map nasıl okunur?", "g15.png",
  [([0.0, 0.15, 1.0, 0.43], "Adım kutuları, veri kutuları, kuyruklar"), ([0.0, 0.55, 1.0, 0.8], "Merdiven: üst bekleme, alt işlem"),
   ([0.0, 0.8, 1.0, 0.95], "Toplam: 60 dk işlem, ≈ 3 gün 5 saat")],
  "Değer akış haritası şöyle okunur. Üstte adım kutuları ve altlarında veri kutuları var: işlem süresi ve yüzde C bölü A. "
  "Başvuru girişi on beş dakika ve yüzde doksan beş; belge kontrolü yirmi dakika ve yüzde yetmiş; kredi inceleme on beş dakika ve yüzde doksan; "
  "sözleşme on dakika ve yüzde doksan sekiz. Aradaki üçgenler kuyruktur, yani bekleyen iş. "
  "En alttaki merdiven çizgisi zaman çizelgesidir: üst basamaklar beklemeyi, alt basamaklar gerçek işlemi gösterir. "
  "Beklemeler dört saat, bir gün ve iki gün. Basamakların üstündeki rakamları toplayınca müşterinin beklediği toplam süreyi bulursun. "
  "Toplam işlem altmış dakika; toplam süre yaklaşık üç gün beş saat. "
  "Süreç verimliliği altmış bölü dört bin altı yüz yirmi dakika, yaklaşık yüzde bir virgül üç. "
  "İlk seferde doğru oranı sıfır virgül doksan beş çarpı sıfır virgül yetmiş çarpı sıfır virgül doksan çarpı sıfır virgül doksan sekiz; yaklaşık yüzde elli dokuz. "
  "Bu resim öğretim amacıyla örnek değerler kullanıyor.")
dikkat("Önce neye dokunursun?", "%C/A'sı en düşük adım: belge kontrolü (%70). Eksik belge 1 günlük kuyruğu da besler → bayi portalında zorunlu belge kontrolü + otomatik belge okuma.",
       "Bu örnekte iyileştirme önceliği açık: yüzde C bölü A'sı en düşük adım belge kontrolü, yüzde yetmiş. "
       "Eksik belge, ardından gelen bir günlük kuyruğu da besler. "
       "Bu yüzden bayi portalında zorunlu belge kontrolü ve otomatik belge okuma ilk hedeftir.")
t("Menü rehberi: swimlane hangi araçta?", ["Araç", "Swimlane nasıl açılır", "İpucu"],
  [["draw.io", "pool → Horizontal Pool · Lane", "Arrange → Layout"],
   ["Visio", "Cross-Functional Flowchart · Swimlane", "Separator: aşama"],
   ["Miro", "Templates → swimlane", "Kenardan bağlayıcı çek"],
   ["PowerPoint / Excel", "Tavsiye edilmez", "Doğrulanamaz, ölçeklenmez"]],
  "Hangi araçta nasıl çizilir? draw.io'da sol paneldeki arama kutusuna {pool} yaz ve {Horizontal Pool} şeklini sürükle. "
  "Şerit eklemek için havuz seçiliyken sağ panelde {Arrange}'dan şerit sayısını artır ya da {Lane} şeklini havuzun içine bırak. "
  "Kutu içine bırakılan şekiller şeritle birlikte taşınır; {Arrange}, {Layout} ile otomatik düzen yapılır. "
  "Visio'da {File}, {New}, {Cross-Functional Flowchart}, {Create}. Şerit için {Cross-Functional Flowchart} sekmesinde {Swimlane}, aşama için {Separator}. "
  "Ayrıntılar Visio videosunda. "
  "Miro'da sol araç çubuğunda {Templates}, aramaya {swimlane} ya da {flowchart} yaz, şablonu ekle. "
  "Kartları şeride sürükle; bağlayıcı için kartın kenarındaki noktadan çek. "
  "PowerPoint ya da Excel ise tavsiye edilmez: doğrulanamaz ve ölçeklenmez.")

# ───────────────────────────── Laboratuvar
m("Laboratuvar: kasko as-is analizi (~60 dk)", ["1. SIPOC: örneği kendi cümlelerinle doldur, 5–7 ana adım",
                                               "2. Bilgi topla: satış temsilcisi + operasyon uzmanı, 20'şer dk",
                                               "\"Son poliçeyi adım adım anlatın\" · \"Nerede bekliyorsunuz?\" · \"En sık hangi hata?\"",
                                               "3. Swimlane: Müşteri, Bayi, Sigorta Operasyonu, Sigorta Şirketi, Sistem"],
  "Laboratuvar: kasko poliçesi tanzimi için {as-is} analizi; yaklaşık altmış dakika. "
  "Bir, SIPOC: bölümün başındaki örneği kopyala; tedarikçi, girdi, süreç, çıktı ve müşteri sütunlarını kendi cümlelerinle doldur. "
  "Süreci beş ile yedi ana adımla sınırla. "
  "İki, bilgi topla: bir satış temsilcisi ve bir operasyon uzmanıyla yirmişer dakikalık görüşme planla. Şunları sor: "
  "son yaptığınız poliçeyi adım adım anlatın; nerede bekliyorsunuz; en sık hangi hata oluyor? "
  "Üç, {swimlane} çiz: şeritler müşteri, bayi, sigorta operasyonu, sigorta şirketi, ki ayrı havuz olabilir, ve sistem. "
  "Adımları fiil artı nesne ile yaz.", bolum="Süreç · Laboratuvar")
m("Laboratuvar: adım 4–8", ["4. Devir teslimleri say; her adıma işlem + bekleme (bilmiyorsan \"?\")",
                            "5. VSM tablosu: Adım | işlem | bekleme | %C/A → lead time, verimlilik",
                            "6. En büyük beklemeye 5 Neden; sonuç tek cümle", "7. To-be: bir iyileştirme, hangi adım ve metrik",
                            "8. Gap: As-is | To-be | Fark | Gereksinim ID"],
  "Dört, işaretle: her devir teslimi say. Her adımın yanına işlem süresini ve bekleme süresini yaz; süreyi bilmiyorsan soru işareti koy ve sor. "
  "Beş, VSM tablosu: adım, işlem süresi, bekleme ve yüzde C bölü A. Toplam süreyi ve süreç verimliliğini hesapla. "
  "Altı, kök neden: en büyük bekleme için beş neden uygula ve sonucu bir cümleyle yaz. "
  "Yedi, {to-be} taslak: bir iyileştirme öner; hangi adımı ve hangi metriği değiştirdiğini göster. "
  "Sekiz, gap analizi tablosu: {as-is}, {to-be}, fark ve gereksinim ID'si.")

# ───────────────────────────── Uygulama paketi
t("Her adımı üç renkten birine boya", ["Sınıf", "Firma örnekleri", "Ne yapılır"],
  [["Değer katan (VA)", "Kredi kararı vermek · krediyi kullandırmak", "Korunur, hızlandırılır"],
   ["Gerekli ama değer katmayan (NNVA)", "KKB sorgusu · rehin tesisi, dain-i mürtehin kontrolü", "Otomatikleştirilir, kısaltılır"],
   ["İsraf (UNVA)", "Aynı belgeyi 3 ekip kontrol · eksik belgeyle bayiye iade", "Kaldırılır"]],
  "Uygulama paketi. İlk başlık: her adımı üç renkten birine boya. VSM'de her adımın yanına bir sınıf yazılır; bu sınıf iyileştirmede hangi adıma dokunacağını belirler. "
  "Değer katan, yani VA: müşterinin para ödemeye razı olacağı iş. Firma örnekleri: kredi kararını vermek ve krediyi kullandırmak. Korunur ve hızlandırılır. "
  "Gerekli ama değer katmayan, yani NNVA: mevzuat ya da risk yüzünden zorunlu ama müşteri için değer üretmeyen iş. "
  "Örnekler: KKB sorgusu; rehin tesisi ve kaskoda dain-i mürtehin kontrolü. Otomatikleştirilir ve kısaltılır. "
  "İsraf, yani UNVA: kaldırılabilecek iş. Örnekler: aynı belgenin bayi, operasyon ve tahsis tarafından üç kez kontrol edilmesi; "
  "eksik belge yüzünden başvurunun bayiye geri gönderilmesi. Kaldırılır.", bolum="Süreç · Uygulama paketi")
t("Ofiste 8 israf (1/2)", ["Kod", "İsraf", "Firma örneği"],
  [["D", "Hata (eksik, yanlış bilgi)", "Fatura bedeli yanlış → kredi/değer oranı yanlış"],
   ["M", "Manuel devir", "Belge e-postayla geliyor, elle yükleniyor"], ["W", "Bekleme", "Manuel incelemede analist kuyruğu"],
   ["PD", "Yarım iş", "Onaylı ama imzasız başvurular (U08: 30 gün sonra iptal)"]],
  "TIMWOODS listesi üretimden gelir; ofis ve yazılım süreçlerinde şu sekizli sınıflandırma daha kolay uygulanır. "
  "VSM'de israfı kırmızı harf koduyla işaretlersin. "
  "D, hata, yani eksik ya da yanlış bilgi: başvuruda araç fatura bedeli yanlış girilmiş, kredi değer oranı yanlış hesaplanıyor. "
  "M, manuel devir: belge bayiden e-postayla geliyor, operasyon sisteme elle yüklüyor. "
  "W, bekleme: manuel incelemeye düşen başvuru analist kuyruğunda bekliyor. "
  "PD, yarım iş: onaylanmış ama sözleşmesi imzalanmamış başvurular; U08'e göre otuz gün sonra iptal.")
t("Ofiste 8 israf (2/2)", ["Kod", "İsraf", "Firma örneği"],
  [["TS", "Bağlam değiştirme", "Analist kredi, muvafakat, rehin kaldırma arasında gidip geliyor"],
   ["EP", "Fazla süreç", "Düşük tutarlara da çift imza"], ["EF", "Fazla özellik", "Portal'da kullanılmayan rapor ekranları"],
   ["H", "Kahramanlık", "Ay sonu kampanyası gece mesaisiyle yetişiyor"]],
  "TS, bağlam değiştirme: analist aynı anda kredi, hasar muvafakati ve rehin kaldırma işleri arasında gidip geliyor. "
  "EP, fazla süreç: tutarı düşük başvurular için de çift imza istenmesi. "
  "EF, fazla özellik: bayi portalında hiç kullanılmayan rapor ekranları. "
  "H, kahramanlık: ay sonu kampanyasında kullandırımların gece mesaisiyle yetiştirilmesi.")
t("Metrik kartı (1/2)", ["Metrik", "Formül", "Ne söyler"],
  [["İşlem süresi (PT)", "Kesintisiz çalışıldığında süre", "Gerçek iş yükü"], ["Toplam süre (LT)", "Σ (işlem + bekleme)", "Müşterinin hissettiği süre"],
   ["Aktivite oranı (%A)", "PT ÷ LT × 100", "Zamanın ne kadarında iş ilerliyor"]],
  "Metrik kartı. İşlem süresi, PT: adımın kesintisiz çalışıldığında sürdüğü süre; gerçek iş yükünü söyler. "
  "Toplam süre, LT: işlem ve bekleme toplamı; müşterinin hissettiği süre. "
  "Aktivite oranı, yüzde A: PT bölü LT çarpı yüz; zamanın ne kadarında iş gerçekten ilerliyor. "
  "Orta seviyedeki VSM tablosunda bu, {process cycle efficiency} adıyla geçiyordu.")
t("Metrik kartı (2/2)", ["Metrik", "Formül", "Ne söyler"],
  [["%C/A", "Sonraki adımın düzeltmeden kullanabildiği oran", "Hangi adım sonrakine sorun gönderiyor"],
   ["Zincirleme %C/A (RFPY)", "Π %C/A", "Hiç geri dönmeden ilerleyen iş oranı"],
   ["Devir sayısı", "Şeritten şeride geçiş sayısı", "Her devir bir bekleme ve hata fırsatı"]],
  "Yüzde C bölü A: bir sonraki adımın, gelen işi düzeltmeden kullanabildiği oran; hangi adımın kendinden sonrakine sorun gönderdiğini söyler. "
  "Zincirleme yüzde C bölü A, yani RFPY: tüm oranların çarpımı; baştan sona hiç geri dönmeden ilerleyen iş oranı. "
  "Devir sayısı: işin bir şeritten diğerine geçiş sayısı; her devir bir bekleme ve hata fırsatıdır.")
dikkat("Tek kısıt kuralı", "Throughput'u kapasitesi en düşük adım belirler. Darboğaz olmayanı hızlandırmak throughput'u değiştirmez, kuyruğu büyütür. Tek öneri: darboğaza ya da en büyük gecikme kaynağına.",
       "Şimdi en önemli kural: tek kısıt kuralı. Bir sürecin birim zamanda bitirebildiği iş sayısını, yani {throughput}'u, "
       "kapasitesi en düşük adım belirler. Darboğaz olmayan bir adımı hızlandırmak {throughput}'u değiştirmez; "
       "bu adım darboğazdan önceyse yalnızca darboğazın önündeki kuyruğu büyütür. "
       "VSM'de ayrıca en büyük gecikme kaynağına bakılır: kapasite darboğazı olmasa da en uzun beklemeyi ve en çok geri dönüşü üreten adım, "
       "toplam süreyi en çok uzatan adımdır. VSM sonunda tek bir öneri yap; o öneri darboğaza ya da en büyük gecikme kaynağına dokunsun.")

# ───────────────────────────── Bağımsız görev
t("Bağımsız görev: kasko yenileme", ["#", "Adım (şerit)", "Bekleme", "İşlem", "%C/A"],
  [["1", "Hatırlatma gönder (Sigorta Op.)", "240 dk", "10 dk", "%95"], ["2", "Yeni poliçeyi ilet (Müşteri / Bayi)", "2.880 dk", "15 dk", "%60"],
   ["3", "Poliçeyi kontrol et (Sigorta Op.)", "480 dk", "10 dk", "%90"], ["4", "Sisteme kaydet (Sigorta Op.)", "60 dk", "5 dk", "%98"]],
  "Bağımsız görev: kasko yenileme değer akışı. Firma kuralı: kasko muafiyetsiz olmalı, dain-i mürtehin Firma olmalı; "
  "bitişten sonra on beş gün içinde yenilenmezse yasal süreç başlar. "
  "Aşağıdaki örnek değerlerle, ki gerçek Firma verisi değildir, metrik kartını doldur, adımları sınıflandır, darboğazı bul ve tek bir iyileştirme öner. "
  "Bir: yenileme hatırlatması gönder, sigorta operasyonu; öncesinde iki yüz kırk dakika bekleme, on dakika işlem, yüzde doksan beş. "
  "İki: yeni poliçeyi ilet, müşteri ya da bayi; iki bin sekiz yüz seksen dakika, yani iki gün bekleme, on beş dakika işlem, yüzde altmış. "
  "Üç: poliçeyi kontrol et, yani muafiyet ve dain-i mürtehin; sigorta operasyonu; dört yüz seksen dakika bekleme, on dakika işlem, yüzde doksan. "
  "Dört: poliçeyi sisteme kaydet, sigorta operasyonu; altmış dakika bekleme, beş dakika işlem, yüzde doksan sekiz. "
  "Doğru yaptığını nasıl anlarsın? Toplam işlem süresini ve toplam süreyi dakika cinsinden buldun; aktivite oranın yüzde ikinin altında; "
  "zincirleme oran yaklaşık yüzde elli. Çözüm videonun sonunda.", bolum="Süreç · Bağımsız görev")

# ───────────────────────────── Sorun giderme
t("Sorun giderme (1/2)", ["Belirti", "Olası neden", "Çözüm"],
  [["Herkes süreci farklı anlatıyor", "Herkes kendi şeridini anlatıyor", "\"Son yaptığınız işi anlatın\"; bir işi baştan sona izle"],
   ["Diyagram sayfaya sığmıyor", "Seviyeler karışmış", "Üstte 5–7 adım; ayrıntı alt sürece"],
   ["Bekleme sürelerini kimse bilmiyor", "Süre ölçülmüyor", "\"?\" yaz; durum değişikliği zamanlarından hesapla (SQL, Kibana)"]],
  "Sorun giderme. Görüşmede herkes süreci farklı anlatıyorsa: herkes kendi şeridini anlatıyor, olması gereken ile olan karışıyordur. "
  "Son yaptığınız işi anlatın diye sor; mümkünse bir işi baştan sona izle. "
  "Diyagram bir sayfaya sığmıyorsa: tek diyagramda farklı seviyeler karışmıştır. Üst seviyede beş ile yedi adım bırak, ayrıntıyı alt süreç diyagramına taşı. "
  "Bekleme sürelerini kimse bilmiyorsa: süre ölçülmüyordur. Soru işareti yaz ve sistem kayıtlarındaki durum değişikliği zamanlarından hesapla; "
  "SQL ya da Kibana ile. İkisini de ilerideki videolarda göreceğiz.", bolum="Süreç · Sorun giderme ve bilgi kontrolü")
t("Sorun giderme (2/2)", ["Belirti", "Olası neden", "Çözüm"],
  [["Çok sayıda geri dönüş oku", "Rework yüksek", "Geri dönüşleri kırmızı çiz, %C/A olarak yaz"],
   ["İyileştirme listesi 10 madde", "Darboğaz belirlenmedi", "Toplam süreye en çok ekleyeni seç; tek öneri"]],
  "Diyagramda çok sayıda geri dönüş oku varsa: yeniden işleme, yani {rework}, yüksektir. "
  "Geri dönüşleri kırmızı çiz ve sayısını yüzde C bölü A olarak adımın altına yaz. "
  "İyileştirme listesi on maddeyi bulduysa: darboğaz belirlenmemiştir. Toplam süreye en çok ekleyen adımı seç; "
  "bekleme ile düşük oranın yol açtığı tekrarı birlikte düşün. İki aday çıkarsa ikisini de yaz, gerekçesiyle birini seç ve tek öneri yap.")

soru("Bilgi kontrolü 1/5", "Toplam süre 3 gün, işlem süresi 1 saat. Müşteri neden yavaşlıktan şikayetçi?",
     ["Adımlar yavaş çalışıyor", "İş zamanının çoğunu kuyrukta geçiriyor", "Çalışan sayısı az", "Sistem yavaş"], 1,
     "Beş soruluk bilgi kontrolü. Birinci soru: toplam süre üç gün, işlem süresi bir saat. Müşteri neden yavaşlıktan şikayetçi? "
     "A, adımlar yavaş çalışıyor. B, iş zamanının çoğunu kuyrukta geçiriyor. C, çalışan sayısı az. D, sistem yavaş.",
     "Doğru cevap B. Üç günün yalnız bir saati iş; geri kalanı kuyrukta bekleme.")
soru("Bilgi kontrolü 2/5", "KKB sorgusu hangi sınıfa girer?",
     ["Değer katan", "Gerekli ama değer katmayan", "İsraf", "Yarım iş"], 1,
     "İkinci soru: KKB sorgusu hangi sınıfa girer? A, değer katan. B, gerekli ama değer katmayan. C, israf. D, yarım iş.",
     "Doğru cevap B: gerekli ama değer katmayan. Risk ve mevzuat gereği zorunlu; otomatikleştirilir ve kısaltılır.")
soru("Bilgi kontrolü 3/5", "%C/A değerleri %90, %80 ve %50 olan üç adımın zincirleme %C/A'sı?",
     ["%73", "%50", "%36", "%220"], 2,
     "Üçüncü soru: yüzde C bölü A değerleri yüzde doksan, yüzde seksen ve yüzde elli olan üç adımın zincirleme oranı kaçtır? "
     "A, yüzde yetmiş üç. B, yüzde elli. C, yüzde otuz altı. D, yüzde iki yüz yirmi.",
     "Doğru cevap C: sıfır virgül dokuz çarpı sıfır virgül sekiz çarpı sıfır virgül beş, yani sıfır virgül otuz altı; yüzde otuz altı.")
soru("Bilgi kontrolü 4/5", "Onaylanıp sözleşmesi imzalanmayan başvurular hangi israf türüdür?",
     ["Bekleme", "Yarım iş", "Fazla özellik", "Kahramanlık"], 1,
     "Dördüncü soru: onaylanıp sözleşmesi imzalanmayan başvurular hangi israf türüdür? A, bekleme. B, yarım iş. C, fazla özellik. D, kahramanlık.",
     "Doğru cevap B: yarım iş, kod PD.")
soru("Bilgi kontrolü 5/5", "Darboğaz olmayan bir adımı iki kat hızlandırırsan ne olur?",
     ["Toplam süre yarıya iner", "Toplam süre değişmez, darboğaz önünde kuyruk büyür", "%C/A artar", "Devir sayısı azalır"], 1,
     "Beşinci soru: darboğaz olmayan bir adımı iki kat hızlandırırsan ne olur? A, toplam süre yarıya iner. "
     "B, toplam süre değişmez, darboğaz önünde kuyruk büyür. C, yüzde C bölü A artar. D, devir sayısı azalır.",
     "Doğru cevap B. Tek kısıt kuralı: {throughput}'u darboğaz belirler.")

# ───────────────────────────── Hızlı başvuru ve çözüm
m("Hızlı başvuru: VSM yapma sırası", ["1. Sınır: ilk tetikleyici ve son çıktı", "2. 5–7 ana adım ve sahibi (şerit)",
                                      "3. İşlem, öncesindeki bekleme, %C/A; bilinmeyene \"?\"", "4. VA / NNVA / İsraf + israf harf kodu",
                                      "5. Metrik kartı · 6. Darboğaz + 5 Neden · 7. Tek iyileştirme ve beklenen metrik"],
  "Hızlı başvuru: VSM yapma sırası, yedi adım. Bir: sürecin sınırını yaz; ilk tetikleyici ve son çıktı. "
  "İki: beş ile yedi ana adımı ve sahibini, yani şeridini listele. "
  "Üç: her adım için işlem süresi, öncesindeki bekleme ve yüzde C bölü A topla; bilinmeyene soru işareti yaz. "
  "Dört: her adımı VA, NNVA ya da israf diye işaretle, israflara harf kodunu yaz. Beş: metrik kartını hesapla. "
  "Altı: darboğazı seç, beş neden ile kök nedeni bul. "
  "Yedi: tek bir iyileştirme öner ve hangi metriği ne kadar değiştirmesini beklediğini yaz.", bolum="Süreç · Çözümler")
t("Çözüm: metrikler", ["Metrik", "Hesap", "Sonuç"],
  [["Toplam işlem", "10 + 15 + 10 + 5", "40 dk"], ["Toplam süre", "40 + (240 + 2.880 + 480 + 60)", "3.700 dk (≈ 61,7 saat)"],
   ["Aktivite oranı", "40 ÷ 3.700", "%1,1"], ["Zincirleme %C/A", "0,95 × 0,60 × 0,90 × 0,98", "%50,3"],
   ["Devir sayısı", "Operasyon → Müşteri/Bayi → Operasyon", "2"]],
  "Bağımsız görevin çözümü. Toplam işlem süresi: on artı on beş artı on artı beş, kırk dakika. "
  "Toplam süre: kırk artı iki yüz kırk, iki bin sekiz yüz seksen, dört yüz seksen ve altmış; yani üç bin yedi yüz dakika, yaklaşık altmış bir virgül yedi saat. "
  "Aktivite oranı: kırk bölü üç bin yedi yüz, yüzde bir virgül bir. "
  "Zincirleme oran: sıfır virgül doksan beş çarpı sıfır virgül altmış çarpı sıfır virgül doksan çarpı sıfır virgül doksan sekiz, yüzde elli virgül üç. "
  "Yani her iki poliçeden biri en az bir kez geri dönüyor. "
  "Devir sayısı: operasyondan müşteri ya da bayiye, oradan tekrar operasyona; iki.")
m("Çözüm: sınıflar, darboğaz, öneri", ["Sınıflar: 1–4 hepsi NNVA", "En büyük gecikme: Adım 2 (2.880 dk, %60)",
                                       "Öneri: kontrol listesi + Portal'da 2 zorunlu alan", "Etki: Adım 2 ↑, Adım 3 geri gönderim ↓"],
  "Sınıflar: dört adımın hepsi NNVA, yani gerekli ama değer katmayan; ikinci adım mevzuat ve sözleşme gereği. "
  "Bu süreçte müşteriye doğrudan değer katan adım yok; amaç süreyi ve geri dönüşü azaltmak. "
  "En büyük gecikme kaynağı ikinci adım: en uzun bekleme, iki bin sekiz yüz seksen dakika, ve en düşük oran, yüzde altmış, aynı adımda. "
  "Geri dönen poliçeler on beş günlük süreyi tüketir. "
  "Tek öneri: hatırlatma mesajına muafiyetsiz olmalı ve dain-i mürtehin Firma olmalı kontrol listesini ekle; "
  "bayi portalında poliçe yüklenirken bu iki alanı zorunlu yap. "
  "Beklenen etki: ikinci adımın oranı yükselir, üçüncü adımdaki geri gönderimler azalır. "
  "Hedef değeri tahminle yazma: önce mevcut oranı ölç, hedefi bu ölçüme göre öner; gerçek projede iş birimiyle birlikte kesinleşir.")
m("Bu videoda neler gördük?", ["Hangi soruya hangi diyagram; akış şeması, SIPOC", "Swimlane kuralları, seviyeler, VSM ve metrikler",
                               "TIMWOODS, DFD, as-is → to-be, process mining, EPC", "Laboratuvar, 3 renk, 8 israf, metrik kartı, tek kısıt",
                               "Bağımsız görev ve çözüm"],
  "Toparlayalım. Hangi soruya hangi diyagramın uyduğunu, akış şeması sembollerini ve SIPOC'u gördük. "
  "{Swimlane} kurallarını, süreç seviyelerini, VSM'i ve metriklerini öğrendik. TIMWOODS, DFD, {as-is}'ten {to-be}'ye dönüşüm, "
  "süreç madenciliği ve EPC'ye değindik. Laboratuvarı, üç renk sınıflamasını, sekiz israfı, metrik kartını ve tek kısıt kuralını çalıştık. "
  "Bağımsız görevi de çözdük. Bir sonraki videoda Firma diyagram okuma atölyesine geçiyoruz: beş gerçek diyagramı adım adım okuyacağız.", ton="sakin")

kaydet(__file__, {
    "baslik": "Business Analyst Teknik Rehberi · 4: Süreç diyagramlama",
    "alt_baslik": "SIPOC · swimlane · değer akışı · israf · metrikler · process mining",
    "kapanis": "Sıradaki video: Diyagram okuma atölyesi",
    "tema": 4,
    "youtube_baslik": "Business Analyst Teknik Rehberi 4/14: Süreç diyagramlama (SIPOC, swimlane, VSM, israf)",
    "etiketler": ["business analyst", "süreç diyagramı", "SIPOC", "swimlane", "value stream map", "lean", "iş analisti"],
}, {"SIPOC": "sipok", "VSM": "vi es em", "DFD": "di ef di", "EPC": "i pi si", "APQC": "ey pi kyu si", "PCF": "pi si ef",
    "RCM": "ar si em", "RACI": "reysi", "RPA": "ar pi ey", "BPM": "bi pi em", "SLA": "es el ey", "SBM": "es be me",
    "TRAMER": "tramer", "TIMWOODS": "timvuds", "NNVA": "en en vi ey", "UNVA": "yu en vi ey", "VA": "vi ey", "RFPY": "ar ef pi uay",
    "PT": "pi ti", "LT": "el ti", "%C/A": "yüzde si bölü ey", "BSV-1001": "be se ve bin bir", "app.diagrams.net": "ap nokta dayagrams nokta net",
    "Ishikawa": "işikava", "ANSI": "ensi", "PD": "pi di", "TS": "ti es", "EP": "i pi", "EF": "i ef"})
