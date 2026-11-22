#!/usr/bin/env python3
"""BA Teknik Rehberi · Video 9: IAM (Identity and Access Management). Belge satır 2541–2850."""
from ortak import m, t, dikkat, g, soru, kaydet

# ───────────────────────────── Giriş
m("IAM nedir?", ["Doğru kişi · doğru kaynak · doğru zaman · doğru neden · doğru yetki", "Süreç, politika ve teknolojilerin bütünü",
                 "Finansta: BDDK, KVKK, iç kontrol, denetim bulguları", "BA: rol modeli, yetki matrisi, onay akışları, SoD, entegrasyon"],
  "IAM, yani {Identity and Access Management}: doğru kişinin, doğru kaynağa, doğru zamanda, doğru nedenle ve doğru yetkiyle erişmesini sağlayan "
  "süreç, politika ve teknolojilerin bütünüdür. Finans sektöründe IAM; BDDK bilgi sistemleri düzenlemeleri, KVKK, iç kontrol ve denetim bulgularının "
  "en sık konu olduğu alanlardan biridir. İş analisti IAM projelerinde rol modelini, yetki matrisini, onay akışlarını, SoD kurallarını "
  "ve entegrasyon gereksinimlerini yazar.", bolum="IAM: giriş ve hedefler", kanca="Kim, neye, neden erişebiliyor? Bu sorunun cevabı senin elinde.", ton="merakli")
m("Bu bölümün hedefleri", ["Kimlik doğrulama ile yetkilendirmeyi benzetme ve Firma örneğiyle ayırmak",
                           "Bayi portalı ve servisler arası çağrı için doğru OAuth akışını seçmek",
                           "JWT'yi çözüp exp, aud, scope ile kabul / ret kararı vermek",
                           "RBAC, ABAC, ReBAC ile kural yazmak, SoD çatışmalarını bulmak"],
  "Bu bölümü bitirdiğinde şunları yapabileceksin. Bir: kimlik doğrulama ile yetkilendirmeyi bir benzetmeyle ve bir Firma örneğiyle ayırmak. "
  "İki: bayi portalı ve servisler arası çağrı için doğru {OAuth} akışını seçmek ve nedenini söylemek. "
  "Üç: bir JWT'yi çözüp {exp}, {aud} ve {scope} alanlarına bakarak isteğin kabul edilip edilmeyeceğine karar vermek. "
  "Dört: RBAC, ABAC ve ReBAC ile Firma yetki kuralları yazmak ve görev ayrılığı, yani SoD çatışmalarını bulmak.")
t("Başlamadan önce gerekenler", ["Gereken", "Nereden", "Hazır mısın?"],
  [["HTTP header ve durum kodları", "Postman bölümü", "401 ile 403 farkı"], ["JSON okuma", "Postman bölümü", "İç içe JSON'da alan bulmak"],
   ["JWT çözücü", "jwt.io (yalnız eğitim token'ı)", "Token yapıştırınca sağda JSON"], ["Firma rolleri", "Çalışma Seti", "Bayi, operasyon, tahsis, analist"]],
  "Başlamadan önce gerekenler. HTTP {header} ve durum kodları: Postman bölümü; dört yüz bir ile dört yüz üç farkını söyleyebiliyorsan hazırsın. "
  "JSON okuma: iç içe bir JSON'da bir alanın değerini bulabiliyorsan tamam. "
  "JWT çözücü: jwt nokta io; yalnız eğitim token'ları için. Sayfaya örnek token yapıştırınca sağda JSON görünüyorsa tamam. "
  "Firma rolleri: çalışma setindeki bayi, kredi operasyon, tahsis ve analist; her rolün ne iş yaptığını bir cümleyle söyleyebiliyorsan başlayabiliriz.")

# ───────────────────────────── Temel
t("Temel kavramlar (1/2)", ["Kavram", "Anlamı", "Örnek"],
  [["Identification", "\"Ben kimim?\" beyanı", "Kullanıcı adı, TCKN"], ["Authentication (AuthN)", "Kimliğin doğrulanması", "Şifre + SMS OTP"],
   ["Authorization (AuthZ)", "Neye erişebileceği", "Bayi yalnız kendi başvurularını görür"], ["Accounting / Audit", "Yapılanın kaydı", "\"tahsis_04 BSV-1001'i onayladı\""]],
  "Temel kavramlar. {Identification}: ben kimim beyanı; kullanıcı adı ya da TCKN. "
  "{Authentication}, kısaca {AuthN}: kimliğin doğrulanması; şifre artı SMS OTP. "
  "{Authorization}, kısaca {AuthZ}: neye erişebileceğinin belirlenmesi; bayi sadece kendi başvurularını görür. "
  "{Accounting} ya da {Audit}: yapılanın kaydı; tahsis_04 BSV-1001'i onayladı gibi bir log.", bolum="IAM · Temel seviye")
t("Temel kavramlar (2/2)", ["Kavram", "Anlamı", "Örnek"],
  [["Least privilege", "İş için gereken en az yetki", "Raporlamaya salt okunur"], ["Need-to-know", "Yalnız gerekli veri", "Çağrı merkezinde TCKN maskeli"],
   ["SoD (Segregation of Duties)", "Kritik işlemi tek kişi baştan sona yapamaz", "Kredi giren onaylayamaz"]],
  "{Least privilege}, en az yetki: iş için gereken en az yetki; raporlama kullanıcısına salt okunur erişim. "
  "{Need-to-know}: sadece gerekli veriye erişim; çağrı merkezinde TCKN'nin maskeli görünmesi. "
  "SoD, yani {Segregation of Duties}, görevler ayrılığı: kritik bir işlemi tek kişi baştan sona yapamaz; kredi giren kişi aynı krediyi onaylayamaz.")
m("Kimlik doğrulama faktörleri ve MFA", ["Bildiğin: şifre, PIN", "Sahip olduğun: telefon, donanım anahtarı, OTP", "Olduğun: biyometri",
                                         "MFA = farklı kategoriden en az iki faktör; iki şifre MFA değil",
                                         "SMS OTP yaygın ama SIM swap riski → push onay ya da FIDO2 / passkey daha güçlü"],
  "Kimlik doğrulama faktörleri üç kategoridir: bildiğin bir şey, yani şifre ya da PIN; sahip olduğun bir şey, yani telefon, donanım anahtarı ya da OTP; "
  "olduğun bir şey, yani biyometri. MFA, farklı kategoriden en az iki faktör demektir; iki şifre MFA değildir. "
  "SMS OTP yaygındır ama {SIM swap} riskine karşı {push} bildirimli uygulama onayı ya da {FIDO2} ve {passkey} daha güçlüdür.")
t("Joiner – Mover – Leaver (JML)", ["Aşama", "Tetikleyici", "Beklenen davranış"],
  [["Joiner", "İK'da işe giriş", "Birthright roller otomatik; ek yetki için talep ve onay"],
   ["Mover", "Departman / pozisyon değişikliği", "Yeni roller verilir, eskiler süre içinde alınır"],
   ["Leaver", "İşten çıkış", "Aynı gün (kritikte anında) tüm hesaplar ve oturumlar kapanır"]],
  "Kimlik yaşam döngüsü: {Joiner}, {Mover}, {Leaver}, kısaca JML. "
  "{Joiner}: tetikleyici İK sistemindeki işe giriş kaydı. Pozisyona göre doğum hakkı, yani {birthright} roller otomatik verilir; ek yetkiler için talep ve onay gerekir. "
  "{Mover}: tetikleyici departman ya da pozisyon değişikliği. Yeni roller verilir, eski roller belirli bir süre içinde alınır; bu yetki birikmesini önler. "
  "{Leaver}: tetikleyici işten çıkış. Aynı gün, kritik sistemlerde anında, tüm hesaplar kapatılır ve oturumlar sonlandırılır.")
dikkat("Dış kullanıcılar da JML'de", "Bayi personeli, dış kaynak, sigorta acentesi · en sık denetim bulgusu: işten ayrılan bayi personelinin aktif hesabı",
       "Dış kullanıcılar için de JML gerekir: bayi personeli, dış kaynak ve sigorta acentesi. "
       "En sık denetim bulgusu, işten ayrılan bayi personelinin aktif kalan hesabıdır. Bayi senin İK sistemine bağlı değildir; bu yüzden ayrı bir süreç ister.")

# ───────────────────────────── Orta
t("Yetkilendirme modelleri", ["Model", "Mantık", "Artı / Eksi"],
  [["RBAC (Role-Based)", "Kullanıcı → Rol → Yetki", "Anlaşılır / rol patlaması"], ["ABAC (Attribute-Based)", "Kullanıcı, kaynak, ortam, aksiyon nitelikleri", "İnce taneli / test zor"],
   ["ReBAC (Relationship-Based)", "İlişkiye göre (başvurunun sahibi bayi)", "Sahiplik için doğal / araç sınırlı"], ["PBAC / Policy-as-code", "Merkezi politika motoru (OPA)", "Tutarlı / ek altyapı"]],
  "Orta seviye: yetkilendirme modelleri. RBAC, yani {Role-Based}: kullanıcı, rol, yetki. Anlaşılır ve denetlenebilir; ama rol patlaması riski var. "
  "ABAC, yani {Attribute-Based}: kullanıcı, kaynak, ortam ve aksiyon niteliklerine göre politika. İnce taneli; ama tasarımı ve testi zor. "
  "ReBAC, yani {Relationship-Based}: ilişkiye göre; örneğin bu başvurunun sahibi bayi. Veri sahipliği için doğal; ama araç desteği sınırlı. "
  "PBAC ya da {Policy-as-code}: merkezi bir politika motoru, örneğin OPA. Tutarlı; ama ek altyapı ister. "
  "Pratikte hibrit kullanılır: RBAC ile kaba yetki, örneğin kredi tahsis uzmanı; ABAC ile ince kural, örneğin onay limiti bir milyon liraya kadar, "
  "sadece kendi bölgesi, mesai saatleri içinde.", bolum="IAM · Orta seviye")
t("Yetki matrisi örneği (1/2)", ["Fonksiyon", "Bayi Satış", "Tahsis Uzmanı", "Tahsis Yöneticisi", "Operasyon"],
  [["Başvuru oluştur", "✓ kendi bayisi", "–", "–", "–"], ["Başvuru görüntüle", "✓ kendi bayisi", "✓", "✓", "✓"],
   ["Kredi onayla ≤ 1M TL", "–", "✓", "✓", "–"], ["Kredi onayla > 1M TL", "–", "–", "✓", "–"], ["Kullandırım yap", "–", "–", "–", "✓"]],
  "Yetki matrisi; iş analistinin tipik çıktısı. Başvuru oluştur: yalnız bayi satış, kendi bayisi için. "
  "Başvuru görüntüle: bayi satış kendi bayisi; tahsis uzmanı, tahsis yöneticisi ve operasyon görebilir. "
  "Kredi onayla, bir milyon TL'ye kadar, ki bu örnek bir limit: tahsis uzmanı ve tahsis yöneticisi. "
  "Kredi onayla, bir milyon TL'nin üstü: yalnız tahsis yöneticisi. Kullandırım yap: yalnız operasyon.")
t("Yetki matrisi örneği (2/2)", ["Fonksiyon", "Çağrı Merkezi", "Denetçi", "Not"],
  [["Başvuru görüntüle", "✓ (maskeli)", "✓ (salt okunur)", ""], ["Onay · kullandırım", "–", "–", ""],
   ["Faiz parametresi değiştir", "–", "–", "Yalnız Ürün Yönetimi, 4 göz"]],
  "Çağrı merkezi başvuruyu maskeli görür; denetçi salt okunur görür. İkisi de onaylayamaz ve kullandıramaz. "
  "Faiz parametresi değiştirme ise matristeki hiçbir rolde yok: sadece ürün yönetimi yapabilir, o da dört göz ilkesiyle.")
m("SoD kural örnekleri", ["Başvuru giren ≠ onaylayan", "Ödeme talimatı giren ≠ onaylayan", "Yetki talep eden ≠ onaylayan",
                          "Parametre değiştiren ≠ onaylayan (maker–checker / 4 göz)", "Önleyici (atamada) + tespit edici (periyodik rapor)"],
  "SoD kural örnekleri: başvuru giren onaylayan olamaz; ödeme talimatı giren onaylayan olamaz; kullanıcı yetkisi talep eden onaylayan olamaz; "
  "parametre değiştiren onaylayan olamaz. Bu {maker-checker}, yani dört göz ilkesidir. "
  "SoD çatışması iki türlü kontrol edilir: rol ataması anında önleyici, yani {preventive}; ve periyodik raporla tespit edici, yani {detective}.")
t("Federasyon ve SSO protokolleri", ["Protokol", "Amaç", "Tipik kullanım"],
  [["SAML 2.0", "Kurumsal SSO · XML", "Jira, Confluence, SaaS"], ["OAuth 2.0", "Yetki devri · token", "Mobil → API"],
   ["OIDC", "OAuth + kimlik · ID token", "Web/mobil giriş"], ["LDAP / Kerberos", "Dizin / iç ağ", "Active Directory"], ["SCIM 2.0", "Hesap aç/kapa", "IdP → SaaS"]],
  "Federasyon ve SSO protokolleri. SAML iki nokta sıfır: kurumsal SSO, yani kimlik doğrulama; XML {assertion}; çalışanın Jira, Confluence ve SaaS uygulamalarına girişi. "
  "{OAuth} iki nokta sıfır: yetki devri, yani {authorization}; {access token} ve {refresh token}; mobil uygulamanın API'ye erişimi, sistemler arası erişim. "
  "{OpenID Connect}, kısaca OIDC: {OAuth} üzerine bir kimlik katmanı; {ID token}, bir JWT; modern web ve mobil giriş, müşteri portalı. "
  "LDAP ve {Kerberos}: dizin sorgusu ve iç ağ kimlik doğrulama; {Active Directory}. "
  "SCIM iki nokta sıfır: kullanıcı hesaplarını otomatik açma ve kapama; REST ve JSON; kimlik sağlayıcıdan SaaS uygulamalara {provisioning}.")
m("OAuth 2.0 akışları", ["Authorization Code + PKCE: kullanıcılı web / mobil (önerilen)", "Client Credentials: servisten servise",
                         "Device Code: klavyesiz cihaz · Refresh Token", "Implicit ve Resource Owner Password artık önerilmez (OAuth 2.1 taslağı çıkarır)"],
  "{OAuth} iki nokta sıfır akışları, yani {grant types}. {Authorization Code} artı PKCE: kullanıcılı web ve mobil uygulamalar için önerilen. "
  "{Client Credentials}: servisten servise. {Device Code}: klavyesiz cihazlar. Ve {Refresh Token}. "
  "{Implicit} ve {Resource Owner Password} akışları güvenlik nedeniyle artık önerilmez; {OAuth} iki nokta bir taslağı bunları çıkarır.")
m("Authorization Code + PKCE (özet)", ["1. code_verifier üret, hash'i (code_challenge) ile yetkilendirme sunucusuna yönlendir",
                                       "2. Kullanıcı giriş + MFA, onay", "3. Tek kullanımlık code ile geri yönlendirme",
                                       "4. code + code_verifier → token endpoint → access (ve ID) token", "5. API: imza, süre, aud, scope doğrular"],
  "{Authorization Code} artı PKCE akışının özeti beş adım. Bir: uygulama {code_verifier} üretir, onun özetiyle, yani {code_challenge} ile kullanıcıyı yetkilendirme sunucusuna yönlendirir. "
  "İki: kullanıcı giriş yapar, MFA'yı tamamlar ve onay verir. Üç: sunucu tek kullanımlık bir {code} ile geri yönlendirir. "
  "Dört: uygulama {code} ve {code_verifier} ile {token endpoint}'inden {access token} alır; OIDC ise {ID token} da alır. "
  "Beş: {access token} ile API çağrılır; API token'ın imzasını, süresini, {aud} ve {scope} değerlerini doğrular.")
m("JWT yapısı", ["header.payload.signature", "iss (yayıncı) · sub (kullanıcı) · aud (hedef)", "exp (bitiş) · iat · scope · roles",
                 "JWT şifreli değil, imzalı → içine kişisel veri konmaz"],
  "JWT yapısı üç parçadır: {header}, nokta, {payload}, nokta, {signature}. Önemli {claim}'ler: {iss}, yayıncı; {sub}, kullanıcı; {aud}, hedef; "
  "{exp}, bitiş; {iat}, üretilme zamanı; {scope} ve {roles}. "
  "Dikkat: JWT şifreli değil, imzalıdır. Herkes içini okuyabilir; bu yüzden içine kişisel veri konmaz.")

# ───────────────────────────── İleri
t("IAM alt alanları ve araçlar", ["Alan", "Kapsam", "Örnek"],
  [["Access Mgmt / SSO", "Giriş, MFA, oturum", "Entra ID, Okta, Keycloak"], ["IGA", "JML, talep, recertification", "SailPoint, Saviynt"],
   ["PAM", "Admin, kasa, just-in-time", "CyberArk, Delinea"], ["CIAM", "Müşteri girişi, onay", "Auth0, Keycloak"], ["Directory", "Kimlik deposu", "Active Directory"]],
  "İleri seviye: IAM alt alanları ve araç kategorileri. {Access Management} ya da SSO: giriş, MFA, federasyon ve oturum; "
  "{Microsoft Entra ID}, {Okta}, {Ping}, {Keycloak}, {ForgeRock}. "
  "IGA, yani {Identity Governance} {and} {Administration}: JML otomasyonu, erişim talebi, yetki gözden geçirme yani {recertification}, ve SoD; "
  "{SailPoint}, {Saviynt}, {One Identity}, {Omada}. "
  "PAM, yani {Privileged Access Management}: admin hesapları, şifre kasası, oturum kaydı ve {just-in-time} erişim; {CyberArk}, {BeyondTrust}, {Delinea}. "
  "CIAM, yani {Customer IAM}: müşteri kayıt ve giriş, onay yönetimi, sosyal giriş, ölçeklenebilirlik; {Auth0}, {Keycloak}, {ForgeRock}, {Entra External ID}. "
  "{Directory}: kimlik deposu; {Active Directory} ve LDAP.", bolum="IAM · İleri seviye")
m("Erişim gözden geçirme ve Zero Trust", ["Recertification: 3–6 ayda bir onay / kaldır", "Yanıt yok = yetki kaldır · kanıt raporu", "Zero Trust: asla güvenme, doğrula", "Koşullu erişim, mikro segmentasyon"],
  "Erişim gözden geçirme, yani {access recertification}: yöneticiler periyodik olarak, kritik sistemlerde örneğin üç ile altı ayda bir, ekiplerinin yetkilerini onaylar ya da kaldırır. "
  "İş analisti gereksinimleri: kampanya kapsamı, gözden geçiren atama kuralı, hatırlatma ve eskalasyon, yanıt yok eşittir yetki kaldır politikası, "
  "ve denetim için kanıt raporu. "
  "{Zero Trust}: asla güvenme, her zaman doğrula. Ağ konumu güven kaynağı sayılmaz; her istek kimlik, cihaz durumu ve bağlama göre değerlendirilir; "
  "NIST SP sekiz yüz tire iki yüz yedi. Uygulamalar: koşullu erişim, yani {conditional access}; risk tabanlı, yani {adaptive} kimlik doğrulama; "
  "mikro segmentasyon; sürekli oturum değerlendirmesi.")
m("Güvence seviyeleri ve CIAM gereksinimleri", ["NIST SP 800-63 (IAL / AAL / FAL): riske göre doğrulama gücü",
                                                "Başvuru sorgulama: tek faktör + cihaz tanıma · IBAN değişikliği, erken kapama: step-up MFA",
                                                "CIAM: uzaktan kimlik (görüntülü görüşme / NFC), e-Devlet ile giriş, KVKK rıza versiyonu",
                                                "Başarısız giriş kilidi · şifre sıfırlamada ele geçirme koruması · cihaz ve oturum listesi"],
  "Kimlik doğrulama güvence seviyeleri: NIST SP sekiz yüz tire altmış üç, yani IAL, AAL ve FAL, gibi çerçeveler işlemin riskine göre gereken doğrulama gücünü tanımlar. "
  "Örneğin başvuru sorgulama için tek faktör artı cihaz tanıma yeterli olabilirken, IBAN değişikliği ya da erken kapama talebi için {step-up} MFA istenir. "
  "Müşteri tarafı, yani CIAM gereksinim örnekleri: uzaktan müşteri edinimi ve kimlik doğrulama, mevzuata uygun görüntülü görüşme ya da NFC kimlik okuma; "
  "e-Devlet ile giriş entegrasyonu; KVKK açık rıza ve aydınlatma metni versiyon kaydı; başarısız giriş kilitleme politikası; "
  "şifre sıfırlama akışının hesap ele geçirmeye karşı korunması; cihaz yönetimi ve oturum listesi.")
m("Makine kimlikleri ve IAM metrikleri", ["Servis hesabı, API anahtarı, sertifika: sahiplik, rotasyon, kasa, interaktif girişe kapalı, envanter",
                                          "Leaver kapatma süresi · yetim (orphan) hesap · SoD ihlali", "Recertification tamamlanma · MFA kapsama",
                                          "Ayrıcalıklı hesap sayısı · erişim talebi karşılama süresi"],
  "Makine kimlikleri: servis hesapları, {API} anahtarları ve sertifikalar. Gereksinim: sahiplik, rotasyon süresi, kasada saklama, "
  "insan hesabı gibi interaktif girişe kapalı olma ve envanter. "
  "IAM metrikleri: {Leaver} hesapların kapatılma süresi, yetim yani {orphan} hesap sayısı, SoD ihlal sayısı, {recertification} tamamlanma oranı, "
  "MFA kapsama oranı, ayrıcalıklı hesap sayısı ve erişim talebi karşılama süresi.")

# ───────────────────────────── Hatalar, mülakat
m("Sık yapılan hatalar", ["Rolü kişi bazında tasarlamak (\"Ayşe'nin rolü\") → rol patlaması", "Yetkiyi yalnız ekranda gizlemek",
                          "Ortak (paylaşılan) hesap", "Mover'da eski yetkiyi almamak (birikme)",
                          "AuthN ile AuthZ'yi karıştırmak; OAuth'u kimlik doğrulama sanmak · dış kullanıcıyı kapsam dışı bırakmak"],
  "Sık yapılan hatalar. Rol tasarımını kişi bazında yapmak, Ayşe'nin rolü gibi; sonuç rol patlaması. "
  "Yetkiyi sadece ekranda gizlemek, API ya da servis katmanında kontrol etmemek. Ortak, yani paylaşılan kullanıcı hesapları; işlemin kime ait olduğu bilinemez. "
  "{Mover} sürecinde eski yetkileri almamak; yetki birikmesi. {Authentication} ile {authorization}'ı karıştırmak; {OAuth}'u kimlik doğrulama protokolü sanmak. "
  "Ve dış kullanıcıları, yani bayi ve acenteyi, IAM kapsamı dışında bırakmak.", bolum="IAM · Hatalar ve mülakat")
m("Mülakat soruları", ["1. Authentication ve authorization farkı", "2. SAML, OAuth 2.0, OIDC farkları", "3. RBAC mı, ABAC mı?",
                       "4. Bayi personeli ayrıldığında hangi süreç?", "5. SoD nedir? Üç örnek", "6. Yetki matrisinde hangi paydaşlar?"],
  "Mülakat soruları. Bir: {authentication} ve {authorization} farkı nedir? Kredi sürecinden örnek verin. "
  "İki: SAML, {OAuth} iki nokta sıfır ve OIDC arasındaki farklar nelerdir? Üç: RBAC ile ABAC'ı ne zaman tercih edersiniz? "
  "Dört: bir bayi personeli işten ayrıldığında hangi süreç çalışmalıdır? Beş: SoD kuralı nedir? Finansman şirketinde üç örnek verin. "
  "Altı: yetki matrisi hazırlarken hangi paydaşlarla çalışırsınız?")
m("Cevap ipuçları", ["Kimlik doğrulama · yetkilendirme", "SAML SSO · OAuth yetki · OIDC kimlik", "RBAC kaba · ABAC ince", "Leaver: hesap süre içinde kapanır", "Giren ≠ onaylayan · iş birimi, güvenlik"],
  "İpuçları, bölümün içeriğinden. Bir: kimlik doğrulama, bayi temsilcisinin şifre ve OTP ile girmesi; yetkilendirme, yalnız kendi bayisinin başvurularını görmesi. "
  "İki: SAML kurumsal SSO ve XML; {OAuth} yetki devri; OIDC, {OAuth} üzerine kimlik. Üç: RBAC kaba yetki için, limit, bayi ve saat gibi ince kurallar için ABAC. "
  "Dört: {Leaver}; bayi bildirir, hesap belirlenen süre içinde kapanır, oturumlar sonlanır. "
  "Beş: başvuru giren onaylayamaz; ödeme giren onaylayamaz; yetki talep eden onaylayamaz. "
  "Altı: iş birimi, bilgi güvenliği, IAM ekibi, iç kontrol ve denetim; rolleri ve SoD kurallarını onlarla doğrularsın.")

# ───────────────────────────── Görsel rehber
g("Modern giriş akışı adım adım", "g27.png",
  [([0.0, 0.1, 1.0, 0.3], "1–3 · Giriş yap, code_verifier, /authorize"), ([0.0, 0.33, 1.0, 0.58], "4–6 · Şifre + OTP yalnız kimlik sunucusunda"),
   ([0.0, 0.58, 1.0, 0.72], "7–8 · code + verifier → token"), ([0.0, 0.72, 1.0, 0.92], "9–11 · API: imza, exp, aud, scope"),
   ([0.0, 0.92, 1.0, 1.0], "Çalınan code tek başına işe yaramaz")],
  "Görsel rehber: {OAuth} iki nokta sıfır {Authorization Code} artı PKCE akışı, on bir adım. Şifreyi yalnız kimlik sunucusu görür; API token görür. "
  "Okunuşu: kullanıcı uygulamada giriş yap'a basar, bir. Uygulama rastgele bir gizli değer, yani {code_verifier} üretir ve özetini, yani {code_challenge}'ı hazırlar, iki. "
  "Tarayıcı kimlik sunucusuna yönlendirilir, bölü {authorize}, üç. "
  "Kullanıcı şifresini ve OTP'sini yalnızca kimlik sunucusunun ekranına girer, dört ve beş; uygulama şifreyi hiç görmez. "
  "Sunucu tek kullanımlık bir kod ile geri yönlendirir, altı. Uygulama bu kodu gizli değerle birlikte token'a çevirir, yedi ve sekiz; "
  "{access} ve {ID token}. Sonra API'yi token ile çağırır, {GET} bölü {applications}, {Bearer}; dokuz. "
  "API token'ın imzasını, süresini yani {exp}'i, hedefini yani {aud}'u ve yetki kapsamını yani {scope}'u doğruladıktan sonra veri döner; on ve on bir. "
  "Alttaki not: yedinci adımda sunucu {code_verifier}'ın özetinin {code_challenge}'a eşit olduğunu kontrol eder; çalınan kod tek başına işe yaramaz.",
  bolum="IAM · Görsel rehber")
m("Bu diyagramdan gereksinimler", ["Token ömrü (ör. access 15 dk, refresh 8 saat)", "MFA hangi işlemlerde zorunlu?",
                                   "Oturum zaman aşımı · çıkışta tüm token'ların iptali", "API hangi scope ile hangi işlemi yapabilir?"],
  "İş analistinin bu diyagramdan yazacağı gereksinimler: token ömrü, örneğin {access token} on beş dakika, {refresh token} sekiz saat; "
  "MFA hangi işlemlerde zorunlu; oturum zaman aşımı; çıkışta tüm token'ların iptali; ve API'nin hangi {scope} ile hangi işlemi yapabileceği.")
g("Kimlik yaşam döngüsü ve rol modeli", "g28.png",
  [([0.0, 0.1, 1.0, 0.43], "JML: Joiner → Mover → Leaver"), ([0.0, 0.45, 1.0, 0.9], "Kullanıcı → Rol → Yetki"),
   ([0.72, 0.5, 1.0, 0.72], "SoD: oluşturan onaylayamaz")],
  "İkinci çizim: JML yaşam döngüsü ve RBAC modeli, SoD örneği. Kimlik yaşam döngüsü rolleri verir; roller yetkileri taşır. "
  "Üst satır bir kimliğin yaşam döngüsü; tetikleyiciler İK sisteminden gelir. {Joiner}, işe giriş: tetik İK işe giriş kaydı, varsayılan roller otomatik atanır. "
  "{Mover}, değişiklik: tetik pozisyon değişikliği; yeni rol ver, eskiyi geri al. {Leaver}, ayrılış: tetik işten çıkış kaydı; tüm erişim kapatılır. "
  "Kesikli ok erişim gözden geçirme: yönetici yetkileri düzenli aralıkla onaylar ya da kaldırır. "
  "Alt satır erişimin nasıl verildiğini gösterir: kişiye doğrudan yetki verilmez, role atanır; rol yetkileri taşır. "
  "Mehmet, bayi on yedi, bayi satış rolüyle başvuru oluşturabilir, onaylayamaz. Ayşe, tahsis, tahsis uzmanı rolüyle krediyi yetki limitine göre onaylar. "
  "Operasyon rolü kullandırım yapar. "
  "Sağdaki kırmızı köşeli çizgi aynı kişide birleşmemesi gereken iki yetkiyi işaretler: başvuruyu oluşturan kişi aynı krediyi onaylayamaz. "
  "Bir kullanıcıya her iki rol de atanmak istenirse sistem engellemeli ya da istisna onayı istemelidir.")
t("Menü rehberi (1/2): Entra ID ve Keycloak", ["Yapmak istediğin", "Entra ID", "Keycloak"],
  [["Kullanıcı", "Users → New user", "Users → Add user"], ["Rol atamak", "Groups → Members", "Role mapping"],
   ["Uygulama (OIDC)", "App registrations", "Clients → OpenID Connect"], ["SAML SSO", "Single sign-on → SAML", "Client type: SAML"]],
  "Menü rehberi: yaygın IAM araçlarında nerede ne yapılır; {Microsoft Entra ID}, adresi entra nokta microsoft nokta com, ve açık kaynak {Keycloak}. "
  "Kullanıcı oluşturmak: {Entra}'da {Identity}, {Users}, {All users}, {New user}; {Keycloak}'ta {Realm} seç, {Users}, {Add user}. "
  "Grup ya da rol atamak: {Entra}'da {Identity}, {Groups}, grup, {Members}; uygulama rolleri için {Enterprise applications}, uygulama, {Users and groups}. "
  "{Keycloak}'ta {Realm roles}, {Create role}; sonra {Users}, kullanıcı, {Role mapping}, {Assign role}. "
  "Uygulama kaydı, yani OIDC istemcisi: {Entra}'da {Identity}, {Applications}, {App registrations}, {New registration}, {Redirect URI}; "
  "{Keycloak}'ta {Clients}, {Create client}, {Client type}: {OpenID Connect}, {Valid redirect URIs}. "
  "SAML ile SSO: {Entra}'da {Enterprise applications}, uygulama, {Single sign-on}, SAML; {Keycloak}'ta {Create client}, {Client type}: SAML.")
t("Menü rehberi (2/2)", ["Yapmak istediğin", "Entra ID", "Keycloak"],
  [["MFA, koşullu erişim", "Conditional Access", "Configure OTP"], ["Erişim gözden geçirme", "Access reviews", "IGA aracı"],
   ["Giriş kayıtları", "Sign-in / Audit logs", "User / Admin events"], ["Token içeriği", "—", "Client scopes → Evaluate"]],
  "MFA ve koşullu erişim: {Entra}'da {Protection}, {Conditional Access}, {New policy}; kullanıcılar, uygulamalar, koşullar ve {Grant}: {Require MFA}. "
  "{Keycloak}'ta {Authentication}, {Flows} ya da {Required actions}, {Configure OTP}. "
  "Erişim gözden geçirme: {Entra}'da {Identity Governance}, {Access reviews}, {New access review}; {Keycloak}'ta yerleşik yok, bir IGA aracıyla yapılır. "
  "Giriş kayıtları: {Entra}'da {Monitoring}, {Sign-in logs} ya da {Audit logs}; {Keycloak}'ta {Events}, {User events} ya da {Admin events}. "
  "Token içeriğini incelemek: {Keycloak}'ta {Clients}, istemci, {Client scopes}, {Evaluate}, {Generated access token}. "
  "Not: menü adları sürüme göre değişebilir. İş analisti genellikle bu ekranları kullanmaz; ama hangi ayarın nerede olduğunu bilmek, "
  "IAM ekibiyle aynı dili konuşmayı sağlar.")

# ───────────────────────────── Laboratuvar
m("Laboratuvar (~60 dk): 1–5", ["1. Rol envanteri (8 rol)", "2. Fonksiyon envanteri", "3. Excel matrisi", "4. SoD tablosu (≥ 4)", "5. JML senaryoları"],
  "Laboratuvar: yetki matrisi, SoD analizi ve token okuma; yaklaşık altmış dakika. "
  "Bir, rol envanteri: bayi satış, bayi yönetici, tahsis uzmanı, tahsis yöneticisi, operasyon, çağrı merkezi, ürün yönetimi ve denetçi. "
  "İki, fonksiyon envanteri: başvuru oluştur, görüntüle, limitlere göre onayla, kullandır, faiz parametresi değiştir, müşteri verisini dışa aktar, kullanıcı yetkisi ver. "
  "Üç, matris: Excel'de satırlar fonksiyon, sütunlar rol. Hücrelere tik, tik kendi bayisi, tik maskeli ya da tire; bölümdeki yetki matrisi örneğinden başla. "
  "Dört, SoD tablosu: fonksiyon A, fonksiyon B, risk ve kontrol, önleyici ya da tespit edici. En az dört çatışma yaz: başvuru gir ve onayla; "
  "parametre değiştir ve onayla; yetki talep et ve onayla; ödeme gir ve ödeme onayla. "
  "Beş, JML senaryoları: bir tahsis uzmanı operasyon birimine geçiyor; hangi roller eklenir, hangileri alınır, ne kadar sürede? "
  "Bir bayi personeli ayrılıyor; bayi bunu nasıl bildirir, hesabı kim kapatır?", bolum="IAM · Laboratuvar")
m("Laboratuvar: 6–9", ["6. OIDC keşif belgesi", "7. JWT çözücüde test token'ı", "8. Postman → OAuth 2.0 alanları", "9. BA çıktısı: 1 sayfa IAM"],
  "Altı, OIDC keşif belgesini oku: tarayıcıda herkese açık bir kimlik sağlayıcının bölü {well-known} bölü {openid-configuration} adresini aç; "
  "örneğin accounts nokta google nokta com'unki. {authorization_endpoint}, {token_endpoint}, {scopes_supported} ve {code_challenge_methods_supported} alanlarını bul "
  "ve diyagramdaki adımlarla eşleştir. "
  "Yedi, JWT okumak: test ortamından alınmış bir token'ı, asla üretim token'ını değil, bir JWT çözücüde aç. Üç parçayı ayırt et; "
  "{iss}, {aud}, {exp}, {scope}, {roles} değerlerini oku. {exp} değerini tarihe çevir ve token ömrünü hesapla. "
  "Sekiz, {Postman} ile {OAuth}: bir isteğin {Authorization} sekmesi, {Type}: {OAuth} iki nokta sıfır, {Configure New Token} bölümündeki alanlar: "
  "{Grant type}, yani {Authorization Code with PKCE}; {Auth URL}; {Access Token URL}; {Client ID}; {Scope}. Bu alanların diyagramdaki hangi adıma karşılık geldiğini yaz. "
  "Dokuz, iş analisti çıktısı: bayi portalı için bir sayfalık IAM gereksinimi; kimlik doğrulama ve MFA kuralları, oturum süresi, rol listesi, SoD kuralları, "
  "JML süreleri, erişim gözden geçirme sıklığı ve log gereksinimleri.")

# ───────────────────────────── Uygulama paketi
t("Otel benzetmesi: AuthN mi, AuthZ mi?", ["Otelde", "IAM'de", "Firma'da"],
  [["Resepsiyon kayıt eder", "AuthN: sen kimsin?", "Parola + SMS kodu"], ["412 numaralı oda kartı", "AuthZ: ne yapabilirsin?", "Yalnız kendi bayisi"],
   ["Kart çıkışta biter", "Token ömrü (exp)", "Dakikalarda geçersiz"], ["Kayıp kart iptal", "Token iptali", "Leaver: hesap kapanır"]],
  "IAM uygulama paketi. Otel benzetmesi: kimlik doğrulama mı, yetkilendirme mi? "
  "Otelde resepsiyon kimliğine bakıp seni kayıt eder; IAM'de bu kimlik doğrulama: sen kimsin? Firma'da bayi temsilcisi kullanıcı adı, parola ve SMS koduyla portala girer. "
  "Otel sana yalnızca dört yüz on iki numaralı odayı ve spor salonunu açan bir kart verir; bu yetkilendirme: neyi yapabilirsin? "
  "Firma'da temsilci yalnızca kendi bayisinin başvurularını görür ve başvuru oluşturabilir; onaylayamaz. "
  "Kartın süresi çıkış günü biter; bu token ömrü, yani {exp}. Firma'da erişim token'ı dakikalar içinde geçersizleşir. "
  "Kartı kaybedersen resepsiyon iptal eder; bu oturum ve token iptali. Firma'da işten ayrılan temsilcinin hesabı kapatılır; JML'de {Leaver}.",
  bolum="IAM · Uygulama paketi")
dikkat("401 ve 403 tek cümlede", "401: \"Seni tanımadım\" (kimlik doğrulama başarısız) · 403: \"Seni tanıdım ama bu işe yetkin yok\"",
       "Bunu tek cümlede hatırla: dört yüz bir seni tanımadım demektir, yani kimlik doğrulama başarısız. "
       "Dört yüz üç ise seni tanıdım ama bu işe yetkin yok demektir.", tip="bilgi")
m("Ön kanal ve arka kanal", ["Ön kanal (front channel): tarayıcı üzerinden yönlendirmeler; geçmiş, eklenti, adres çubuğu görebilir",
                             "Burada yalnız kısa ömürlü, tek kullanımlık code taşınır",
                             "Arka kanal (back channel): sunucu ↔ kimlik sağlayıcı, doğrudan ve şifreli; token burada alınır",
                             "Kural: token ve gizli bilgi arka kanaldan · diyagramda okları işaretle"],
  "Ön kanal ve arka kanal. Ön kanal, yani {front channel}: bilgi kullanıcının tarayıcısı üzerinden yönlendirmelerle taşınır. "
  "Tarayıcı geçmişi, eklentiler ve adres çubuğu bu bilgiyi görebilir; burada yalnızca kısa ömürlü, tek kullanımlık {code} taşınır. "
  "Arka kanal, yani {back channel}: uygulama sunucusu ile kimlik sağlayıcı arasında doğrudan, şifreli bağlantı; token burada alınır. "
  "Kural: token ve gizli bilgiler arka kanaldan gider. PKCE diyagramında tarayıcıdan geçen her oku ön kanal, sunucudan sunucuya giden her oku arka kanal olarak işaretle.")
t("Hangi OAuth akışı, ne zaman?", ["Akış", "Ne zaman", "Firma örneği"],
  [["Auth Code + PKCE", "Kullanıcı adına", "Bayi portalı · önerilen"], ["Client Credentials", "Servis kendi adına", "Karar motoru → KKB · önerilen"],
   ["Implicit", "Token adres çubuğunda", "Önerilmez (RFC 9700)"], ["Resource Owner Password", "Parolayı uygulama alır", "Önerilmez"]],
  "Hangi {OAuth} akışı, ne zaman? {Authorization Code} artı PKCE: bir kullanıcı adına işlem yapılıyorsa; bayi portalı ve mobil uygulama; önerilen. "
  "{Client Credentials}: kullanıcı yok, bir servis kendi adına başka servisi çağırıyorsa; karar motorunun KKB entegrasyon servisini çağırması; önerilen. "
  "{Implicit}: eskiden tarayıcı uygulamaları için kullanılırdı; token adres çubuğunda döner. Önerilmez; {OAuth} güvenlik en iyi uygulamaları, RFC dokuz bin yedi yüz. "
  "{Resource Owner Password}: uygulama kullanıcının parolasını doğrudan alır. Önerilmez; MFA'yı ve federasyonu bozar.")
m("İzin, rol, ayrıcalık, scope", ["İzin (permission): tek işlem hakkı → \"başvuruyu onayla\"", "Rol: izin kümesi → Kredi Analisti = görüntüle + onayla + reddet",
                                  "Ayrıcalık (privilege): çoğu yerde izinle eş; yönetici izinleri = \"ayrıcalıklı erişim\"",
                                  "Scope: uygulamanın kullanıcı adına istediği sınır → basvuru:read basvuru:create; rol fazlasına izin verse de token aşamaz"],
  "İzin, ayrıcalık ve {scope} farkı. İzin, yani {permission}, tek bir işlem hakkıdır: başvuruyu onayla. "
  "Rol bir izin kümesidir: kredi analisti rolü eşittir görüntüle artı onayla artı reddet. "
  "Ayrıcalık, yani {privilege}, çoğu kaynakta izinle eş anlamlı kullanılır; yönetici düzeyi izinler için ayrıcalıklı erişim denir. "
  "{Scope} ise bir uygulamanın kullanıcı adına istediği izin sınırıdır: bayi portalı token'ı {basvuru:read} ve {basvuru:create} {scope}'unu taşır; "
  "kullanıcının rolü daha fazlasına izin verse bile token bu sınırın dışına çıkamaz.")
t("Yetkilendirme modelleri: aynı soruya üç cevap", ["Model", "Karar neye bakar", "Ne zaman yetmez"],
  [["RBAC", "Rol: KREDI_ANALISTI onaylar", "Rol şişmesi"], ["ABAC", "bayi_id eşitse görür", "Test, denetim zor"],
   ["ReBAC", "Bölge müdürü kendi bölgesi", "Eski ilişki verisi"]],
  "Yetkilendirme modelleri: aynı soruya üç cevap. RBAC kararı kullanıcının rolüne bakarak verir: KREDI_ANALISTI rolü başvuru onaylayabilir. "
  "Ne zaman yetmez? Rol sayısı her bayi ve her limit için patlar; rol şişmesi. "
  "ABAC kullanıcı, kaynak ve ortam özelliklerine bakar: kullanıcının {bayi_id} değeri başvurunun {bayi_id} değerine eşitse görüntüleyebilir. "
  "Ne zaman yetmez? Kuralları test etmek ve denetlemek zorlaşır. "
  "ReBAC varlıklar arası ilişkilere bakar: bölge müdürü, yönettiği bölgedeki bayilerin başvurularını görür. Ne zaman yetmez? İlişki verisi güncel tutulmazsa yanlış erişim verir. "
  "Ve Firma gibi kurumlarda RBAC temel alınır; bayi ve tutar sınırı gibi ince kurallar ABAC ile eklenir.")

# ───────────────────────────── JWT alıştırması
m("JWT okuma alıştırması", ["Eğitim için üretilmiş token; gerçek sisteme ait değil", "Token → jwt.io sayfasına yapıştır",
                            "Gerçek üretim token'ını asla çevrimiçi çözücüye yapıştırma", "İmza \"invalid\" görünebilir: anahtarı bilmiyorsun"],
  "JWT okuma alıştırması. Belgedeki token eğitim için üretildi; gerçek bir sisteme ait değil. jwt nokta io sayfasına yapıştır. "
  "Gerçek bir üretim token'ını asla çevrimiçi bir çözücüye yapıştırma; token geçerliliği süresince başkasının eline geçebilir. "
  "jwt nokta io üzerinde imza doğrulaması {invalid} görünebilir; bu normaldir, çünkü imza anahtarını bilmiyorsun. "
  "Bir API token'ı kabul etmeden önce imzayı kimlik sağlayıcının anahtarıyla doğrular.", bolum="IAM · JWT alıştırması")
t("Beklenen çözüm (payload)", ["Claim", "Değer"],
  [["iss · sub", "https://sso.ornek-firma.test · bayi-kullanici-42"], ["aud", "basvuru-api"],
   ["iat · exp", "1795165200 (20 Kasım 2026 12:00) · 1795166100 (12:15)"], ["scope", "basvuru:read basvuru:create"],
   ["bayi_id · roles", "B2 · [\"BAYI_TEMSILCISI\"]"]],
  "Beklenen çözüm, yani {payload}: {iss}, https sso nokta ornek firma nokta test. {sub}, bayi kullanıcı kırk iki. {aud}, başvuru api. "
  "{iat}, 1795165200; yani yirmi Kasım iki bin yirmi altı, saat on iki sıfır sıfır, Türkiye saati. {exp}, 1795166100; aynı gün on iki on beş. "
  "Token on beş dakika geçerli. {scope}: {basvuru:read} ve {basvuru:create}. {bayi_id}: B2. {roles}: BAYI_TEMSILCISI.")
m("Sorular", ["1. Saat 12:20'de basvuru-api'ye istek?", "2. 12:05'te POST /basvurular/{id}/onay?",
              "3. 12:05'te B1 bayisinin başvurusu istenirse?", "4. 12:05'te token karar-api'ye gönderilirse?"],
  "Dört soru; çözümleri videonun sonunda. Bir: bu token'la saat on iki yirmide başvuru api'ye istek gelirse sonuç ne olur? "
  "İki: saat on iki sıfır beşte aynı token'la {POST} bölü başvurular bölü id bölü onay çağrılırsa? "
  "Üç: saat on iki sıfır beşte bu token'la B1 bayisinin bir başvurusu istenirse hangi kural devreye girmeli? "
  "Dört: saat on iki sıfır beşte aynı token karar api adlı başka bir servise gönderilirse?")
m("Bağımsız görev: erken kapama ve rehin kaldırma", ["Kural: rehin son taksitle ya da erken kapamada ~1 saatte kaldırılır",
                                                     "Roller: Müşteri Hizmetleri, Tahsilat, Rehin Operasyonu, Operasyon Yöneticisi, Denetçi",
                                                     "İşlemler: tutar hesapla, ödeme kaydet, talimat oluştur, talimatı onayla, geçmişi görüntüle",
                                                     "1. Rol × işlem matrisi (E / boş) · 2. ≥ 2 SoD kuralı · 3. Bir ABAC kuralı"],
  "Bağımsız görev: erken kapama ve rehin kaldırma yetki matrisi. Firma kuralı: rehin son taksitle ya da erken kapamada yaklaşık bir saat içinde kaldırılır. "
  "Roller: müşteri hizmetleri, tahsilat, rehin operasyonu, operasyon yöneticisi ve denetçi. "
  "İşlemler: erken kapama tutarını hesapla, ödemeyi kaydet, rehin kaldırma talimatı oluştur, talimatı onayla ve işlem geçmişini görüntüle. "
  "Bir: rol çarpı işlem matrisi çiz; her hücreye E, yani evet, ya da boş yaz. İki: en az iki görev ayrılığı kuralı yaz ve matriste bu kuralları ihlal eden bir rol olmadığını kontrol et. "
  "Üç: bir ABAC kuralı ekle. Doğru yaptığını nasıl anlarsın? Ödemeyi kaydeden kişi aynı işlemde rehni tek başına kaldıramıyor; denetçi hiçbir şeyi değiştiremiyor.")

# ───────────────────────────── Sorun giderme, bilgi kontrolü
t("Sorun giderme (BA gözüyle) 1/2", ["Belirti", "Olası neden", "Ne sorarsın / yazarsın"],
  [["Giriş var ama ekran 403", "Rol yok ya da scope eksik", "Grup, token roles / scope nedir?"],
   ["15 dakikada bir atılıyor", "Erişim token'ı doluyor, yenileme yok", "Refresh token ve oturum süresi gereksinimi"],
   ["Ayrılan bayi temsilcisi giriş yapıyor", "Leaver bayi sistemine bağlı değil", "\"İlişik kesilince hesap X saatte kapanmalı\"; X güvenlikle"]],
  "Sorun giderme, iş analisti gözüyle. Kullanıcı giriş yapıyor ama ekran dört yüz üç veriyorsa: rol atanmamış ya da token'daki {scope} eksik. "
  "Sor: kullanıcının grubu ve token'daki {roles} ve {scope} değerleri nedir? "
  "Çalışan girişte on beş dakikada bir atılıyorsa: erişim token'ının süresi doluyor ve yenileme yapılmıyor. {Refresh token} ve oturum süresi gereksinimini netleştir. "
  "İşten ayrılan bayi temsilcisi hâlâ giriş yapabiliyorsa: {Leaver} adımı bayi sistemiyle bağlı değil. "
  "Gereksinim: bayi ilişiği kesildiğinde hesap X saat içinde kapatılmalıdır; X'i bilgi güvenliğiyle belirle.", bolum="IAM · Sorun giderme ve bilgi kontrolü")
t("Sorun giderme (BA gözüyle) 2/2", ["Belirti", "Olası neden", "Ne sorarsın / yazarsın"],
  [["Aynı kişi tahsilatı kaydedip rehni kaldırıyor", "SoD kuralı yok", "SoD kuralını yaz, gözden geçirmede raporlat"],
   ["Gece 03:00 farklı ülkeden bayi girişi", "Hesap ele geçirilmiş olabilir", "Olağandışı giriş için tespit + ek doğrulama (koşullu erişim)"]],
  "Aynı kişi hem tahsilatı kaydedip hem rehni kaldırabiliyorsa: SoD kuralı tanımlanmamış. SoD kuralını yaz ve erişim gözden geçirmede raporlat. "
  "Gece saat üçte farklı bir ülkeden bayi hesabıyla giriş varsa: hesap ele geçirilmiş olabilir. "
  "Olağandışı giriş için tespit ve ek doğrulama gereksinimi yaz; yani koşullu erişim.")
soru("Bilgi kontrolü 1/5", "Doğru parola girildi ama \"başvuruyu onayla\" 403 döndü. Sorun nerede?",
     ["Ağ", "Veritabanı", "Kimlik doğrulama", "Yetkilendirme"], 3,
     "Beş soruluk bilgi kontrolü. Birinci soru: kullanıcı doğru parolayı girdi ama başvuruyu onayla düğmesi dört yüz üç döndü. Sorun nerede? "
     "A, ağ. B, veritabanı. C, kimlik doğrulama. D, yetkilendirme.",
     "Doğru cevap D: yetkilendirme.")
soru("Bilgi kontrolü 2/5", "Karar motoru kullanıcı olmadan KKB entegrasyon servisini çağırıyor. Hangi akış?",
     ["Client Credentials", "Authorization Code + PKCE", "Implicit", "Resource Owner Password"], 0,
     "İkinci soru: karar motoru, kullanıcı olmadan KKB entegrasyon servisini çağırıyor. Hangi akış? "
     "A, {Client Credentials}. B, {Authorization Code} artı PKCE. C, {Implicit}. D, {Resource Owner Password}.",
     "Doğru cevap A: {Client Credentials}.")
soru("Bilgi kontrolü 3/5", "\"Temsilci yalnız kendi bayi_id'sine ait başvuruları görür\" en doğal hangi modelle?",
     ["RBAC", "ACL", "MAC", "ABAC"], 3,
     "Üçüncü soru: temsilci yalnızca kendi {bayi_id}'sine ait başvuruları görür kuralı hangi modelle en doğal ifade edilir? A, RBAC. B, ACL. C, MAC. D, ABAC.",
     "Doğru cevap D: ABAC.")
soru("Bilgi kontrolü 4/5", "Token'daki aud alanı neyi söyler?",
     ["Token'ı kimin ürettiğini", "Kullanıcının rolünü", "Token'ın hangi servis için üretildiğini", "Bitiş zamanını"], 2,
     "Dördüncü soru: token'daki {aud} alanı neyi söyler? A, token'ı kimin ürettiğini. B, kullanıcının rolünü. C, token'ın hangi servis için üretildiğini. D, token'ın bitiş zamanını.",
     "Doğru cevap C.")
soru("Bilgi kontrolü 5/5", "Token neden tarayıcı adres çubuğunda taşınmamalı?",
     ["URL uzunluğu sınırı", "Ön kanaldaki bilgi geçmiş ve eklentilerle sızabilir", "Tarayıcı JSON okuyamaz", "HTTPS adres çubuğunu şifrelemez"], 1,
     "Beşinci soru: token neden tarayıcı adres çubuğunda taşınmamalı? A, URL uzunluğu sınırı. B, ön kanaldaki bilgi geçmiş ve eklentilerle sızabilir. "
     "C, tarayıcı JSON okuyamaz. D, HTTPS adres çubuğunu şifrelemez.",
     "Doğru cevap B.")
m("Hızlı başvuru: token kontrol sırası", ["1. İmza geçerli mi? değilse 401 · 2. iss beklenen mi? değilse 401",
                                          "3. exp geçmişte mi? öyleyse 401 · 4. aud bu servis mi? değilse 401",
                                          "5. scope / roles yeterli mi? değilse 403", "6. Kaynak kuralı (bayi_id) → 403 ya da varlığı gizlemek için 404"],
  "Hızlı başvuru: bir token'ı kontrol sırası. Bir: imza, kimlik sağlayıcının anahtarıyla geçerli mi? Değilse dört yüz bir. "
  "İki: {iss} beklenen kimlik sağlayıcı mı? Değilse dört yüz bir. Üç: {exp} geçmişte mi? Öyleyse dört yüz bir. Dört: {aud} bu servis mi? Değilse dört yüz bir. "
  "Beş: {scope} ya da {roles} bu işlem için yeterli mi? Değilse dört yüz üç. "
  "Altı: kaynak düzeyi kural, örneğin {bayi_id} eşleşmesi, sağlanıyor mu? Değilse dört yüz üç; ya da kaydın varlığını gizlemek için dört yüz dört.",
  bolum="IAM · Çözümler")
m("Çözümler: JWT soruları", ["1. 12:20 > exp (12:15) → 401; refresh token ile yeni token", "2. scope'ta onay yok, rol BAYI_TEMSILCISI → 403",
                             "3. bayi_id B2 ≠ B1 → ABAC reddeder: 403 ya da 404 (gereksinim kararı, yazılı olmalı)",
                             "4. aud = basvuru-api; karar-api için değil → 401"],
  "JWT sorularının çözümü. Bir: on iki yirmi, {exp} değerinden, yani on iki on beşten sonra; token süresi dolmuş, dört yüz bir. "
  "Uygulama {refresh token} ile yeni erişim token'ı almalı. "
  "İki: token geçerli ama {scope}'ta onay izni yok, yalnız {basvuru:read} ve {basvuru:create}; rol de BAYI_TEMSILCISI; dört yüz üç. "
  "Üç: token'daki {bayi_id} B2, başvurunun bayisi B1; ABAC kuralı reddeder: dört yüz üç, ya da kaydın varlığını belli etmemek için dört yüz dört. "
  "Hangisinin döneceği bir gereksinim kararıdır; yazılı olmalı. "
  "Dört: {aud} eşittir başvuru api; karar api bu token'ı kendisi için üretilmediği için reddetmeli; dört yüz bir.")
t("Çözüm: rol × işlem matrisi", ["İşlem", "MH", "Tahsilat", "Rehin Op.", "Op. Yön.", "Denetçi"],
  [["Tutar hesapla", "E", "E", "", "", ""], ["Ödeme kaydet", "", "E", "", "", ""], ["Talimat oluştur", "", "", "E", "", ""],
   ["Talimat onayla", "", "", "", "E", ""], ["Geçmiş", "E", "E", "E", "E", "E"]],
  "Bağımsız görevin örnek çözümü. Erken kapama tutarını hesapla: müşteri hizmetleri ve tahsilat. Ödemeyi kaydet: yalnız tahsilat. "
  "Rehin kaldırma talimatı oluştur: yalnız rehin operasyonu. Talimatı onayla: yalnız operasyon yöneticisi. "
  "İşlem geçmişini görüntüle: beş rolün hepsi, denetçi dahil.")
m("Çözüm: SoD, ABAC ve açık soru", ["SoD 1: ödeme kaydeden talimat oluşturamaz", "SoD 2: oluşturan onaylayamaz (4 göz)", "ABAC: kalan borç 0 ise talimat", "Açık soru: onay adımı ~1 saat hedefi"],
  "SoD bir: ödemeyi kaydeden kullanıcı aynı sözleşme için rehin kaldırma talimatı oluşturamaz. "
  "SoD iki: talimatı oluşturan kullanıcı aynı talimatı onaylayamaz; dört göz ilkesi. "
  "ABAC: rehin kaldırma talimatı yalnızca sözleşmenin kalan borcu sıfır olduğunda oluşturulabilir. "
  "Not: talimatın onayı için ayrı bir adım, yaklaşık bir saat hedefini zorlayabilir. Bu çatışmayı açık soru olarak not et; gerçek projede iş birimine sorulur. "
  "Örneğin sistem kalan borcu otomatik doğruluyorsa onay adımı kaldırılabilir mi?")
m("Bu videoda neler gördük?", ["Temel kavramlar, faktörler, MFA, JML", "RBAC, ABAC, ReBAC, yetki matrisi, SoD", "SAML, OAuth, OIDC, PKCE, JWT",
                               "IGA, PAM, CIAM, Zero Trust, güvence seviyeleri, metrikler", "Otel benzetmesi, kanallar, akış seçimi, JWT alıştırması, yetki matrisi görevi"],
  "Toparlayalım. Temel kavramları, kimlik doğrulama faktörlerini, MFA'yı ve JML'i gördük. RBAC, ABAC, ReBAC, yetki matrisi ve SoD'yi öğrendik. "
  "SAML, {OAuth}, OIDC, PKCE ve JWT yapısını çalıştık. IGA, PAM, CIAM, {Zero Trust}, güvence seviyeleri ve metriklere baktık. "
  "Otel benzetmesi, ön ve arka kanal, akış seçimi, JWT alıştırması ve yetki matrisi göreviyle uyguladık. "
  "Bir sonraki videoda Jira ile backlog ve teslimat yönetimine geçiyoruz.", ton="sakin")

kaydet(__file__, {
    "baslik": "Business Analyst Teknik Rehberi · 9: IAM",
    "alt_baslik": "Kimlik doğrulama · yetkilendirme · OAuth / OIDC · JWT · RBAC / ABAC · SoD",
    "kapanis": "Sıradaki video: Jira",
    "tema": 9,
    "youtube_baslik": "Business Analyst Teknik Rehberi 9/14: IAM (OAuth, JWT, RBAC/ABAC, SoD, JML)",
    "etiketler": ["business analyst", "IAM", "OAuth 2.0", "JWT", "RBAC", "SoD", "iş analisti"],
}, {"IAM": "ay ey em", "MFA": "em ef ey", "PIN": "pin", "SIM": "sim", "JML": "cey em el", "RBAC": "ar bi ey si", "ABAC": "ey bi ey si",
    "ReBAC": "ri bi ey si", "PBAC": "pi bi ey si", "OPA": "o pi ey", "SAML": "semıl", "OIDC": "o ay di si", "LDAP": "el dap", "SCIM": "skim",
    "SaaS": "sas", "IdP": "ay di pi", "PKCE": "pi key si i", "JWT": "cey dabılyu ti", "IGA": "ay ci ey", "PAM": "pem", "CIAM": "si ay em",
    "NIST": "nist", "SP": "es pi", "IAL": "ay ey el", "AAL": "ey ey el", "FAL": "ef ey el", "NFC": "en ef si", "IBAN": "iban", "RFC": "ar ef si",
    "ACL": "ey si el", "MAC": "mek", "TCKN": "te ce ka en", "SMS": "es em es", "OTP": "o ti pi", "TL": "te le", "1M": "bir milyon",
    "BSV-1001": "be se ve bin bir", "BSV-1001'i": "be se ve bin biri", "tahsis_04": "tahsis sıfır dört", "KREDI_ANALISTI": "kredi analisti",
    "BAYI_TEMSILCISI": "bayi temsilcisi", "jwt.io": "cey dabılyu ti nokta io", "B1": "be bir", "B2": "be iki"})
