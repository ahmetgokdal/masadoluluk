# 🚀 AKILLI KABİN İZLEME SİSTEMİ - KURULUM REHBERİ

## 📋 GEREKSİNİMLER

### 1️⃣ Python 3.8 veya Üzeri

**Windows:**
1. https://www.python.org/downloads/ adresine gidin
2. "Download Python" butonuna tıklayın
3. İndirilen dosyayı çalıştırın
4. ⚠️ **ÖNEMLİ:** "Add Python to PATH" kutucuğunu işaretleyin
5. "Install Now" tıklayın
6. Kurulum bitince **Command Prompt** açın ve test edin:
   ```bash
   python --version
   ```
   Çıktı: `Python 3.8.x` veya üzeri olmalı

**Mac:**
1. https://www.python.org/downloads/ adresine gidin
2. Mac için Python'u indirin
3. İndirilen .pkg dosyasını çalıştırın
4. Terminal'i açın ve test edin:
   ```bash
   python3 --version
   ```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

---

### 2️⃣ Node.js 14 veya Üzeri

**Windows & Mac:**
1. https://nodejs.org/ adresine gidin
2. **LTS (Long Term Support)** versiyonunu indirin
3. İndirilen dosyayı çalıştırın
4. Kurulum tamamlandığında test edin:
   ```bash
   node --version
   npm --version
   ```

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
node --version
npm --version
```

---

## 📂 3️⃣ DOSYALARI İNDİRME

### GitHub'dan Clone (Önerilen):
```bash
# Terminal veya Command Prompt'u açın
cd Desktop  # veya istediğiniz bir klasör
git clone https://github.com/KULLANICI_ADINIZ/smart-cabin-monitoring.git
cd smart-cabin-monitoring
```

### ZIP İndirme:
1. ZIP dosyasını indirin
2. İstediğiniz bir klasöre çıkarın
3. Terminal/Command Prompt'u açın
4. Klasöre gidin:
   ```bash
   cd path/to/smart-cabin-monitoring
   ```

---

## 🚀 4️⃣ UYGULAMAYI BAŞLATMA

### Windows:

#### Yöntem 1: Çift Tıklama (En Kolay)
1. `BASLAT.bat` dosyasına **çift tıklayın**
2. İlk açılışta paketler yüklenecek (3-5 dakika)
3. Uygulama otomatik açılacak

#### Yöntem 2: Command Prompt
1. **Command Prompt** açın (Win+R → `cmd` → Enter)
2. Proje klasörüne gidin:
   ```bash
   cd Desktop\smart-cabin-monitoring
   ```
3. Uygulamayı başlatın:
   ```bash
   python smart_cabin_desktop.py
   ```

---

### Mac / Linux:

#### Terminal'de:
1. **Terminal** açın
2. Proje klasörüne gidin:
   ```bash
   cd ~/Desktop/smart-cabin-monitoring
   ```
3. Script'e çalıştırma izni verin:
   ```bash
   chmod +x baslat.sh
   ```
4. Uygulamayı başlatın:
   ```bash
   ./baslat.sh
   ```

**Alternatif:**
```bash
python3 smart_cabin_desktop.py
```

---

## ⏱️ İLK AÇILIŞ

### Ne Olacak?

1. **Paket Yükleme (3-5 dakika):**
   ```
   📦 Python paketleri kontrol ediliyor...
   📥 Paketler yükleniyor...
   ✅ Tüm Python paketleri hazır
   
   📦 Node.js paketleri kontrol ediliyor...
   📥 Frontend paketleri yükleniyor...
   ✅ Frontend paketleri mevcut
   ```

2. **Veritabanı Hazırlama (10-20 saniye):**
   ```
   🗄️  Yerel veritabanı ayarlanıyor...
   📊 Veritabanı ilk kez dolduruluyor...
   ✅ Veritabanı dolduruldu
   ```

3. **Sunucular Başlıyor:**
   ```
   🔧 Backend başlatılıyor...
   ✅ Backend hazır (http://127.0.0.1:8001)
   
   🎨 Frontend başlatılıyor...
   ✅ Frontend hazır (http://127.0.0.1:3000)
   ```

4. **Uygulama Açılıyor:**
   - Tarayıcı otomatik açılır
   - Veya native pencere açılır (pywebview kuruluysa)

---

## 🔐 İLK GİRİŞ

Uygulama açıldığında giriş ekranını göreceksiniz:

```
Kullanıcı Adı: admin
Şifre: admin123
```

"Giriş Yap" butonuna tıklayın.

---

## 📹 ESP32 KAMERA EKLEME

### Adım 1: Kamera IP'sini Öğrenin
1. ESP32'nizi açın
2. Serial Monitor'den IP adresini öğrenin
3. Örnek: `192.168.3.210`

### Adım 2: Kamerayı Test Edin
Tarayıcıda açın:
```
http://192.168.3.210/capture
```
Bir fotoğraf görmelisiniz.

### Adım 3: Uygulamaya Ekleyin
1. Dashboard'da **Ayarlar** menüsüne gidin
2. **Kamera Yönetimi** bölümüne gidin
3. **"Yeni Kamera Ekle"** butonuna tıklayın
4. Bilgileri girin:
   - **Kabin Numarası:** 1 (1-50 arası)
   - **Kamera URL:** `http://192.168.3.210/capture`
5. **"Test Et"** butonuna tıklayın
   - ✅ Başarılı olursa görüntü göreceksiniz
6. **"Kaydet"** butonuna tıklayın

---

## 🔔 TELEGRAM BOT KURULUMU (İSTEĞE BAĞLI)

### Adım 1: Bot Oluşturun
1. Telegram'ı açın
2. **@BotFather** kullanıcısını arayın ve mesaj gönderin
3. `/newbot` yazın
4. Bot için bir **ad** girin (örn: "Kabin İzleme Bot")
5. Bot için bir **username** girin (örn: "kabin_izleme_bot")
6. **Token**'ı kopyalayın (örn: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Adım 2: Chat ID Öğrenin
1. Botunuza bir mesaj gönderin (örn: "/start")
2. Tarayıcıda bu URL'yi açın:
   ```
   https://api.telegram.org/bot[TOKEN]/getUpdates
   ```
   `[TOKEN]` yerine kendi token'ınızı yazın
   
3. Çıktıda şunu arayın:
   ```json
   "chat": {
     "id": 123456789,
     ...
   }
   ```
4. Bu `id` numarasını kopyalayın

### Adım 3: Uygulamaya Ekleyin
1. Dashboard'da **Ayarlar** → **Telegram** bölümüne gidin
2. **Bot Token:** Adım 1'deki token'ı yapıştırın
3. **Chat ID Ekle:** Adım 2'deki ID'yi girin
4. **Kaydet** butonuna tıklayın

---

## ✅ HER ŞEY HAZIR!

Artık sistemin tüm özellikleri kullanılabilir:

- ✅ **Dashboard:** 50 kabinin gerçek zamanlı durumu
- ✅ **Kamera İzleme:** ESP32'den canlı görüntü
- ✅ **Öğrenci Takibi:** Oturum süreleri
- ✅ **PDF Raporlar:** Detaylı aktivite raporları
- ✅ **Telegram Bildirimleri:** Anlık uyarılar

---

## 🔄 SONRAKI AÇILIŞLAR

İlk kurulumdan sonra, uygulamayı her zaman çok hızlı başlatabilirsiniz:

**Windows:**
```bash
BASLAT.bat
```

**Mac/Linux:**
```bash
./baslat.sh
```

Açılış süresi: **10-15 saniye** ⚡

---

## ⚠️ SORUN GİDERME

### Python Bulunamadı
```bash
# Windows
python --version

# Yoksa Python'u yeniden kurun ve "Add to PATH" seçeneğini işaretleyin
```

### Node.js Bulunamadı
```bash
node --version

# Yoksa https://nodejs.org/ adresinden kurun
```

### Port Kullanımda
```bash
# 3000 veya 8001 portu kullanımdaysa:

# Windows
netstat -ano | findstr :3000
taskkill /PID [PID] /F

# Mac/Linux
lsof -i :3000
kill -9 [PID]
```

### Kamera Bağlanamıyor
- ✅ ESP32 ve bilgisayar **aynı WiFi ağında** olmalı
- ✅ Firewall kamera erişimini engelliyor olabilir
- ✅ Kamera URL'sini tarayıcıda test edin

### Frontend Yüklenmiyor
```bash
cd frontend
rm -rf node_modules
npm install
# veya
yarn install
```

---

## 📞 YARDIM

Sorun yaşıyorsanız:

1. **Dokümantasyon:** `MASAUSTU_KULLANIM.md` dosyasını okuyun
2. **Hızlı Başlangıç:** `HIZLI_BASLANGIC.md` dosyasına bakın
3. **GitHub Issues:** Proje sayfasında issue açın

---

## 🎉 BAŞARILAR!

Keyifli kullanımlar! 🚀

**Sorularınız varsa çekinmeden sorun!**
