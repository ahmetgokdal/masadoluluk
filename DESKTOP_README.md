# 🖥️ Akıllı Kabin İzleme Sistemi - Masaüstü Uygulaması

## 📋 Gereksinimler

### Yazılım
- **Node.js 18+** https://nodejs.org/
- **Python 3.11** https://www.python.org/downloads/
- **MongoDB Community** https://www.mongodb.com/try/download/community
- **Yarn** (npm install -g yarn)

### Donanım  
- ESP32-CAM cihazları (kamera URL'leri)

---

## 🚀 Kurulum Adımları

### 1️⃣ Projeyi İndir
```bash
# ZIP olarak indir veya
git clone <repository-url>
cd <proje-klasörü>
```

### 2️⃣ MongoDB'yi Başlat
```bash
# Windows
net start MongoDB

# Mac/Linux
sudo systemctl start mongod
# veya
brew services start mongodb-community
```

### 3️⃣ Backend Kurulumu
```bash
cd backend
pip install -r requirements.txt
python seed_data.py  # Veritabanını doldur
```

### 4️⃣ Frontend Kurulumu
```bash
cd frontend
yarn install
```

---

## ▶️ Çalıştırma

### Geliştirme Modu (Development)
```bash
cd frontend
yarn electron-dev
```

Bu komut:
- React dev server'ı başlatır (http://localhost:3000)
- Backend'i başlatır (http://localhost:8001)
- Electron penceresi açar
- Hot reload aktif

### Production Build (Çalıştırılabilir Dosya)

#### Windows için
```bash
cd frontend
yarn electron-build-win
```
Çıktı: `frontend/dist/Akıllı Kabin İzleme Sistemi Setup.exe`

#### Mac için
```bash
cd frontend
yarn electron-build-mac
```
Çıktı: `frontend/dist/Akıllı Kabin İzleme Sistemi.dmg`

#### Linux için
```bash
cd frontend
yarn electron-build-linux
```
Çıktı: `frontend/dist/Akıllı Kabin İzleme Sistemi.AppImage`

---

## 🔐 Giriş Bilgileri

**Varsayılan kullanıcı:**
- Kullanıcı Adı: `admin`
- Şifre: `admin123`

---

## ⚙️ Yapılandırma

### Kamera Ekleme
1. Uygulamaya giriş yapın
2. **Ayarlar** → **Kamera Yapılandırması**
3. **Kamera Ekle** butonuna tıklayın
4. Kabin numarası ve kamera URL'sini girin
   - Örnek: http://192.168.3.210/capture

### Telegram Bot Kurulumu
1. @BotFather ile Telegram bot oluşturun
2. Bot token'ı alın
3. **Ayarlar** → **Telegram Ayarları**
4. Bot token'ı girin ve kaydedin

### Öğrenci Atama
1. **Öğrenciler** sayfasına gidin
2. Kabin kartındaki **Düzenle** butonuna tıklayın
3. Öğrenci ID ve adını girin

---

## 📁 Proje Yapısı

```
project/
├── frontend/                    # React + Electron
│   ├── public/
│   │   └── electron.js         # Electron main process
│   ├── src/
│   │   ├── pages/              # Dashboard, Reports, etc.
│   │   ├── components/         # UI components
│   │   ├── services/           # API & WebSocket
│   │   └── mock.js             # Mock data (fallback)
│   └── package.json
│
├── backend/                     # FastAPI
│   ├── server.py               # Ana server
│   ├── models.py               # Pydantic models
│   ├── auth.py                 # Authentication
│   ├── tracker_service.py      # Real-time tracking
│   ├── telegram_bot.py         # Telegram integration
│   ├── seed_data.py            # Database seeding
│   └── requirements.txt
│
└── README.md
```

---

## 🔄 Güncelleme

Kod değişiklikleri yaptığınızda:

### Geliştirme sırasında
- Değişiklikler otomatik yüklenir (hot reload)
- Electron penceresi açık kalır

### Yeni build için
```bash
cd frontend
yarn electron-build-win  # veya mac/linux
```

---

## 🐛 Sorun Giderme

### Backend Başlamıyor
```bash
# Log kontrol et
cd backend
python -m uvicorn server:app --host 127.0.0.1 --port 8001
```

### MongoDB Bağlantı Hatası
```bash
# MongoDB çalışıyor mu?
mongosh --eval "db.version()"

# Başlat
sudo systemctl start mongod
```

### Electron Penceresi Açılmıyor
```bash
# Node modules'ü temizle
cd frontend
rm -rf node_modules
yarn install
yarn electron-dev
```

### Kamera Görüntüsü Gelmiyor
- ESP32-CAM'in network'te olduğundan emin olun
- URL'i tarayıcıda test edin
- IP adresini kontrol edin

---

## 📊 Özellikler

✅ **Gerçek Zamanlı İzleme**
- WebSocket ile anlık güncelleme
- Kabin durumu değişiklikleri (active/idle/long_break)
- Session tracking

✅ **Raporlama**
- Günlük / Haftalık / Aylık raporlar
- PDF export (yakında)
- Telegram otomatik gönderim

✅ **Öğrenci Yönetimi**
- Kabine öğrenci atama
- Performans takibi
- Aktivite grafikleri

✅ **Masaüstü Özellikleri**
- Tek çalıştırılabilir dosya
- Otomatik backend başlatma
- Sistem tray icon (yakında)
- Otomatik güncelleme (yakında)

---

## 🔒 Güvenlik

- Kullanıcı şifrelerini değiştirin (production için)
- MongoDB authentication açın
- Firewall kuralları ayarlayın
- HTTPS kullanın (uzaktan erişim için)

---

## 📞 Destek

Sorularınız için:
- GitHub Issues
- Email: support@cabin-system.com

---

## 📝 Lisans

Bu proje özel kullanım içindir.

---

**🎉 İyi Kullanımlar!**
