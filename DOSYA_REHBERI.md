# 📂 DOSYA REHBERİ - Hangi Dosya Ne İşe Yarar?

## 🎯 ÖNEMLİ DOSYALAR (Mutlaka İndirilmeli)

### 🚀 Başlatma Dosyaları
| Dosya | Ne İşe Yarar | Platform |
|-------|--------------|----------|
| **BASLAT.bat** | Çift tıkla çalıştır | ✅ Windows |
| **baslat.sh** | Terminal'den çalıştır | ✅ Mac/Linux |
| **smart_cabin_desktop.py** | Ana uygulama kodu | ✅ Tüm platformlar |

### 📚 Dokümantasyon Dosyaları
| Dosya | İçerik | Ne Zaman Kullan |
|-------|--------|-----------------|
| **ADIM_ADIM.txt** | Görsel adım adım rehber | İlk kurulum |
| **KURULUM_REHBERI.md** | Detaylı kurulum talimatları | İlk kurulum |
| **HIZLI_BASLANGIC.md** | 3 adımda başlangıç | Hızlı başlama |
| **MASAUSTU_KULLANIM.md** | Tam kullanım kılavuzu | Kullanım sırasında |
| **README_DESKTOP.md** | Proje genel bilgileri | Genel bakış |

### 🔧 Backend Dosyaları (backend/ klasörü)
| Dosya | Ne İşe Yarar |
|-------|--------------|
| **server.py** | API endpoints (giriş, stats, kabinler) |
| **db_connector.py** | Veritabanı bağlantısı (Mongita) |
| **tracker_service.py** | Kabin takip servisi |
| **camera_detector.py** | Kamera görüntü işleme (OpenCV) |
| **telegram_bot.py** | Telegram bildirimleri |
| **auth.py** | Kullanıcı girişi |
| **models.py** | Veri modelleri |
| **seed_data.py** | İlk veri oluşturma |
| **requirements.txt** | Python paket listesi |

### 🎨 Frontend Dosyaları (frontend/ klasörü)
| Dosya/Klasör | Ne İşe Yarar |
|--------------|--------------|
| **src/** | React uygulama kodları |
| **src/pages/** | Dashboard, Login, Settings sayfaları |
| **src/components/** | UI bileşenleri |
| **src/services/** | API ve WebSocket |
| **public/** | Statik dosyalar |
| **package.json** | Node.js paket listesi |

---

## 📦 İNDİRME ÖNCESİ KONTROL LİSTESİ

Şu dosyaların ve klasörlerin olduğundan emin olun:

### ✅ Kök Dizinde Olması Gerekenler:
```
smart-cabin-monitoring/
├── ✅ BASLAT.bat                 (Windows başlatıcı)
├── ✅ baslat.sh                  (Mac/Linux başlatıcı)
├── ✅ smart_cabin_desktop.py    (Ana uygulama)
├── ✅ ADIM_ADIM.txt              (Kurulum rehberi)
├── ✅ KURULUM_REHBERI.md         (Detaylı kurulum)
├── ✅ HIZLI_BASLANGIC.md         (Hızlı başlangıç)
├── ✅ MASAUSTU_KULLANIM.md       (Kullanım kılavuzu)
├── ✅ backend/                   (Backend klasörü)
└── ✅ frontend/                  (Frontend klasörü)
```

### ✅ backend/ Klasöründe Olması Gerekenler:
```
backend/
├── ✅ server.py
├── ✅ db_connector.py
├── ✅ tracker_service.py
├── ✅ camera_detector.py
├── ✅ telegram_bot.py
├── ✅ auth.py
├── ✅ models.py
├── ✅ seed_data.py
└── ✅ requirements.txt
```

### ✅ frontend/ Klasöründe Olması Gerekenler:
```
frontend/
├── ✅ src/
├── ✅ public/
├── ✅ package.json
└── ✅ tailwind.config.js
```

---

## 🚫 İNDİRMENİZE GEREK OLMAYAN DOSYALAR

Bu dosyalar test ve geliştirme için kullanıldı, indirmenize gerek yok:

❌ **test_desktop_backend.py** - Test dosyası
❌ **test_mongita.py** - Test dosyası
❌ **test_result.md** - Test sonuçları
❌ **desktop_app.py** - Eski versiyon
❌ **camera_proxy.py** - Kullanılmıyor
❌ **START_APP.py** - Eski başlatıcı
❌ **data/** klasörü - Otomatik oluşturulur
❌ **node_modules/** - Otomatik yüklenecek
❌ **.git/** - Git deposu
❌ **.ruff_cache/** - Cache dosyaları

---

## 📋 DOSYA BOYUTLARI VE İNDİRME SÜRESİ

### Toplam Boyut (Gerekli Dosyalar):
- **Backend:** ~50 KB (Python kodları)
- **Frontend:** ~200 KB (React kodları, node_modules hariç)
- **Dokümantasyon:** ~50 KB
- **TOPLAM:** ~300 KB

### İndirme Sonrası (Paketler Yüklendikten Sonra):
- **node_modules:** ~200 MB
- **Python paketleri:** ~500 MB
- **Toplam disk kullanımı:** ~1 GB

---

## 🗂️ KLASÖR YAPISI (Kurulumdan Sonra)

```
smart-cabin-monitoring/
│
├── 📄 BASLAT.bat                    ← Windows başlatıcı
├── 📄 baslat.sh                     ← Mac/Linux başlatıcı
├── 📄 smart_cabin_desktop.py        ← Ana uygulama
│
├── 📚 ADIM_ADIM.txt                 ← Kurulum rehberi
├── 📚 KURULUM_REHBERI.md
├── 📚 HIZLI_BASLANGIC.md
├── 📚 MASAUSTU_KULLANIM.md
├── 📚 README_DESKTOP.md
│
├── 🔧 backend/                      ← Backend kodları
│   ├── server.py                   (API endpoints)
│   ├── db_connector.py             (Veritabanı)
│   ├── tracker_service.py          (Kabin takip)
│   ├── camera_detector.py          (Kamera AI)
│   ├── telegram_bot.py             (Telegram)
│   ├── auth.py                     (Giriş sistemi)
│   ├── models.py                   (Veri modelleri)
│   ├── seed_data.py                (İlk veri)
│   └── requirements.txt            (Python paketleri)
│
├── 🎨 frontend/                     ← Frontend kodları
│   ├── src/                        (React kodları)
│   │   ├── pages/                 (Sayfalar)
│   │   ├── components/            (Bileşenler)
│   │   └── services/              (API çağrıları)
│   ├── public/                     (Statik dosyalar)
│   └── package.json                (Node.js paketleri)
│
└── 💾 data/                         ← Otomatik oluşturulur
    ├── cabin_db/                   (Mongita veritabanı)
    └── .db_seeded                  (İlk kurulum bayrağı)
```

---

## 🎯 HIZLI BAŞLANGIÇ İÇİN MİNİMAL DOSYALAR

Sadece çalıştırmak için bu dosyaların olması yeterli:

```
MİNİMAL SETİ:
✅ smart_cabin_desktop.py
✅ BASLAT.bat (veya baslat.sh)
✅ backend/ (tüm dosyalar)
✅ frontend/ (tüm dosyalar)
```

Dokümantasyon dosyaları isteğe bağlıdır.

---

## 💡 İPUÇLARI

### Windows Kullanıcıları:
1. **BASLAT.bat** dosyasına çift tıklayın
2. İlk açılış 3-5 dakika sürer
3. Pencereyi KAPATMAYIN

### Mac/Linux Kullanıcıları:
1. Terminal'de: `./baslat.sh`
2. İlk açılış 3-5 dakika sürer
3. Terminal'i KAPATMAYIN

### İlk Kurulum:
- İnternet bağlantısı gerekli (paket indirme için)
- Python 3.8+ ve Node.js 14+ kurulu olmalı

### Sonraki Açılışlar:
- 10-15 saniye sürer ⚡
- İnternet gerekmez (lokal çalışır)

---

## 📞 YARDIM

Dosyalarla ilgili sorun yaşıyorsanız:

1. **ADIM_ADIM.txt** dosyasını okuyun
2. **KURULUM_REHBERI.md** dosyasına bakın
3. Bana soru sorun!

---

## ✅ KONTROL LİSTESİ

İndirme öncesi:
- [ ] Python 3.8+ kurulu mu?
- [ ] Node.js 14+ kurulu mu?
- [ ] Yeterli disk alanı var mı? (1 GB)

İndirme sonrası:
- [ ] BASLAT.bat dosyası var mı?
- [ ] backend/ klasörü var mı?
- [ ] frontend/ klasörü var mı?
- [ ] smart_cabin_desktop.py var mı?

Başarılar! 🚀
