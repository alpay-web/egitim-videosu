#!/usr/bin/env python3
"""BA Teknik Rehberi · Video 1: Rehberin kullanımı + UML. Anlatımlı (düz okuma değil), hiçbir bölüm atlanmadan.
Çalıştır: python v01_giris_uml.py  → v01_giris_uml.json"""
import json
from pathlib import Path

S = []


def m(baslik, maddeler, anlatim, **k):
    S.append({"baslik": baslik, "maddeler": maddeler, "anlatim": anlatim, **k})


def t(baslik, basliklar, satirlar, anlatim, **k):
    S.append({"baslik": baslik, "tur": "tablo", "tablo": {"basliklar": basliklar, "satirlar": satirlar},
              "anlatim": anlatim, **k})


def dikkat(baslik, metin, anlatim, tip="uyari", **k):
    S.append({"baslik": baslik, "tur": "ipucu", "ipucu": {"tip": tip, "metin": metin}, "anlatim": anlatim, **k})


def g(baslik, dosya, odaklar, anlatim, **k):
    S.append({"baslik": baslik, "tur": "gorsel", "gorsel": f"gorseller/{dosya}",
              "odaklar": [{"kutu": b, "etiket": e} for b, e in odaklar], "anlatim": anlatim, **k})


def soru(baslik, metin, secenekler, dogru, anlatim, cevap_cumle, **k):
    S.append({"baslik": baslik, "tur": "soru", "soru": {"metin": metin, "secenekler": secenekler, "dogru": dogru,
              "cevap_cumle": cevap_cumle, "bekle": 4}, "anlatim": anlatim, **k})


# ───────────────────────────── Rehber nasıl kullanılır
m("Bu rehber ne öğretiyor?", ["Modelleme: UML, BPMN, süreç", "Veri ve entegrasyon: SQL, ELK, Postman",
                              "Kimlik yönetimi: IAM", "İş birliği: Jira, Confluence, Miro, Visio", "Çalışma biçimi: Agile"],
  "Bir iş analisti olarak teknik konuşmalarda geri kalmamak istiyorsan, bu seri tam sana göre. "
  "Rehber beş alanı kapsıyor. İlki modelleme: UML, BPMN ve süreç diyagramları. "
  "İkincisi veri ve entegrasyon: SQL, ELK ve Postman. Üçüncüsü kimlik yönetimi, yani IAM. "
  "Dördüncüsü iş birliği araçları: Jira, Confluence, Miro ve Visio. Beşincisi de çalışma biçimi: Agile.",
  bolum="Rehberi nasıl kullanmalı?", kanca="Bir analist, ekibin konuştuğu her teknik dili okuyabilmeli.", ton="merakli")
m("Her bölüm aynı sırayla ilerler", ["Temel: kavramlar ve notasyon", "Orta: günlük işte kullanım",
                                     "İleri: karmaşık senaryo, otomasyon", "Sonra: sık hatalar ve mülakat soruları"],
  "Her konu aynı merdivenle ilerliyor. Temel seviyede kavramları ve notasyonu öğreniyorsun. "
  "Orta seviyede bunları günlük işte nasıl kullandığını görüyorsun. "
  "İleri seviyede karmaşık senaryolara, yönetişime ve otomasyona çıkıyorsun. "
  "Sonra da sık yapılan hatalar ve mülakat soruları geliyor; bunlar iş görüşmesinde doğrudan karşına çıkabilir.")
t("Konu konu: BA ne yapar? (1/3)", ["Konu", "BA bu konuyla ne yapar?"],
  [["UML", "Sistem davranışını, veri modelini anlatır"], ["BPMN", "İş sürecini standart notasyonla modeller"],
   ["Süreç diyagramı", "Yöntemi seçer, as-is / to-be çalıştayı yönetir"], ["SQL", "Veriyi kendi sorgular, gereksinimi doğrular"]],
  "Şimdi her konunun senin işindeki karşılığına bakalım. UML ile sistem davranışını ve veri modelini anlatırsın. "
  "BPMN ile iş sürecini standart bir notasyonla modellersin. "
  "Süreç diyagramlamada doğru yöntemi seçer, mevcut durum ve hedef durum, yani {as-is} ve {to-be} çalıştaylarını yönetirsin. "
  "SQL ile veriyi başkasına sormadan kendin sorgular, gereksinimi veriyle doğrularsın.")
t("Konu konu: BA ne yapar? (2/3)", ["Konu", "BA bu konuyla ne yapar?"],
  [["ELK", "Loglardan hatanın izini sürer"], ["Postman", "API'leri dener ve test eder"],
   ["IAM", "Erişim süreçlerini ve yetki modelini tasarlar"], ["Jira", "Backlog'u ve teslimatı yönetir"]],
  "ELK ile loglardan bir hatanın izini sürersin. Postman ile API'leri dener ve test edersin. "
  "IAM tarafında erişim süreçlerini ve yetki modelini tasarlarsın. "
  "Jira ile de {backlog}'u, yani yapılacak işler listesini ve teslimatı yönetirsin.")
t("Konu konu: BA ne yapar? (3/3)", ["Konu", "BA bu konuyla ne yapar?"],
  [["Confluence", "Gereksinim ve kararları belgeler"], ["Miro", "Atölye ve ortak çizim yürütür"],
   ["Visio", "Resmi diyagramları üretir"], ["Agile", "Ekiple birlikte değer teslim eder"]],
  "Confluence, gereksinimleri ve alınan kararları belgelediğin yerdir. "
  "Miro ile atölye yürütür, ekiple birlikte ortak çizim yaparsın. Visio ile resmi, kurumsal diyagramları üretirsin. "
  "Agile ise hepsinin çerçevesi: ekiple birlikte, küçük adımlarla değer teslim edersin.")
t("İleri seviyede hedef ne?", ["Konu", "İleri seviye hedefi"],
  [["UML", "Diyagramları gereksinimle izlenebilir çizmek"], ["BPMN", "Olay alt süreci, hata ve telafi"],
   ["Süreç", "Değer akışı, süreç madenciliği"], ["SQL", "Window fonksiyonu, CTE, sorgu planı"],
   ["ELK", "ES|QL, Query DSL, pano ve alarm"], ["Postman", "Script'li test, veri güdümlü koşum, CI"]],
  "Her konunun bir de ileri seviye hedefi var. UML'de hedef, {sequence}, {state} ve {class} diyagramlarını gereksinimle izlenebilir çizmek. "
  "BPMN'de olay alt süreçlerini, hata ve telafi akışlarını, yürütülebilir modelleri doğru kullanmak. "
  "Süreçte değer akışı ve süreç madenciliğiyle iyileştirme fırsatı bulmak. "
  "SQL'de {window} fonksiyonları, CTE, sorgu planı ve veri kalitesi analizi. "
  "ELK'de i es kyu el ya da {Query} DSL ile analiz, pano ve alarm tasarımı. "
  "Postman'de script'li testler, veri güdümlü koşum ve CI entegrasyonu.")
t("İleri seviyede hedef ne? (devam)", ["Konu", "İleri seviye hedefi"],
  [["IAM", "SoD, recertification, OAuth / OIDC"], ["Jira", "İleri JQL, otomasyon, izlenebilirlik"],
   ["Confluence", "Bilgi mimarisi, şablon, yönetişim"], ["Miro", "Uzaktan çalıştay, story mapping"],
   ["Visio", "Veri bağlantılı diyagram, kural doğrulama"], ["Agile", "Regüle ortamda ölçekli Agile, metrik"]],
  "IAM'de görevler ayrılığı, yani SoD, periyodik yetki gözden geçirme, yani {recertification}, ve OAuth ile OIDC akışlarını gereksinime dökmek. "
  "Jira'da ileri JQL, otomasyon, iş akışı tasarımı ve izlenebilirlik. "
  "Confluence'ta bilgi mimarisi, şablon ve yönetişim. "
  "Miro'da uzaktan çalıştay tasarımı, {story mapping} ve {event storming}. "
  "Visio'da veri bağlantılı diyagram, kural doğrulama ve şablon standardı. "
  "Agile'da ise hibrit ve regüle bir ortamda ölçekli Agile ve metrik yönetimi.")
m("Önerilen çalışma sırası", ["1. Agile", "2. Süreç diyagramları ve BPMN", "3. UML", "4. Jira ve Confluence",
                             "5. Miro ve Visio", "6. SQL", "7. Postman ve ELK", "8. IAM"],
  "Rehber bir çalışma sırası öneriyor ve mantığı çok net. Birinci sırada Agile var, çünkü diğer araçların hangi süreçte kullanıldığını o anlatır. "
  "İkinci sırada süreç diyagramları ve BPMN: iş sürecini okumak ve çizmek. Üçüncü sırada UML: sistem davranışı ve veri modeli. "
  "Dördüncü sırada Jira ve Confluence: gereksinimi kaydetmek ve paylaşmak. Beşinci sırada Miro ve Visio: atölye ve resmi diyagram. "
  "Altıncı sırada SQL: veriyle doğrulamak. Yedinci sırada Postman ve ELK: entegrasyonu test etmek ve hatayı izlemek. "
  "Sekizinci ve son sırada IAM: yetki ve erişim gereksinimleri.")
dikkat("Tek başına çalışıyorsan", "Cevabı olmayan yerde: varsayım yap, açık soru olarak işaretle, alıştırmayı bitir.",
       "Burada dikkat etmen gereken bir çalışma kuralı var. Rehber, yanında soru soracağı bir iş birimi olmayan junior bir analist için yazıldı. "
       "Çalışma setinde cevabı olmayan bir noktaya gelirsen, rehber sana bir varsayım verir ve onu açık soru olarak işaretler. "
       "Kısacası: cevabı olmayan yerde varsayım yap, açık soru olarak işaretle, alıştırmayı bitir. "
       "Gerçek bir projede bu açık soruları iş birimine götürürsün.", tip="ipucu")
m("Her araç bölümünün iskeleti", ["Hedefler ve ön koşullar", "Temel, orta, ileri seviye", "Görsel rehber ve menüler",
                                  "Laboratuvar", "Uygulama paketi", "Çözümler"],
  "Her araç bölümü aynı iskeletle ilerliyor. Önce hedefler ve ön koşullar. Sonra temel, orta ve ileri seviye. "
  "Ardından görsel rehber ve menüler, yani bir ekranın nasıl okunacağı. Sonra elini kirleteceğin bir laboratuvar. "
  "Sonra uygulama paketi: bağımsız görev, sorun giderme, bilgi kontrolü ve hızlı başvuru. En sonda çözümler. "
  "Bir tavsiye: çözümlere bakmadan önce görevi kendin bitir.")

# ───────────────────────────── UML giriş
S.append({"baslik": "UML nedir?", "tur": "rakam", "kartlar": [
    {"deger": "2.5.1", "etiket": "Güncel sürüm (Aralık 2017)"}, {"deger": "14", "birim": "tür", "etiket": "Diyagram"},
    {"deger": "2.4", "etiket": "OCL kısıt dili"}],
    "anlatim": "İlk konumuz UML, yani {Unified Modeling Language}. Yazılım ve iş sistemlerini görsel olarak modellemek için "
               "OMG tarafından standartlaştırılmış bir dil. Güncel resmi sürüm iki nokta beş nokta bir, Aralık 2017'de yayımlandı; "
               "bu son sürümler yeni diyagram eklemedi, spesifikasyonu sadeleştirdi. Toplam on dört diyagram türü var. "
               "Kısıt dili olarak da OCL iki nokta dört kullanılıyor. "
               "Şunu aklında tut: UML senin için bir çizim aracı değil, gereksinimi belirsizlikten arındırmanın ortak dilidir.",
    "bolum": "UML"})
m("Bu bölümün sonunda…", ["Use case, class, sequence, state çiz ve oku", "Aynı diyagramı hem çiz hem metinle üret",
                          "Çokluk hatalarını kurallarla yakala", "Tek sayfalık C4 bağlam diyagramı çiz"],
  "Bu bölümü bitirdiğinde dört şey yapabileceksin. Bayi portalı için {use case}, {class}, {sequence} ve {state} diyagramlarını çizip, "
  "başkasının çizdiğini cümle cümle okuyacaksın. Aynı diyagramı hem çizim aracında hem de metinle, yani Mermaid ya da PlantUML ile üreteceksin. "
  "Bir {class} diyagramındaki çokluk değerlerini iş kurallarıyla karşılaştırıp hatalı olanı yakalayacaksın. "
  "Ve şirketin dış sistemlerle ilişkisini tek sayfalık bir C4 bağlam diyagramında göstereceksin.")
t("Başlamadan önce gerekenler", ["Gereken", "Hazır olduğunu nasıl anlarsın?"],
  [["Nesne, özellik, ilişki kavramı", "Başvuru-müşteri ilişkisini kutu ve çizgiyle çizebiliyorsun"],
   ["draw.io (ücretsiz)", "Sol altta + More Shapes düğmesi görünüyor"],
   ["Mermaid Live Editor", "Koda yazınca sağda diyagram anında değişiyor"],
   ["PlantUML çevrimiçi sunucu", "@startuml ile başlayan kod resim üretiyor"]],
  "Başlamadan önce dört şeye ihtiyacın var. Birincisi nesne, özellik ve ilişki kavramları; "
  "başvurunun bir müşteriye ait olduğunu kutu ve çizgiyle çizebiliyorsan hazırsın. "
  "İkincisi ücretsiz {draw dot io}; tarayıcıda açtığında sol altta {More Shapes} düğmesi görünüyorsa tamam. "
  "Üçüncüsü Mermaid canlı düzenleyici; soldaki koda yazınca sağda diyagram anında değişiyorsa çalışıyor. "
  "Dördüncüsü PlantUML çevrimiçi sunucusu; {at start} UML ile başlayan örnek kod bir resim üretiyorsa hazırsın.")

# ───────────────────────────── Temel
dikkat("Neden UML?", "Aynı varlığa farklı adlar: müşteri, başvuru sahibi, kiracı. UML bunu görünür kılar.",
       "Peki neden UML? Çünkü iş birimi, geliştirici, test ve mimar aynı şeyi farklı kelimelerle anlatır. "
       "Biri müşteri der, biri başvuru sahibi der, öbürü kiracı. "
       "UML aktörü, sistemi, nesneyi, mesajı ve durumu standart sembollerle gösterir. "
       "Böylece aynı varlığa farklı adlar verildiği görünür hale gelir: müşteri, başvuru sahibi, kiracı. UML bunu görünür kılar.",
       tip="ipucu", bolum="UML · Temel seviye")
t("14 diyagram (1/2): yapısal", ["Diyagram", "BA için tipik kullanım"],
  [["Class (sınıf)", "Domain modeli: müşteri, başvuru, sözleşme"], ["Object (nesne)", "Örnek veriyle modeli doğrulama"],
   ["Component (bileşen)", "Kredi motoru, CRM, sigorta modülü"], ["Deployment (dağıtım)", "Sunucu, DMZ, mobil, bulut"],
   ["Package (paket)", "Modülleri gruplama"], ["Composite Structure", "İç parçalar ve portlar (nadir)"],
   ["Profile", "Kuruma özel stereotype (ileri)"]],
  "On dört diyagram iki ana gruba ayrılır. İlki yapısal diyagramlar. "
  "{Class}, yani sınıf diyagramı, domain modelidir: müşteri, başvuru, sözleşme, araç, poliçe. "
  "{Object}, yani nesne diyagramı, sınıf modelini örnek veriyle doğrulamaya yarar. "
  "{Component}, yani bileşen diyagramı, kredi motoru, CRM, sigorta modülü gibi parçaları gösterir. "
  "{Deployment}, yani dağıtım diyagramı, sunucu, DMZ, mobil uygulama ve bulut ortamını gösterir. "
  "{Package}, yani paket, modülleri gruplar. {Composite Structure} bileşenin iç parçalarını ve portlarını gösterir; BA bunu nadiren kullanır. "
  "{Profile} ise kuruma özel {stereotype} tanımıdır, ileri seviye bir konudur.")
t("14 diyagram (2/2): davranış ve etkileşim", ["Diyagram", "BA için tipik kullanım"],
  [["Use Case", "Kapsam, aktör–sistem etkileşimi"], ["Activity (aktivite)", "İş akışı, karar, paralellik"],
   ["State Machine (durum)", "Başvuru, sözleşme yaşam döngüsü"], ["Sequence (sıralı)", "Ekran → API → kredi bürosu mesajları"],
   ["Communication", "Mesajları bağlantı odaklı gösterme"], ["Timing", "Zaman kısıtı: OTP 180 sn geçerli"],
   ["Interaction Overview", "Birden çok sequence'ı bağlama"]],
  "İkinci grup davranış ve etkileşim diyagramları. {Use Case} kapsamı ve aktör ile sistem etkileşimini gösterir. "
  "{Activity}, yani aktivite diyagramı, iş akışını, karar noktalarını ve paralelliği gösterir. "
  "{State Machine}, yani durum diyagramı, başvuru ya da sözleşme yaşam döngüsünü gösterir. "
  "{Sequence}, yani sıralı diyagram, ekrandan API'ye, oradan kredi bürosuna giden mesaj sırasını gösterir. "
  "{Communication} diyagramı aynı mesajları bağlantı odaklı gösterir. "
  "{Timing} diyagramı zaman kısıtlarını gösterir; örneğin bir OTP kodunun 180 saniye geçerli olması. "
  "{Interaction Overview} ise birden çok {sequence} diyagramını bir akışla bağlar.")
dikkat("En çok kullanılan beşli", "Use Case · Activity · Sequence · State Machine · Class",
       "Şimdi önemli bir not. Günlük işte en çok kullanacağın beşli şunlar: {Use Case}, {Activity}, {Sequence}, {State Machine} ve {Class}. "
       "Hepsini her projede çizmen gerekmez. Soruya en küçük, ama yeterli görünümle cevap verirsin.")
m("Use case diyagramı: semboller", ["Aktör (çöp adam): sistemle etkileşen rol", "Use case (elips): fiil + nesne",
                                    "Sistem sınırı (dikdörtgen): kapsam", "İlişkiler: association, include, extend, generalization"],
  "{Use case} diyagramının dört sembolü var. Aktör, yani çöp adam, sistemle etkileşen bir roldür; "
  "bayi satış temsilcisi gibi bir insan da olabilir, KKB, e-Devlet ya da sigorta şirketi gibi bir sistem de. "
  "{Use case}, yani elips, aktöre değer üreten bir hedeftir ve fiil artı nesne olarak yazılır: Kredi başvurusu yap. "
  "Sistem sınırı, yani dikdörtgen, kapsamın içini ve dışını ayırır. "
  "İlişkiler de dört tane: aktörle {use case} arasındaki {association}; her zaman çağrılan ortak adım için {include}, örneğin kimlik doğrula; "
  "koşullu ek davranış için {extend}, örneğin ek teminat iste; ve bireysel ile kurumsal müşterinin müşteriden türemesi gibi {generalization}.")
t("Use case anlatımı şablonu (1/2)", ["Alan", "Örnek: taşıt kredisi başvurusu"],
  [["Birincil aktör", "Bayi satış temsilcisi"], ["Ön koşul", "Bayi portalına giriş yapılmış, araç seçilmiş"],
   ["Tetikleyici", "Müşteri krediyle alım yapmak istiyor"],
   ["Ana akış", "TCKN ve iletişim, KVKK onayı, KKB sorgusu, ödeme planı, karar motoru, sonuç"]],
  "Diyagram tek başına yetmez; her {use case} bir anlatımla, yani bir şablonla yazılır. Örneğimiz taşıt kredisi başvurusu. "
  "Birincil aktör bayi satış temsilcisi. Ön koşul: kullanıcı bayi portalına giriş yapmış ve araç seçilmiş. "
  "Tetikleyici: müşteri krediyle alım yapmak istiyor. "
  "Ana akış altı adım: TCKN ve iletişim bilgisi girilir, KVKK onayı alınır, sistem KKB sorgusu yapar, "
  "ödeme planı hesaplanır, başvuru karar motoruna gönderilir ve sonuç ekranda gösterilir.")
t("Use case anlatımı şablonu (2/2)", ["Alan", "Örnek"],
  [["Alternatif akış", "KKB 5 sn'de yanıt vermez → manuel inceleme (U04)"],
   ["İstisna akış", "Müşteri KVKK onayı vermez → başvuru başlamaz"],
   ["Son koşul", "Başvuru no üretildi, durum kaydı, audit log"],
   ["İş kuralları", "BR-12 kredi/değer, BR-15 vade 6–60 ay, BR-21 yaş"]],
  "Alternatif akış: KKB beş saniye içinde yanıt vermezse, U04'te tanımlandığı gibi başvuru manuel incelemeye alınır "
  "ve kullanıcıya başvurunun incelemeye alındığı söylenir. "
  "İstisna akış: müşteri KVKK onayı vermezse başvuru başlatılamaz. "
  "Son koşul: başvuru numarası üretilmiş, durum kaydı oluşmuş ve {audit log} yazılmıştır. "
  "İş kuralları da şablona bağlanır: BR-12 kredi değer oranı, BR-15 vadenin altı ile altmış ay arasında olması, BR-21 yaş sınırı.")
dikkat("Son koşulu atlama", "Son koşul, test ekibinin 'iş bitti mi?' sorusunun cevabıdır.",
       "Burada dikkat: son koşulu atlamak çok yaygın bir hata. "
       "Çünkü son koşul, test ekibinin iş bitti mi sorusunun cevabıdır; olmazsa kabul kriteri havada kalır.")
m("Activity diyagramı: semboller", ["Başlangıç: dolu daire · bitiş: halkalı daire", "Aksiyon: yuvarlak köşeli kutu",
                                    "Karar / birleşme: eşkenar dörtgen", "Fork / join: kalın çubuk (paralel)",
                                    "Swimlane: sorumlu rol · object node: belge", "Guard: [skor >= 1500]"],
  "{Activity} diyagramının sembolleri de basit. Başlangıç dolu bir daire, bitiş ise halkalı bir dairedir. "
  "Aksiyon yuvarlak köşeli bir kutudur. Karar ve birleşme noktası eşkenar dörtgendir. "
  "{Fork} ve {join}, yani kalın çubuk, paralel akışı açar ve kapatır. "
  "{Swimlane}, yani şerit, sorumlu rolü; {object node} ise bir belgeyi ya da veriyi gösterir. "
  "Koşul, yani {guard}, köşeli parantez içinde yazılır; örneğin skor büyük eşit 1500.")

# ───────────────────────────── Orta
m("Sequence diyagramı: öğeler", ["Zaman yukarıdan aşağı akar", "Lifeline: katılımcı + kesikli çizgi",
                                 "Senkron mesaj: dolu ok · asenkron: açık ok", "Dönüş mesajı: kesikli ok",
                                 "Activation bar, self-message"],
  "Orta seviyeye geçiyoruz ve ilk durak {sequence} diyagramı. Burada zaman yukarıdan aşağı akar. "
  "Her katılımcının bir {lifeline}'ı vardır: üstte bir kutu, altında kesikli bir yaşam çizgisi. "
  "Senkron mesaj dolu okla, asenkron mesaj açık okla çizilir. Dönüş mesajı ise kesikli oktur. "
  "Bir katılımcının o an çalıştığını {activation bar} gösterir; kendine gönderdiği mesaja da {self message} denir.",
  bolum="UML · Orta seviye")
t("Combined fragment'lar (1/2)", ["Fragment", "Anlamı · örnek"],
  [["alt", "if / else: skor yeterli → onay, değilse ret"], ["opt", "Koşullu tek dal: kampanya kodu varsa indirim"],
   ["loop", "Tekrar: borçlu ve kefil için KKB sorgusu"], ["par", "Paralel: KKB ve MERNİS aynı anda"]],
  "Mantığı taşıyan kutulara {combined fragment} denir. {alt}, if else demektir: skor yeterliyse onay, değilse ret. "
  "{opt}, koşullu tek bir daldır: kampanya kodu varsa indirim hesaplanır. "
  "{loop} tekrar demektir: borçlu ve varsa kefil için KKB sorgusu, kişi başına bir tur. "
  "{par} paralel demektir: KKB ve MERNİS sorgusu aynı anda yapılır.")
t("Combined fragment'lar (2/2)", ["Fragment", "Anlamı · örnek"],
  [["break", "Akışı kes: kara liste eşleşmesi"], ["ref", "Başka diyagrama referans: kimlik doğrulama"],
   ["critical", "Bölünemez kısım: ödeme planı kaydı"]],
  "{break} akışı keser: kara liste eşleşmesi olursa işlem sonlanır. "
  "{ref} başka bir diyagrama referanstır: kimlik doğrulama ayrı bir {sequence} diyagramında anlatılır. "
  "{critical} ise bölünemez kısımdır: ödeme planı kaydı yarıda kesilemez.")
m("Metinle sequence: örneği okuyalım", ["Bayi → portal → başvuru API", "par: KKB skoru ile ödeme planı birlikte",
                                        "API → karar motoru: skor, gelir, LTV", "alt: onay → 201 + başvuru no",
                                        "alt: ret → 200 + ret mesajı"],
  "Rehber bu diyagramı PlantUML koduyla da veriyor; kodu satır satır okumak yerine ne anlattığını konuşalım. "
  "Bayi, başvuru bilgilerini portala girer, portal da başvuru API'sine istek gönderir. "
  "Sonra bir {par} bloğu var: bir yanda KKB'den skor sorgulanır, diğer yanda ödeme planı hesaplanır; yani KKB skoru ile ödeme planı birlikte. "
  "Ardından API, karar motorundan karar ister ve ona skor, gelir ve LTV bilgisini verir. "
  "En sonda {alt} bloğu: onay gelirse portala 201 ve başvuru numarası döner. Ret gelirse 200 ve ret mesajı döner, gerekçe koduyla birlikte.")
m("State machine diyagramı", ["Bir nesnenin yaşam döngüsü", "Geçiş etiketi: olay [guard] / aksiyon",
                              "U08: Taslak → Değerlendirmede → … → Kullandırıldı", "Son durumlar: Reddedildi, İptal / Süresi Doldu",
                              "İleri: composite, history (H), entry / exit / do", "Zaman aşımı: after(30 gün) / İptal et"],
  "{State machine}, yani durum diyagramı, bir nesnenin yaşam döngüsünü gösterir. "
  "Geçiş etiketinin kalıbı şöyle: önce olay, köşeli parantezde koşul yani {guard}, eğik çizgiden sonra da aksiyon. "
  "U08'deki başvuru durumları taslaktan başlar, değerlendirmeye geçer, oradan onay, manuel inceleme ya da ek belgeye dallanır "
  "ve sözleşme imzası, kullandırım kontrolü üzerinden kullandırıldı durumuna varır. "
  "Reddedildi ile İptal ya da süresi doldu da son durumlardır. "
  "İleri öğeler de var: içinde alt durumlar barındıran {composite state}, kaldığı yeri hatırlayan {history state}, "
  "durum girişinde, çıkışında ve süresince çalışan {entry}, {exit} ve {do} aktiviteleri. "
  "Ve zaman aşımı olayı: after otuz gün, iptal et.")
t("Class diyagramı (1/2)", ["Öğe", "Gösterim · örnek"],
  [["Sınıf", "Üç bölme: ad, nitelikler, operasyonlar"], ["Görünürlük", "+ public, - private, # protected, ~ package"],
   ["Association", "Düz çizgi + çokluk: Müşteri 1 — 0..* Sözleşme"],
   ["Aggregation", "Boş elmas: Bayi ◇ Satış temsilcisi (bağımsız yaşar)"],
   ["Composition", "Dolu elmas: Sözleşme ◆ Ödeme planı satırı"]],
  "{Class} diyagramı domain modelinin omurgasıdır. Sınıf üç bölmeli bir kutudur: ad, nitelikler ve operasyonlar. "
  "Görünürlük işaretleri şöyle: artı {public}, eksi {private}, diyez {protected}, yaklaşık işareti {package}. "
  "{Association} düz bir çizgidir ve uçlarına çokluk yazılır: bir müşterinin sıfır ya da daha çok sözleşmesi olur. "
  "{Aggregation} boş elmastır: bayi ile satış temsilcisi; temsilci bayi olmadan da yaşayabilir. "
  "{Composition} dolu elmastır: sözleşme ile ödeme planı satırı; sözleşme silinirse satır da ölür.")
t("Class diyagramı (2/2)", ["Öğe", "Gösterim · örnek"],
  [["Generalization", "Boş üçgen ok: Kurumsal müşteri ▷ Müşteri"], ["Dependency", "Kesikli ok: Fiyatlama ⇢ Faiz tablosu"],
   ["Realization", "Kesikli + boş üçgen: KKB adapter ⇢ arayüz"],
   ["Enumeration", "«enumeration»: TASLAK, DEGERLENDIRMEDE, …"], ["Çokluk", "1 · 0..1 · 0..* · 1..* · 2..5"]],
  "{Generalization} boş üçgenli oktur: kurumsal müşteri bir müşteridir. "
  "{Dependency} kesikli oktur: fiyatlama servisi faiz tablosunu geçici olarak kullanır. "
  "{Realization} kesikli çizgi artı boş üçgendir: KKB adapter, kredi bürosu arayüzünü uygular. "
  "{Enumeration} ise sabit değer listesidir: taslak, değerlendirmede, manuel inceleme, onaylandı, reddedildi, iptal ve devamı. "
  "Çokluk değerleri de şunlar: bir; sıfır ya da bir; sıfır ya da çok; bir ya da çok; ve iki ile beş gibi bir aralık.")
S.append({"baslik": "Component ve Deployment", "tur": "karsilastirma",
          "sol": {"baslik": "Component", "renk": "mavi"}, "sag": {"baslik": "Deployment", "renk": "yesil"},
          "satirlar": [["Sağlanan arayüz: lollipop ○", "Node: 3B kutu"], ["Gereken arayüz: socket ◐", "Ortam ve artifact"],
                       ["Entegrasyon envanteri için ideal", "HTTPS, MQ, SFTP yolları; güvenlik ekibiyle kapsam"]],
          "anlatim": "İki yapısal diyagramı yan yana koyalım. Önce {Component}: sağlanan arayüz bir lolipop, yani yuvarlakla gösterilir. "
                     "Gereken arayüz ise bir soket, yani yarım ayla gösterilir. "
                     "Bu diyagram entegrasyon envanteri çıkarmak için idealdir. "
                     "Şimdi {Deployment}: her node üç boyutlu bir kutudur. "
                     "Çalışma ortamı ve {artifact}, yani dağıtılan dosya, onun içinde durur. "
                     "İletişim yolları da yazılır: HTTPS, MQ, SFTP; bu diyagramla güvenlik ve altyapı ekibiyle kapsam konuşursun."})

# ───────────────────────────── İleri
m("İleri seviye (1/2)", ["Stereotype ve profile: «entity», «PII», «auditable»",
                         "OCL: diyagramın anlatamadığı kurallar", "Robustness (ECB): boundary, control, entity",
                         "İzlenebilirlik: REQ → use case → sequence → API → test"],
  "İleri seviyede dört konu var. Birincisi {stereotype} ve {profile}. "
  "Entity, PII, auditable gibi kurumsal etiketler bir profile içinde tanımlanır; "
  "örneğin PII olarak işaretlenen her nitelik otomatik olarak maskelemeye ve KVKK envanterine bağlanabilir. "
  "İkincisi OCL: diyagramın anlatamadığı kuralları kesinleştirir; birazdan örneklerini göreceğiz. "
  "Üçüncüsü {Robustness}, yani ECB analizi: {use case}'ten {sequence}'a geçmeden önce {boundary} yani ekran ve API, "
  "{control} yani iş mantığı, {entity} yani veri nesnelerini çıkarırsın; eksik ekranlar erken yakalanır. "
  "Dördüncüsü izlenebilirlik: gereksinim numarasından {use case}'e, oradan {sequence}'a, API'ye ve test senaryosuna giden zincir. "
  "Enterprise Architect, Visual Paradigm ya da Cameo gibi araçlarda bu zincir {trace}, {refine} ve {satisfy} ilişkileriyle kurulur.",
  bolum="UML · İleri seviye")
t("OCL ile iş kuralı yazmak", ["Kural", "Ne söylüyor?"],
  [["Vade kuralı", "Vade 6 ile 60 ay arasında"], ["Bireysel üst sınır", "Bireyselde 2.000.000 TL üstü finanse edilmez"],
   ["Bireysel ilk kademe", "400.000 TL'ye kadar kredi değer oranı en fazla %70"],
   ["Kurumsal kredi değer", "Kurumsalda fatura bedelinin %90'ına kadar"],
   ["Kredi kapat()", "Ön koşul: AKTIF · son koşul: KAPANDI"]],
  "Rehber OCL'i gerçek kurallarla gösteriyor. Vade kuralı: vade altı ile altmış ay arasında olmalı. "
  "Bireysel üst sınır: bireyselde fatura bedeli iki milyon lira üstü olan araç finanse edilmez. "
  "Bireysel ilk kademe: fatura bedeli dört yüz bin liraya kadar olan araçta kredi değer oranı en fazla yüzde yetmiştir. "
  "Kurumsal kredi değer kuralı: kurumsalda kredi fatura bedelinin yüzde doksanına kadar çıkabilir. "
  "Bir de operasyon kuralı var: kredi kapatılmadan önce durumu aktif olmalı, kapatıldıktan sonra kapandı olmalı; "
  "bunlara ön koşul ve son koşul denir.")
m("İleri seviye (2/2)", ["Model ≠ diyagram: sınıf bir kez tanımlanır", "XMI: araçlar arası taşıma",
                         "Text-as-model: PlantUML, Mermaid, Git", "C4 üst seviye + UML detay"],
  "İleri seviyenin geri kalanı da şu dört fikir. Model ile diyagram aynı şey değildir: gerçek bir modelleme aracında sınıf bir kez tanımlanır, "
  "birçok diyagramda görünür ve değişiklik her yere yansır. Visio ya da Miro gibi çizim araçlarında bu tutarlılığı sen elle sağlarsın. "
  "XMI, UML modellerini araçlar arasında taşımaya yarayan formattır. "
  "{Text as model} yaklaşımında diyagramları PlantUML ya da Mermaid ile metin olarak yazarsın; böylece Git'te versiyonlanır, "
  "Confluence'a gömülür ve kod incelemesine girer. "
  "Son olarak C4: mimarinin üst seviyesi için C4, detay için UML {sequence} ve {state}; bu çok yaygın bir ikilidir.")
m("Sık yapılan hatalar", ["Use case'e ekran adı vermek", "Include / extend okunu ters çizmek",
                          "Use case'i akış diyagramı sanmak", "Sequence'ta dönüş ve hata dallarını atlamak",
                          "Aggregation / composition karışıklığı, boş çokluk", "State'te çıkmaz durum bırakmak"],
  "Şimdi en sık yapılan altı hatayı konuşalım. Birincisi {use case}'e ekran adı vermek: başvuru ekranı değil, başvuru yap demelisin. "
  "İkincisi {include} ve {extend} okunu ters çizmek. "
  "Üçüncüsü {use case} diyagramını akış diyagramı sanmak; o sıra göstermez. "
  "Dördüncüsü {sequence}'ta dönüş mesajlarını ve hata dallarını, yani {alt} bloğunu atlamak. "
  "Beşincisi {aggregation} ile {composition}'ı karıştırmak ve çoklukları boş bırakmak. "
  "Altıncısı {state} diyagramında son durum olmayan çıkmaz durumlar bırakmak.", bolum="UML · Hatalar ve mülakat")
dikkat("Ok yönü kuralı", "include: ana use case → ortak parça. extend: ek davranış → ana use case.",
       "Bu konu mülakatta çok sorulduğu için ayrıca altını çiziyorum. "
       "{include} oku ana {use case}'ten ortak parçaya gider. {extend} oku ise koşullu ek davranıştan ana {use case}'e döner. "
       "Kısacası: include ana use case'ten ortak parçaya; extend ek davranıştan ana use case'e.")
m("Mülakat soruları", ["1. Include ile extend farkı? Örnek ver", "2. Activity mi, BPMN mi? Ne zaman?",
                       "3. Sözleşme yaşam döngüsü hangi diyagramla?", "4. Composition ve aggregation farkı",
                       "5. Sequence'ta alt ile opt farkı", "6. Son koşulu neden yazarız?"],
  "Bu bölümün mülakat soruları ve kısa cevapları şöyle. Bir: {include} ile {extend} farkı nedir, kredi başvurusundan örnek ver. "
  "Cevap: kimlik doğrula her başvuruda çalışır, {include}; ek belge yükle yalnızca belge eksikse eklenir, {extend}. "
  "İki: {activity} mi, BPMN mi, ne zaman? Sistem içi mantık ve UML modeliyle bütünlük gerekiyorsa {activity}; "
  "iş birimiyle konuşulan, kurumlar arası iş süreci için BPMN. "
  "Üç: sözleşme yaşam döngüsü hangi diyagramla? {State machine} ile, çünkü durumları ve izin verilen geçişleri gösterir. "
  "Dört: {composition} ve {aggregation} farkı nedir? Bütünü silince parça da ölüyorsa {composition}, yaşıyorsa {aggregation}. "
  "Beş: {sequence}'ta {alt} ile {opt} farkı nedir? {alt} birden çok daldan birini seçer, {opt} tek bir dalı ya çalıştırır ya atlar. "
  "Altı: son koşulu neden yazarız? Çünkü işin bittiğini ve testin neyi doğrulayacağını o söyler.")

# ───────────────────────────── Görsel rehber
g("Class diyagramı nasıl okunur?", "g01.png",
  [([0.0, 0.05, 0.85, 0.42], "Kutu: ad, nitelik, operasyon"), ([0.0, 0.55, 1.0, 0.78], "Association · aggregation · composition"),
   ([0.0, 0.78, 1.0, 1.0], "Generalization · realization · dependency")],
  "Şimdi görsellerle çalışalım. İlki {class} diyagramı okuma kılavuzu. "
  "Üstte bir kutunun anatomisi var; kutu ad, nitelik ve operasyon bölmelerinden oluşur: ad bölmesinde varlığın adı, nitelik bölmesinde görünürlük, ad ve tip, "
  "operasyon bölmesinde de ad, parametre ve dönüş tipi. Altı çizili nitelik {static} demektir, yani tüm nesnelerde ortak bir değer. "
  "Altta ilişki türleri: ilk sırada {association}, {aggregation} ve {composition}; düz çizgi, boş elmas ve dolu elmas. "
  "İkinci sırada {generalization}, {realization} ve {dependency}; boş üçgen, kesikli çizgiyle boş üçgen ve kesikli ok. "
  "Okuma sırası şu: önce kutuların adları, sonra çizgiler, en son kutuların içi. "
  "Her çizgi için iki cümle kur: bir müşterinin sıfır ya da daha çok sözleşmesi vardır; her sözleşme tam bir müşteriye aittir.",
  bolum="UML · Görsel rehber")
dikkat("Aggregation mı, composition mı?", "Sor: bütünü silersem parça da silinir mi? Evet → dolu elmas. Hayır → boş elmas.",
       "Bu ayrımı hatırlamanın tek bir sorusu var. Sor: bütünü silersem parça da silinir mi? "
       "Sözleşme silinirse taksitleri anlamsızlaşır, demek ki evet, dolu elmas, yani {composition}. "
       "Bayi kapanırsa personel başka bayide çalışabilir, demek ki hayır, boş elmas, yani {aggregation}. "
       "Bir de şunu unutma: elmas her zaman bütün tarafında durur.")
g("Use case diyagramı", "g02.png",
  [([0.0, 0.1, 0.62, 0.65], "Kredi başvurusu: include ve extend"), ([0.5, 0.2, 1.0, 0.95], "Dış aktörler: KKB, tahsis uzmanı")],
  "İkinci görsel bayi portalının {use case} diyagramı. Bayi temsilcisi portalda kredi başvurusu yapar. "
  "Kredi başvurusunda include ve extend birlikte görünüyor: her başvuruda kimlik doğrulama ve KKB skoru sorgulama her zaman çalışır, bu {include}. "
  "Belge eksikse başvuruya ek belge yükleme koşullu olarak eklenir, bu da {extend}. "
  "Ok yönlerine dikkat et: {include} oku ana {use case}'ten ortak parçaya gider, {extend} oku ek davranıştan ana {use case}'e döner. "
  "Sağdaki dış aktörlere bak: KKB servisi ve tahsis uzmanı. KKB bir insan değil ama sistemin dışında olduğu için aktördür.")
g("Sequence diyagramı", "g03.png",
  [([0.1, 0.25, 0.8, 0.5], "3–4: par kutusu"), ([0.15, 0.5, 1.0, 0.85], "alt: onay (6–7) / ret (8–9)")],
  "Üçüncü görsel bir {sequence} diyagramı. Numaraları sırayla takip et: bayi başvuruyu girer, portal API'ye gönderir. "
  "Üç ve dört numaralı mesajlar {par} kutusunun içinde. Dikkat: bu çizim sadeleştirilmiş. "
  "Gerçek bir {par} kutusu kesikli yatay bir çizgiyle en az iki bölmeye ayrılır ve bölmeler aynı anda çalışır; "
  "örneğin üstte KKB sorgusu, altta kimlik doğrulama. "
  "Aşağıdaki {alt} kutusuna gel: onay durumunda altı ve yedi, ret durumunda sekiz ve dokuz çalışır; ikisi asla birlikte çalışmaz. "
  "Aynı diyagramı test ekibi entegrasyon senaryosu olarak, geliştirici de API sözleşmesi olarak kullanır.")
g("State machine diyagramı", "g04.png",
  [([0.0, 0.15, 0.7, 0.7], "İnceleme: onay, ret ya da ek belge"), ([0.6, 0.15, 1.0, 0.9], "Onaydan sonra: 30 gün, imza, kullandırım")],
  "Dördüncü görsel bir {state machine} diyagramı. Başvuru taslak olarak doğar, gönderilince incelemeye alınır. "
  "İnceleme üç şekilde sonuçlanır: onay, ret ya da ek belge isteği. Ek belge tamamlanınca başvuru yeniden incelemeye döner. "
  "Onaydan sonra yol şöyle: onaylanan başvuru otuz gün içinde imzalanmazsa, U08'de olduğu gibi iptal olur; imzalanırsa kullandırıma gider. "
  "Bu diyagramın sana değeri şu: reddedilen başvuru yeniden incelemeye alınabilir mi gibi soruların cevabını tek bakışta görürsün. "
  "Ok yoksa geçiş de yoktur; sistem bu geçişi engellemelidir. "
  "Not: bu çizim okumayı öğretmek için sade; on iki durumun tamamı birazdan Mermaid örneğinde ve atölyedeki U08'de.")

# ───────────────────────────── Menü rehberi
t("UML'i hangi araçta çizersin? (1/2)", ["Araç", "Nasıl başlarsın, neye dikkat edersin?"],
  [["draw.io (ücretsiz)", "More Shapes → UML · Style → Line end · Export as PNG"],
   ["Visio (Plan 1/2)", "New → UML Class · sağ tık Add/Delete Members · Align"]],
  "Peki bunları nerede çizeceksin? {draw dot io} ücretsizdir: yeni diyagram açtığında şablon listesinde UML'i seçersin. "
  "Sol paneldeki {More Shapes} ile UML ve UML 2.5 kütüphanelerini açarsın. Sınıf kutusunu sürükler, satıra çift tıklayıp yazarsın. "
  "Ok ucunu değiştirmek için çizgiyi seçer, sağ panelde {Style} altından {Line end} ile elmas ya da üçgen seçersin; "
  "kesikli çizgi için de {Style}, {Pattern}, {dashed}. Bitince {Export as} ile PNG, SVG ya da PDF alırsın. "
  "Visio'da {New} menüsünden UML Class, Use Case, Sequence ya da State Machine şablonunu açarsın. "
  "Sınıf şekline sağ tıklayıp {Add Delete Members} ile nitelik ve operasyon eklersin; "
  "ilişki şekilleri şablonun panelindedir; hizalama için de {Align} ve {Auto Align and Space}.")
t("UML'i hangi araçta çizersin? (2/2)", ["Araç", "Nasıl başlarsın?"],
  [["PlantUML (metin)", "@startuml … @enduml · Git'te versiyonlanır"],
   ["Mermaid (metin)", "classDiagram, sequenceDiagram, stateDiagram-v2"],
   ["Enterprise Architect / Visual Paradigm", "Gerçek model deposu, «trace» bağı"]],
  "Metinle çizmek istersen iki seçenek var. PlantUML'de {at start} UML ile {at end} UML arasına yazarsın, diyagram otomatik çizilir "
  "ve Git'te versiyonlanır. Mermaid Confluence, GitHub ve Markdown düzenleyicilerde çalışır; "
  "{classDiagram}, {sequenceDiagram} ya da {stateDiagram} v2 anahtar kelimesiyle başlarsın. "
  "Enterprise Architect ya da Visual Paradigm ise gerçek bir model deposudur: "
  "bir sınıfı bir kez tanımlar, birçok diyagramda kullanır ve gereksinimle {trace} bağı kurarsın.")
m("Mermaid söz dizimi: ilişki okları", ["--  association", "*--  composition", "o--  aggregation", "<|--  generalization",
                                        "..|>  realization · ..>  dependency", "Tırnaktaki sayı: çokluk"],
  "Rehberdeki Mermaid örneğinde müşteri, sözleşme, taksit ve kurumsal müşteri sınıfları var; ezberlemen gereken şey oklar. "
  "İki tire {association} demektir. Yıldız ve iki tire {composition}. Küçük o ve iki tire {aggregation}. "
  "Küçüktür, dik çizgi ve iki tire {generalization}. İki nokta, dik çizgi ve büyüktür {realization}; iki nokta ve büyüktür {dependency}. "
  "Tırnak içindeki sayı da çokluğu verir: örneğin müşteri bir, sözleşme sıfır ya da çok.")

# ───────────────────────────── Laboratuvar
m("Laboratuvar: domain modeli (1/2) · ~40 dk", ["1. Varlıkları bul: Müşteri, Başvuru, Araç, Bayi…",
                                                 "2. draw.io: her varlığa bir Class", "3. Her sınıfa 3–5 nitelik; PII'yi not et",
                                                 "4. İlişki ve çokluk: Sözleşme ◆ 1..* Taksit"],
  "Şimdi yaklaşık kırk dakikalık bir laboratuvar. Birinci adım varlıkları bulmak: kredi sürecinin metnini oku ve geçen isimlerin altını çiz. "
  "Müşteri, başvuru, araç, bayi, sözleşme, taksit, poliçe ve teminat; her biri bir sınıf adayı. "
  "İkinci adım: {draw dot io}'da boş bir diyagram aç, UML kütüphanesini işaretle ve her varlık için bir {Class} şekli koy. "
  "Üçüncü adım: her sınıfa üç ila beş nitelik yaz; TCKN ve telefon gibi kişisel verileri not et, ileride PII olarak işaretlenecek. "
  "Dördüncü adım ilişki ve çokluk: müşteri bir, başvuru sıfır ya da çok; başvuru bir, sözleşme sıfır ya da bir; "
  "sözleşme dolu elmasla bir ya da çok taksit; sözleşme bir, poliçe sıfır ya da çok; bayi bir, başvuru sıfır ya da çok; "
  "çok başvuru bir araca.", bolum="UML · Laboratuvar")
m("Laboratuvar: domain modeli (2/2)", ["5. Kalıtım: Bireysel, Kurumsal → Müşteri", "6. Her çizgi için iki cümle kur, sesli oku",
                                       "7. Yeni sayfada sequence ekle", "8. PNG ve .drawio'yu Confluence'a koy"],
  "Beşinci adım kalıtım: bireysel müşteri ve kurumsal müşteri, müşteriden türer; kasko ve trafik de poliçeden. "
  "Altıncı adım doğrulama: her çizgi için iki cümle kur ve sesli oku. Cümle çalışma setindeki bir kurala ters düşüyorsa çizgi yanlıştır. "
  "Bir başvurunun birden çok sözleşmesi olabilir mi gibi sorular gereksinim boşluklarını ortaya çıkarır. "
  "Yedinci adım: aynı dosyada yeni bir sayfa aç ve {sequence} örneğini MERNİS ve sigorta şirketi entegrasyonlarıyla genişlet. "
  "Sekizinci adım: PNG olarak dışa aktar, Confluence'taki gereksinim sayfasına koy ve kaynak dosyayı da ekle.")

# ───────────────────────────── Uygulama paketi
t("Sık UML hataları ve doğrusu (1/3)", ["Hata", "Doğrusu"],
  [["include oku ters: KKB sorgula → başvuru", "Kredi başvurusu yap → «include» → KKB sorgula"],
   ["extend oku ters: değerlendir → manuel", "Manuel incelemeye al → «extend» → değerlendir"],
   ["Use case'i adımlara bölmek: formu aç, kaydet", "Tek use case: Kredi başvurusu yap"]],
  "Uygulama paketinde rehber sekiz hatayı yanlış ve doğru haliyle veriyor. "
  "Birinci hata {include} okunun ters olması: KKB sorgula'dan başvuruya çizmek. Doğrusu, kredi başvurusu yap'tan KKB sorgula'ya. "
  "İkinci hata {extend} okunun ters olması: değerlendir'den manuel incelemeye çizmek. "
  "Doğrusu, manuel incelemeye al'dan başvuruyu değerlendir'e, çünkü ok koşullu eklenen davranıştan çıkar. "
  "Üçüncü hata {use case}'i adımlara bölmek: formu aç, TCKN yaz, kaydet. Doğrusu tek bir {use case}: kredi başvurusu yap; "
  "adımlar senaryonun içinde yazılır.", bolum="UML · Uygulama paketi")
t("Sık UML hataları ve doğrusu (2/3)", ["Hata", "Doğrusu"],
  [["Veritabanını aktör yapmak", "Aktör dışarıdadır: KKB, sigorta; DB çizilmez"],
   ["Kefil çokluğu 1..*", "Kefil 0..1: ortak araçta biri borçlu, biri kefil"],
   ["Sözleşme — Taksit düz çizgi", "Sözleşme ◆— Taksit: dolu elmas"]],
  "Dördüncü hata veritabanını aktör yapmak. Aktör sistemin dışındadır: KKB ve sigorta şirketi dış aktördür, veritabanı diyagramda yer almaz. "
  "Beşinci hata kefil çokluğunu bir ya da çok yazmak. Doğrusu sıfır ya da bir, çünkü kural şu: "
  "ortak araçta biri borçlu, diğeri kefil olur ve çapraz kefalet yoktur. "
  "Altıncı hata sözleşme ile taksiti düz çizgiyle bağlamak. Doğrusu dolu elmas, çünkü taksit sözleşme olmadan var olamaz.")
t("Sık UML hataları ve doğrusu (3/3)", ["Hata", "Doğrusu"],
  [["KKB yanıtı düz çizgi", "Dönüş kesikli: KKB --> karar motoru: skor"],
   ["ONAYLANDI → IPTAL : iptal et", "gün sonu [30 gün geçti] / bayiye bildir"]],
  "Yedinci hata KKB yanıtını düz çizgiyle çizmek. Dönüş mesajı kesiklidir; düz çizgi yeni bir çağrı demektir. "
  "Sekizinci hata {state} geçişinde koşulu eylem gibi yazmak: onaylandı'dan iptal'e giden oka sadece iptal et yazmak. "
  "Doğrusu olay, koşul, eylem sırasıdır: gün sonu, köşeli parantezde otuz gün geçti, eğik çizgi, bayiye bildir.")
g("Aynı model metinle: U08 (Mermaid)", "g05.png",
  [([0.0, 0.0, 1.0, 0.35], "Taslak → değerlendirme → manuel inceleme"), ([0.0, 0.3, 1.0, 0.65], "Komite, şartlı onay, onay"),
   ([0.0, 0.6, 1.0, 1.0], "İmza → kullandırım kontrol → kullandırıldı")],
  "Bu görsel, U08 başvuru yaşam döngüsünün Mermaid koduyla üretilmiş hali. Kodu Mermaid canlı düzenleyici sayfasına yapıştırınca bu çıkar. "
  "Yukarıdan okuyalım: taslak, zorunlu belgeler tamsa değerlendirmeye gider; değerlendirme, manuel inceleme ve ek belge arasında gidip gelebilir. "
  "Kural uyarısı ya da KKB zaman aşımı olursa manuel incelemeye düşer. "
  "Orta kısımda komite, şartlı onay ve onay var: manuel inceleme onay, şartlı onay ya da ret verebilir; limit dışıysa komiteye gider. "
  "Şartlar kabul edilip yeniden hesaplanınca onaylandı olur. "
  "Alt kısımda imza ile kullandırım kontrolü ve kullandırıldı var: imza ve evrakla sözleşme imzalanır, kullandırım kontrolüne gider; "
  "eksik evrak varsa bayiye iade edilir, ödeme emri onaylanınca kullandırıldı olur.")
dikkat("Doğru yaptığını nasıl anlarsın?", "12 durum · 18 ok · IPTAL'e 2 yerden · REDDEDILDI'ye 2 yerden ok gelir",
       "Kendini kontrol etmek için şu sayıya bak: on iki durum ve başlangıç ile bitiş hariç on sekiz ok. "
       "İptal'e iki yerden, taslaktan ve onaylandı'dan; reddedildi'ye de iki yerden, manuel incelemeden ve komiteden ok gelir. "
       "Bir de teknik dikkat: kodda durum adları Türkçe karakter içermez, büyük harfle yazılır; örneğin İptal ya da süresi doldu, IPTAL olur.")
m("C4 bağlam diyagramı", ["4 seviye: Context, Container, Component, Code", "BA için en faydalısı: Context",
                          "Kişiler: bayi satış temsilcisi, kredi analisti", "Dış sistemler: KKB, sigorta şirketi",
                          "Her ok bir fiil: skor sorgular (5 sn zaman aşımı)"],
  "Şimdi C4 modeli. C4 bir sistemi dört yakınlaştırma seviyesinde anlatır: Context, Container, Component ve Code. "
  "Senin için en faydalısı ilki, yani bağlam: sistem bir kutu, etrafında kullanıcılar ve dış sistemler. "
  "Mülakatta şirketin kredi sistemini bir sayfada anlat derlerse cevabı budur. "
  "Rehberdeki örnekte kişiler bayi satış temsilcisi ve kredi analisti; temsilci başvuru gönderir, analist manuel incelemedeki başvuruya karar verir. "
  "Dış sistemler KKB ve sigorta şirketi: KKB'den kredi notu ve risk raporu, sigortadan kasko poliçesi ve dain-i mürtehin bilgisi gelir. "
  "Kontrol kuralı basit: mavi kutular kişiler ve bizim sistemimiz, gri kutular dış sistemler ve her ok bir fiille etiketlidir; "
  "örneğin skor sorgular, beş saniye zaman aşımı.")
m("Bağımsız görev: bireysel ve kurumsal müşteri", ["Kurumsal: kredi ≤ fatura × %90", "Bireysel: kredi / değer kademeli",
                                                   "İkinci el: 8 yaş, 160.000 km, 75.000 ₺", "Ortak araç: biri borçlu, biri kefil",
                                                   "En fazla 7 sınıf, 0..1 çokluk, 2 kısıt notu"],
  "Sıra bağımsız görevde. İhtiyaç şu: şirket hem bireysel hem kurumsal müşteriye kredi veriyor. "
  "Kurumsalda kredi tutarı fatura bedelinin yüzde doksanını aşamaz. Bireyselde kredi değer oranı tutara göre kademelidir. "
  "İkinci el araçta garanti sekiz yaş, yüz altmış bin kilometre ve yetmiş beş bin lira sınırlarına bağlıdır. "
  "Ortak araçta biri borçlu, diğeri kefildir. "
  "İstenen: en fazla yedi sınıflık bir {class} diyagramı; içinde {generalization}, {composition}, en az bir sıfır ya da bir çokluk "
  "ve kuralları gösteren en az iki kısıt notu olsun. "
  "Doğru yaptıysan, bir başvuruda en fazla kaç kefil olur sorusunu sadece diyagrama bakarak cevaplayabilirsin.")
t("Sorun giderme (1/2)", ["Belirti", "Çözüm"],
  [["Mermaid 'Parse error'", "Kimliği ASCII yaz: state \"Manuel inceleme\" as MANUEL"],
   ["PlantUML 'Syntax Error'", "İlk ve son satırı, ok yazımını kontrol et"],
   ["C4 'Cannot include'", "Standart biçim: !include <C4/C4_Context>"]],
  "Takıldığında işine yarayacak sorun giderme tablosu. Mermaid {Parse error} veriyorsa, sınıf ya da durum adında boşluk veya Türkçe karakter vardır; "
  "kimliği ASCII yaz, görünen adı ayrı ver: örneğin {state} Manuel inceleme, {as} MANUEL. "
  "PlantUML {Syntax Error} veriyorsa başlangıç ya da bitiş satırı eksiktir veya ok yazımı hatalıdır; "
  "ilk ve son satırı ve ok yazımını kontrol et, hata satırı resimde görünür. "
  "C4 kodu {Cannot include} diyorsa, standart kütüphane biçimini kullan; yerel dosya yolu yalnızca kendi bilgisayarındaki PlantUML'de çalışır.",
  bolum="UML · Sorun giderme ve bilgi kontrolü")
t("Sorun giderme (2/2)", ["Belirti", "Çözüm"],
  [["draw.io'da UML şekli yok", "+ More Shapes → UML ve Entity Relation → Apply"],
   ["Ok ucu yanlış tip", "Oku seç → Style → Line end"],
   ["Çizgiler kesişiyor, okunmuyor", "9'dan fazla sınıf varsa paketlere böl"]],
  "{draw dot io}'da UML şekilleri yoksa kütüphane kapalıdır: {More Shapes}'ten UML ve {Entity Relation}'ı işaretleyip {Apply} de. "
  "Ok ucu yanlış tipteyse, mesela elmas yerine düz ok çıktıysa, oku seç ve {Style} altından {Line end} ile doğru ucu seç. "
  "Diyagram okunmuyor ve çizgiler kesişiyorsa muhtemelen tek diyagramda dokuzdan fazla sınıf vardır; "
  "başvuru, teminat ve ödeme gibi paketlere böl, her paketi ayrı çiz.")
soru("Bilgi kontrolü 1/5", "'Manuel incelemeye al' yalnızca KKB zaman aşımında devreye giriyor. 'Başvuruyu değerlendir' ile ilişkisi?",
     ["include, ana use case'ten ona", "extend, ondan ana use case'e", "generalization", "association"], 1,
     "Beş soruluk bilgi kontrolü. Birinci soru: manuel incelemeye al, yalnızca KKB zaman aşımında devreye giriyor. "
     "Başvuruyu değerlendir ile ilişkisi nedir? A, {include}, ana {use case}'ten ona. B, {extend}, ondan ana {use case}'e. "
     "C, {generalization}. D, {association}. "
     "Doğru cevap B: {extend}, ondan ana {use case}'e. Koşullu bir davranış olduğu için {extend}, ve ok ek davranıştan ana {use case}'e gider.", 4)
soru("Bilgi kontrolü 2/5", "Taksit kaydı, sözleşme silinince anlamını yitiriyor. İlişki türü?",
     ["Association", "Aggregation", "Composition", "Dependency"], 2,
     "İkinci soru: taksit kaydı, sözleşme silinince anlamını yitiriyor. İlişki türü nedir? "
     "A, {Association}. B, {Aggregation}. C, {Composition}. D, {Dependency}. "
     "Doğru cevap C: {Composition}. Bütün silinince parça da ölüyor, yani dolu elmas.", 2)
soru("Bilgi kontrolü 3/5", "Senkron çağrının ardından ters yönde çizilen kesikli ok neyi gösterir?",
     ["Asenkron çağrı", "Dönüş mesajı", "Kendi kendine çağrı", "Koşullu dal (alt)"], 1,
     "Üçüncü soru: {sequence} diyagramında senkron bir çağrının ardından ters yönde çizilen kesikli ok neyi gösterir? "
     "A, asenkron çağrı. B, dönüş mesajı. C, kendi kendine çağrı. D, koşullu dal, yani {alt}. "
     "Doğru cevap B: dönüş mesajı.", 2)
soru("Bilgi kontrolü 4/5", "'onay [30 gün geçti] / bildir' etiketinde köşeli parantez neyi gösterir?",
     ["Olay", "Eylem", "Koşul (guard)", "Durum adı"], 2,
     "Dördüncü soru: onay, köşeli parantezde otuz gün geçti, eğik çizgi, bildir etiketinde köşeli parantez neyi gösterir? "
     "A, olay. B, eylem. C, koşul, yani {guard}. D, durum adı. "
     "Doğru cevap C: koşul, yani {guard}. Kalıbı hatırla: olay, koşul, eylem.", 2)
soru("Bilgi kontrolü 5/5", "Bir başvuruda en fazla bir kefil olabiliyor ve kefil zorunlu değil. Doğru çokluk?",
     ["1", "0..1", "1..*", "0..*"], 1,
     "Beşinci soru: bir başvuruda en fazla bir kefil olabiliyor ve kefil zorunlu değil. Doğru çokluk nedir? "
     "A, bir. B, sıfır ya da bir. C, bir ya da çok. D, sıfır ya da çok. "
     "Doğru cevap B: sıfır ya da bir. Sıfır, zorunlu olmadığı için; bir, en fazla bir kefil olduğu için.", 2)
t("Hızlı başvuru: ok ve ilişki yazımı (1/2)", ["Anlam", "Çizimde · Mermaid / PlantUML"],
  [["Association", "Düz çizgi · A -- B"], ["Composition", "Dolu elmas, bütün tarafında · A *-- B"],
   ["Aggregation", "Boş elmas, bütün tarafında · A o-- B"], ["Generalization", "Boş üçgen, üst sınıfta · A <|-- B"]],
  "Son olarak cebinde tutacağın hızlı başvuru tablosu. {Association}: düz çizgi, metinde A iki tire B. "
  "{Composition}: dolu elmas, bütün tarafında; metinde yıldız iki tire. "
  "{Aggregation}: boş elmas, yine bütün tarafında; metinde küçük o iki tire. "
  "{Generalization}: boş üçgen, üst sınıf tarafında; metinde küçüktür, dik çizgi, iki tire.")
t("Hızlı başvuru: ok ve ilişki yazımı (2/2)", ["Anlam", "Çizimde · yazımı"],
  [["Senkron çağrı", "Düz çizgi, dolu ok · A -> B: mesaj"], ["Dönüş", "Kesikli çizgi · B --> A: yanıt"],
   ["include", "Kesikli ok, ana → dahil edilen · .> <<include>>"], ["extend", "Kesikli ok, ek → ana · .> <<extend>>"]],
  "{Sequence} tarafında senkron çağrı düz çizgi ve dolu oktur; PlantUML'de A tire büyüktür B, iki nokta, mesaj. "
  "Dönüş ise kesikli çizgidir: B iki tire büyüktür A, iki nokta, yanıt. "
  "{include}, ana {use case}'ten dahil edilene giden kesikli oktur ve include etiketi taşır. "
  "{extend}, ek davranıştan ana {use case}'e giden kesikli oktur ve extend etiketi taşır. "
  "Mermaid'de {use case} diyagramı olmadığını da unutma.")
g("Çözüm: bağımsız görev", "g06.png",
  [([0.0, 0.0, 0.7, 0.4], "Müşteri: bireysel ve kurumsal"), ([0.25, 0.35, 1.0, 0.65], "Başvuru: kefil 0..1, kurallar notta"),
   ([0.3, 0.55, 0.85, 1.0], "Araç ◆ başvuru · kasko 0..1")],
  "Ve bağımsız görevin örnek çözümü. Üstte müşteri: bireysel ve kurumsal müşteri, soyut müşteri sınıfından türüyor. "
  "Ortada başvuru: kefil sıfır ya da bir, kurallar notta; borçlu ilişkisi müşteriye, kefil ilişkisi ise yalnızca bireysel müşteriye bağlı. "
  "Notta vade altı ile altmış ay, kurumsalda tutarın fatura bedelinin yüzde doksanını aşmaması ve bireyselde kademeli oran yazıyor. "
  "Altta araç ve kasko: araç başvuruya dolu elmasla bağlı, kasko sıfır ya da bir. "
  "Araç notunda ikinci el garanti sınırları var: sekiz yaş, yüz altmış bin kilometre, yetmiş beş bin lira.",
  bolum="UML · Çözümler")
dikkat("Çözümdeki kararların gerekçesi", "Kurumsal kefil kuralı yok → varsay ve açık soru yap. Çapraz kefalet çoklukla gösterilemez → kısıt notu.",
       "Bu çözümdeki kararların gerekçelerine dikkat et, çünkü asıl öğrenme burada. "
       "Kefil yalnızca bireysel müşteriye bağlandı; kurumsal kefil kuralı çalışma setinde yok. "
       "Bu yüzden kurumsal başvuruda kefil olmadığını varsayıyoruz ve bunu açık soru olarak not ediyoruz. "
       "Araç başvuruya {composition} ile bağlı, çünkü başvurusuz araç kaydı bu modelde anlam taşımıyor. "
       "Kasko sıfır ya da bir, çünkü başvuru aşamasında poliçe henüz olmayabilir; kullandırımdan önce zorunlu olduğu bir kısıt notuyla eklenmeli. "
       "Ve çapraz kefalet yasağı, yani A, B'ye kefilken B'nin A'ya kefil olamaması, çoklukla gösterilemez; bunu da kısıt notuyla yazarsın. "
       "Özetle: kurumsal kefil kuralı yoksa varsay ve açık soru yap; çapraz kefalet çoklukla gösterilemez, kısıt notu yaz.")
m("Bu videoda neler gördük?", ["UML: 14 diyagram, en çok kullanılan beşli", "Use case anlatımı ve ok yönleri",
                               "Sequence fragment'ları, state geçiş kalıbı", "Class ilişkileri ve çokluk", "OCL, C4, laboratuvar ve görev"],
  "Toparlayalım. UML'in on dört diyagramını ve en çok kullanacağın beşliyi gördük. "
  "{Use case} anlatımını ve {include} ile {extend} ok yönlerini öğrendik. "
  "{Sequence} {fragment}'larını ve {state} geçişindeki olay, koşul, eylem kalıbını konuştuk. "
  "{Class} ilişkilerini ve çokluğu, OCL ile iş kuralını, C4 bağlam diyagramını, laboratuvarı ve bağımsız görevi tamamladık. "
  "Bir sonraki videoda BPMN ile iş süreçlerini modellemeye başlıyoruz.", ton="sakin")

sen = {
    "baslik": "Business Analyst Teknik Rehberi · 1: Rehber ve UML",
    "alt_baslik": "Rehberin kullanımı · UML temel, orta, ileri · uygulama",
    "kapanis": "Sıradaki video: BPMN",
    "tema": 1, "ingilizce_mod": "sozluk", "hiz_tavani": 1.9, "cumle_arasi": 0.6,
    "youtube_baslik": "Business Analyst Teknik Rehberi 1/14: UML (use case, class, sequence, state)",
    "etiketler": ["business analyst", "UML", "use case", "sequence diagram", "class diagram", "iş analisti"],
    "telaffuz": {
        "UML": "yu em el", "BPMN": "bi pi em en", "OMG": "o em ci", "OCL": "o si el", "KKB": "ka ka be", "KVKK": "ka ve ka ka",
        "TCKN": "te ce ka en", "API": "ey pi ay", "API'ye": "ey pi aya", "API'den": "ey pi aydan", "API'si": "ey pi ayı",
        "ECB": "i si bi", "XMI": "eks em ay", "PII": "pi ay ay", "C4": "si for", "LTV": "el ti vi", "MERNİS": "mernis",
        "OTP": "o ti pi", "DMZ": "di em zi", "MQ": "em kyu", "SFTP": "es ef ti pi", "HTTPS": "eyç ti ti pi es", "PNG": "pi en ci",
        "SVG": "es vi ci", "PDF": "pi di ef", "CRM": "si ar em", "SQL": "es kü el", "ELK": "elk", "IAM": "ay ey em",
        "SoD": "es o di", "OAuth": "o of", "OIDC": "o ay di si", "JQL": "cey kyu el", "CTE": "si ti i", "CI": "si ay",
        "DSL": "di es el", "ES": "i es", "ASCII": "aski", "DB": "di bi", "U04": "u sıfır dört", "U07": "u sıfır yedi",
        "U08": "u sıfır sekiz", "U08'de": "u sıfır sekizde", "U04'te": "u sıfır dörtte", "U08'deki": "u sıfır sekizdeki",
        "BR-12": "be re on iki", "BR-15": "be re on beş", "BR-21": "be re yirmi bir", "Mermaid": "mörmeyd", "Mermaid'de": "mörmeyd'de", "Mermaid'in": "mörmeydin",
        "PlantUML": "plant yu em el", "Postman": "post men", "Jira": "cira", "Confluence": "konfluens", "Miro": "miro",
        "Visio": "vizyo", "Agile": "ecayl", "draw.io": "dro ay o", "Git": "git", "GitHub": "git hab",
        "Enterprise": "entırprayz", "Architect": "arkitekt", "Visual": "vijuıl", "Paradigm": "paradaym", "Cameo": "kemio",
        "e-Devlet": "e devlet",
    },
}
sen["sahneler"] = S
Path(__file__).with_suffix(".json").write_text(json.dumps(sen, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(S), "sahne", sum(len(s["anlatim"].split()) for s in S), "kelime")
