#!/usr/bin/env python3
"""BA Teknik Rehberi · Video 10: Jira. Belge satır 2851–3212."""
from ortak import m, t, dikkat, g, soru, kaydet

# ───────────────────────────── Giriş
m("Jira nedir? Yeni terimler", ["Atlassian'ın iş takibi ve proje yönetimi ürünü", "Agile ekiplerde backlog, sprint, board, sürüm için fiili standart",
                                "Jira Software + Jira Work Management → tek ürün \"Jira\"", "Cloud: issue → work item · issue type → work type · project → space",
                                "Data Center'da eski terimler sürebilir; mülakatta ikisini de bil"],
  "Jira, {Atlassian}'ın iş takibi ve proje yönetimi ürünüdür; Agile ekipler için {backlog}, {sprint}, {board} ve sürüm yönetiminde fiili standarttır. "
  "Son dönemde önemli terminoloji değişiklikleri oldu: {Jira Software} ve {Jira Work Management} tek ürün, yani Jira altında birleşti. "
  "{Jira Cloud}'da {issue} yerine {work item}, yani iş öğesi; {issue type} yerine {work type}; ve {project} yerine {space} terimleri kullanılmaya başlandı. "
  "Kurumun {Data Center}, yani kendi sunucusunda kurulu sürümü kullanıyorsa eski terimleri görmeye devam edebilirsin; mülakatta iki terimi de bildiğini göstermek avantajdır.",
  bolum="Jira: giriş ve hedefler", kanca="Gereksinimin doğduğu yerden teslim edildiği yere kadar her adım.", ton="merakli")
m("BA için Jira ve hedefler", ["Gereksinim yaşam döngüsü · sağlıklı backlog · izlenebilirlik · raporlama",
                               "INVEST'e uyan, ≥ 3 kabul kriterli story (normal, uç durum, hatalı giriş)",
                               "Günlük soruları farklı workflow'larda çalışan JQL'e çevirmek",
                               "Story workflow'u: her durumun çıkışı ve geçiş koşulları", "Pano ve raporlardan iki cümlelik sprint özeti"],
  "İş analisti için Jira; gereksinimin yaşam döngüsünü yönetmek, {backlog}'u sağlıklı tutmak, izlenebilirlik kurmak ve ilerlemeyi raporlamak demektir. "
  "Bu bölümü bitirdiğinde şunları yapabileceksin. Bir: Firma kurallarından INVEST'e uyan, en az üç kabul kriterli {user story} yazmak; "
  "normal akış, uç durum ve hatalı giriş. İki: açık işler, engelliler, bu sprint gibi günlük soruları farklı {workflow}'larda da çalışan JQL'e çevirmek. "
  "Üç: bir {story} {workflow}'u tasarlayıp her durumun çıkış yolunu ve geçiş koşullarını tanımlamak. "
  "Dört: sprint panosunu ve raporları okuyarak bir sprint hakkında iki cümlelik durum özeti yazmak.")
t("Başlamadan önce gerekenler", ["Gereken", "Nereden", "Hazır mısın?"],
  [["Jira Cloud (ücretsiz plan)", "atlassian.com → Jira → Get it free", "Solda Spaces ve Filters"], ["Scrum şablonlu proje", "Spaces → Create space → Scrum", "Backlog ve Board var"],
   ["User story kalıbı", "Temel seviye", "\"Bir [rol] olarak …\""], ["Firma kuralları", "Çalışma Seti §1.3", "U04 ve U08 kuralları"]],
  "Başlamadan önce gerekenler. {Jira Cloud} hesabı; küçük ekipler için ücretsiz plan: atlassian nokta com, Jira, {Get it free}. "
  "Sol menüde {Spaces}, eski adıyla {Projects}, ve {Filters} görünüyorsa tamam. "
  "Scrum şablonlu bir proje: {Spaces}, {Create space}, eski adıyla {Projects}, {Create project}, sonra {Scrum}. Sol menüde {Backlog} ve {Board} varsa tamam. "
  "{User story} kalıbı: bu bölümün temel seviyesi; bir rol olarak, şunu istiyorum, böylece cümlesini kurabiliyorsan tamam. "
  "Firma kuralları: çalışma setinin bir nokta üç bölümü; U04 ve U08 kurallarını biliyorsan başlayabiliriz.")

# ───────────────────────────── Temel
t("İş öğesi hiyerarşisi", ["Seviye", "Tip", "Örnek"],
  [["(Premium, Plans)", "Initiative / Theme", "Dijital kredi yolculuğu 2026"], ["1", "Epic", "Bayi portalından uçtan uca dijital başvuru"],
   ["0", "Story · Task · Bug", "KVKK onayı SMS ile · KKB test erişimi · son taksit 1 kuruş farkı"], ["-1", "Sub-task", "API endpoint, birim test, UI"]],
  "Temel seviye: iş öğesi hiyerarşisi. En üstte, Premium ve {Plans} ile, {Initiative} ya da {Theme}: dijital kredi yolculuğu iki bin yirmi altı. "
  "Bir seviyesinde {Epic}: bayi portalından uçtan uca dijital başvuru. "
  "Sıfır seviyesinde üç tip. {Story}: bayi olarak müşterinin KVKK onayını SMS ile almak istiyorum. {Task}: KKB test ortamı erişimi talep et. "
  "{Bug}: ödeme planında son taksit bir kuruş fark ediyor. "
  "Eksi bir seviyesinde {Sub-task}: {API} {endpoint} geliştirme, birim test, arayüz.", bolum="Jira · Temel seviye")
m("User story ve INVEST", ["\"Bir [rol] olarak, [amaç] için [ihtiyaç] istiyorum.\"", "Independent · Negotiable · Valuable",
                           "Estimable · Small · Testable"],
  "{User story} formatı: bir rol olarak, amaç için ihtiyaç istiyorum. İyi bir {story} INVEST kriterlerine uyar: "
  "{Independent}, bağımsız; {Negotiable}, pazarlığa açık; {Valuable}, değerli; {Estimable}, tahmin edilebilir; {Small}, küçük; {Testable}, test edilebilir.")
m("Kabul kriteri (Gherkin)", ["Senaryo: bireyselde kredi/değer üst sınırı aşılıyor", "Diyelim ki fatura 400.000 TL ve azami oran %70",
                              "Eğer ki bayi Portal'da 300.000 ₺ girerse", "O zaman \"Kredi tutarı en fazla 280.000 ₺ olabilir (kredi/değer %70)\"",
                              "Ve \"Devam\" düğmesi pasif olmalı"],
  "Kabul kriteri, {Gherkin} biçiminde. Senaryo: bireysel kredide kredi değer üst sınırı aşılıyor. "
  "Diyelim ki müşteri bireysel ve aracın fatura bedeli dört yüz bin TL; ve bu bedel için azami kredi değer oranı yüzde yetmiş. "
  "Eğer ki bayi Portal'da kredi tutarına üç yüz bin lira girerse, o zaman sistem şu uyarıyı göstermeli: "
  "kredi tutarı en fazla iki yüz seksen bin lira olabilir, kredi değer yüzde yetmiş. Ve devam düğmesi pasif olmalı.")
m("Temel alanlar ve board türleri", ["Summary, Description, Priority, Assignee, Reporter", "Labels, Components, Fix Version, Sprint, Story Points", "Linked: blocks, relates to, duplicates", "Scrum board · Kanban board", "Team-managed · Company-managed"],
  "Temel alanlar: {Summary}, {Description}, {Priority}, {Assignee}, {Reporter}, {Labels}, {Components}, {Fix Version}, {Sprint}, {Story Points}, {Due date} "
  "ve bağlı iş öğeleri: {blocks}, {is blocked by}, {relates to}, {duplicates}, {clones}. "
  "{Board} türleri: {Scrum board}, sprint ve {backlog}; {Kanban board}, sürekli akış ve WIP limiti. "
  "{Space} şablonlarında iki seçenek var: {team-managed}, ekip kendi yönetir, basit; ve {company-managed}, yöneticilerin paylaşılan şemalarla yönettiği, kurumsal.")

# ───────────────────────────── Orta
m("Workflow tasarımı", ["Kategoriler: To Do · In Progress · Done", "Geçişe condition (yalnız atanan kişi)",
                        "Validator (zorunlu alan; Done'da Fix Version) · post-function (çözüm alanı, bildirim)",
                        "Backlog → Analizde → Hazır (DoR) → Geliştirmede → Kod İncelemede → Testte → UAT → Done"],
  "Orta seviye: {workflow} tasarımı. Durumlar, yani {status}'ler, üç kategoriye ayrılır: {To Do}, {In Progress} ve {Done}. "
  "Geçişlere, yani {transition}'lara üç şey eklenir: koşul, yani {condition}, örneğin sadece atanan kişi; "
  "doğrulayıcı, yani {validator}, örneğin {Done}'a geçerken {Fix Version} zorunlu; ve sonrası işlev, yani {post-function}, örneğin çözüm alanını doldur, bildirim gönder. "
  "Örnek {story} {workflow}'u: {Backlog}, analizde, hazır yani DoR, geliştirmede, kod incelemede, testte, UAT ve {Done}.", bolum="Jira · Orta seviye")
t("Definition of Ready ve Done", ["DoR (sprint'e alınabilir)", "DoD (tamamlandı)"],
  [["Story INVEST'e uygun", "Kod gözden geçirildi, birleştirildi"], ["Kabul kriterleri yazıldı, PO onayladı", "Kabul kriterleri test edildi, geçti"],
   ["Bağımlılıklar biliniyor / çözüldü", "Regresyon ve otomasyon güncel"], ["Tasarım / wireframe eklendi", "Confluence güncellendi"],
   ["Tahmin yapıldı", "Güvenlik ve loglama karşılandı"]],
  "{Definition of Ready}, kısaca DoR, yani sprint'e alınabilir; ve {Definition of Done}, kısaca DoD, yani tamamlandı. "
  "DoR: {story} INVEST'e uygun; kabul kriterleri yazıldı ve PO onayladı; bağımlılıklar biliniyor ya da çözüldü; tasarım ya da {wireframe} eklendi; tahmin yapıldı. "
  "DoD: kod gözden geçirildi ve birleştirildi; kabul kriterleri test edildi, testler geçti; regresyon ve otomasyon testleri güncel; "
  "dokümantasyon, yani Confluence, güncellendi; güvenlik ve loglama gereksinimleri karşılandı.")
m("JQL örnekleri (1/2)", ["Aktif sprintteki tamamlanmamış story'lerim: project = KRD AND sprint in openSprints() AND type = Story AND assignee = currentUser() AND statusCategory != Done",
                          "Son 14 günde açılan, yüksek öncelikli, çözülmemiş hatalar: type = Bug AND priority in (Highest, High) AND created >= -14d AND resolution = EMPTY",
                          "Kabul kriteri boş, \"Hazır\" story'ler: status = \"Hazır\" AND \"Kabul Kriterleri\" is EMPTY"],
  "JQL, yani {Jira Query Language}. Birinci örnek, aktif sprintteki tamamlanmamış {story}'lerim: {project} eşittir KRD {AND} {sprint in openSprints} {AND} {type} eşittir {Story} "
  "{AND} {assignee} eşittir {currentUser} {AND} {statusCategory} eşit değildir {Done}. "
  "İkinci örnek, son on dört günde açılan, yüksek öncelikli, çözülmemiş hatalar: {project in} KRD ve SGR; {type} eşittir {Bug}; {priority in} {Highest} ve {High}; "
  "{created} büyük eşit eksi on dört gün; {resolution} eşittir {EMPTY}; önceliğe göre azalan, oluşturulmaya göre artan sıralı. "
  "Üçüncü örnek, kabul kriteri alanı boş olan ve sprinte alınmaya hazır görünen {story}'ler: {status} eşittir hazır {AND} kabul kriterleri {is EMPTY}.")
m("JQL örnekleri (2/2)", ["parent = KRD-120", "status changed to \"UAT\" during (-7d, now())", "statusCategory != Done AND updated <= -30d", "Operatörler: ~, IN, IS EMPTY, WAS, CHANGED", "currentUser(), openSprints(), startOfWeek()"],
  "Dördüncü örnek, bir {epic} altındaki tüm işler: {parent} eşittir KRD-120. "
  "Beşinci örnek, son bir haftada durumu UAT'ye geçenler: {status changed to} UAT {during}, eksi yedi gün ile {now}. "
  "Altıncı örnek, otuz gündür güncellenmeyen açık işler, yani {backlog} temizliği: {statusCategory} eşit değildir {Done} {AND} {updated} küçük eşit eksi otuz gün. "
  "Operatörler: eşittir, eşit değildir, dalga yani içerir, {IN}, {NOT IN}, {IS EMPTY}, {WAS}, {CHANGED}, {BEFORE}, {AFTER}, {DURING}. "
  "Fonksiyonlar: {currentUser}, {openSprints}, {startOfWeek}, {endOfMonth} ve {membersOf}.")
m("Raporlar", ["Burndown: sprintte kalan iş · Burnup: kapsam ve tamamlanan", "Velocity: sprint başı tamamlanan puan",
               "Cumulative Flow Diagram: darboğaz · Control Chart: cycle time", "Sprint Report · Version Report",
               "Dashboard: kayıtlı JQL (filtre) tabanlı gadget'lar"],
  "Raporlar: {Burndown}, sprint içinde kalan iş; {Burnup}, kapsam ve tamamlanan; {Velocity}, sprint başı tamamlanan puan; "
  "{Cumulative Flow Diagram}, darboğaz tespiti; {Control Chart}, {cycle time}; {Sprint Report} ve {Version Report}. "
  "{Dashboard}'lar filtre, yani kayıtlı JQL tabanlı {gadget}'larla kurulur.")

# ───────────────────────────── İleri
m("Jira Automation", ["Tetikleyici → koşul → aksiyon", "Tüm sub-task'lar Done → üst story \"Testte\"",
                      "Highest bug → Teams bildirimi + on-call'a ata", "\"Hazır\"a geçerken kabul kriteri boş → geri al, yorum ekle",
                      "Her pazartesi 30 gündür dokunulmamış işler → PO'ya e-posta"],
  "İleri seviye: {Jira Automation}. Mantık: tetikleyici, koşul, aksiyon. Örnekler: tüm {sub-task}'lar {Done} olunca üst {story}'yi testte durumuna taşı. "
  "{Highest} öncelikli bir {bug} açılırsa {Teams} kanalına bildirim gönder ve {on-call} kişiye ata. "
  "{Story} hazır durumuna geçerken kabul kriteri boşsa geri al ve yorum ekle. "
  "Her pazartesi otuz gündür dokunulmamış işleri PO'ya e-postayla listele. "
  "{Smart value} örneği: {issue.key} tire {issue.summary} UAT'ye alındı; sorumlu {issue.assignee.displayName}.", bolum="Jira · İleri seviye")
m("Planlama, test, izlenebilirlik", ["Plans (eski Advanced Roadmaps, Premium): kapasite, bağımlılık, sürüm · Timeline",
                                     "Jira Product Discovery: fikir ve önceliklendirme (RICE, değer/efor)",
                                     "Xray, Zephyr: Test, Test Set, Test Plan, Test Execution · kapsama raporu",
                                     "İzlenebilirlik: hedef (Confluence) → Epic → Story → Test → Bug → Release"],
  "Planlama ve ölçek: {Plans}, eski adıyla {Advanced Roadmaps}, Premium; birden çok ekip ve {space} boyunca kapasite, bağımlılık ve sürüm planlaması; "
  "{Timeline} görünümü; ve {Jira Product Discovery} ile fikir ve önceliklendirme yönetimi, yani RICE ya da değer bölü efor. "
  "Test yönetimi: {Xray}, {Zephyr} gibi eklentilerle {Test}, {Test Set}, {Test Plan}, {Test Execution} iş tipleri; {story} ile test kapsama raporu; "
  "{Gherkin} senaryolarının otomasyon sonuçlarının Jira'ya geri yazılması. "
  "İzlenebilirlik, yani {traceability}: iş hedefi Confluence'ta, sonra {Epic}, {Story}, {Test}, {Bug}, {Release}. "
  "Gereksinim matrisi Confluence'ta Jira makrolarıyla canlı tutulur. Denetimde şu soru cevaplanabilir olmalı: "
  "bu değişiklik hangi gereksinime, hangi teste, hangi onaya dayanıyor?")
m("Yönetişim, entegrasyonlar, metrikler", ["Şemalar: workflow, field configuration, screen, permission, notification · custom field disiplini",
                                           "En az yetki · work item security level · TCKN ve müşteri verisi eklenmez / maskelenir",
                                           "Bitbucket/GitHub/GitLab (KRD-245 commit) · CI/CD · Confluence · Slack/Teams · JSM · Rovo",
                                           "Velocity tek başına değil: lead time, cycle time, throughput, WIP, escaped defects, sprint hedefi"],
  "Yönetişim: {space} şemaları, yani {workflow}, {field configuration}, {screen}, {permission} ve {notification scheme}; "
  "özel alan, yani {custom field} disiplini; her yeni alan performans ve karmaşıklık maliyeti taşır. "
  "İzin şemalarında en az yetki; hassas bilgi için {work item security level}. Kişisel ve müşteri verisi, örneğin TCKN ya da ekran görüntüsünde müşteri bilgisi, "
  "Jira'ya eklenmez ya da maskelenir. "
  "Entegrasyonlar: {Bitbucket}, {GitHub}, {GitLab}; commit, branch ve PR'ın iş öğesine bağlanması, örneğin KRD-245 KKB {timeout} ele alındı mesajı. "
  "CI/CD dağıtım bilgisi, Confluence, {Slack} ve {Teams}, ve {Jira Service Management}; olay ve talep yönetiminden geliştirme {backlog}'una aktarım. "
  "{Rovo} ve yapay zeka özellikleriyle {epic}'i {story}'lere bölme ve özetleme; plan ve lisansa bağlı. "
  "Metrikler: {velocity} tek başına performans ölçüsü değildir; {lead time}, {cycle time}, {throughput}, WIP, kaçan hata yani {escaped defects} "
  "ve sprint hedefine ulaşma oranı birlikte okunur.")

# ───────────────────────────── Hatalar, mülakat
m("Sık yapılan hatalar", ["Story yerine teknik görev (\"API yaz\")", "Kabul kriterlerini yorumlara dağıtmak", "Epic'leri sonsuza kadar açık bırakmak",
                          "Her ekibe farklı workflow ve alan", "Story point'i saat gibi kullanmak, ekipler arası kıyaslamak"],
  "Sık yapılan hatalar. {Story} yerine teknik görev yazmak, örneğin API yaz; kullanıcı değerini kaybetmek. "
  "Kabul kriterlerini yorumlara dağıtmak; tek bir güncel kaynak olmaması. {Epic}'leri sonsuza kadar açık bırakmak, {backlog}'u çöplüğe çevirmek. "
  "Her ekip için farklı {workflow} ve alan açmak; kurumsal raporlamanın imkânsız hale gelmesi. "
  "Ve {story point}'i saat gibi kullanmak ya da ekipler arası karşılaştırmak.", bolum="Jira · Hatalar ve mülakat")
m("Mülakat soruları", ["1. Epic, story, task farkı?", "2. İyi story ve kabul kriteri (örnek)", "3. Aktif sprintte bloklanmış işler JQL'i",
                       "4. DoR ve DoD farkı; BA hangisinden sorumlu?", "5. İzlenebilirlik Jira + Confluence ile", "6. Cumulative Flow Diagram ne söyler?"],
  "Mülakat soruları. Bir: {epic}, {story} ve {task} arasındaki fark nedir? İki: iyi bir {user story} ve kabul kriteri nasıl yazılır? Bir örnek verin. "
  "Üç: aktif sprintte bloklanmış işleri getiren JQL'i yazın. Dört: DoR ve DoD farkı nedir, iş analisti hangisinden daha çok sorumludur? "
  "Beş: gereksinim izlenebilirliğini Jira ve Confluence ile nasıl kurarsınız? Altı: {Cumulative Flow Diagram} size ne söyler?")
m("Cevap ipuçları", ["Epic birkaç sprint · story bir sprint, kullanıcı değeri · task teknik iş", "Persona + değer + ≥ 3 AC (normal, sınır, hata)",
                     "sprint in openSprints() AND (status = Blocked OR Flagged is not EMPTY)", "BA daha çok DoR'dan: hazır story",
                     "Epic → Story → Test, Confluence'ta Jira makrosu · CFD: bant genişliyorsa darboğaz"],
  "İpuçları, bölümün içeriğinden. Bir: {epic} birkaç sprint sürer; {story} bir sprintte biter ve kullanıcı değeri taşır; {task} teknik iştir. "
  "İki: belirli persona, değer cümlesi ve en az üç kabul kriteri; normal, sınır ve hata. "
  "Üç: {sprint in openSprints} {AND}, parantez içinde {status} eşittir {Blocked} {OR} {Flagged is not EMPTY}; engelli kelimesinin anlamını birazdan göreceğiz. "
  "Dört: iş analisti daha çok DoR'dan sorumludur; sprinte hazır {story}. "
  "Beş: {Epic}, {Story} ve {Test} bağları, Confluence'ta Jira makrosuyla canlı matris. "
  "Altı: {Cumulative Flow Diagram}'da bir durumun bandı genişliyorsa orada iş birikiyor, yani darboğaz var.")

# ───────────────────────────── Görsel rehber
g("Jira ekranı nasıl okunur?", "g29.png",
  [([0.02, 0.08, 0.22, 0.95], "1 · Sol gezinme, + Create"), ([0.22, 0.08, 1.0, 0.15], "2 · Arama"),
   ([0.22, 0.15, 1.0, 0.27], "3 · Space başlığı ve sekmeler"), ([0.22, 0.27, 0.72, 0.95], "4 · Board"), ([0.72, 0.27, 1.0, 0.95], "5 · İş öğesi detayı")],
  "Görsel rehber: {Jira Cloud} ekran yerleşimi; şematik, numaralı bölgeler. "
  "Bir, sol gezinme: artı {Create} ile yeni iş öğesi aç. {For you}: sana atananlar ve son çalıştıkların. {Spaces}: takım alanları. "
  "{Filters}: kayıtlı JQL sorguları. {Dashboards}: panolar. {Plans}: çoklu ekip planlaması, Premium. "
  "İki, arama: bölü tuşu hızlı aramayı açar. Gelişmiş arama için {Filters}, {Search work items}, JQL moduna geç. "
  "Üç, {space} başlığı ve sekmeler: {Summary}, {Backlog} yani sprint planlama, {Board} yani aktif sprint, {Timeline} yani {epic} yol haritası, "
  "{Reports} ve {Releases}. Sağdaki üç nokta, {Space settings}. "
  "Dört, {Board}: sütunlar {workflow} durumlarına bağlıdır. Kartı sürüklemek durumu değiştirir; yasak bir geçişse kart bırakılamaz. "
  "Üstte {Quick filters} ve {Group by}, yani {Assignee} ya da {Epic}. "
  "Beş, iş öğesi detayı: kartı tıklayınca sağda açılır. Durum menüsü izin verilen geçişleri listeler. "
  "Alt bölümde açıklama, kabul kriterleri, alt işler, bağlantılar, yorumlar ve geçmiş, yani {History}.", bolum="Jira · Görsel rehber")
dikkat("Arayüz terimleri değişti", "2025: issue → work item, project → space + yeni sol gezinme · Data Center'da üstte yatay menü (Your work, Projects, Filters, Dashboards)",
       "Not: {Atlassian} iki bin yirmi beşte arayüz terimlerini değiştirdi; {issue} oldu {work item}, {project} oldu {space}; ve yeni bir sol gezinme getirdi. "
       "Kurumunda {Data Center} sürümü kullanılıyorsa üstte yatay menü, yani {Your work}, {Projects}, {Filters}, {Dashboards}, ve eski terimler görünür; "
       "menü mantığı aynıdır.", tip="bilgi")
g("Hiyerarşi ve workflow", "g30.png",
  [([0.0, 0.08, 1.0, 0.38], "Initiative → Epic → Story · Task · Bug → Sub-task"), ([0.0, 0.42, 1.0, 0.78], "Workflow: üç kategori, geri dönüşler"),
   ([0.25, 0.86, 0.8, 1.0], "Geçiş kuralları: validator")],
  "İş öğesi hiyerarşisi ve örnek {story} {workflow}'u. Üst satır işin büyükten küçüğe nasıl parçalandığını gösterir: "
  "{Initiative}, dijital kredi iki bin yirmi altı; {Epic}, uçtan uca dijital başvuru; {Story}, {Task} ya da {Bug}, KVKK onayını SMS ile al; "
  "{Sub-task}, SMS servisi entegre. {Initiative} için Premium ya da {Plans} gerekir; {story} bir sprintte biter, {epic} birkaç sprint sürer. "
  "Alt satır bir {story}'nin geçebileceği durumlar: {Backlog}, analizde, hazır; bunlar {To Do} kategorisi. "
  "Geliştirme, testte, UAT; bunlar {In Progress} kategorisi. Ve {Done}. Renkler Jira'nın üç durum kategorisine karşılık gelir; raporlar bu kategorilere göre hesaplanır. "
  "Kesikli oklar geri dönüş geçişleridir: testte ya da UAT'de hata bulunursa {story} geliştirmeye döner; hata bulundu ve UAT reddi. "
  "Alttaki kurallar geçişlere eklenen kontrollerdir: hazır durumuna geçiş için kabul kriteri dolu olmalı, yani {validator}; "
  "{Done}'a geçiş için {Fix version} zorunlu, çözüm alanı otomatik dolar.")
t("Menü rehberi (1/3)", ["Yapmak istediğin", "Yol"],
  [["Yeni space", "Spaces → Create space → Scrum / Kanban"], ["Yeni iş öğesi", "+ Create ya da c → Work type, Summary"],
   ["Story → epic", "Parent alanı → epic"], ["Alt iş · ilişki", "Add child work item · Link work item"],
   ["Sprint başlat", "Backlog → Create sprint → Start sprint"]],
  "Menü ve kısayol rehberi. Yeni {space}: {Spaces}, {Create space}, şablon {Scrum} ya da {Kanban}; {Team-managed} ya da {Company-managed} seç. "
  "Yeni iş öğesi: artı {Create} ya da c tuşu; {Space}, {Work type} yani {Epic}, {Story}, {Task} ya da {Bug}, {Summary} ve {Description}. "
  "{Story}'yi {epic}'e bağlamak: {story} detayı, {Parent} alanı, {epic} seç. Alt iş eklemek: {Add child work item}. "
  "İki işi ilişkilendirmek: {Link work item}; {blocks}, {is blocked by}, {relates to}. "
  "Sprint oluşturup başlatmak: {Backlog}, {Create sprint}, işleri sürükle, {Start sprint}; ad, süre ve sprint hedefi.")
t("Menü rehberi (2/3)", ["Yapmak istediğin", "Yol"],
  [["Sprinti kapat", "Board → Complete sprint"], ["JQL · filtre kaydet", "Search work items → JQL · Save filter"],
   ["Toplu değişiklik", "… → Bulk change"], ["Pano", "Create dashboard → Add gadget"], ["Raporlar · sürüm", "Reports · Releases → Create version"]],
  "Sprinti kapatmak: {Board}, {Complete sprint}; bitmeyen işler {backlog}'a ya da sonraki sprinte. "
  "JQL ile aramak: {Filters}, {Search work items}, JQL moduna geç, sorguyu yaz, {Enter}. Filtre kaydetmek: arama sonucu, {Save filter}; ad ve paylaşım izni. "
  "Toplu değişiklik: arama sonucu, üç nokta, {Bulk change}; {Edit}, {Transition} ya da {Move}. "
  "Pano oluşturmak: {Dashboards}, {Create dashboard}, {Add gadget}; {Filter results}, {Pie chart}, {Created vs. resolved}, {Sprint burndown}. "
  "Raporlar: {Space}, {Reports}; {Burndown}, {Velocity}, {Cumulative flow}, {Control chart}. "
  "Sürüm: {Space}, {Releases}, {Create version}; işe {Fix versions} alanından bağla.")
t("Menü rehberi (3/3)", ["Yapmak istediğin", "Yol"],
  [["Workflow düzenle", "Space settings → Work types → Edit workflow · ⚙ → Workflows"], ["Özel alan", "Work types → alanı sürükle · ⚙ → Fields"],
   ["Otomasyon", "Space settings → Automation → Create rule"], ["Kısayollar", "c · / · . · i · m · j/k · ?"]],
  "{Workflow} düzenlemek: {team-managed}'da {Space settings}, {Work types}, tip, {Edit workflow}; {company-managed}'da dişli, {Work items}, {Workflows}; yönetici yetkisi gerekir. "
  "Özel alan eklemek: {team-managed}'da {Space settings}, {Work types}, tip, alanı sürükle; {company-managed}'da dişli, {Work items}, {Fields}. "
  "Otomasyon kuralı: {Space settings}, {Automation}, {Create rule}; {Trigger}, {Condition}, {Action}. "
  "Kısayollar: c oluştur; bölü ara; nokta komut menüsü; i bana ata; m yorum; j ve k sonraki ve önceki; soru işareti tüm kısayollar.")

# ───────────────────────────── Laboratuvar
m("Laboratuvar (~90 dk): 1–5", ["1. Create space → Scrum → Team-managed → \"Kredi Dijital\", KRD",
                                "2. Story workflow: Analizde, Testte, UAT + Testte → In Progress · Board settings → Columns",
                                "3. Özel alan: \"Kabul Kriterleri\" (paragraph)", "4. Epic: \"Bayi portalından uçtan uca dijital başvuru\"",
                                "5. 5 story + Parent + Gherkin AC"],
  "Laboratuvar: bir sprinti baştan sona yönet; yaklaşık doksan dakika. {Atlassian}'ın ücretsiz planıyla kendi {Jira Cloud} sitende yapılabilir. "
  "Bir, {space}: {Spaces}, {Create space}, {Scrum}, {Team-managed}; adı kredi dijital, anahtarı KRD. "
  "İki, {workflow}: {Space settings}, {Work types}, {Story}, {Edit workflow}. Analizde, testte ve UAT durumlarını ekle; "
  "testte durumundan {In Progress}'e geri geçişi tanımla. {Board} sütunlarını {Board settings}, {Columns}'tan eşle. "
  "Üç, özel alan: {Story} tipine kabul kriterleri adlı, {paragraph} türünde bir alan ekle. "
  "Dört, {epic}: artı {Create}, {Epic}; bayi portalından uçtan uca dijital başvuru. "
  "Beş, {story}'ler: beş {story} oluştur, her birinin {Parent} alanına {epic}'i seç ve {Gherkin} kabul kriteri yaz. "
  "Örnekler: KVKK onayını SMS ile al; kredi değer üst sınır uyarısı; ödeme planı hesaplama; KKB zaman aşımında manuel incelemeye alma; başvuru durum sorgulama.",
  bolum="Jira · Laboratuvar")
m("Laboratuvar: 6–10", ["6. Ödeme planı → is blocked by → \"Faiz tablosu servisi\" (Task)", "7. Story points: 3, 2, 5, 3, 2",
                        "8. Create sprint → 3 story → Start sprint; hedef: \"Bayi başvuruyu KVKK onayıyla gönderebilir\"",
                        "9. Kartları taşı; birini Testte'den geri al, History", "10. JQL filtreleri: \"Aktif sprint – açık işler\" · kabul kriteri eksik story'ler"],
  "Altı, bağlantı: ödeme planı {story}'sine {Link}, {is blocked by}, faiz tablosu servisi adlı yeni bir {Task}. "
  "Yedi, tahmin: {story points} üç, iki, beş, üç, iki. "
  "Sekiz, sprint: {Backlog}, {Create sprint}, üç {story}'yi sürükle, {Start sprint}; hedef: bayi başvuruyu KVKK onayıyla gönderebilir. "
  "Dokuz, {board}: kartları durumlar arasında taşı; birini testte durumundan geri {In Progress}'e götür ve {History} sekmesinde kaydı gör. "
  "On, JQL: {Filters}, {Search work items}; {project} eşittir KRD {AND} {sprint in openSprints} {AND} {statusCategory} eşit değildir {Done} {ORDER BY} {rank}. "
  "Aktif sprint, açık işler adıyla kaydet. İkinci filtre: {project} eşittir KRD {AND} {type} eşittir {Story} {AND} kabul kriterleri {is EMPTY}; "
  "yani kabul kriteri eksik {story}'ler.")
m("Laboratuvar: son adımlar", ["Pano: Filter results + Pie chart (Status) + Sprint burndown",
                               "Otomasyon: Work item transitioned (→ Testte) → Add comment \"{{issue.key}} teste alındı…\" → Turn on",
                               "Complete sprint → Sprint report ve Velocity", "BA çıktısı: 5 maddelik demo + 3 \"gereksinim kalitesi\" gözlemi"],
  "Pano: {Dashboards}, {Create dashboard}; {gadget}'lar: birinci filtreyle {Filter results}, {Status}'a göre {Pie chart} ve {Sprint burndown}. "
  "Otomasyon: {Space settings}, {Automation}, {Create rule}. {Trigger}: {Work item transitioned}, testte durumuna. "
  "{Action}: {Add comment}; {issue.key} teste alındı, test sorumlusu bilgilendirildi. {Turn on}. Bir kartı testte durumuna taşıyıp yorumun eklendiğini gör. "
  "Sprinti kapat: {Board}, {Complete sprint}; sonra {Reports}, {Sprint report} ve {Velocity}'yi incele. "
  "İş analisti çıktısı: {sprint review} için beş maddelik demo senaryosu, retrospektif için gereksinim kalitesi hakkında üç gözlem yaz.")

# ───────────────────────────── Uygulama paketi
m("Taşınabilir JQL", ["Her proje kendi workflow'u: \"Open\", \"To Do\", \"Yapılacak\"", "Ama her durum üç kategoriden birine bağlı: To Do, In Progress, Done",
                      "Genel sorularda durum adı yerine kategori", "Belirli adım soruluyorsa durum adı: status = \"UAT\""],
  "Jira uygulama paketi. Taşınabilir JQL: günlük dilden güvenli sorguya. Her proje kendi {workflow}'unu tanımlar: bir projede {Open}, diğerinde {To Do}, "
  "üçüncüsünde yapılacak olabilir. Ama Jira her durumu üç sabit kategoriden birine bağlar: {To Do}, {In Progress} ve {Done}. "
  "Bu yüzden açık işler gibi genel sorularda durum adı yerine kategori kullan. "
  "Belirli bir adımı soruyorsan, örneğin UAT bekleyenler, durum adını kullan: {status} eşittir UAT.", bolum="Jira · Uygulama paketi")
t("Günlük soru → taşınabilir JQL (1/2)", ["Günlük soru", "Kırılgan", "Taşınabilir"],
  [["Açık işler", "status in (Open, …)", "statusCategory != Done"], ["Biten", "status = Closed", "statusCategory = Done"],
   ["Çalışılan", "status = \"In Progress\"", "statusCategory = …"], ["Bana atanmış açık", "assignee = \"ayse.k\"", "currentUser() + kategori"]],
  "Açık işler: kırılgan yazım {status in} {Open}, {To Do}, {Reopened}; taşınabilir yazım {statusCategory} eşit değildir {Done}. "
  "Biten işler: kırılgan {status} eşittir {Closed}; taşınabilir {statusCategory} eşittir {Done}. "
  "Üzerinde çalışılanlar: kırılgan {status} eşittir {In Progress}; taşınabilir {statusCategory} eşittir {In Progress}. "
  "Bana atanmış açık işler: kırılgan {assignee} eşittir ayse nokta k; taşınabilir {assignee} eşittir {currentUser} {AND} {statusCategory} eşit değildir {Done}.")
t("Günlük soru → taşınabilir JQL (2/2)", ["Günlük soru", "Kırılgan", "Taşınabilir"],
  [["14 gün dokunulmayan", "—", "updated < -14d"], ["7 günde açılan", "updated (yanlış)", "created >= -7d"],
   ["Aktif sprint", "sprint = \"KRD Sprint 12\"", "openSprints()"], ["Sprinte alınmamış", "—", "sprint is EMPTY"]],
  "On dört gündür dokunulmayan: {updated} küçüktür eksi on dört gün {AND} {statusCategory} eşit değildir {Done}. "
  "Son yedi günde açılan: kırılgan yazım {updated} büyük eşit eksi yedi gün, yanlış alan; doğrusu {created} büyük eşit eksi yedi gün. "
  "Aktif sprint: kırılgan {sprint} eşittir KRD {Sprint} on iki; taşınabilir {sprint in openSprints}. "
  "Henüz sprinte alınmamış: {sprint is EMPTY} {AND} {statusCategory} eşit değildir {Done}.")
t("\"Engelli\" kelimesinin üç anlamı", ["Anlam", "Nasıl görünür", "JQL"],
  [["\"Blocked\" durumu", "Panoda Blocked sütunu", "status = Blocked"], ["Bayrak (Flagged)", "Sarı zeminli kart", "Flagged is not EMPTY"],
   ["Başka işe bağlılık", "\"is blocked by\" bağlantısı", "issueLinkType = \"is blocked by\""]],
  "Engelli kelimesinin üç anlamı var; biri engelli işleri göster dediğinde hangisini kastettiğini sor. "
  "Bir: {workflow}'da {Blocked} adında bir durum; panoda {Blocked} sütunu; JQL {status} eşittir {Blocked}. "
  "İki: kart üzerinde bayrak, yani {Flagged}; panoda sarı zeminli kart; JQL {Flagged is not EMPTY}. "
  "Üç: başka bir işe bağlılık; {is blocked by} bağlantısı; JQL {issueLinkType} eşittir {is blocked by}. "
  "Belirli bir iş için: {issue in linkedIssues}, KRD-214, {is blocked by}.")
m("Örnek story: KRD-214", ["KKB zaman aşımında başvuruyu manuel incelemeye almak",
                           "Bir bayi satış temsilcisi olarak, KKB yanıt vermediğinde başvurumun kaybolmamasını ve ne olacağını bilmeyi istiyorum",
                           "böylece müşteriye doğru bilgi verip başvuruyu yeniden girmek zorunda kalmam"],
  "Örnek {story}, kalite kontrolünden geçmiş hali: KRD-214, KKB zaman aşımında başvuruyu manuel incelemeye almak. "
  "Bir bayi satış temsilcisi olarak, KKB yanıt vermediğinde başvurumun kaybolmamasını ve ne olacağını bilmeyi istiyorum; "
  "böylece müşteriye doğru bilgi verip başvuruyu yeniden girmek zorunda kalmam.")
m("KRD-214: kabul kriterleri", ["AC1 normal: DEGERLENDIRMEDE, KKB 1,2 sn → uyarı yoksa ONAYLANDI, varsa MANUEL_INCELEME (U08)",
                                "AC2 sınır: KKB tam 5,0 sn → otomatik karar, MANUEL_INCELEME değil",
                                "AC3 zaman aşımı: 5 sn'de yanıt yok → MANUEL_INCELEME + \"Başvurunuz incelemeye alındı, sonuç size bildirilecek.\"",
                                "AC4 hatalı yanıt: hata kodu → MANUEL_INCELEME + hata kodu geçmişe"],
  "Kabul kriterleri, {Scenario}, {Given}, {When}, {Then} biçiminde. AC1, normal akış: başvuru DEGERLENDIRMEDE durumunda ve KKB bir virgül iki saniye içinde skor döndü. "
  "Karar motoru başvuruyu değerlendirdiğinde: kural uyarısı yoksa ONAYLANDI, varsa MANUEL_INCELEME durumuna geçer; U08. "
  "AC2, sınır değeri: KKB yanıtı tam beş virgül sıfır saniyede geldi. Başvuru otomatik karara gider, MANUEL_INCELEME'ye alınmaz. "
  "AC3, zaman aşımı: KKB beş saniye içinde yanıt vermedi. Başvurunun durumu MANUEL_INCELEME olur ve bayi ekranında şu mesaj görünür: "
  "başvurunuz incelemeye alındı, sonuç size bildirilecek. "
  "AC4, hatalı yanıt: KKB beş saniye içinde bir hata kodu döndü. Başvuru MANUEL_INCELEME durumuna alınır ve hata kodu başvuru geçmişine yazılır.")
dikkat("Varsayım ve açık soru", "AC2 \"tam 5,0 sn\" bir varsayım: çalışma seti \"5 sn'yi aşarsa\" diyor, sınır dahil mi yazmıyor. AC4 davranışı tanımsız → açık soru.",
       "Notlara dikkat: AC2'deki tam beş virgül sıfır saniye bir varsayımdır. Çalışma seti beş saniyeyi aşarsa diyor; sınırın dahil olup olmadığı yazılmamış. "
       "Bu eğitimde tam beş virgül sıfır saniye zaman aşımı sayılmaz varsayımıyla ilerle ve {story}'ye açık soru olarak ekle; gerçek projede iş birimine sorarsın. "
       "AC4'ün davranışı da çalışma setinde tanımlı değil; o da açık soru olarak eklenir.")
t("KRD-214 için INVEST", ["INVEST", "Kontrol", "Sonuç"],
  [["Independent", "Başka story bitmeden test?", "Evet, KKB taklit servisiyle"], ["Negotiable", "Mesaj ve hata davranışı tartışılır mı?", "Evet, AC4 açık soru"],
   ["Valuable", "Kimin hangi kaybını önlüyor?", "Bayinin yeniden girmesini"], ["Estimable · Small", "Büyüklük · bir sprint", "Evet · evet"],
   ["Testable", "Her AC için test?", "Evet, 4 test"]],
  "INVEST kontrolü. {Independent}: başka bir {story} bitmeden test edilebiliyor mu? Evet, KKB taklit servisiyle. "
  "{Negotiable}: mesaj metni ve hata davranışı tartışılabilir mi? Evet; AC4 açık soru. "
  "{Valuable}: kimin hangi kaybını önlüyor? Bayinin başvuruyu yeniden girmesini. {Estimable}: ekip büyüklük verebiliyor mu? Evet. "
  "{Small}: bir sprintte biter mi? Evet. {Testable}: her AC için test yazılabiliyor mu? Evet, dört test.")
m("Story kalite kuralları", ["Persona belirli (\"kullanıcı\" değil)", "\"So that\" kısmı \"I want\" kısmını tekrar etmez",
                             "≥ 3 AC: normal, uç durum, hatalı giriş · 8'den fazla AC → böl",
                             "\"Hızlı\", \"kullanıcı dostu\", \"uygun\" yok; mesaj metni ve durum adı aynen"],
  "Kalite kuralları. Persona belirli olmalı; kullanıcı değil. {So that} kısmı {I want} kısmını tekrar etmemeli. "
  "En az üç kabul kriteri olmalı: normal akış, uç durum, hatalı giriş. Sekizden fazla kabul kriteri {story}'nin bölünmesi gerektiğini gösterir. "
  "Hızlı, kullanıcı dostu, uygun gibi ölçülemeyen kelimeler kullanılmaz; mesaj metni ve durum adı aynen yazılır.")
t("Workflow: her durumun bir çıkışı (1/2)", ["Durum", "Kim · koşul", "Çıkışlar"],
  [["To Do", "Ekip", "In Progress"], ["In Progress", "Geliştirici · atanan dolu", "Code Review, Blocked"],
   ["Code Review", "Geliştirici", "In Progress (düzeltme), QA"], ["QA", "Test uzmanı · kabul kriteri dolu", "In Progress (hata), UAT"]],
  "{Workflow} tasarımı: her durumun bir çıkışı olmalı. {To Do}: ekip taşır; çıkış {In Progress}. "
  "{In Progress}: geliştirici taşır; koşul, atanan kişi dolu olmalı; çıkışlar {Code Review} ve {Blocked}. "
  "{Code Review}: geliştirici; çıkışlar düzeltme için {In Progress} ve QA. "
  "QA: test uzmanı; koşul, kabul kriteri alanı dolu olmalı; çıkışlar hata için {In Progress} ve UAT.")
t("Workflow: her durumun bir çıkışı (2/2)", ["Durum", "Kim · koşul", "Çıkışlar"],
  [["UAT", "BA / iş birimi · yalnız BA ve PO", "Done, In Progress"], ["Blocked", "Herkes · engel açıklaması", "In Progress"],
   ["Done", "PO · Resolution dolu", "(Reopen yalnız PO)"]],
  "UAT: iş analisti ya da iş birimi; koşul, yalnızca BA ve PO rolü taşıyabilir; çıkışlar {Done} ve {In Progress}. "
  "{Blocked}: herkes taşıyabilir; koşul, engel açıklaması yazılmalı; çıkış {In Progress}. "
  "{Done}: PO taşır; koşul, {Resolution} alanı dolmalı; yeniden açma, yani {Reopen}, yalnızca PO. "
  "{Blocked}'tan çıkış yoksa işler orada kalır ve raporları bozar. {Done}'a geçerken {Resolution} doldurulmazsa iş bazı raporlarda hâlâ çözülmemiş görünür.")

# ───────────────────────────── Bağımsız görev, sorun giderme, bilgi kontrolü
m("Bağımsız görev", ["1. U08: \"Taslakta 30 gün işlem görmeyen başvuru otomatik iptal\" → story + ≥ 3 AC + INVEST",
                     "2a. Bu sprintte bana atanmış, bitmemiş story'ler", "2b. 10 gündür güncellenmeyen açık Bug'lar, en eskisi üstte",
                     "2c. Bayraklı ve yüksek öncelikli açık işler"],
  "Bağımsız görev. Bir: U08 kuralı için bir {story} yaz: taslak durumunda otuz gün işlem görmeyen başvuru otomatik iptal edilir. "
  "En az üç kabul kriteri, yani normal, sınır ve hatalı ya da istisna, ve INVEST tablosu olsun. "
  "İki: üç soruyu JQL'e çevir; proje anahtarı KRD. A: bu sprintteki, bana atanmış, bitmemiş {story}'ler. "
  "B: on gündür güncellenmeyen açık hatalar, yani {Bug}, en eskisi üstte. C: bayraklı, yani {Flagged}, ve yüksek öncelikli tüm açık işler.",
  bolum="Jira · Bağımsız görev ve sorun giderme")
t("Sorun giderme (1/2)", ["Belirti", "Olası neden", "Çözüm"],
  [["openSprints() sonuç yok", "Proje Kanban; sprint yok", "Scrum proje ya da durum/tarih koşulu"],
   ["\"The value 'Bug' does not exist\"", "Tip adı farklı (\"Hata\")", "type = yaz, otomatik tamamlamayı kullan"],
   ["Story backlog'da, panoda yok", "Filtre kapsamıyor ya da sprintte değil", "Board settings → Columns eşlemesi"]],
  "Sorun giderme. {sprint in openSprints} hiç sonuç döndürmüyorsa: proje Kanban şablonlu, sprint kullanılmıyor. "
  "Scrum şablonlu proje kullan ya da sprint koşulu yerine durum ya da tarih koşulu yaz. "
  "JQL {The value} {Bug} {does not exist for the field} {type} diyorsa: iş tipi adı farklı, örneğin Türkçe arayüzde hata. "
  "Sorgu kutusunda {type} eşittir yazıp otomatik tamamlamadaki değerleri kullan. "
  "{Story} {backlog}'da var ama panoda yoksa: pano filtresi bu iş tipini ya da durumu kapsamıyor, ya da iş sprintte değil. "
  "{Board settings}, {Columns}'ta durumun bir sütuna eşlendiğini kontrol et.")
t("Sorun giderme (2/2)", ["Belirti", "Olası neden", "Çözüm"],
  [["Kart sütuna sürüklenmiyor", "Geçiş yok ya da koşul sağlanmıyor", "Durum düğmesindeki geçiş listesi"],
   ["Burndown düz çizgi", "Puan yok ya da Done'a taşınmamış", "Tahmin gir; Done en sağ sütun mu?"]],
  "Kartı bir sütuna sürükleyemiyorsan: {workflow}'da bu geçiş yok ya da koşulunu sağlamıyorsun. İşi aç, durum düğmesindeki geçiş listesine bak; eksikse yöneticiden iste. "
  "{Burndown} düz çizgiyse: {story}'lere puan girilmemiş ya da işler {Done} sütununa taşınmamış. "
  "Tahmin alanını doldur; {Done} sütununun en sağdaki sütun olduğunu kontrol et.")
soru("Bilgi kontrolü 1/5", "Farklı workflow'lu üç projede \"tüm açık işler\" sorgusu hangisi?",
     ["status = Open", "resolution = Unresolved AND status = \"To Do\"", "statusCategory != Done", "status != Closed"], 2,
     "Beş soruluk bilgi kontrolü. Birinci soru: farklı {workflow}'ları olan üç projede tüm açık işler sorgusu hangisi? "
     "A, {status} eşittir {Open}. B, {resolution} eşittir {Unresolved} {AND} {status} eşittir {To Do}. C, {statusCategory} eşit değildir {Done}. "
     "D, {status} eşit değildir {Closed}.",
     "Doğru cevap C.", bolum="Jira · Bilgi kontrolü ve çözümler")
soru("Bilgi kontrolü 2/5", "\"Son bir haftada açılan hatalar\" için hangi alan?", ["created", "updated", "resolved", "due"], 0,
     "İkinci soru: son bir haftada açılan hatalar için hangi alan kullanılır? A, {created}. B, {updated}. C, {resolved}. D, {due}.",
     "Doğru cevap A: {created}.")
soru("Bilgi kontrolü 3/5", "Bir story'nin 11 kabul kriteri var. Ne yaparsın?",
     ["Puanını artırırım", "Kriterleri tek cümlede birleştiririm", "Bir sonraki sprinte taşırım", "İş kuralı ya da akış adımına göre bölerim"], 3,
     "Üçüncü soru: bir {story}'nin on bir kabul kriteri var. Ne yaparsın? A, puanını artırırım. B, kriterleri tek cümlede birleştiririm. "
     "C, bir sonraki sprinte taşırım. D, {story}'yi iş kuralı ya da akış adımına göre bölerim.",
     "Doğru cevap D: bölerim.")
soru("Bilgi kontrolü 4/5", "Hangi kabul kriteri ölçülebilir?",
     ["\"Ekran hızlı açılmalı\"", "\"Hata mesajı kullanıcı dostu olmalı\"", "\"Vade 61 girilince 'Vade 6–60 ay arasında olmalıdır.' görünür\"", "\"Sistem uygun durumda uyarı vermeli\""], 2,
     "Dördüncü soru: hangi kabul kriteri ölçülebilir? A, ekran hızlı açılmalı. B, hata mesajı kullanıcı dostu olmalı. "
     "C, vade altmış bir girilince vade altı ile altmış ay arasında olmalıdır mesajı görünür. D, sistem uygun durumda uyarı vermeli.",
     "Doğru cevap C.")
soru("Bilgi kontrolü 5/5", "Panoda sarı zeminli kart neyi gösterir?",
     ["Yüksek öncelik", "Bayraklı (Flagged) iş", "Süresi geçmiş iş", "Alt görevli iş"], 1,
     "Beşinci soru: panoda sarı zeminli kart neyi gösterir? A, yüksek öncelik. B, bayraklı, yani {Flagged} iş. C, süresi geçmiş iş. D, alt görevli iş.",
     "Doğru cevap B.")
t("Hızlı başvuru: JQL kalıpları", ["İhtiyaç", "JQL"],
  [["Sprintte bana ait, bitmemiş", "sprint in openSprints() AND assignee = currentUser() AND statusCategory != Done"],
   ["Epic altındakiler · bayraklı", "parent = KRD-120 · Flagged is not EMPTY"], ["Bu hafta teslim", "duedate >= startOfWeek() AND duedate <= endOfWeek()"],
   ["Çözümsüz · metin", "resolution is EMPTY · text ~ \"KKB\""], ["Sıralama", "ORDER BY priority DESC, updated ASC"]],
  "Hızlı başvuru: JQL kalıpları. Bu sprintte bana ait, bitmemiş: {sprint in openSprints} {AND} {assignee} eşittir {currentUser} {AND} {statusCategory} eşit değildir {Done}. "
  "Bir {epic}'in altındakiler: {parent} eşittir KRD-120. Bayraklı: {Flagged is not EMPTY}. "
  "Bu hafta teslim: {duedate} büyük eşit {startOfWeek} {AND} {duedate} küçük eşit {endOfWeek}. "
  "Çözümsüz: {resolution is EMPTY}. Metin araması: {text} dalga KKB. Sıralama: {ORDER BY} {priority} {DESC}, {updated} {ASC}.")
m("Çözüm: KRD-231", ["Persona: bayi satış temsilcisi", "AC1: 31 gün → IPTAL", "AC2: tam 30 gün → iptal yok (açık soru)", "AC3: DEGERLENDIRMEDE → iptal yok"],
  "Bağımsız görevin örnek çözümü. KRD-231: bir bayi satış temsilcisi olarak, otuz gün boyunca işlem yapmadığım taslak başvuruların kendiliğinden iptal edilmesini istiyorum; "
  "böylece başvuru listem yalnızca üzerinde çalışılan kayıtları gösterir. "
  "AC1, normal: taslak başvurunun son işlem tarihi otuz bir gün önce; günlük iptal işi çalışınca başvurunun durumu IPTAL olur, iptal nedeni otuz gün işlem yok yazılır. "
  "AC2, sınır: son işlem tarihi tam otuz gün önce; başvuru iptal edilmez. Varsayım: otuz günü aşınca, yani otuz birinci gün iptal edilir; açık soru. "
  "AC3, istisna: başvuru DEGERLENDIRMEDE durumunda ve otuz günden eski; bu kural nedeniyle iptal edilmez, çünkü kural yalnızca TASLAK durumuna uygulanır.")
dikkat("Açık sorular ve ayrı story", "\"İşlem\" tanımı (alan değişikliği mi, görüntüleme mi?) açık soru · onaydan 30 gün sonra iptal AYRI story",
       "İşlem kelimesinin tanımı, yani alan değişikliği mi, yalnız görüntüleme mi, açık soru olarak eklenmeli. "
       "Onaydan otuz gün sonra iptal kuralı ayrı bir {story}'dir; ikisini birleştirmek kabul kriterlerini karıştırır. "
       "INVEST kontrolü: onay sonrası iptalden bağımsız test edilebilir; işlem tanımı ve otuzuncu gün kararı açık; bayinin listesini temiz tutar, "
       "eski taslaklar yanlışlıkla gönderilmez; günlük iş artı durum değişikliği, tahmin edilebilir; bir sprintte biter; "
       "tarih değiştirilmiş test verisiyle üç senaryo test edilir.", tip="bilgi")
m("Çözüm: JQL", ["a: project = KRD AND type = Story AND sprint in openSprints() AND assignee = currentUser() AND statusCategory != Done",
                 "b: project = KRD AND type = Bug AND statusCategory != Done AND updated < -10d ORDER BY updated ASC",
                 "c: project = KRD AND Flagged is not EMPTY AND priority in (Highest, High) AND statusCategory != Done"],
  "JQL çözümleri. A: {project} eşittir KRD {AND} {type} eşittir {Story} {AND} {sprint in openSprints} {AND} {assignee} eşittir {currentUser} "
  "{AND} {statusCategory} eşit değildir {Done}. "
  "B: {project} eşittir KRD {AND} {type} eşittir {Bug} {AND} {statusCategory} eşit değildir {Done} {AND} {updated} küçüktür eksi on gün, "
  "{ORDER BY} {updated} {ASC}. "
  "C: {project} eşittir KRD {AND} {Flagged is not EMPTY} {AND} {priority in} {Highest}, {High} {AND} {statusCategory} eşit değildir {Done}.")
m("Bu videoda neler gördük?", ["Terimler, hiyerarşi, user story, INVEST, Gherkin, alanlar", "Workflow, DoR/DoD, JQL, raporlar",
                               "Automation, Plans, test, izlenebilirlik, yönetişim, metrikler", "Ekran, menüler, sprint laboratuvarı",
                               "Taşınabilir JQL, örnek story, workflow çıkışları, çözümler"],
  "Toparlayalım. Yeni terimleri, hiyerarşiyi, {user story}'yi, INVEST'i, {Gherkin}'i ve alanları gördük. {Workflow}, DoR ve DoD, JQL ve raporları öğrendik. "
  "Otomasyon, {Plans}, test yönetimi, izlenebilirlik, yönetişim ve metriklere baktık. Ekranı, menüleri ve sprint laboratuvarını çalıştık. "
  "Taşınabilir JQL, örnek {story}, {workflow} çıkışları ve çözümlerle bitirdik. "
  "Bir sonraki videoda Confluence ile gereksinim dokümantasyonuna geçiyoruz.", ton="sakin")

kaydet(__file__, {
    "baslik": "Business Analyst Teknik Rehberi · 10: Jira",
    "alt_baslik": "User story · kabul kriteri · workflow · JQL · raporlar · otomasyon",
    "kapanis": "Sıradaki video: Confluence",
    "tema": 10,
    "youtube_baslik": "Business Analyst Teknik Rehberi 10/14: Jira (user story, JQL, workflow, sprint)",
    "etiketler": ["business analyst", "Jira", "JQL", "user story", "kabul kriteri", "Scrum", "iş analisti"],
}, {"JQL": "cey kyu el", "INVEST": "invest", "DoR": "di o ar", "DoD": "di o di", "PO": "pi o", "QA": "kyu ey", "UAT": "yu ey ti", "WIP": "vip",
    "RICE": "rays", "CI/CD": "si ay si di", "PR": "pi ar", "JSM": "cey es em", "AC": "ey si", "AC1": "ey si bir", "AC2": "ey si iki",
    "AC3": "ey si üç", "AC4": "ey si dört", "AC2'deki": "ey si ikideki", "AC4'ün": "ey si dördün", "KRD": "ka re de", "SGR": "se ge re",
    "KRD-120": "ka re de yüz yirmi", "KRD-214": "ka re de iki yüz on dört", "KRD-231": "ka re de iki yüz otuz bir",
    "KRD-245": "ka re de iki yüz kırk beş", "KRD-247": "ka re de iki yüz kırk yedi", "KRD-250": "ka re de iki yüz elli", "KRD-240": "ka re de iki yüz kırk",
    "DEGERLENDIRMEDE": "değerlendirmede", "ONAYLANDI": "onaylandı", "MANUEL_INCELEME": "manuel inceleme",
    "MANUEL_INCELEME'ye": "manuel incelemeye", "IPTAL": "iptal", "TASLAK": "taslak", "atlassian.com": "ıtlesiın nokta kom",
    "ayse.k": "ayşe nokta ka", "TL": "te le"})
