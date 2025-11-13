# ⚡ HIZLI BAŞLANGIÇ

## 🚀 3 Adımda Çalıştır

### 1️⃣ Gereksinimler
- ✅ Python 3.8+ ([İndir](https://www.python.org/downloads/))
- ✅ Node.js 14+ ([İndir](https://nodejs.org/))

### 2️⃣ Başlat
**Windows:**
```bash
BASLAT.bat
```
*veya*
```bash
python smart_cabin_desktop.py
```

**Linux/Mac:**
```bash
./baslat.sh
```
*veya*
```bash
python3 smart_cabin_desktop.py
```

### 3️⃣ Giriş Yap
```
Kullanıcı Adı: admin
Şifre: admin123
```

---

## 📹 ESP32 Kamera Ekleme

1. **Dashboard** → **Ayarlar**
2. **Kameralar** bölümü
3. **"Ekle"** butonuna tıkla
4. Bilgileri gir:
   ```
   Kabin No: 1
   Kamera URL: http://192.168.3.210/capture
   ```
5. **Test Et** → **Kaydet**

---

## 🔔 Telegram Bot (İsteğe Bağlı)

1. Telegram'da [@BotFather](https://t.me/botfather) aç
2. `/newbot` yaz, bot oluştur
3. **Token'ı kopyala**
4. **Dashboard** → **Ayarlar** → **Telegram**
5. Token'ı yapıştır → **Kaydet**

**Chat ID alma:**
- Botuna mesaj gönder
- Bu URL'yi aç:
  ```
  https://api.telegram.org/bot[TOKEN]/getUpdates
  ```
- `"chat":{"id":` bölümündeki sayıyı kopyala
- Dashboard'da ekle

---

## 💡 İlk Kullanım

### İlk Açılış
- ⏳ İlk açılış 3-5 dakika sürebilir (paketler yükleniyor)
- ✅ Sonraki açılışlar 10-15 saniye

### Veri Konumu
Tüm veriler `data/` klasöründe:
```
data/
├── cabin_db/     # Veritabanı
└── .db_seeded    # İlk kurulum bayrağı
```

### Yedekleme
```bash
# Windows
xcopy data data_backup /E /I

# Linux/Mac
cp -r data data_backup
```

---

## ❓ Sorun mu Yaşıyorsunuz?

### Uygulama Açılmıyor
```bash
# Python sürümü kontrol et
python --version  # 3.8+ olmalı

# Paketleri manuel yükle
cd backend
pip install -r requirements.txt

cd ../frontend
yarn install
```

### Kamera Bağlanamıyor
- ✅ ESP32 ve bilgisayar aynı ağda mı?
- ✅ URL doğru mu? (örn: `http://192.168.3.210/capture`)
- ✅ Tarayıcıda URL'yi test edin

### Port Kullanımda
```bash
# 3000 ve 8001 portları boş olmalı
# Windows
netstat -ano | findstr :3000
netstat -ano | findstr :8001

# Linux/Mac
lsof -i :3000
lsof -i :8001
```

---

## 📚 Detaylı Dokümantasyon

➡️ [MASAUSTU_KULLANIM.md](MASAUSTU_KULLANIM.md) - Tam dokümantasyon

---

## 🎉 Hazırsınız!

**Keyifli kullanımlar! 🚀**

📊 Dashboard: http://127.0.0.1:3000
📖 Dokümantasyon: MASAUSTU_KULLANIM.md
💬 Destek: [Issues](https://github.com/your-repo/issues)
