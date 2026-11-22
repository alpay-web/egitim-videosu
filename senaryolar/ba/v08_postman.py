#!/usr/bin/env python3
"""BA Teknik Rehberi · Video 8: Postman. Belge satır 2169–2540."""
from ortak import m, t, dikkat, g, soru, kaydet

# ───────────────────────────── Giriş
m("Postman nedir, BA için ne demek?", ["API tasarla, çağır, test et, belgele, otomatikleştir",
                                       "Entegrasyon gereksinimi gerçekten çalışıyor mu?", "Servis sözleşmesi (request/response) doğrulama",
                                       "Hata senaryoları · UAT test verisi", "Kabul kriteri → çalıştırılabilir test"],
  "{Postman}, API'leri tasarlamak, çağırmak, test etmek, belgelemek ve otomatikleştirmek için kullanılan bir platformdur. "
  "İş analisti için {Postman} şu demek: entegrasyon gereksiniminin gerçekten çalışıp çalışmadığını görmek; servis sözleşmesini, yani {request} ve {response}'u doğrulamak; "
  "hata senaryolarını denemek; UAT'de test verisi hazırlamak; ve kabul kriterlerini çalıştırılabilir testlere çevirmek.",
  bolum="Postman: giriş ve hedefler", kanca="Kabul kriterini kâğıtta bırakma; çalıştır.", ton="merakli")
m("Bu bölümün hedefleri", ["Bir API isteğini (metot, URL, header, body) okuyup Postman'de kurmak",
                           "Firma kurallarından sınır değer setleri: vade 5 / 6 / 60 / 61 ay, kurumsal %90",
                           "Aynı isteği CSV'nin her satırıyla çalıştırıp sonuç okumak", "Collection'ı Newman ile komut satırından çalıştırıp rapor almak"],
  "Bu bölümü bitirdiğinde şunları yapabileceksin. Bir: bir API isteğini, yani metot, URL, {header} ve {body}'yi okuyup {Postman}'de yeniden oluşturmak. "
  "İki: Firma kurallarından sınır değer test setleri türetmek; vade beş, altı, altmış ve altmış bir ay; kurumsal yüzde doksan oranı. "
  "Üç: aynı isteği bir CSV dosyasının her satırıyla çalıştırıp sonuçları okumak. "
  "Dört: {collection}'ı {Newman} ile komut satırından çalıştırıp rapor almak.")
t("Başlamadan önce gerekenler", ["Gereken", "Nereden", "Hazır mısın?"],
  [["HTTP ve JSON temeli", "Temel seviye", "200, 400, 401, 404, 500"], ["Postman masaüstü", "postman.com/downloads", "Sol üstte workspace adı"],
   ["Node.js · Newman", "nodejs.org · npm install -g newman", "node -v · newman -v"], ["Firma kuralları", "Çalışma Seti §1.3", "Vade ve %90 kuralı"]],
  "Başlamadan önce gerekenler. HTTP ve JSON temeli: bu bölümün temel seviyesi. İki yüz, dört yüz, dört yüz bir, dört yüz dört ve beş yüz kodlarının anlamını söyleyebiliyorsan hazırsın. "
  "{Postman} masaüstü, ücretsiz plan: postman nokta com bölü downloads. Uygulama açılıyor ve sol üstte {workspace} adı görünüyorsa tamam. "
  "{Newman} için {Node.js}: nodejs nokta org; terminalde {node} tire v bir sürüm numarası yazıyorsa tamam. "
  "{Newman}: terminalde {npm install} tire g {newman}; {newman} tire v bir sürüm yazıyorsa tamam. "
  "Ve Firma kuralları: çalışma setinin bir nokta üç bölümü; vade aralığını ve kurumsal yüzde doksan kuralını biliyorsan başlayabiliriz.")

# ───────────────────────────── Temel
t("HTTP ve REST: metotlar", ["Metot", "Amaç", "Örnek"],
  [["GET", "Kaynağı okuma", "GET /api/v1/applications/BSV-1001"], ["POST", "Yeni kaynak / işlem tetikleme", "POST /api/v1/applications"],
   ["PUT", "Tamamen güncelleme", "PUT /api/v1/customers/123"], ["PATCH", "Kısmi güncelleme", "PATCH …/BSV-1001 { \"durum\": \"IPTAL\" }"],
   ["DELETE", "Silme", "DELETE /api/v1/campaigns/KMP26"]],
  "Temel seviye: HTTP ve REST. {GET} kaynağı okur: {GET} bölü api bölü v1 bölü {applications} bölü BSV-1001. "
  "{POST} yeni kaynak oluşturur ya da işlem tetikler: {POST} bölü api bölü v1 bölü {applications}. "
  "{PUT} kaynağı tamamen günceller: {PUT} bölü {customers} bölü yüz yirmi üç. "
  "{PATCH} kısmi günceller: {PATCH} BSV-1001, durum IPTAL. {DELETE} siler: {DELETE} bölü {campaigns} bölü KMP26.", bolum="Postman · Temel seviye")
t("Durum kodları", ["Grup", "Kodlar"],
  [["Başarı", "200 OK · 201 Created · 204 No Content"], ["İstemci (1)", "400 Bad Request (doğrulama) · 401 Unauthorized (kimlik) · 403 Forbidden (yetki)"],
   ["İstemci (2)", "404 Not Found · 409 Conflict (mükerrer) · 422 Unprocessable Entity (iş kuralı) · 429 Too Many Requests"],
   ["Sunucu", "500 Internal Server Error · 502 / 503 / 504 (ağ geçidi, servis, zaman aşımı)"]],
  "Durum kodları. Başarı: iki yüz {OK}, iki yüz bir {Created}, iki yüz dört {No Content}. "
  "İstemci hataları: dört yüz {Bad Request}, doğrulama hatası; dört yüz bir {Unauthorized}, kimlik yok ya da geçersiz; dört yüz üç {Forbidden}, yetki yok. "
  "Dört yüz dört {Not Found}; dört yüz dokuz {Conflict}, mükerrer ya da çakışma; dört yüz yirmi iki {Unprocessable Entity}, iş kuralı ihlali; "
  "dört yüz yirmi dokuz {Too Many Requests}. "
  "Sunucu hataları: beş yüz {Internal Server Error}; beş yüz iki, beş yüz üç ve beş yüz dört; ağ geçidi, servis ve zaman aşımı.")
m("Bir isteğin parçaları ve Postman yapısı", ["Metot · URL (base + path + query param)", "Header: Content-Type: application/json, Authorization: Bearer …, X-Correlation-Id",
                                              "Body: JSON, form-data, raw XML · Auth sekmesi",
                                              "Workspace → Collection → Folder → Request · Environment (DEV, TEST, UAT) · History · Console"],
  "Bir isteğin parçaları: metot; URL, yani {base} artı {path} artı {query param}; {header}'lar, örneğin {Content-Type} {application/json}, "
  "{Authorization} {Bearer} ve {X-Correlation-Id}; {body}, yani JSON, {form-data} ya da {raw} XML; ve {Auth} sekmesi. "
  "{Postman} arayüzündeki yapı: {Workspace}, kişisel ya da ekip; içinde {Collection}, bir API'ye ait istek grubu; içinde {Folder}, senaryo ya da kaynak; içinde {Request}. "
  "{Environment}: DEV, TEST, UAT gibi ortam değişkenleri. {History}. Ve {Console}: ham istek ve yanıtı ve logları gösterir; hata ayıklamada ilk bakılacak yer.")
m("Değişkenler ve kapsamları", ["Dar kapsam geneli ezer: Global → Collection → Environment → Data → Local",
                                "Kullanım: {{baseUrl}}/applications/{{basvuruId}}", "Gizli bilgi: secret tipli değişken ya da vault",
                                "Paylaşılan ortama gerçek değer yazılmaz"],
  "Değişkenler ve kapsamları; dar kapsam geneli ezer. Genişten dara: {Global}, {Collection}, {Environment}, {Data}, yani iterasyon verisi, ve {Local}. "
  "Kullanım: çift süslü parantez içinde {baseUrl}, bölü {applications}, bölü çift süslü parantez içinde {basvuruId}. "
  "Şifre ya da {client secret} gibi gizli bilgiler için {secret} tipli değişken ya da {vault} kullanılır; paylaşılan ortama gerçek değer yazılmaz.")

# ───────────────────────────── Orta
m("Test scriptleri (Post-response)", ["pm.test(\"Durum kodu 201\") → pm.response.to.have.status(201)",
                                      "Yanıt süresi 2 sn altında → responseTime below 2000", "basvuruId formatı → /^BSV-\\d+$/",
                                      "taksitTutari > 0 ve vade within(6, 60)", "pm.collectionVariables.set(\"basvuruId\", …): sonraki isteğe taşı"],
  "Orta seviye: test scriptleri, yani {Post-response} sekmesi ve {pm} API'si. "
  "Birinci test, durum kodu iki yüz bir: {pm.response.to.have.status} iki yüz bir. "
  "İkinci test, yanıt süresi iki saniyenin altında: {responseTime} {below} iki bin. "
  "Üçüncü test, başvuru numarası formatı doğru: {basvuruId}, BSV tire ve rakamlarla eşleşmeli. "
  "Dördüncü test: {pm.expect} {body.odemePlani.taksitTutari} {to.be.above} sıfır; yani ödeme planındaki taksit tutarı sıfırdan büyük ve vade altı ile altmış arasında, yani {within} altı, altmış. "
  "Son satır kimliği sonraki istek için saklar: {pm.collectionVariables.set} {basvuruId}.", bolum="Postman · Orta seviye")
m("Pre-request script ve dinamik değişkenler", ["Dinamik veri, zaman damgası, imza (HMAC), token alma",
                                                "istekId = {{$guid}} → X-Correlation-Id header'ına upsert",
                                                "{{$guid}} · {{$timestamp}} · {{$randomInt}} · {{$randomFirstName}}"],
  "{Pre-request} script: dinamik veri üretimi, zaman damgası, imza, yani HMAC, ya da token alma. "
  "Örnek: {istekId} değişkenine dolar {guid} değeri atanır, sonra bu değer {X-Correlation-Id} {header}'ına {upsert} ile yazılır. "
  "Dinamik değişkenler: dolar {guid}, dolar {timestamp}, dolar {randomInt} ve dolar {randomFirstName}.")
m("JSON Schema ile sözleşme doğrulama", ["type: object · required: basvuruId, durum, vade", "basvuruId: string",
                                         "durum enum: TASLAK, DEGERLENDIRMEDE, MANUEL_INCELEME, ONAYLANDI, REDDEDILDI",
                                         "vade: integer, minimum 6, maximum 60 · pm.test(\"Şema uyumlu\")"],
  "{JSON Schema} ile sözleşme doğrulama. {type} {object}; {required} alanlar {basvuruId}, durum ve vade. "
  "{basvuruId} {string}. Durum bir {enum}: TASLAK, DEGERLENDIRMEDE, MANUEL_INCELEME, ONAYLANDI, REDDEDILDI; yani başvuru yaşam döngüsündeki durumlar. "
  "Vade {integer}, {minimum} altı, {maximum} altmış. Test: şema uyumlu, {jsonSchema} ile.")
m("Yetkilendirme ve SOAP", ["Auth: API Key, Basic, Bearer Token, OAuth 2.0 (Client Credentials, Authorization Code + PKCE), AWS Signature, mTLS",
                            "Collection seviyesinde tanımla, isteklerde \"Inherit auth from parent\"",
                            "SOAP: raw → XML · text/xml + SOAPAction (1.1) ya da application/soap+xml (1.2)",
                            "xml2Json(pm.response.text()) · finans ve sigortada SOAP hâlâ yaygın"],
  "Yetkilendirme, {Auth} sekmesi: {API Key}, {Basic}, {Bearer Token}, {OAuth} iki nokta sıfır, yani {Client Credentials} ya da {Authorization Code} artı PKCE; "
  "{AWS Signature}; ve mTLS için sertifika ayarları, {Settings}, {Certificates}. "
  "{Auth} {collection} seviyesinde tanımlanır, isteklerde {Inherit auth from parent} kullanılır. "
  "SOAP servisleri: {Body}, {raw}, XML. Header {Content-Type} {text/xml}, {charset} utf-8; SOAP bir nokta bir için {SOAPAction} header'ıyla; "
  "ya da SOAP bir nokta iki için {application/soap+xml}. Yanıt {xml2Json} ile JSON'a çevrilip test edilebilir. "
  "Finans ve sigorta entegrasyonlarında, örneğin sigorta şirketi teklif servislerinde, SOAP hâlâ yaygındır.")
t("Collection Runner: sınır değer verisi", ["senaryo", "tip", "araç", "tutar", "vade", "beklenen"],
  [["min_vade", "BIREYSEL", "400000", "250000", "6", "201"], ["max_vade", "BIREYSEL", "400000", "250000", "60", "201"],
   ["vade_asim", "BIREYSEL", "400000", "250000", "61", "422"], ["kredi_deger_asim", "BIREYSEL", "400000", "300000", "36", "422"],
   ["kurumsal_yuzde90", "KURUMSAL", "1000000", "900000", "36", "201"], ["ust_sinir_asim · tutar_sifir", "BIREYSEL", "2500000 · 400000", "400000 · 0", "36", "422 · 400"]],
  "{Collection Runner} ve veri odaklı test: aynı isteği bir CSV ya da JSON dosyasıyla farklı girdilerle çalıştırırsın; bu sınır değer analizidir. "
  "Sütunlar: senaryo, müşteri tipi, araç bedeli, tutar, vade ve beklenen kod. "
  "min_vade: bireysel, dört yüz bin araç, iki yüz elli bin tutar, altı ay, beklenen iki yüz bir. max_vade: aynı değerler, altmış ay, iki yüz bir. "
  "vade_asim: altmış bir ay, dört yüz yirmi iki. kredi_deger_asim: üç yüz bin tutar, otuz altı ay, dört yüz yirmi iki. "
  "kurumsal_yuzde90: kurumsal, bir milyon araç, dokuz yüz bin tutar, iki yüz bir. "
  "ust_sinir_asim: iki milyon beş yüz bin araç, dört yüz bin tutar, dört yüz yirmi iki. tutar_sifir: sıfır tutar, dört yüz. "
  "Testte beklenen kod {pm.iterationData.get} ile okunur ve durum koduyla karşılaştırılır.")
m("Akış kontrolü", ["pm.execution.setNextRequest(\"İstek adı\")", "Zincir: token al → başvuru oluştur → durum sorgula → iptal et"],
  "Akış kontrolü: {pm.execution.setNextRequest}, parantez içinde istek adı, ile sıradaki isteği belirleyip bir senaryo zinciri kurarsın: "
  "token al, başvuru oluştur, durum sorgula, iptal et.")

# ───────────────────────────── İleri
m("Komut satırı ve CI/CD", ["Newman: açık kaynak, npm, dışa aktarılan collection JSON'ı çalıştırır",
                            "Postman CLI: resmi araç; workspace'ten ID ile çeker, sonuçları buluta yollar (API key)",
                            "newman run … -e uat.postman_environment.json -d sinir_degerler.csv --reporters cli,junit,htmlextra",
                            "postman login --with-api-key · postman collection run <id> -e <id>"],
  "İleri seviye: komut satırı ve CI/CD. İki seçenek var. {Newman}: açık kaynaklı, npm ile kurulan, dışa aktarılmış {collection} JSON'larını çalıştıran klasik araç. "
  "{Postman CLI}: {Postman}'ın resmi aracı; {collection}'ı {workspace}'ten ID ile çekebilir ve sonuçları {Postman} bulutuna gönderir; {API key} gerekir. "
  "{Newman} komutu: {npm install} tire g {newman} ve {newman-reporter-htmlextra}; sonra {newman run}, kredi-api {collection} dosyası, "
  "tire e ile {uat} ortam dosyası, tire d ile {sinir_degerler} nokta csv, {reporters} {cli}, {junit}, {htmlextra}, ve {junit} raporu için {results} bölü {junit} nokta xml. "
  "{Postman CLI} komutu: {postman login} {with-api-key}, sonra {postman collection run}, {collection} kimliği ve tire e ile ortam kimliği.",
  bolum="Postman · İleri seviye")
m("Pipeline, mock, OpenAPI, monitor", ["Test başarısızsa build kırılır · JUnit → Jenkins / Azure DevOps / GitLab · HTML artefakt",
                                       "Kurumlar sık Newman'ı seçer: bulut bağımlılığı, veri politikası",
                                       "Mock server: örnek yanıtlarla sahte API; BA örnek yanıtları tanımlar",
                                       "OpenAPI 3.x içe aktar, contract testing · Monitors: bulutta periyodik çalıştırma"],
  "{Pipeline}'da test başarısız olursa build kırılır; JUnit raporu {Jenkins}, {Azure DevOps} ya da {GitLab}'a, HTML raporu artefakt olarak eklenir. "
  "Kurumlar bulut bağımlılığı ve veri politikaları nedeniyle sıklıkla {Newman}'ı tercih eder. "
  "{Mock server}: backend hazır olmadan örnek yanıtlarla, yani {examples} ile sahte API; frontend ve entegrasyon ekipleri paralel çalışır. "
  "İş analisti örnek yanıtları gereksinimin parçası olarak tanımlar: başarılı, iş kuralı hatası, sistem hatası. "
  "API tasarımı ve dokümantasyon: {OpenAPI} üç nokta x tanımını içe aktarma, {collection} üretme, şema ile {collection} senkronu; "
  "{collection}'dan yayımlanabilir dokümantasyon. {Contract testing}: yanıtların {OpenAPI} şemasına uygunluğu. "
  "{Monitors}: {collection}'ın belirli aralıklarla bulutta çalıştırılması; sağlık kontrolü ve SLA izleme. "
  "İç ağdaki servisler için uygun değilse {Newman} artı zamanlayıcı kullanılır.")
m("Ekip çalışması ve güvenlik kontrol listesi", ["Fork / pull request / merge · rol bazlı workspace · API Governance · Postbot · Postman Vault",
                                                 "Token yok → 401 · başka bayinin başvurusu → 403 (BOLA / IDOR)",
                                                 "Aşırı büyük payload → 413 / 400 · rate limit → 429",
                                                 "Hata mesajında stack trace ya da kişisel veri yok · kişisel veri maskeli"],
  "Ekip çalışması ve yönetişim: {fork}, {pull request}, {merge}; rol bazlı {workspace} erişimi; adlandırma ve güvenlik için {API Governance} kuralları; "
  "yapay zeka asistanı {Postbot} ile test ve doküman önerisi; hassas veriler için yerel saklama, {Postman Vault}. "
  "Güvenlik testleri için iş analisti kontrol listesi: token olmadan çağrı dört yüz bir dönmeli. "
  "Başka bayinin başvurusuna erişim dört yüz üç dönmeli; bu BOLA ya da IDOR kontrolüdür. "
  "Aşırı büyük {payload} dört yüz on üç ya da dört yüz; hız sınırı, yani {rate limit}, dört yüz yirmi dokuz. "
  "Hata mesajında {stack trace} ya da kişisel veri dönmemeli; kişisel veriler yanıtta maskeli gelmeli.")

# ───────────────────────────── Hatalar, mülakat
m("Sık yapılan hatalar", ["Token, şifre, müşteri verisini paylaşılan collection'a kaydetmek", "Yalnız 200 senaryosu; 4xx/5xx ve sınırlar yok",
                          "Birbirine bağımlı, sırası belirsiz testler", "Ortam URL'sini isteğe sabit yazmak", "Yalnız durum koduna bakmak"],
  "Sık yapılan hatalar. Token, şifre ve müşteri verisini paylaşılan {collection} ya da ortama kaydetmek. "
  "Sadece iki yüz senaryosunu test etmek; dört yüzlü, beş yüzlü kodları ve sınır değerleri atlamak. "
  "Testleri birbirine bağımlı ve sırası belirsiz yazmak. Ortama özel URL'leri isteğin içine sabit yazmak, değişken kullanmamak. "
  "Ve yanıt içeriğini değil, yalnız durum koduna bakmak.", bolum="Postman · Hatalar ve mülakat")
m("Mülakat soruları", ["1. 401 ile 403 farkı?", "2. Değişken kapsamları; çakışırsa hangisi?", "3. Kabul kriteri → Postman testi (örnek)",
                       "4. Newman CI/CD'de nasıl?", "5. Backend hazır değilken entegrasyon testi?", "6. SOAP servisi Postman'de nasıl test edilir?"],
  "Mülakat soruları. Bir: dört yüz bir ile dört yüz üç farkı nedir? İki: {Postman}'de değişken kapsamları nelerdir, çakışırsa hangisi geçerli olur? "
  "Üç: bir kabul kriterini {Postman} testine nasıl çevirirsiniz? Örnek verin. Dört: {Newman}'ı CI/CD'de nasıl kullanırsınız? "
  "Beş: backend hazır değilken entegrasyon testine nasıl başlarsınız? Altı: SOAP servisini {Postman} ile nasıl test edersiniz?")
m("Cevap ipuçları", ["401 kimlik · 403 yetki", "En dar kapsam kazanır", "within(6, 60) + 5 / 61 negatif", "newman + junit → build kırılır", "Mock server · raw XML + SOAPAction"],
  "İpuçları, bölümün içeriğinden. Dört yüz bir: kimlik yok ya da geçersiz; dört yüz üç: kimlik var, yetki yok. "
  "Kapsamda en dar olan kazanır: {local}, {data}, {environment}, {collection}, {global}. "
  "Kabul kriteri örneği: vade altı ile altmış arasında olmalı; testte vade {within} altı, altmış; ayrıca beş ve altmış bir ile negatif testler. "
  "CI/CD: {newman run}, tire d veri dosyası, {junit} raporu; test kalırsa build kırılır. "
  "Backend yokken: {mock server} ve örnek yanıtlar. SOAP: {raw} XML, {SOAPAction} header'ı ve {xml2Json}.")

# ───────────────────────────── Görsel rehber
g("Önce kavram: bir API çağrısının parçaları", "g25.png",
  [([0.02, 0.14, 0.48, 0.92], "İstek: dört kısım"), ([0.53, 0.14, 0.99, 0.92], "Yanıt: üç kısım")],
  "Görsel rehber. Önce kavram: HTTP istek ve yanıt anatomisi. Bir API çağrısı iki parçadır: istek dört kısım, yanıt üç kısım. "
  "İstek, yani {request}: bir, metot ve URL; {POST}, api nokta ornek, bölü v1 bölü {applications}. İki, {header}'lar: {Content-Type} {application/json}; "
  "{Authorization} {Bearer} ve token; {X-Correlation-Id}. Üç, sorgu parametreleri, {GET}'te; durum eşittir ONAY ve sayfa eşittir bir. "
  "Dört, gövde, yani {body}: tutar iki yüz elli bin, vade otuz altı. "
  "Yanıt, yani {response}: bir, durum kodu; iki yüz bir {Created}. İki yüzlüler başarı, dört yüzlüler istemci, beş yüzlüler sunucu. "
  "İki, {header}'lar: {Content-Type} ve {Location}, yani yeni kaydın adresi, bölü v1 bölü {applications} bölü BSV-1001. "
  "Üç, gövde: {basvuruId} BSV-1001, durum ALINDI. Altta: testte kod, süre, alanlar ve şema kontrol edilir.", bolum="Postman · Görsel rehber")
g("Postman ekranı nasıl okunur?", "g26.png",
  [([0.02, 0.08, 1.0, 0.15], "1–2 · Workspace, New, Import · ortam seçici"), ([0.02, 0.15, 0.27, 0.93], "3 · Sol kenar çubuğu"),
   ([0.27, 0.16, 1.0, 0.27], "4–6 · Metot, URL, Send"), ([0.27, 0.26, 1.0, 0.55], "7 · İstek sekmeleri"),
   ([0.27, 0.56, 1.0, 0.82], "8–9 · Yanıt sekmeleri, durum satırı"), ([0.27, 0.82, 1.0, 0.93], "10 · Console")],
  "Postman ekran yerleşimi; şematik, numaralı bölgeler. "
  "Bir: {workspace} seçici, {New} ve {Import}. Çalışma alanını seçersin; {New} ile HTTP isteği, {collection} ya da {environment} oluşturursun; "
  "{Import} ile {OpenAPI} dosyası, {cURL} komutu ya da başkasının verdiği {collection} JSON'unu içeri alırsın. "
  "İki: ortam seçici; DEV, TEST, UAT arasında geçiş. Yanındaki göz simgesi aktif değişkenleri gösterir. "
  "{No environment} seçiliyse {baseUrl} çözülmez ve hata alırsın. "
  "Üç: sol kenar çubuğu; {Collections} ağacı, {Environments}, {History}. Koleksiyon adının yanındaki üç nokta menüsü: {Run collection}, {Add request}, "
  "{Add folder}, {Export}, {Fork}. "
  "Dört metot; beş URL, adres ve değişkenler; çift süslü parantez turuncu ya da kırmızı görünüyorsa değişken tanımlı değildir. "
  "Altı {Send}; ok menüsünde {Send and Download}. "
  "Yedi istek sekmeleri: {Params}, yani sorgu; {Authorization}; {Headers}; {Body}, {raw} ve JSON seç; {Scripts}, yani {Pre-request} ve {Post-response}; "
  "ve {Settings}, SSL doğrulama ve yönlendirme. "
  "Sekiz yanıt sekmeleri: {Body}, yani {Pretty}, {Raw} ve {Preview}; {Headers}; {Cookies}; {Test Results}, geçen ve kalan testler. "
  "Dokuz durum satırı: HTTP kodu, süre ve boyut; koda tıklayınca açıklama görünür. "
  "On {Console}: gerçekte gönderilen isteği, çözülmüş değişkenlerle, ve {console.log} çıktılarını gösterir; hata ayıklamada ilk bakacağın yer. "
  "Kısayol kontrol alt C.")
t("Menü ve kısayol rehberi (1/2)", ["Yapmak istediğin", "Yol"],
  [["Yeni collection · ortam", "Collections → + · Environments → + → ad, tip, değer → Save"], ["Collection değişkeni · ortak auth", "Variables sekmesi · Authorization → Inherit"],
   ["Test yazmak", "Scripts → Post-response → Snippets"], ["cURL'den istek · kod olarak al", "Import → cURL · </> Code"]],
  "Menü ve kısayol rehberi. Yeni {collection}: sol çubukta {Collections}, artı; ya da {New}, {Collection}. "
  "Ortam oluşturmak: {Environments}, artı; değişken adı, tip, yani {default} ya da {secret}, ve değer; {Save}. "
  "{Collection} değişkeni: {collection}'a tıkla, {Variables} sekmesi. Ortak yetkilendirme: {Authorization} sekmesi; isteklerde {Inherit auth from parent}. "
  "Test yazmak: istek, {Scripts}, {Post-response}; sağdaki {Snippets} listesinden hazır kod seç, örneğin {Status code}: {Code is} iki yüz. "
  "{cURL}'den istek oluşturmak: {Import}, {cURL} metnini yapıştır. İsteği kod olarak almak: sağ kenardaki {Code}; {cURL}, {Python}, {Java} ve diğerleri.")
t("Menü ve kısayol rehberi (2/2)", ["Yapmak istediğin", "Yol"],
  [["Toplu çalıştırma", "Collection … → Run → iterasyon, gecikme, veri dosyası"], ["Örnek yanıt · mock", "Save as example · Mock collection"],
   ["Newman için dışa aktarma", "Export → Collection v2.1 · ortam … → Export"], ["Kaydet · sekme · gönder", "Ctrl+S · Ctrl+T · Ctrl+Enter"]],
  "{Collection}'ı toplu çalıştırmak: üç nokta, {Run}; iterasyon sayısı, gecikme ve veri dosyası, CSV ya da JSON; {Run}. "
  "Mock için örnek yanıt kaydetmek: yanıt alındıktan sonra {Save as example}. {Mock server}: üç nokta, {Mock collection}; ya da sol çubukta {Mock servers}. "
  "{Newman} için dışa aktarmak: üç nokta, {Export}, {Collection} v iki nokta bir; ortam için {Environments}, üç nokta, {Export}. "
  "Kaydet: Ctrl+S; yeni sekme: Ctrl+T; gönder: Ctrl+Enter. Tablolarda iki sütun var: yapmak istediğin ve yol.")

# ───────────────────────────── Laboratuvar
m("Laboratuvar (~45 dk): ilk adımlar", ["postman-echo.com: gönderdiğini geri döndürür · gerçek müşteri verisi yok",
                                "1. Create Workspace → \"BA Lab\" · 2. Ortam LAB: baseUrl = https://postman-echo.com",
                                "3. Collection \"Kredi API Lab\" → folder \"Başvuru\"", "4. GET {{baseUrl}}/get · Params basvuruId = BSV-1001",
                                "5. Body → Pretty: args · 200 OK ve süre"],
  "Laboratuvar: herkese açık test servisiyle ilk test setin; yaklaşık kırk beş dakika. "
  "{Postman}'ın kendi ücretsiz test servisi {postman-echo} nokta com kullanılır: gönderdiğin veriyi sana geri döndürür. Gerçek müşteri verisi kullanma. "
  "Bir: sol üst {workspace} menüsü, {Create Workspace}, adı BA {Lab}, {Personal}. "
  "İki: {Environments}, artı, adı LAB. Değişken {baseUrl} eşittir https {postman-echo} nokta com; {Save}; sağ üstten LAB'ı seç. "
  "Üç: {Collections}, artı, adı kredi API {Lab}; içine {Add folder}, başvuru. "
  "Dört: klasöre {Add request}, adı başvuru sorgula. Metot {GET}, URL {baseUrl} bölü {get}. {Params} sekmesine {basvuruId} eşittir BSV-1001 ekle; "
  "URL otomatik olarak soru işareti {basvuruId} eşittir BSV-1001 olur. {Send}. "
  "Beş: yanıtı oku; {Body}, {Pretty}. {args} alanında gönderdiğin parametreyi gör; durum satırında iki yüz {OK} ve süreyi oku.",
  bolum="Postman · Laboratuvar")
m("Laboratuvar: testler", ["6. Test: durum kodu 200 · args.basvuruId eql \"BSV-1001\"",
                       "7. POST {{baseUrl}}/post · body: { tckn, tutar, vade } değişkenlerle",
                       "8. Collection değişkenleri: tckn = 11111111110 (sahte), tutar = 250000, vade = 36",
                       "9. Testler: tutar 250000 · vade 6–60 · yanıt 2 sn altı"],
  "Altı, ilk test: {Scripts}, {Post-response}'a iki test yaz. Durum kodu iki yüz; ve parametre geri döndü, yani {args} nokta {basvuruId} eşittir BSV-1001. "
  "{Send}, sonra {Test Results} sekmesine bak. "
  "Yedi, {POST} isteği: yeni istek, başvuru oluştur; metot {POST}, URL {baseUrl} bölü {post}. {Body}, {raw}, JSON: TCKN, tutar ve vade, değişkenlerle. "
  "Sekiz, {collection} değişkenleri: {Variables} altında TCKN on bir tane bir ve sonda sıfır, sahte bir numara; tutar 250000; vade otuz altı. {Send}. "
  "Dokuz, {POST} testi: echo servisi gövdeyi {json} alanında döndürür. Üç test: tutar doğru iletildi, yani iki yüz elli bin; "
  "vade altı ile altmış ay aralığında; yanıt iki saniyeden hızlı.")
m("Laboratuvar: son adımlar", ["Console: {{tutar}} yerine 250000 gitti", "veri.csv: 100000/6 · 250000/36 · 400000/60 · 500000/72 → Run",
                         "Son satırda \"Vade 6-60 ay\" testi KALIR: sınır değer testi hatayı yakaladı",
                         "Export (v2.1) + ortam → newman run … -e LAB… -d veri.csv", "BA çıktısı: 5 kabul kriteri → 5 pm.test"],
  "Sonra alt çubuktan {Console}'u aç, son isteği genişlet; çift süslü parantez içindeki tutar yerine iki yüz elli bin gittiğini gör. "
  "Veri odaklı çalıştırma: bilgisayarında {veri} nokta csv oluştur; sütunlar tutar ve vade. Satırlar: 100000 ve altı; 250000 ve otuz altı; "
  "400000 ve altmış; 500000 ve yetmiş iki. {Collection}, üç nokta, {Run}, {Data} alanında {veri} nokta csv'yi seç, {Run}. "
  "CSV'deki sütun adları değişken gibi davranır. Son satırda vade altı ile altmış ay testinin kaldığını gör: sınır değer testinin hatayı nasıl yakaladığını gösterir. "
  "Dışa aktar ve komut satırı: {collection}'ı {Export} et, v iki nokta bir; ortamı da {export} et. Terminalde {npm install} tire g {newman}; "
  "sonra {newman run}, kredi API {Lab} {collection} dosyası, tire e LAB ortam dosyası, tire d {veri} nokta csv. "
  "Son olarak iş analisti çıktısı: başvuru API kabul kriterlerinden beş tanesini seç ve her biri için bir {pm.test} satırı yaz.")

# ───────────────────────────── Uygulama paketi
m("Sınır değer analizi", ["Rastgele değer seçilmez", "Her sınırın bir altı, kendisi, bir üstü + aralığın ortası",
                          "Hataların çoğu sınırda: < yerine <= yazılması"],
  "Postman uygulama paketi: kurallardan test seti üretmek. Sınır değer analizi: hangi değerler test edilir? "
  "Bir kuralı test etmek için rastgele değer seçilmez. Her sınırın bir altı, kendisi ve bir üstü denenir; "
  "ayrıca geçerli aralığın ortasından bir değer alınır. Hataların çoğu sınırda çıkar: küçüktür yerine küçük eşit yazılması gibi.",
  bolum="Postman · Uygulama paketi")
t("Sınır değerler (Firma §1.3)", ["Kural", "Geçersiz alt", "Alt sınır", "İç", "Üst sınır", "Geçersiz üst"],
  [["Vade 6–60 ay", "5", "6", "36", "60", "61"], ["Kurumsal ≤ fatura × %90 (fatura 1.000.000 ₺)", "—", "—", "500.000", "900.000", "900.001"]],
  "Firma kuralları için sınır değerler. Vade altı ile altmış ay: geçersiz alt beş, alt sınır altı, geçerli iç otuz altı, üst sınır altmış, geçersiz üst altmış bir. "
  "Kurumsal kredi, fatura bedelinin yüzde doksanını aşamaz; fatura bir milyon lira. Geçerli iç beş yüz bin, üst sınır dokuz yüz bin, geçersiz üst dokuz yüz bin bir. "
  "Bunlara ek olarak her alan için biçim hatalarını da dene: alanı hiç göndermemek, boş metin, sayı yerine abc, negatif değer. "
  "Bireysel kredi değer kademelerinde de aynı yöntem kullanılır; kademenin araç değerine mi kredi tutarına mı uygulandığını önce çalışma setinden teyit et.")
t("Veri güdümlü test: kural_testi.csv", ["senaryo", "fatura", "tutar", "vade", "beklenen"],
  [["vade_alt_gecersiz", "1000000", "500000", "5", "RED_VADE"], ["vade_alt_sinir · vade_ic · vade_ust_sinir", "1000000", "500000", "6 · 36 · 60", "GECERLI"],
   ["vade_ust_gecersiz", "1000000", "500000", "61", "RED_VADE"], ["oran_sinir", "1000000", "900000", "36", "GECERLI"],
   ["oran_gecersiz", "1000000", "900001", "36", "RED_ORAN"]],
  "Veri güdümlü test: bir istek, yedi senaryo. Bir: bilgisayarında {kural_testi} nokta csv oluştur; hepsi kurumsal müşteri, fatura bir milyon. "
  "vade_alt_gecersiz: tutar beş yüz bin, vade beş; beklenen RED_VADE. vade_alt_sinir, vade_ic ve vade_ust_sinir: vade altı, otuz altı ve altmış; beklenen GECERLI. "
  "vade_ust_gecersiz: vade altmış bir; RED_VADE. oran_sinir: tutar dokuz yüz bin, vade otuz altı; GECERLI. "
  "oran_gecersiz: tutar dokuz yüz bin bir; RED_ORAN.")
m("Kural testi isteği ve script", ["Add folder \"Kural testi\" → POST {{baseUrl}}/post · body: musteri_tipi, fatura, tutar, vade",
                                   "kuralKontrol: vade tamsayı değil ya da < 6 ya da > 60 → RED_VADE",
                                   "KURUMSAL ve tutar > fatura × 0.90 → RED_ORAN · yoksa GECERLI",
                                   "pm.test(senaryo + \" → \" + beklenen): kuralKontrol(govde) eql beklenen"],
  "İki: kredi API {Lab} {collection}'ında yeni bir klasör aç, {Add folder}, kural testi; içine yeni istek: adı kural testi, metot {POST}, URL {baseUrl} bölü {post}; "
  "{Body}, {raw}, JSON: müşteri tipi, fatura, tutar ve vade, değişkenlerle. "
  "Üç: {Scripts}, {Post-response} sekmesine {kuralKontrol} adlı bir fonksiyon yaz. "
  "Gerçek API'de beklenen karar yanıttan okunur; echo servisi gönderdiğimizi geri verdiği için burada kuralı kendimiz uygulayıp CSV'deki beklenenle karşılaştırıyoruz. "
  "Kural: {if}, vade {Number.isInteger} değilse ya da vade altıdan küçük ya da altmıştan büyükse, {return} RED_VADE. "
  "Müşteri KURUMSAL ve tutar fatura çarpı sıfır virgül doksandan büyükse RED_ORAN. Değilse GECERLI. "
  "Test adı senaryo, ok ve beklenen sonuçtan oluşur; {kuralKontrol} gövdesinin sonucu beklenene eşit olmalı.")
m("Çalıştır ve kendini sına", ["4. Kural testi … → Run folder → Data: kural_testi.csv → 7 iterasyon → Run",
                               "Beklenen: 7 iterasyon, 7 başarılı (ör. \"vade_ust_gecersiz → RED_VADE\")",
                               "Mantık Node.js'te aynı 7 satırla doğrulandı",
                               "Kendini sına: vade > 60 yerine vade >= 60 → yalnız \"vade_ust_sinir\" kalır"],
  "Dört: kural testi klasörünün yanındaki üç nokta, {Run folder}; {Data} alanından {kural_testi} nokta csv'yi seç; iterasyon sayısı otomatik yedi olur; {Run}. "
  "Beklenen: yedi iterasyon, yedi başarılı test. Test adlarında senaryo ve beklenen sonuç görünür; örneğin vade_ust_gecersiz, ok, RED_VADE. "
  "Bu mantık {Node.js}'te aynı yedi satırla çalıştırılarak doğrulanmıştır. "
  "Kendini sına: script'teki vade büyüktür altmış ifadesini vade büyük eşit altmış yap ve yeniden çalıştır. Yalnız vade_ust_sinir testi kalmalı. "
  "Sınır değer testinin neden gerekli olduğu tam olarak budur.")
dikkat("Sınırdaki tek karakter", "vade > 60 ↔ vade >= 60: tek karakter, bir senaryo kaybı. Sınır değer testi tam bunu yakalar.",
       "Buna dikkat et: büyüktür ile büyük eşit arasındaki fark tek bir karakter, ama altmış aylık bir krediyi reddetmek demek. "
       "Kodu okuyarak bu hatayı bulmak zordur; sınır değer testi ise hemen yakalar.")
t("Newman ile komut satırı", ["Seçenek", "Anlamı"],
  [["-e", "Ortam dosyası (baseUrl gibi)"], ["-d", "Veri dosyası; satır sayısı kadar iterasyon"],
   ["--reporters cli,junit", "Ekran + JUnit XML"], ["--reporter-junit-export", "XML raporun yolu; CI okur"], ["--bail · --folder", "İlk hatada dur · yalnız o klasör"]],
  "{Newman} ile komut satırından çalıştırma: {newman run}, kredi API {Lab} {collection} dosyası; tire e LAB ortam dosyası; tire d {kural_testi} nokta csv; "
  "tire tire {folder} kural testi; {reporters} {cli} ve {junit}; {reporter-junit-export} {sonuc} nokta xml. "
  "Seçenekler: tire e ortam dosyası, {baseUrl} gibi değişkenler. Tire d veri dosyası, CSV ya da JSON; satır sayısı kadar iterasyon. "
  "{reporters} {cli} virgül {junit}: hem ekrana hem JUnit XML'e rapor. {reporter-junit-export}: XML raporun yolu; CI araçları bu dosyayı okur. "
  "{bail}: ilk hatada durur; uzun setlerde zaman kazandırır.")
dikkat("Newman'da beklenen", "Önce collection'ı yeniden Export (v2.1). --folder yalnız o klasörü çalıştırır. Özet: iterations 7, assertions 7, failed 0 · sonuc.xml oluşur.",
       "Beklenen: önce {collection}'ı yeniden {Export} et, v iki nokta bir, ki yeni klasör dosyada olsun. "
       "Tire tire {folder} seçeneği yalnız o klasörü çalıştırır; laboratuvardaki eski istekler bu CSV ile çalışsaydı kendi testleri kalırdı. "
       "Ekranda bir özet tablo: {iterations} 7, {assertions} yedi, {failed} sıfır. Klasörde {sonuc} nokta xml oluşur.", tip="bilgi")
m("Değişken kapsamı: aynı isim iki yerde", ["En dar kapsam kazanır: local → data (CSV) → environment → collection → global",
                                            "Lab: collection tutar = 250000, CSV'deki tutar sütunu onu ezer",
                                            "Beklenmedik değer → Console'da gerçekte giden değere bak"],
  "Değişken kapsamı: aynı isim iki yerde olursa en dar kapsam kazanır: {local}, {data} yani CSV, {environment}, {collection}, {global}. "
  "Laboratuvarda tutar {collection} değişkeni 250000 iken CSV'deki tutar sütunu onu ezer. "
  "Bir test beklenmedik değerle çalışıyorsa {Console}'da isteğin gerçekte hangi değerle gittiğine bak.")
m("Bağımsız görev: kasko poliçesi testi", ["Kural: kasko muafiyetsiz, dain-i mürtehin Firma, bitiş gelecekte",
                                           "1. {{baseUrl}}/post: { police: { muafiyet: 0, dainiMurtehin: \"Firma\", bitis: \"2027-11-20\" } }",
                                           "2. Üç pm.test: muafiyet sıfır · dain-i mürtehin Firma (harf duyarsız) · bitiş bugünden sonra",
                                           "3. muafiyet 2500 → yalnız ilk test kalır · tarih geçince 3. test de kalır"],
  "Bağımsız görev: kasko poliçesi doğrulama testi. Firma kuralı: kasko muafiyetsiz olmalı ve dain-i mürtehin Firma olmalı; poliçenin bitiş tarihi gelecekte olmalı. "
  "Bir: {baseUrl} bölü {post} adresine şu gövdeyi gönderen bir istek oluştur: poliçe; muafiyet sıfır, {dainiMurtehin} Firma, bitiş 2027-11-20. "
  "İki: üç ayrı {pm.test} yaz: muafiyet sıfır; dain-i mürtehin Firma, büyük küçük harf fark etmeksizin; bitiş tarihi bugünden sonra. "
  "Üç: gövdede muafiyet değerini iki bin beş yüz yap ve yalnız ilk testin kaldığını gör. "
  "Not: bitiş tarihi sabit yazıldığı için bu tarih geçince üçüncü test de kalır; o zaman tarihi ileri al.", bolum="Postman · Bağımsız görev ve sorun giderme")
t("Sorun giderme (1/2)", ["Belirti", "Olası neden", "Çözüm"],
  [["{{baseUrl}} kırmızı, \"Invalid URL\"", "Ortam seçili değil", "Sağ üstten LAB'ı seç"], ["Body'de {{fatura}} olduğu gibi", "Tek istek Send ile; CSV yalnız Runner'da dolar", "Runner'dan veri dosyasıyla"],
   ["JSONError: Unexpected token", "Yanıt HTML ya da body'de boş sayı", "Raw ile oku; CSV'de boş hücre?"]],
  "Sorun giderme. {baseUrl} kırmızı ve istek {Invalid URL} veriyorsa: ortam seçili değildir; sağ üstteki ortam seçiciden LAB'ı seç. "
  "{Body}'de fatura değişkeni olduğu gibi gidiyorsa: tek isteği {Send} ile gönderdin; CSV değerleri yalnız {Runner}'da dolar. {Collection Runner}'dan veri dosyasıyla çalıştır. "
  "{JSONError} {Unexpected token} alıyorsan: yanıt JSON değil, bir HTML hata sayfası; ya da gövdede sayı alanı boş kaldı. "
  "{Body}, {Raw} ile yanıtı oku; CSV'de boş hücre var mı bak.")
t("Sorun giderme (2/2)", ["Belirti", "Olası neden", "Çözüm"],
  [["Runner 1 iterasyon yapıyor", "Veri dosyası yok ya da satır sonu okunamadı", "Dosya adı görünüyor mu? UTF-8 kaydet · başlık satırı şart"],
   ["newman: command not found", "Kurulmadı ya da PATH'te yok", "npm install -g newman, terminali yeniden aç"],
   ["Postman'de geçiyor, Newman'da kalıyor", "Ortam export edilmedi ya da eski", "Ortamı yeniden export et, -e ile ver"]],
  "{Runner} bir iterasyon yapıyorsa: veri dosyası seçilmemiş ya da satır sonu biçimi okunamamıştır. {Data} alanında dosya adının göründüğünü kontrol et; "
  "dosyayı UTF-8 olarak yeniden kaydet. Not: başlık satırı yoksa {Postman} ilk satırı başlık sayar ve bir satır eksik çalışır. "
  "{newman} {command not found}: {Newman} kurulmamış ya da {PATH}'te yok; {npm install} tire g {newman}, terminali kapatıp aç. "
  "Testler {Postman}'de geçiyor, {Newman}'da kalıyorsa: ortam dosyası {export} edilmemiş ya da eskidir. Ortamı yeniden {export} et ve tire e ile ver.")

soru("Bilgi kontrolü 1/5", "Kural \"vade 6–60 ay\". Hangi dört değer sınır testine girer?",
     ["0, 30, 60, 90", "5, 6, 60, 61", "6, 12, 24, 60", "1, 6, 59, 100"], 1,
     "Beş soruluk bilgi kontrolü. Birinci soru: kural vade altı ile altmış ay. Hangi dört değer sınır testine girer? "
     "A, sıfır, otuz, altmış, doksan. B, beş, altı, altmış, altmış bir. C, altı, on iki, yirmi dört, altmış. D, bir, altı, elli dokuz, yüz.",
     "Doğru cevap B: beş, altı, altmış, altmış bir.", bolum="Postman · Bilgi kontrolü ve çözümler")
soru("Bilgi kontrolü 2/5", "Fatura 1.000.000 ₺ olan kurumsal müşteride hangi tutar reddedilmeli?",
     ["900.000", "899.999", "900.001", "500.000"], 2,
     "İkinci soru: fatura bir milyon lira olan kurumsal müşteride hangi tutar reddedilmeli? "
     "A, dokuz yüz bin. B, sekiz yüz doksan dokuz bin dokuz yüz doksan dokuz. C, dokuz yüz bin bir. D, beş yüz bin.",
     "Doğru cevap C: dokuz yüz bin bir.")
soru("Bilgi kontrolü 3/5", "CSV'de ve collection'da aynı adlı değişken varsa hangisi kullanılır?",
     ["Collection", "CSV (data)", "Global", "İlk tanımlanan"], 1,
     "Üçüncü soru: CSV'de ve {collection}'da aynı adlı değişken varsa hangisi kullanılır? A, {collection}. B, CSV, yani {data}. C, {global}. D, ilk tanımlanan.",
     "Doğru cevap B: CSV. Dar kapsam kazanır.")
soru("Bilgi kontrolü 4/5", "Newman'da veri dosyası hangi seçenekle verilir?", ["-e", "-d", "-r", "-g"], 1,
     "Dördüncü soru: {Newman}'da veri dosyası hangi seçenekle verilir? A, tire e. B, tire d. C, tire r. D, tire g.",
     "Doğru cevap B: tire d.")
soru("Bilgi kontrolü 5/5", "Yanıt kodu 422 ne anlama gelir?",
     ["Sunucu çöktü", "Yetki yok", "İstek biçimi doğru ama iş kuralına uymuyor", "Kayıt bulunamadı"], 2,
     "Beşinci soru: yanıt kodu dört yüz yirmi iki ne anlama gelir? A, sunucu çöktü. B, yetki yok. C, istek biçimi doğru ama iş kuralına uymuyor. D, kayıt bulunamadı.",
     "Doğru cevap C.")
t("Hızlı başvuru: sık test satırları", ["Amaç", "Kod"],
  [["Durum kodu · süre", "to.have.status(201) · responseTime below(5000)"], ["Alan var · değer", "to.have.property(\"basvuruId\") · durum eql(\"MANUEL_INCELEME\")"],
   ["Header", "to.have.header(\"X-Correlation-Id\")"], ["Sonraki isteğe taşı", "pm.collectionVariables.set(\"basvuruId\", …)"],
   ["CSV değeri", "pm.iterationData.get(\"vade\")"]],
  "Hızlı başvuru: sık kullanılan test satırları. Durum kodu: {to.have.status} iki yüz bir. Yanıt süresi: {responseTime} {below} beş bin. "
  "Alan var: {to.have.property} {basvuruId}. Alan değeri: durum {eql} MANUEL_INCELEME. Header: {to.have.header} {X-Correlation-Id}. "
  "Değeri sonraki isteğe taşı: {pm.collectionVariables.set} {basvuruId}. CSV değeri oku: {pm.iterationData.get} vade.")
m("Çözüm: kasko testleri", ["p = yanıt json.police", "\"Kasko muafiyetsiz\": p.muafiyet eql 0",
                            "\"Dain-i mürtehin Firma\": String(p.dainiMurtehin).toLowerCase() eql \"firma\"",
                            "\"Poliçe bitişi gelecekte\": new Date(p.bitis) > Date.now()", "muafiyet 2500 → yalnız ilk test kalır · Node.js'te doğrulandı"],
  "Bağımsız görevin çözümü. p, yanıttaki {json} nokta {police}. Birinci test, kasko muafiyetsiz: p nokta muafiyet sıfıra eşit. "
  "İkinci test, dain-i mürtehin Firma: {dainiMurtehin} değeri metne çevrilip küçük harfe indirilir ve firma'ya eşit olmalı. "
  "Üçüncü test, poliçe bitişi gelecekte: {new Date} p nokta bitiş, {Date.now}'dan büyük olmalı. "
  "Muafiyet iki bin beş yüz yapılınca yalnız kasko muafiyetsiz testi kalır. Bu üç testin mantığı {Node.js}'te doğrulanmıştır.")
m("Bu videoda neler gördük?", ["HTTP metotları, durum kodları, istek parçaları, değişkenler", "Test ve pre-request scriptleri, JSON Schema, auth, SOAP, Runner",
                               "Newman, Postman CLI, mock, OpenAPI, monitor, güvenlik", "Ekran, menüler, laboratuvar", "Sınır değer, veri güdümlü kural testi, Newman raporu"],
  "Toparlayalım. HTTP metotlarını, durum kodlarını, isteğin parçalarını ve değişken kapsamlarını gördük. "
  "Test ve {pre-request} scriptlerini, {JSON Schema}'yı, yetkilendirmeyi, SOAP'ı ve {Runner}'ı öğrendik. "
  "{Newman}, {Postman CLI}, {mock}, {OpenAPI}, {monitor} ve güvenlik kontrol listesine baktık. Ekranı, menüleri ve laboratuvarı çalıştık. "
  "Sınır değer analiziyle veri güdümlü bir kural testi kurup {Newman} raporu aldık. "
  "Bir sonraki videoda kimlik ve erişim yönetimi, yani IAM ile devam ediyoruz.", ton="sakin")

kaydet(__file__, {
    "baslik": "Business Analyst Teknik Rehberi · 8: Postman",
    "alt_baslik": "HTTP · test scriptleri · sınır değer · veri güdümlü test · Newman",
    "kapanis": "Sıradaki video: IAM",
    "tema": 8,
    "youtube_baslik": "Business Analyst Teknik Rehberi 8/14: Postman (API testi, sınır değer, Newman)",
    "etiketler": ["business analyst", "Postman", "API testi", "Newman", "sınır değer analizi", "iş analisti"],
}, {"HTTP": "eyç ti ti pi", "REST": "rest", "JSON": "ceyson", "XML": "eks em el", "CSV": "si es vi", "UAT": "yu ey ti", "DEV": "dev",
    "TEST": "test", "HMAC": "eyç mek", "PKCE": "pi key si i", "mTLS": "em ti el es", "SSL": "es es el", "CI": "si ay", "CI/CD": "si ay si di",
    "BOLA": "bola", "IDOR": "aydor", "KMP26": "ka me pe yirmi altı", "BSV-1001": "be se ve bin bir", "IPTAL": "iptal", "ALINDI": "alındı",
    "TASLAK": "taslak", "DEGERLENDIRMEDE": "değerlendirmede", "MANUEL_INCELEME": "manuel inceleme", "ONAYLANDI": "onaylandı",
    "REDDEDILDI": "reddedildi", "BIREYSEL": "bireysel", "KURUMSAL": "kurumsal", "RED_VADE": "red vade", "RED_ORAN": "red oran",
    "GECERLI": "geçerli", "LAB": "lab", "min_vade": "min vade", "max_vade": "maks vade", "vade_asim": "vade aşım",
    "kredi_deger_asim": "kredi değer aşım", "kurumsal_yuzde90": "kurumsal yüzde doksan", "ust_sinir_asim": "üst sınır aşım",
    "tutar_sifir": "tutar sıfır", "vade_alt_gecersiz": "vade alt geçersiz", "vade_alt_sinir": "vade alt sınır", "vade_ic": "vade iç",
    "vade_ust_sinir": "vade üst sınır", "vade_ust_gecersiz": "vade üst geçersiz", "oran_sinir": "oran sınır", "oran_gecersiz": "oran geçersiz",
    "postman.com/downloads": "postman nokta kom bölü daunlouds", "Ctrl+T": "kontrol ti", "Ctrl+Enter": "kontrol entır", "nodejs.org": "nod ceyes nokta org"})
