# 🖥️ AKILLI KABİN İZLEME SİSTEMİ - MASAÜSTÜ UYGULAMASI

## 🚀 Hızlı Başlangıç

### Tek Tıkla Çalıştırma

**Windows:**
```bash
python smart_cabin_desktop.py
```

**Alternatif (çift tıklama):**
`smart_cabin_desktop.py` dosyasına çift tıklayın

---

## 📋 Gereksinimler

### Otomatik Kurulum
Uygulama ilk çalıştırmada tüm gereksinimleri otomatik olarak kurar:
- ✅ Python paketleri (FastAPI, OpenCV, vb.)
- ✅ Node.js paketleri (React bağımlılıkları)
- ✅ Yerel veritabanı (Mongita - dosya tabanlı)

### Manuel Kurulum (isteğe bağlı)

**Python Paketleri:**
```bash
cd backend
pip install -r requirements.txt
```

**Node.js Paketleri:**
```bash
cd frontend
yarn install
# veya
npm install
```

---

## 🎯 Özellikler

### ✨ Otomatik Özellikler
- 🗄️ **Yerleşik Veritabanı**: MongoDB kurulumu gerektirmez
- 📦 **Otomatik Kurulum**: Eksik paketleri otomatik yükler
- 🔄 **İlk Çalıştırma**: Örnek verilerle otomatik doldurulur
- 🌐 **Native Pencere**: Tarayıcı değil, gerçek masaüstü uygulaması

### 📊 Sistem Özellikleri
- **50 Kabin Yönetimi**: Tüm kabinleri tek ekrandan izleyin
- **Canlı Kamera İzleme**: ESP32 kameralarından gerçek zamanlı görüntü
- **Otomatik Durum Tespiti**: Yapay zeka ile doluluk tespiti
- **Öğrenci Takibi**: Oturum süreleri ve aktivite geçmişi
- **PDF Raporlar**: Detaylı aktivite raporları
- **Telegram Bildirimleri**: Anında uyarılar

---

## 🔐 Giriş Bilgileri

**Varsayılan Kullanıcı:**
- Kullanıcı Adı: `admin`
- Şifre: `admin123`

*(Ayarlar sayfasından değiştirebilirsiniz)*

---

## 📹 Kamera Bağlantısı

### ESP32 Kamera Ekleme

1. **Dashboard'dan Ayarlar'a gidin**
2. **"Kamera Ekle" butonuna tıklayın**
3. **Kamera bilgilerini girin:**
   - Kabin No: `1-50 arası`
   - Kamera URL: `http://192.168.3.210/capture`
4. **"Test Et" ile bağlantıyı kontrol edin**
5. **Kaydet**

### Kamera URL Formatı
```
http://[ESP32_IP_ADRESI]/capture
```

**Örnek:**
- `http://192.168.3.210/capture`
- `http://192.168.1.100/capture`

### Çoklu Kamera
Her kabine ayrı kamera ekleyebilirsiniz:
- Kabin 1: `http://192.168.3.210/capture`
- Kabin 2: `http://192.168.3.211/capture`
- Kabin 3: `http://192.168.3.212/capture`

---

## 📂 Veri Depolama

Tüm veriler `data/` klasöründe saklanır:

```
app/
├── data/
│   ├── cabin_db/          # Veritabanı dosyaları
│   ├── .db_seeded         # İlk kurulum bayrağı
│   └── reports/           # PDF raporlar
├── smart_cabin_desktop.py # Ana uygulama
└── backend/
    └── server.py          # API sunucusu
```

---

## ⚙️ Ayarlar ve Yapılandırma

### Telegram Bot Ayarlama

1. **Telegram'da BotFather'a gidin**: [@BotFather](https://t.me/botfather)
2. `/newbot` komutunu gönderin
3. **Bot adı ve username belirleyin**
4. **Bot Token'ı kaydedin**
5. **Uygulamada Ayarlar > Telegram bölümüne gidin**
6. **Token'ı yapıştırın ve kaydedin**

### Chat ID Alma

1. **Telegram'da botunuza mesaj gönderin**
2. **Bu URL'yi ziyaret edin:**
   ```
   https://api.telegram.org/bot[TOKEN]/getUpdates
   ```
3. **"chat":{"id": bölümündeki sayıyı kopyalayın**
4. **Uygulamada ekleyin**

---

## 🐛 Sorun Giderme

### Uygulama Açılmıyor

**Çözüm 1: Python Sürümü**
```bash
python --version  # 3.8 veya üzeri olmalı
```

**Çözüm 2: Paketleri Manuel Yükleyin**
```bash
pip install fastapi uvicorn mongita pywebview opencv-python-headless
```

**Çözüm 3: Port Kullanımda**
```bash
# 3000 ve 8001 portları kullanımda olabilir
netstat -ano | findstr :3000
netstat -ano | findstr :8001
```

### Kamera Bağlanamıyor

**Kontrol Listesi:**
- ✅ ESP32 ve bilgisayar aynı ağda mı?
- ✅ Kamera URL'si doğru mu?
- ✅ ESP32 çalışıyor mu? (test: tarayıcıda URL'yi açın)
- ✅ Firewall kamera bağlantısını engelliyor mu?

**Test Komutu:**
```bash
curl http://192.168.3.210/capture --output test.jpg
```

### Frontend Yüklenmiyor

**Çözüm:**
```bash
cd frontend
rm -rf node_modules
yarn install
# veya
npm install
```

### Veritabanı Hatası

**Sıfırlama:**
```bash
rm -rf data/cabin_db
rm data/.db_seeded
python smart_cabin_desktop.py  # Yeniden oluşturur
```

---

## 🔄 Güncelleme ve Bakım

### Uygulamayı Güncellemek
```bash
git pull origin main
python smart_cabin_desktop.py  # Otomatik paket güncellemesi
```

### Veritabanını Yedeklemek
```bash
cp -r data/cabin_db data/cabin_db_backup
```

### Veritabanını Geri Yüklemek
```bash
rm -rf data/cabin_db
cp -r data/cabin_db_backup data/cabin_db
```

---

## 📱 Telegram Komutları

Telegram botunuz bu komutları destekler:

- `/start` - Botu başlat
- `/stats` - Anlık istatistikler
- `/cabins` - Tüm kabin durumları
- `/alerts` - Son uyarılar

---

## 🎓 Kullanım Senaryoları

### Senaryo 1: İlk Kurulum
1. `python smart_cabin_desktop.py` çalıştırın
2. Paketlerin yüklenmesini bekleyin (3-5 dakika)
3. Tarayıcı/pencere otomatik açılır
4. `admin/admin123` ile giriş yapın

### Senaryo 2: Kamera Ekleme
1. Dashboard > Ayarlar
2. Kamera Yönetimi > Yeni Kamera
3. Kabin seçin, URL girin
4. Test Et > Kaydet

### Senaryo 3: Rapor Alma
1. Dashboard > Raporlar
2. Tarih aralığı seçin
3. Kabin veya öğrenci seçin
4. PDF İndir

---

## 💡 İpuçları

### Performans İyileştirme
- 🚀 **SSD kullanın**: Veritabanı erişimi daha hızlı
- 🎥 **Kamera kalitesi**: Düşük çözünürlük daha hızlı işlenir
- 💾 **RAM**: En az 4GB önerilir

### Güvenlik
- 🔐 **Şifre değiştirin**: İlk girişte admin şifresini değiştirin
- 🔒 **Firewall**: Sadece yerel ağdan erişime izin verin
- 🛡️ **Yedekleme**: Düzenli veritabanı yedeği alın

---

## 📞 Destek

**Sorun mu yaşıyorsunuz?**

1. **Log dosyalarını kontrol edin**
2. **Terminal/konsol çıktısını inceleyin**
3. **GitHub Issues açın** (varsa)
4. **Discord/Slack kanalına yazın** (varsa)

---

## 📄 Lisans

MIT License - İstediğiniz gibi kullanabilirsiniz

---

## 🎉 Hoş Geldiniz!

Artık akıllı kabin izleme sisteminiz hazır!

**Keyifli kullanımlar! 🚀**
