# 🖥️ Akıllı Kabin İzleme Sistemi - Masaüstü Uygulaması

> ESP32 kameralar ile gerçek zamanlı kabin izleme, öğrenci takibi ve otomatik raporlama sistemi

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Özellikler

### 🏢 Kabin Yönetimi
- **50 Kabin Desteği**: Tüm kabinleri tek ekrandan yönetin
- **Gerçek Zamanlı Durum**: Active, Idle, Long Break, Empty
- **Otomatik Tespitü: Yapay zeka ile doluluk analizi

### 📹 Kamera Entegrasyonu
- **ESP32 Kamera Desteği**: Lokal ağdan doğrudan erişim
- **Canlı Görüntü**: Real-time video stream
- **Hareket Algılama**: OpenCV tabanlı

### 👥 Öğrenci Takibi
- **Oturum Yönetimi**: Başlangıç/bitiş zamanları
- **Süre Hesaplama**: Otomatik session tracking
- **Aktivite Geçmişi**: Detaylı kayıtlar

### 📊 Raporlama
- **PDF Raporlar**: Tarih aralığına göre
- **Öğrenci Bazlı**: Bireysel performans
- **Kabin Bazlı**: Doluluk istatistikleri

### 🔔 Bildirimler
- **Telegram Entegrasyonu**: Anlık uyarılar
- **Haftalık Raporlar**: Otomatik gönderim
- **Özel Uyarılar**: Long break, inactivity vb.

### 💾 Yerleşik Veritabanı
- **MongoDB Gerektirmez**: File-based Mongita
- **Kolay Yedekleme**: Tek klasör kopyalama
- **Taşınabilir**: Tüm veriler `data/` klasöründe

---

## 🚀 Hızlı Başlangıç

### Tek Komutla Çalıştır

**Windows:**
```bash
BASLAT.bat
```

**Linux/Mac:**
```bash
./baslat.sh
```

### Manuel Başlatma
```bash
python smart_cabin_desktop.py
```

**İlk Açılış:**
- ⏳ 3-5 dakika (otomatik paket kurulumu)
- ✅ Sonraki açılışlar: 10-15 saniye

---

## 📋 Gereksinimler

### Yazılım
- **Python 3.8+** - [İndir](https://www.python.org/downloads/)
- **Node.js 14+** - [İndir](https://nodejs.org/)

### Donanım (Önerilen)
- **RAM**: 4GB+
- **Disk**: 500MB (sistem + veri)
- **İşlemci**: Dual-core 2GHz+

---

## 📖 Dokümantasyon

| Dosya | İçerik |
|-------|--------|
| [HIZLI_BASLANGIC.md](HIZLI_BASLANGIC.md) | ⚡ 3 adımda başlangıç |
| [MASAUSTU_KULLANIM.md](MASAUSTU_KULLANIM.md) | 📚 Detaylı kullanım kılavuzu |
| [README_DESKTOP.md](README_DESKTOP.md) | 📖 Bu dosya |

---

## 🔐 Varsayılan Giriş

```
Kullanıcı Adı: admin
Şifre: admin123
```

> ⚠️ İlk girişte şifrenizi değiştirin!

---

## 📂 Proje Yapısı

```
smart-cabin-monitoring/
├── smart_cabin_desktop.py      # 🚀 Ana uygulama
├── BASLAT.bat                  # Windows başlatıcı
├── baslat.sh                   # Linux/Mac başlatıcı
│
├── backend/                    # FastAPI backend
│   ├── server.py              # API endpoints
│   ├── tracker_service.py     # Kabin takip servisi
│   ├── camera_detector.py     # Kamera & AI
│   ├── telegram_bot.py        # Telegram entegrasyonu
│   ├── auth.py                # Kimlik doğrulama
│   ├── models.py              # Veri modelleri
│   ├── db_connector.py        # Veritabanı (Mongita)
│   ├── seed_data.py           # İlk veri
│   └── requirements.txt       # Python paketleri
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # UI bileşenleri
│   │   ├── pages/            # Dashboard, Settings, vb.
│   │   └── services/         # API & WebSocket
│   └── package.json          # Node.js paketleri
│
└── data/                       # Uygulama verisi
    ├── cabin_db/              # Mongita veritabanı
    └── .db_seeded             # İlk kurulum bayrağı
```

---

## 🎯 Kullanım Senaryoları

### 1️⃣ İlk Kurulum ve Başlatma
```bash
# 1. Uygulamayı başlat
python smart_cabin_desktop.py

# 2. Paketlerin yüklenmesini bekle (3-5 dk)
# 3. Tarayıcı/pencere otomatik açılır
# 4. admin/admin123 ile giriş yap
```

### 2️⃣ ESP32 Kamera Ekleme
```bash
# Dashboard → Ayarlar → Kameralar
# 1. "Ekle" butonuna tıkla
# 2. Bilgileri gir:
#    - Kabin No: 1
#    - URL: http://192.168.3.210/capture
# 3. "Test Et" ile kontrol
# 4. Kaydet
```

### 3️⃣ Telegram Bot Kurulumu
```bash
# 1. @BotFather ile bot oluştur
# 2. Token'ı kopyala
# 3. Dashboard → Ayarlar → Telegram
# 4. Token'ı yapıştır
# 5. Chat ID ekle
```

### 4️⃣ Rapor Alma
```bash
# Dashboard → Raporlar
# 1. Tarih aralığı seç
# 2. Kabin veya öğrenci seç
# 3. PDF İndir
```

---

## 🔧 Yapılandırma

### Veritabanı
Tüm veriler `data/cabin_db/` klasöründe saklanır (Mongita - file-based).

**Yedekleme:**
```bash
# Windows
xcopy data data_backup /E /I

# Linux/Mac
cp -r data data_backup
```

**Sıfırlama:**
```bash
rm -rf data/cabin_db
rm data/.db_seeded
python smart_cabin_desktop.py  # Yeniden oluşturur
```

### Portlar
- **Frontend**: 3000
- **Backend**: 8001

Değiştirmek için `smart_cabin_desktop.py` dosyasını düzenleyin.

---

## 🐛 Sorun Giderme

### Uygulama Açılmıyor

**Python sürümü kontrolü:**
```bash
python --version  # 3.8+ olmalı
```

**Paketleri manuel yükle:**
```bash
cd backend
pip install -r requirements.txt

cd ../frontend
yarn install
```

### Kamera Bağlanamıyor

**Kontrol listesi:**
- ✅ ESP32 ve bilgisayar aynı WiFi ağında mı?
- ✅ Kamera URL'si doğru mu?
- ✅ ESP32 çalışıyor mu?

**Test:**
```bash
# Tarayıcıda aç
http://192.168.3.210/capture

# veya curl ile test et
curl http://192.168.3.210/capture --output test.jpg
```

### Port Zaten Kullanımda

**Windows:**
```bash
netstat -ano | findstr :3000
netstat -ano | findstr :8001
# Process ID'yi öğren ve kapat
taskkill /PID [PID] /F
```

**Linux/Mac:**
```bash
lsof -i :3000
lsof -i :8001
# Process'i kapat
kill -9 [PID]
```

### Frontend Yüklenmiyor

```bash
cd frontend
rm -rf node_modules
yarn install
# veya
npm install
```

---

## 🛠️ Geliştirme

### Backend Geliştirme
```bash
cd backend
python -m uvicorn server:app --reload --host 127.0.0.1 --port 8001
```

### Frontend Geliştirme
```bash
cd frontend
yarn start
```

### Test
```bash
# Backend test
python test_desktop_backend.py

# Mongita test
python test_mongita.py
```

---

## 📦 Paket Listesi

### Python (Backend)
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Mongita** - File-based MongoDB
- **OpenCV** - Görüntü işleme
- **ReportLab** - PDF oluşturma
- **python-telegram-bot** - Telegram API

### JavaScript (Frontend)
- **React** - UI framework
- **TailwindCSS** - Styling
- **Axios** - HTTP client
- **Chart.js** - Grafikler

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz!

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing`)
5. Pull Request açın

---

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🙏 Teşekkürler

- **FastAPI** - Modern Python web framework
- **React** - Kullanıcı arayüzü
- **Mongita** - Embedded MongoDB
- **OpenCV** - Bilgisayarlı görü
- **Tüm katkıda bulunanlara** ❤️

---

## 📞 İletişim & Destek

- 🐛 **Bug Raporları**: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 **Sorularınız**: [Discussions](https://github.com/your-repo/discussions)
- 📧 **Email**: support@yourproject.com

---

<div align="center">

**Akıllı Kabin İzleme Sistemi**

Yapımcılar ile ❤️

🚀 [Demo](https://demo.yourproject.com) • 
📖 [Dokümantasyon](https://docs.yourproject.com) • 
💬 [Destek](https://support.yourproject.com)

</div>
