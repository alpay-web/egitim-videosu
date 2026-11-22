#!/usr/bin/env python3
"""BA Teknik Rehberi · Video 11: Confluence. Belge satır 3213–3493."""
from ortak import m, t, dikkat, g, soru, kaydet

m("Confluence nedir?", ["Atlassian'ın bilgi tabanı ve dokümantasyon platformu", "Jira \"ne yapılıyor\" · Confluence \"neden ve nasıl\"",
                        "BA için tek doğru kaynak (single source of truth)", "Cloud: whiteboard, database, Live Docs, Rovo"],
  "Confluence, {Atlassian}'ın ekip bilgi tabanı ve dokümantasyon platformudur. Jira ne yapılıyor sorusunu, Confluence neden ve nasıl sorusunu cevaplar. "
  "İş analisti için Confluence; gereksinim dokümanlarının, toplantı ve karar kayıtlarının, süreç ve arayüz tanımlarının tek doğru kaynağıdır, "
  "yani {single source of truth}. Cloud sürümünde sayfaların yanında {whiteboard}, {database}, {Live Docs} gibi içerik türleri ve {Rovo} yapay zeka özellikleri bulunur.",
  bolum="Confluence: giriş ve hedefler", kanca="Altı ay sonra bu kararı neden verdiğimizi kim hatırlayacak?", ton="merakli")
m("Bu bölümün hedefleri", ["Firma projesi için space sayfa ağacı kurmak", "Gereksinimleri Page Properties ile yapılandırıp tek raporda toplamak",
                           "Jira işlerini bağlayıp gereksinim → story izlenebilirliği", "CQL ve etiketlerle doğru sayfayı saniyede bulmak"],
  "Bu bölümü bitirdiğinde şunları yapabileceksin. Bir: bir Firma projesi için Confluence alanı, yani {space}, sayfa ağacı kurmak. "
  "İki: gereksinim sayfalarını {Page Properties} ile yapılandırıp tek bir özet tabloda, yani {Page Properties Report}'ta toplamak. "
  "Üç: Jira işlerini sayfaya bağlayıp gereksinimden {story}'ye izlenebilirlik kurmak. Dört: CQL ve etiketlerle doğru sayfayı saniyeler içinde bulmak.")
t("Başlamadan önce gerekenler", ["Gereken", "Nereden", "Hazır mısın?"],
  [["Confluence Cloud (ücretsiz plan)", "atlassian.com → Confluence", "Solda Spaces"], ["Jira bölümü", "Bu rehber", "KRD'de ≥ 3 story"],
   ["Sayfa düzenleme", "Temel seviye", "/ yazınca makro listesi"]],
  "Başlamadan önce tablo üç sütun: gereken, nereden ve hazır olduğunu nasıl anlarsın. Confluence Cloud hesabı, küçük ekipler için ücretsiz plan; atlassian nokta com, Confluence. Sol menüde {Spaces} görünüyorsa tamam. "
  "Jira bölümü tamamlanmış olmalı; KRD projesinde en az üç {story} varsa tamam. "
  "Sayfa düzenleme: bu bölümün temel seviyesi; editörde bölü yazınca makro listesi açılıyorsa başlayabiliriz.")
m("Yapı ve editör temelleri", ["Site → Space → sayfa ağacı (parent / child) → sayfa, blog, whiteboard, database",
                               "Her space: kendi izinleri, ana sayfası, şablonları",
                               "Editör: / makro · başlıklar · tablo · status (TASLAK / İNCELEMEDE / ONAYLANDI)",
                               "Panel, expand, @bahsetme, tarih, action item, sayfa ve Jira bağlantıları"],
  "Temel seviye. Yapı: {Site}, {Space}, yani ekip, proje ya da ürün alanı; sayfa ağacı, yani {parent} ve {child} sayfalar; "
  "sonra sayfa, blog yazısı, {whiteboard} ya da {database}. Her {space}'in kendi izinleri, ana sayfası ve şablonları vardır. "
  "Editör temelleri: bölü ile makro ve eleman ekleme; başlık seviyeleri, ki navigasyon ve içindekiler buna dayanır; tablolar; "
  "durum etiketi, yani {status lozenge}: TASLAK, İNCELEMEDE, ONAYLANDI; panel, yani bilgi, uyarı, not; {expand}, açılır bölüm; et işaretiyle bahsetme; tarih; "
  "eylem maddesi, yani {action item}; ve sayfa ile Jira bağlantıları.", bolum="Confluence · Temel seviye")
t("BA için sayfa türleri (1/2)", ["Sayfa", "İçerik"],
  [["Proje ana sayfası", "Amaç, kapsam, paydaşlar, linkler, durum"], ["PRD / BRD", "Hedefler, kapsam, hikayeler, varsayımlar, açık sorular"],
   ["Toplantı notu", "Katılımcılar, gündem, kararlar, aksiyonlar"], ["Karar kaydı (decision log)", "Bağlam, seçenekler, karar, gerekçe, karar veren, tarih"]],
  "İş analisti için temel sayfa türleri. Proje ana sayfası: amaç, kapsam, paydaşlar, linkler ve durum. "
  "Ürün gereksinim dokümanı, yani PRD ya da BRD: hedefler, kapsam, kullanıcı hikayeleri, varsayımlar ve açık sorular. "
  "Toplantı notu: katılımcılar, gündem, kararlar ve aksiyonlar. "
  "Karar kaydı, yani {decision log}: bağlam, seçenekler, karar, gerekçe, karar veren ve tarih.")
t("BA için sayfa türleri (2/2)", ["Sayfa", "İçerik"],
  [["Süreç dokümanı", "BPMN/swimlane, adım tablosu, RACI"], ["Arayüz / API spesifikasyonu", "Endpoint, alanlar, hata kodları, örnek mesaj"],
   ["Sözlük (glossary)", "İş terimleri ve tanımları"], ["Sürüm notu", "İçerik, etkiler, bilinen sorunlar"]],
  "Süreç dokümanı: BPMN ya da {swimlane} diyagramı, adım tablosu ve RACI. Arayüz ya da API spesifikasyonu: {endpoint}, alanlar, hata kodları ve örnek mesajlar. "
  "Sözlük, yani {glossary}: iş terimleri ve tanımları. Sürüm notu: sürüm içeriği, etkiler ve bilinen sorunlar.")
t("Sık kullanılan makrolar (1/2)", ["Makro", "Kullanım"],
  [["Jira work item / Jira filtre", "Story listesini JQL ile canlı gömme"], ["Table of Contents", "Uzun dokümanda gezinme"],
   ["Page Properties + Report", "Her sayfanın özet tablosunu tek raporda toplama"], ["Excerpt / Excerpt Include", "Bir metni tek yerde yazıp çok yerde kullanma"]],
  "Orta seviye: iş analistinin sık kullandığı makrolar. {Jira work item} ya da Jira filtre: {story} listesini JQL ile sayfaya canlı gömme; "
  "gereksinim ile iş arasında izlenebilirlik. {Table of Contents}: uzun dokümanlarda gezinme. "
  "{Page Properties} artı {Page Properties Report}: her gereksinim sayfasındaki özet tabloyu, yani durum, sahip ve önceliği, tek bir raporda toplama. "
  "{Excerpt} ve {Excerpt Include}: bir metni, örneğin bir iş kuralı tanımını, tek yerde yazıp birçok sayfada yeniden kullanma.", bolum="Confluence · Orta seviye")
t("Sık kullanılan makrolar (2/2)", ["Makro", "Kullanım"],
  [["Include Page", "Ortak bölümü gömme (KVKK notu)"], ["Status, Panel, Expand", "Okunabilirlik ve durum"],
   ["Draw.io / Gliffy / Lucidchart, Mermaid/PlantUML", "Diyagramı sayfada düzenlenebilir tutma"], ["Children Display / Content by Label", "Etiket bazlı listeler"],
   ["Code Block", "JSON, SQL, XML örnekleri"]],
  "{Include Page}: ortak bölümleri, örneğin KVKK notunu gömme. {Status}, {Panel} ve {Expand}: okunabilirlik ve durum gösterimi. "
  "draw.io, {Gliffy}, {Lucidchart}; ve Mermaid ya da PlantUML eklentileri: diyagramı sayfa içinde düzenlenebilir tutma. "
  "{Children Display} ve {Content by Label}: etiket bazlı içerik listeleri. {Code Block}: JSON, SQL ve XML örnekleri.")
m("Şablon: gereksinim sayfası (1/2)", ["Space seviyesinde özel şablon → tüm BA'lar aynı yapıyla yazar",
                                       "1. Page Properties: Gereksinim ID, Durum, Sahip, Öncelik, Kaynak kural, Jira, Hedef sürüm",
                                       "2. Bağlam ve problem · 3. Hedefler, KPI · 4. Kapsam / kapsam dışı",
                                       "5. Paydaşlar, RACI · 6. Süreç (as-is / to-be) · 7. Fonksiyonel gereksinimler"],
  "Şablon oluşturma: {space} seviyesinde özel şablonlar tanımlanır; tüm iş analistleri aynı yapıyla yazar. Örnek gereksinim sayfası şablonu on üç başlık. "
  "Bir: {Page Properties} tablosu; gereksinim ID, durum, sahip, öncelik, kaynak kural, Jira ve hedef sürüm. Bu rehberin her yerinde aynı alan adları kullanılır. "
  "İki: bağlam ve problem tanımı. Üç: hedefler ve başarı ölçütleri, yani KPI. Dört: kapsam ve kapsam dışı. Beş: paydaşlar ve RACI. "
  "Altı: süreç, yani {as-is} ve {to-be} diyagramları. Yedi: fonksiyonel gereksinimler tablosu; ID, açıklama, iş kuralı, kabul kriteri, Jira linki.")
m("Şablon: gereksinim sayfası (2/2)", ["8. Fonksiyonel olmayan: performans, güvenlik, loglama, erişilebilirlik, KVKK",
                                       "9. Ekran tasarımları (Figma / Balsamiq) · 10. Entegrasyonlar, veri akışı",
                                       "11. Varsayımlar, kısıtlar, riskler", "12. Açık sorular (soru, soran, sorumlu, cevap, tarih) · 13. Onay geçmişi"],
  "Sekiz: fonksiyonel olmayan gereksinimler; performans, güvenlik, loglama, erişilebilirlik ve KVKK. Dokuz: ekran tasarımları, {Figma} ya da {Balsamiq} gömme. "
  "On: entegrasyonlar ve veri akışı. On bir: varsayımlar, kısıtlar ve riskler. "
  "On iki: açık sorular; soru, soran, sorumlu, cevap ve tarih. On üç: onay geçmişi; onaylayan, rol, tarih ve versiyon.")
t("Karar kaydı örneği", ["Alan", "İçerik"],
  [["Karar", "Hata kodunda ret yok; ≤ 3 tekrar, sonra MANUEL_INCELEME"], ["Bağlam · seçenekler", "Ret oranı yapay artıyor · A / B / C"],
   ["Seçilen · gerekçe", "C · geçici hata ilk tekrarda çözülür"], ["Sonuçlar", "Retry politikası, izleme alarmı"],
   ["Karar veren / tarih", "Kredi Tahsis Müdürü / 2026-03-10"]],
  "Karar kaydı, yani {decision record} örneği. Karar: KKB sorgusu hata kodu döndürürse başvuru otomatik reddedilmez; toplam süre beş saniyeyi aşmamak kaydıyla "
  "en fazla üç kez tekrar denenir, ardından MANUEL_INCELEME'ye alınır. Zaman aşımında, yani beş saniyede, tekrar yapılmaz; U04. "
  "Bağlam: servis kesintilerinde ret oranı yapay olarak artıyor, bayi şikayetleri var. "
  "Seçenekler: A, otomatik ret; B, manuel kuyruk; C, üç kez tekrar dene, sonra manuel. Seçilen: C. "
  "Gerekçe: geçici hataların çoğu ilk tekrarda çözülüyor; müşteri deneyimi korunuyor. "
  "Sonuçlar: {retry} politikası ve izleme alarmı gereksinimi eklenecek. Karar veren ve tarih: kredi tahsis müdürü, mimari kurul; 2026-03-10.")
m("Jira ile entegrasyon", ["Sayfadaki metni seçip doğrudan Jira iş öğesi oluşturma", "Jira epic'ine gereksinim sayfasını bağlama",
                           "Sürüm sayfasında fixVersion = \"2026.04\" filtresini canlı tablo"],
  "Jira ile entegrasyon: Confluence sayfasındaki metni seçip doğrudan Jira iş öğesi oluşturma; Jira {epic}'ine gereksinim sayfasını bağlama; "
  "sürüm sayfasında {fixVersion} eşittir 2026.04 filtresini canlı tablo olarak gösterme.")

# ───────────────────────────── İleri
m("Bilgi mimarisi", ["Space yapısı organizasyon şemasına değil, aramaya göre",
                     "Ana sayfa → vizyon ve yol haritası → gereksinimler → süreçler → API → veri ve sözlük → kararlar → toplantılar → sürüm → arşiv",
                     "Etiket standardı: gereksinim, karar, api, kvkk", "Sayfa adı: [REQ-KRD-012] Kredi/değer kuralı"],
  "İleri seviye: bilgi mimarisi. {Space} yapısını organizasyon şemasına değil, kullanıcının arama davranışına göre kur. "
  "Önerilen ağaç: ana sayfa; ürün vizyonu ve yol haritası; gereksinimler, {epic} bazında; süreçler; entegrasyonlar ve API; veri modeli ve sözlük; "
  "kararlar; toplantılar; sürüm notları; arşiv. Etiketleme standardı: gereksinim, karar, api, kvkk. "
  "Sayfa adlandırma kuralı: köşeli parantez içinde REQ-KRD-012, sonra kredi değer kuralı.", bolum="Confluence · İleri seviye")
m("Database, versiyon, onay, otomasyon", ["Database: gereksinim envanteri, risk kaydı, API envanteri; Jira alanlarıyla bağlı",
                                          "Whiteboard notları → Jira iş öğesi", "Sayfa geçmişi, versiyon karşılaştırma, düzenleme kısıtı, onay akışı (Comala)",
                                          "Automation: yayında bildirim · 6 ay güncellenmeyene hatırlatma · \"Onaylandı\"da kilitle"],
  "{Database}'ler: Confluence {database} ile gereksinim envanteri, risk kaydı ya da API envanteri satır sütun yapısında tutulur; "
  "Jira alanlarıyla bağlantılı olabilir, sayfa ya da {whiteboard} içine gömülür. "
  "{Whiteboard}'da yapılan beyin fırtınası yapışkan notları Jira iş öğesine dönüştürülebilir. "
  "Versiyon ve onay yönetimi: sayfa geçmişi ve versiyon karşılaştırma, kritik sayfalar için düzenleme kısıtı, onay akışı, "
  "yani {Comala Document Management} gibi eklentiler ya da otomasyonla durum değişikliği; ve onaylanmış versiyon etiketi. "
  "Denetim için onayın kim tarafından, hangi versiyona verildiği kanıtlanabilir olmalıdır. "
  "{Confluence Automation}: sayfa yayımlanınca paydaşlara bildirim; altı aydır güncellenmeyen sayfaların sahibine hatırlatma, yani içerik bayatlaması; "
  "onaylandı etiketi eklenince sayfayı kilitleme.")
m("Rovo, yönetişim, docs-as-code", ["Rovo: özetleme, aksiyon çıkarma, taslak, soru-cevap · BA doğrular · plan ve ayara bağlı",
                                    "Space izinleri, sayfa kısıtı, misafir erişimi, ekran görüntüsünde kişisel veri maskeleme, arşiv",
                                    "Data Center ↔ Cloud makro farkı → migration'da makro envanteri",
                                    "Docs-as-code: Git (Markdown, OpenAPI) → Confluence; tek doğru kaynak net olmalı"],
  "{Rovo} ve yapay zeka: sayfa ve {whiteboard} özetleme, toplantı notundan aksiyon çıkarma, taslak üretme, şirket içi bilgi üzerinde soru cevap. "
  "Üretilen içerik her zaman iş analisti tarafından doğrulanır; hassas veriler için kurum politikası kontrol edilir. Özellikler plan ve yönetici ayarlarına bağlıdır. "
  "Yönetişim ve güvenlik: {space} izinleri, yani görüntüle, ekle, sil, yönet; sayfa kısıtlamaları; misafir ve harici kullanıcı erişimi; "
  "kişisel veri içeren ekran görüntülerinin maskelenmesi; arşivleme politikası. "
  "{Data Center} ile Cloud arasında makro ve özellik farkları olabilir; {migration} projelerinde makro envanteri çıkarılır. "
  "{Docs-as-code} alternatifi: teknik ekipler API dokümantasyonunu Git'te, yani {Markdown} ve {OpenAPI} ile tutup Confluence'a otomatik yayımlayabilir. "
  "İş analisti için önemli olan tek doğru kaynağın hangisi olduğunun net olmasıdır.")

# ───────────────────────────── Hatalar, mülakat
m("Sık yapılan hatalar", ["Aynı gereksinim birden çok sayfada (kopyala-yapıştır yerine excerpt)", "Sahip, durum, son güncelleme belirsiz",
                          "Kararlar toplantıda ya da e-postada kalıyor", "Derin, karmaşık ağaçlar; aranamayan başlıklar",
                          "Diyagramı statik resim eklemek; kaynak kayboluyor"],
  "Sık yapılan hatalar. Aynı gereksinimin birden çok sayfada farklı versiyonları; kopyala yapıştır yerine {excerpt} kullan. "
  "Sayfanın sahibi, durumu ve son güncelleme tarihinin belli olmaması. Kararların sadece toplantıda ya da e-postada kalması; karar kaydı tutulmaması. "
  "Derin ve karmaşık sayfa ağaçları; aranamayan başlıklar. Ve diyagramları statik resim olarak eklemek; kaynağın kaybolması.", bolum="Confluence · Hatalar ve mülakat")
m("Mülakat soruları ve ipuçları", ["1. Space yapısı → aramaya göre ağaç", "2. Jira senkronu → /jira makrosu", "3. Page Properties Report → özet tablo", "4. Karar kaydı alanları", "5. Güncellik → sahip, hatırlatma"],
  "Mülakat soruları ve bölümden ipuçları. Bir: bir projenin Confluence {space} yapısını nasıl kurarsınız? Aramaya göre bir ağaç ve numara önekleri. "
  "İki: gereksinim dokümanını Jira ile nasıl senkron tutarsınız? Jira makrosu ve {Page Properties}'teki Jira alanı. "
  "Üç: {Page Properties Report} ne işe yarar? Etiketli sayfaların özet tablosunu toplar. "
  "Dört: bir karar kaydında hangi alanlar olmalıdır? Bağlam, seçenekler, karar, gerekçe, karar veren ve tarih. "
  "Beş: dokümantasyonun güncel kalmasını nasıl sağlarsınız? Sahip atayarak, otomasyon hatırlatmasıyla ve etiketlerle.")

# ───────────────────────────── Görsel rehber
g("Confluence ekranı nasıl okunur?", "g31.png",
  [([0.02, 0.08, 0.33, 0.95], "1 · Space ve sayfa ağacı"), ([0.33, 0.08, 1.0, 0.16], "2 · Editör araç çubuğu, Publish"),
   ([0.33, 0.16, 1.0, 0.27], "3 · Sayfa başlığı"), ([0.33, 0.24, 1.0, 0.44], "4 · Page Properties"),
   ([0.33, 0.5, 0.75, 0.86], "5 · / menüsü"), ([0.33, 0.86, 1.0, 0.95], "6 · Sayfa altı ve ••• menüsü")],
  "Görsel rehber: Confluence ekran yerleşimi; şematik, numaralı bölgeler. "
  "Bir, {space} ve sayfa ağacı: {space}'in tüm içeriği hiyerarşik görünür. Bir sayfanın yanındaki artı alt sayfa ekler; üç nokta ile taşıma, kopyalama, arşivleme yapılır. "
  "Sayfaları sürükleyerek sıralayabilirsin. "
  "İki, editör araç çubuğu: başlık stili, kalın ve italik, liste, tablo, bağlantı, görsel, et işaretiyle bahsetme, eylem maddesi ve artı ekle, yani tüm makrolar. "
  "{Publish} yayımlar; yayımlanmamış değişiklikler taslak olarak kalır. "
  "Üç, sayfa başlığı: adı standarda göre ver; köşeli parantez içinde REQ-KRD-012, kredi değer kuralı. Arama başlığa ağırlık verir. "
  "Dört, {Page Properties} tablosu: sayfanın özet bilgileri; durum İNCELEMEDE, sahip, {epic} KRD-120. "
  "Başka bir sayfadaki {Page Properties Report} makrosu, aynı etiketi taşıyan tüm sayfaların tablolarını tek listede toplar. "
  "Beş, bölü menüsü: yazarken bölü ile makro eklersin. Bölü jira ile {story} listesi gömersin, bölü {status} ile renkli durum etiketi koyarsın. "
  "Altı, sayfa altı ve üç nokta menüsü: etiket ekleme, yorumlar, sayfa geçmişi yani {Page history}, kısıtlamalar yani kilit simgesi, "
  "ve dışa aktarma, PDF ya da Word.", bolum="Confluence · Görsel rehber")
t("Menü rehberi (1/3)", ["Yapmak istediğin", "Yol"],
  [["Yeni space", "Spaces → Create space → şablon → ad, anahtar"], ["Yeni sayfa", "+ Create → Page (Live doc, Whiteboard, Database, Folder)"],
   ["Şablondan sayfa", "+ Create → Templates (Meeting notes, Decision, Product requirements, Retrospective)"],
   ["Space şablonu", "Space settings → Content → Templates → Create new template"]],
  "Menü ve kısayol rehberi, Confluence Cloud. Yeni {space}: {Spaces}, {Create space}, şablon, yani {Knowledge base} ya da {Project}; ad ve anahtar. "
  "Yeni sayfa: üstteki artı {Create}, {Page}; ya da sayfa ağacında artı simgesi. Aynı menüde {Live doc}, {Whiteboard}, {Database} ve {Folder} seçenekleri. "
  "Şablondan sayfa: artı {Create}, {Templates}; şablonu ara: {Meeting notes}, {Decision}, {Product requirements}, {Retrospective}. "
  "{Space} şablonu oluşturmak: {Space settings}, {Content}, {Templates}, {Create new template}.")
t("Menü rehberi (2/3)", ["Yapmak istediğin", "Yol"],
  [["Makro eklemek", "/ → /jira, /toc, /status, /expand, /page properties"], ["Jira listesi", "/jira → JQL → tablo, sütunlar"],
   ["Metinden Jira işi", "Metni seç → Jira simgesi → Create work item"], ["Eylem maddesi · karar", "[] + boşluk, @ kişi, // tarih · /decision"],
   ["Geçmiş ve karşılaştırma", "••• → Page history → Compare"]],
  "Makro eklemek: editörde bölü yaz, sonra makro adı; bölü jira, bölü {toc}, bölü {status}, bölü {expand}, bölü {page properties}. "
  "Jira listesi gömmek: bölü jira, JQL sekmesine sorguyu yapıştır; görünüm tablo, sütunları seç. "
  "Metinden Jira işi açmak: yayımlanmış sayfada metni seç; açılan küçük menüde Jira simgesi, {Create work item}. "
  "Eylem maddesi: yeni satırda köşeli parantez aç kapa ve boşluk; et işaretiyle kişi, çift bölü ile tarih. Karar kaydı: bölü {decision} makrosu ya da {Decision} şablonu. "
  "Sayfa geçmişi ve karşılaştırma: üç nokta, {Page history}, iki versiyonu seç, {Compare}.")
t("Menü rehberi (3/3)", ["Yapmak istediğin", "Yol"],
  [["Düzenlemeyi kısıtla", "Kilit → \"Anyone can view, only some can edit\""], ["Dışa aktar · etiket", "••• → Export (PDF / Word) · Add label"],
   ["Takip · otomasyon", "Watch · Space settings → Automation"], ["Kısayollar", "/ · e · c · Ctrl+Shift+S · ["]],
  "Düzenlemeyi kısıtlamak: sağ üst kilit simgesi, {Anyone can view, only some can edit}. Dışa aktarmak: üç nokta, {Export}, PDF ya da Word. "
  "Etiket eklemek: sayfa altı, {Add label}; ya da üç nokta, {Labels}. Takip etmek: göz simgesi, yani {Watch}; değişikliklerde bildirim. "
  "Otomasyon: {Space settings}, {Automation}, {Create rule}. "
  "Kısayollar: bölü arama ya da editörde makro; e düzenle; c yeni sayfa; Ctrl+Shift+S kaydet ve kapat; köşeli parantez sayfa ağacını gizle.")

# ───────────────────────────── Laboratuvar
m("Laboratuvar (~60 dk): 1–5", ["1. Create space → \"Kredi Dijital\", KRD", "2. Uygulama paketindeki ağacı kur (00 Başlangıç … 90 Arşiv)",
                                "3. Şablon \"Gereksinim sayfası\": /page properties (7 satır) + 13 başlık · Durum: /status gri TASLAK",
                                "4. [REQ-KRD-012] Kredi/değer kuralı · [REQ-KRD-013] KVKK onayı · etiket: gereksinim",
                                "5. İçerik: iş kuralı, Gherkin, açık sorular, draw.io BPMN (yoksa PNG + .bpmn ek)"],
  "Laboratuvar: gereksinim {space}'ini kur; yaklaşık altmış dakika. Bir, {space}: {Spaces}, {Create space}, boş ya da {Project} şablonu; adı kredi dijital, anahtarı KRD. "
  "İki, ağaç: ana sayfa altına uygulama paketindeki ağacı kur; sıfır sıfır başlangıçtan doksan arşive. "
  "Üç, şablon: {Space settings}, {Content}, {Templates}, {Create new template}; adı gereksinim sayfası. "
  "İçerik: bölü {page properties} ile gereksinim ID, durum, sahip, öncelik, kaynak kural, Jira, hedef sürüm satırları; ardından on üç başlık. "
  "Durum hücresine bölü {status} ile gri TASLAK koy. "
  "Dört, iki gereksinim sayfası: gereksinimler altına şablondan REQ-KRD-012 kredi değer kuralı ve REQ-KRD-013 KVKK onayı oluştur; ikisine de gereksinim etiketini ekle. "
  "Beş, içerik: kredi değer sayfasına iş kuralını, {Gherkin} kabul kriterlerini ve bir açık soru tablosunu yaz. "
  "Süreç bölümüne BPMN diyagramını draw.io makrosuyla düzenlenebilir olarak ekle; eklenti yoksa PNG'yi koy ve kaynak nokta bpmn dosyasını sayfaya ek olarak yükle.",
  bolum="Confluence · Laboratuvar")
m("Laboratuvar: 6–11", ["6. /jira → parent = KRD-120 → Key, Summary, Status", "7. /page properties report → Label: gereksinim; bir sayfayı \"İNCELEMEDE\" yap",
                        "8. Decision şablonu: KKB kararı (3 tekrar, sonra MANUEL_INCELEME)", "9. Meeting notes: refinement, ≥ 2 eylem maddesi",
                        "10. Değiştir → Page history → Compare · 11. Export → PDF"],
  "Altı, Jira bağı: bölü jira, JQL {parent} eşittir KRD-120; tablo görünümü; {Key}, {Summary}, {Status}. "
  "Yedi, rapor sayfası: gereksinimler ana sayfasına bölü {page properties report} ekle; {Label}: gereksinim. İki sayfanın özet tablosu otomatik listelenir. "
  "Bir sayfada durumu İNCELEMEDE yapıp rapordaki değişikliği gör. "
  "Sekiz, karar kaydı: kararlar altına {Decision} şablonuyla şu kararı yaz: KKB hata verirse beş saniye içinde en fazla üç tekrar, sonra MANUEL_INCELEME; "
  "zaman aşımında tekrar yok; seçenekler, gerekçe, karar veren ve tarih. "
  "Dokuz, toplantı notu: {Meeting notes} şablonuyla bir {refinement} toplantısı notu; en az iki eylem maddesi, köşeli parantez, et işareti ve tarih. "
  "On, versiyon: kredi değer sayfasında bir değişiklik yap, yayımla; üç nokta, {Page history}, {Compare} ile farkı gör. "
  "On bir, dışa aktar: üç nokta, {Export}, PDF ile sayfayı indir ve düzenini kontrol et.")

# ───────────────────────────── Uygulama paketi
m("Bir BA alanının sayfa ağacı", ["KRD · Kredi Dijital (space)", "00 Başlangıç · 10 Süreçler (P01 AS-IS, P01 TO-BE)",
                                  "20 Gereksinimler: özet (Report), [REQ-KRD-012], [REQ-KRD-021]", "30 Kararlar · 40 Toplantı notları · 50 Sözlük · 90 Arşiv"],
  "Confluence uygulama paketi. Bir iş analisti alanının sayfa ağacı: sayfaları nereye koyacağını başta belirlemezsen altı ay sonra kimse bir şey bulamaz. "
  "Firma kredi dönüşüm projesi için örnek yapı; numara önekleri sıralamayı sabit tutar. "
  "KRD, kredi dijital {space}. Sıfır sıfır başlangıç: proje özeti, paydaşlar, kapsam. On süreçler: P01 kredi başvurusundan kullandırıma, AS-IS ve TO-BE. "
  "Yirmi gereksinimler: gereksinim özeti, yani {Page Properties Report}; REQ-KRD-012 kredi değer kuralı; REQ-KRD-021 KKB zaman aşımı davranışı. "
  "Otuz kararlar, karar kaydı. Kırk toplantı notları. Elli sözlük. Doksan arşiv.", bolum="Confluence · Uygulama paketi")
m("Page Properties: adımlar", ["1. [REQ-KRD-021] sayfası → /page properties", "2. İki sütunlu tablo: alan adı | değer",
                               "3. EARS: \"KKB yanıt süresi 5 saniyeyi aştığında, karar motoru başvuruyu MANUEL_INCELEME durumuna almalıdır.\" Doğrulama: Test",
                               "4. Etiket: gereksinim → Publish · 5. REQ-KRD-012'yi aynı alan adlarına getir",
                               "6. Özet sayfa: /page properties report → Label: gereksinim, Space: KRD"],
  "{Page Properties}: gereksinimleri tabloya dönüştürmek. Her gereksinim sayfasının başına aynı alanları taşıyan küçük bir tablo konur; "
  "Confluence bunları toplayıp tek bir özet sayfada gösterir. Böylece elli gereksinimin durumunu tek ekranda görürsün. "
  "Bir: REQ-KRD-021 KKB zaman aşımı davranışı sayfasını oluştur; editörde bölü {page properties} yaz ve makroyu ekle. "
  "İki: makronun içine iki sütunlu bir tablo koy; sol sütun alan adı, sağ sütun değer. "
  "Üç: makronun altına gereksinimi {EARS} kalıbıyla yaz: KKB yanıt süresi beş saniyeyi aştığında, karar motoru başvuruyu MANUEL_INCELEME durumuna almalıdır. "
  "Doğrulama yöntemi: test. Dört: sayfaya gereksinim etiketini ekle ve yayımla. "
  "Beş: laboratuvardaki REQ-KRD-012 sayfasının tablosunu da bu alan adlarına göre güncelle; hedef sürüm satırını da ekle. Alan adları harfi harfine aynı olmalı. "
  "Altı: gereksinim özeti sayfasında bölü {page properties report} ekle; {Label}: gereksinim, {Space}: KRD; sütunları seç, yayımla.")
t("Page Properties tablosu (REQ-KRD-021)", ["Alan", "Değer"],
  [["Gereksinim ID", "REQ-KRD-021"], ["Durum", "İNCELEMEDE"], ["Sahip", "(kendi adını @ ile an)"],
   ["Kaynak kural", "Firma Çalışma Seti §1.3 · U04"], ["Jira · Öncelik", "KRD-214 (/jira ile) · Must"]],
  "Tablonun içeriği: gereksinim ID, REQ-KRD-021. Durum, İNCELEMEDE. Sahip, kendi adını et işaretiyle an. "
  "Kaynak kural, Firma çalışma seti bir nokta üç ve U04. Jira, KRD-214; bölü jira ile ekle. Öncelik, {Must}. "
  "Beklenen: özet sayfada iki satırlık bir tablo; her satır bir gereksinim sayfası, sütunlar tablodaki alan adları. "
  "Bir gereksinim sayfasında durumu değiştirip yayımladığında özet tablo da değişir.")
t("CQL: Confluence'ın sorgu dili", ["İhtiyaç", "CQL"],
  [["KRD'deki gereksinim sayfaları", "space = KRD AND label = \"gereksinim\" AND type = page"],
   ["Son 7 günde değişen", "… AND lastmodified >= now(\"-7d\")"], ["Başlığında REQ-KRD", "title ~ \"REQ-KRD\""],
   ["Benim oluşturduklarım", "creator = currentUser()"], ["İçinde KKB geçen", "space = KRD AND text ~ \"KKB\""]],
  "CQL, Jira'daki JQL'in Confluence karşılığıdır; arama sayfasındaki filtrelerin arkasında, REST API'de ve bazı makroların filtre ayarlarında kullanılır. "
  "KRD alanındaki gereksinim sayfaları: {space} eşittir KRD {AND} {label} eşittir gereksinim {AND} {type} eşittir {page}. "
  "Son yedi günde değişen gereksinimler: aynı koşullar {AND} {lastmodified} büyük eşit {now} eksi yedi gün. "
  "Başlığında REQ-KRD geçenler: {title} dalga REQ-KRD. Benim oluşturduklarım: {creator} eşittir {currentUser}. "
  "İçinde KKB geçen sayfalar: {space} eşittir KRD {AND} {text} dalga KKB.")
t("Etiket stratejisi", ["Etiket", "Ne için", "Örnek kullanım"],
  [["gereksinim", "Tüm gereksinim sayfaları", "Page Properties Report kaynağı"], ["karar", "Karar kayıtları", "\"Ne karar vermiştik?\""],
   ["kvkk", "Kişisel veri içeren süreç / gereksinim", "KVKK denetiminde hızlı liste"], ["p01, u04", "Çalışma seti diyagram kodları", "Bir sürecin tüm sayfaları"]],
  "Etiket stratejisi. Gereksinim: tüm gereksinim sayfaları; {Page Properties Report} kaynağı. Karar: karar kayıtları; bu konuda ne karar vermiştik araması. "
  "KVKK: kişisel veri içeren süreç ve gereksinimler; KVKK denetiminde hızlı liste. "
  "P01, U04: çalışma setindeki diyagram kodları; bir sürece ait tüm sayfalar.")
dikkat("Etiket tuzağı", "Küçük harf, tek kelime. \"gereksinim\" ≠ \"gereksinimler\": rapor birini kaçırır (çoğul eki yeni etiket yaratır).",
       "Etiketler küçük harf ve tek kelime olmalı. Dikkat: gereksinim ve gereksinimler iki farklı etikettir; rapor birini kaçırır. "
       "Confluence etiketleri küçük harfe çevirir ama çoğul eki yeni bir etiket yaratır.")
m("Bağımsız görev", ["1. Ağacı kendi deneme alanında kur", "2. REQ-KRD-030 (taslakta 30 gün → iptal) · REQ-KRD-031 (onaydan 30 gün → iptal)",
                     "Page Properties, EARS, etiketler: gereksinim ve u08", "3. 30 Kararlar: \"30. gün dahil mi?\" seçenekleri ve karar sahibi",
                     "4. Özet rapor 5 satır (012, 013, 021, 030, 031); lab yoksa 4"],
  "Bağımsız görev. Bir: ağacı kendi deneme alanında kur. İki: U08 kuralı için iki gereksinim sayfası oluştur: REQ-KRD-030, taslakta otuz gün işlem yoksa iptal; "
  "ve REQ-KRD-031, onaydan otuz gün sonra iptal. Her biri {Page Properties}, {EARS} cümlesi, gereksinim ve u08 etiketi taşısın. "
  "Üç: otuz kararlar altına bir karar sayfası aç: otuzuncu gün dahil mi sorusu için seçenekleri ve kimin karar vereceğini yaz. "
  "Dört: gereksinim özeti raporunun beş satır gösterdiğini doğrula: 012, 013, 021, 030 ve 031. Laboratuvarı yapmadıysan 013 olmadan dört satır görürsün.",
  bolum="Confluence · Bağımsız görev ve sorun giderme")
t("Sorun giderme", ["Belirti", "Olası neden", "Çözüm"],
  [["Report boş", "Etiket farklı ya da başka alan", "Etiket ve Label/Space ayarı"], ["Bazı sütunlar boş", "Alan adları farklı (Sahip / Sahibi)", "Birebir aynı ad; şablon"],
   ["Jira makrosu \"Unable to render\"", "Bağlantı yok ya da yetki yok", "Jira'da işi açabiliyor musun?"], ["Arama sayfayı bulmuyor", "Kısıtlı ya da taslak", "Kilit ve yayın durumu"],
   ["\"Kim neyi değiştirdi?\"", "—", "Page history → Compare"]],
  "Sorun giderme. {Page Properties Report} boşsa: etiket yazımı farklı ya da rapor başka alana bakıyor. Sayfalardaki etiketi ve raporun {Label} ve {Space} ayarlarını karşılaştır. "
  "Raporda bazı sütunlar boşsa: alan adları sayfalar arasında farklı, örneğin sahip ve sahibi. Alan adlarını birebir aynı yap; bir sayfa şablonu kullan. "
  "Jira makrosu {Unable to render} diyorsa: Confluence ile Jira bağlantısı yok ya da Jira projesine yetkin yok. "
  "Jira'da işi açabildiğini kontrol et; yöneticiye uygulama bağlantısını sor. "
  "Bir sayfayı arama bulmuyorsa: sayfa kısıtlı, yani {restriction}, ya da taslak olarak kalmış. Sayfanın kilit simgesine ve yayın durumuna bak. "
  "Kim neyi değiştirdi sorusu için: sayfa, üç nokta, {Page history}, iki sürümü seç, {Compare}.")
soru("Bilgi kontrolü 1/5", "40 gereksinimin durumunu tek tabloda görmek için hangi makro ikilisi?",
     ["Jira + Status", "Excerpt + Excerpt Include", "Table of Contents + Children", "Page Properties + Page Properties Report"], 3,
     "Beş soruluk bilgi kontrolü. Birinci soru: kırk gereksinimin durumunu tek tabloda görmek için hangi makro ikilisi kullanılır? "
     "A, Jira ve {Status}. B, {Excerpt} ve {Excerpt Include}. C, {Table of Contents} ve {Children}. D, {Page Properties} ve {Page Properties Report}.",
     "Doğru cevap D.", bolum="Confluence · Bilgi kontrolü ve çözümler")
soru("Bilgi kontrolü 2/5", "Rapor bir sayfayı göstermiyor, diğerlerini gösteriyor. İlk kontrol?",
     ["Sayfanın etiketi", "Sayfanın uzunluğu", "Sayfanın rengi", "Tarayıcı önbelleği"], 0,
     "İkinci soru: rapor bir sayfayı göstermiyor, diğerlerini gösteriyor. İlk neyi kontrol edersin? A, sayfanın etiketi. B, sayfanın uzunluğu. C, sayfanın rengi. D, tarayıcı önbelleği.",
     "Doğru cevap A: etiket.")
soru("Bilgi kontrolü 3/5", "CQL'de \"son 7 günde değişen\" koşulu?",
     ["updated > 7", "lastmodified >= now(\"-7d\")", "modified in last 7 days", "date > -7"], 1,
     "Üçüncü soru: CQL'de son yedi günde değişen koşulu hangisi? A, {updated} büyüktür yedi. B, {lastmodified} büyük eşit {now} eksi yedi gün. "
     "C, {modified in last} yedi {days}. D, {date} büyüktür eksi yedi.",
     "Doğru cevap B.")
soru("Bilgi kontrolü 4/5", "Gereksinim sayfasının başlığına neden ID konur?",
     ["Görünüm için", "Confluence zorunlu tutar", "Jira, test ve notlarda tek kimlikle başvurulsun diye", "Sayfa sırası için"], 2,
     "Dördüncü soru: gereksinim sayfasının başlığına neden ID konur? A, görünüm için. B, Confluence zorunlu tutar. "
     "C, Jira, test ve toplantı notlarında tek bir kimlikle başvurulabilsin diye. D, sayfa sırası için.",
     "Doğru cevap C.")
soru("Bilgi kontrolü 5/5", "Bir kararın gerekçesini altı ay sonra bulmak için en iyi yer?",
     ["Karar kaydı sayfası", "Toplantı sohbet geçmişi", "Jira yorumu", "E-posta"], 0,
     "Beşinci soru: bir kararın gerekçesini altı ay sonra bulmak için en iyi yer? A, karar kaydı sayfası. B, toplantı sohbet geçmişi. C, Jira yorumu. D, e-posta.",
     "Doğru cevap A: karar kaydı sayfası.")
t("Hızlı başvuru: editör komutları", ["Yaz", "Ne ekler"],
  [["/page properties · /page properties report", "Alan tablosu · etiketli sayfalardan özet"], ["/jira · /status", "İş ya da JQL tablosu · renkli durum"],
   ["/decision · /toc", "Karar öğesi · içindekiler"], ["/excerpt · @", "Yeniden kullanılabilir parça · kişi anma"]],
  "Hızlı başvuru: sık kullanılan editör komutları. Bölü {page properties}: rapor için alan tablosu. Bölü {page properties report}: etiketli sayfalardan özet tablo. "
  "Bölü jira: tek iş ya da JQL sonucu tablosu. Bölü {status}: renkli durum etiketi. Bölü {decision}: karar öğesi. Bölü {toc}: içindekiler. "
  "Bölü {excerpt}: başka sayfada yeniden kullanılabilir parça. Et işareti: kişi anma.")
m("Çözümler", ["REQ-KRD-030: TASLAK 30 gün → IPTAL", "REQ-KRD-031: ONAYLANDI + 30 gün → IPTAL", "031: sözleşmeye geçiş esas; açık soru", "Karar: gün 30 mu, 31 mi?", "Rapor: 5 sayfa (lab yoksa 4)"],
  "Çözümler. REQ-KRD-030, {EARS}: bir başvuru TASLAK durumundayken son işlemden itibaren otuz gün geçtiğinde, sistem başvuruyu IPTAL durumuna almalı "
  "ve iptal nedenini kaydetmelidir. Doğrulama: test. "
  "REQ-KRD-031: bir başvuru ONAYLANDI durumuna geçtiği günden itibaren otuz gün içinde SOZLESME_IMZALANDI durumuna geçmediğinde, sistem başvuruyu IPTAL durumuna almalıdır. "
  "Çalışma seti onaydan otuz gün sonra iptal diyor ama otuz gün içinde neyin olması gerektiğini yazmıyor; bu eğitimde sözleşmeye geçiş esas alındı. "
  "Gerçek projede bu bir açık sorudur. Doğrulama: test. "
  "Karar sayfası: seçenek A, otuzuncu gün dolduğu gün iptal; seçenek B, otuz gün tamamlandıktan sonraki gün, yani otuz birinci gün iptal. "
  "Karar sahibi: kredi operasyon yöneticisi. Etki: bayi bildirim metni ve test verisi. "
  "Rapor: gereksinim etiketli beş sayfa görünür; laboratuvar yapılmadıysa dört sayfa.")
m("Bu videoda neler gördük?", ["Yapı, editör, BA sayfa türleri", "Makrolar, 13 başlıklı şablon, karar kaydı, Jira entegrasyonu",
                               "Bilgi mimarisi, database, onay, otomasyon, Rovo, yönetişim", "Ekran, menüler, laboratuvar",
                               "Sayfa ağacı, Page Properties, CQL, etiketler, çözümler"],
  "Toparlayalım. Confluence yapısını, editörü ve iş analistinin sayfa türlerini gördük. Makroları, on üç başlıklı şablonu, karar kaydını ve Jira entegrasyonunu öğrendik. "
  "Bilgi mimarisi, {database}, onay, otomasyon, {Rovo} ve yönetişime baktık. Ekranı, menüleri ve laboratuvarı çalıştık. "
  "Sayfa ağacı, {Page Properties}, CQL ve etiketlerle bitirdik. Bir sonraki videoda Miro ile çalıştay ve beyin fırtınası yöneteceğiz.", ton="sakin")

kaydet(__file__, {
    "baslik": "Business Analyst Teknik Rehberi · 11: Confluence",
    "alt_baslik": "Sayfa ağacı · şablon · Page Properties · karar kaydı · CQL",
    "kapanis": "Sıradaki video: Miro",
    "tema": 11,
    "youtube_baslik": "Business Analyst Teknik Rehberi 11/14: Confluence (gereksinim sayfası, Page Properties, CQL)",
    "etiketler": ["business analyst", "Confluence", "gereksinim dokümanı", "Page Properties", "CQL", "iş analisti"],
}, {"CQL": "si kyu el", "JQL": "cey kyu el", "PRD": "pi ar di", "BRD": "bi ar di", "RACI": "reysi", "KPI": "key pi ay", "EARS": "iırs", "REST": "rest",
    "KRD": "ka re de", "KRD-120": "ka re de yüz yirmi", "KRD-214": "ka re de iki yüz on dört", "REQ-KRD-012": "rek ka re de sıfır on iki",
    "REQ-KRD-013": "rek ka re de sıfır on üç", "REQ-KRD-021": "rek ka re de sıfır yirmi bir", "REQ-KRD-030": "rek ka re de sıfır otuz",
    "REQ-KRD-031": "rek ka re de sıfır otuz bir", "REQ-KRD": "rek ka re de", "REQ-KRD-012'yi": "rek ka re de sıfır on ikiyi",
    "MANUEL_INCELEME": "manuel inceleme", "MANUEL_INCELEME'ye": "manuel incelemeye", "TASLAK": "taslak", "İNCELEMEDE": "incelemede",
    "ONAYLANDI": "onaylandı", "IPTAL": "iptal", "SOZLESME_IMZALANDI": "sözleşme imzalandı", "AS-IS": "ez iz", "TO-BE": "tu bi",
    "2026.04": "iki bin yirmi altı nokta sıfır dört", "Ctrl+Shift+S": "kontrol şift es", "atlassian.com": "ıtlesiın nokta kom"})
