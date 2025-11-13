#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖥️ AKILLI KABİN İZLEME SİSTEMİ - MASAÜSTÜ UYGULAMASI
Tek tıkla çalışan, tüm özellikleri içeren masaüstü versiyonu
"""

import sys
import os
import threading
import time
import webbrowser
import subprocess
from pathlib import Path
import logging

# Logging ayarla
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Dizinler
BASE_DIR = Path(__file__).parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🏢  AKILLI KABİN İZLEME SİSTEMİ - MASAÜSTÜ             ║
║                                                              ║
║     📊 Dashboard | 📹 Kamera İzleme | 👥 Öğrenci Takibi    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🚀 Sistem başlatılıyor...
""")

class SmartCabinApp:
    """Ana masaüstü uygulama sınıfı"""
    
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.backend_ready = False
        self.frontend_ready = False
        
    def check_python_packages(self):
        """Backend için gerekli Python paketlerini kontrol et"""
        logger.info("📦 Python paketleri kontrol ediliyor...")
        
        # Requirements.txt varsa kullan
        requirements_file = BACKEND_DIR / "requirements.txt"
        if requirements_file.exists():
            logger.info("📝 requirements.txt bulundu, paketler kontrol ediliyor...")
            try:
                # requirements.txt'ten yükle (--user flag ile)
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", str(requirements_file), "--user", "--quiet"],
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 dakika timeout
                )
                if result.returncode == 0:
                    logger.info("✅ Tüm Python paketleri hazır")
                else:
                    logger.warning(f"⚠️  Bazı paketler yüklenemedi: {result.stderr}")
                    logger.info("💡 Python paketlerini manuel yüklemek için:")
                    logger.info(f"   pip install -r {requirements_file} --user")
            except subprocess.TimeoutExpired:
                logger.warning("⚠️  Paket yükleme zaman aşımına uğradı")
            except Exception as e:
                logger.warning(f"⚠️  Paket yükleme hatası: {e}")
        else:
            # Manuel kontrol
            logger.info("📋 Manuel paket kontrolü...")
            required_packages = [
                'fastapi', 'uvicorn', 'mongita', 'opencv-python-headless', 
                'motor', 'reportlab', 'python-telegram-bot', 'pywebview'
            ]
            
            missing = []
            for package in required_packages:
                try:
                    if package == 'opencv-python-headless':
                        __import__('cv2')
                    elif package == 'python-telegram-bot':
                        __import__('telegram')
                    else:
                        __import__(package)
                except ImportError:
                    missing.append(package)
            
            if missing:
                logger.warning(f"⚠️  Eksik paketler: {', '.join(missing)}")
                logger.info("📥 Paketler yükleniyor...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "--quiet"
                ] + missing)
                logger.info("✅ Paketler yüklendi")
            else:
                logger.info("✅ Tüm Python paketleri mevcut")
        
        return True
    
    def check_node_packages(self):
        """Frontend için Node.js paketlerini kontrol et"""
        logger.info("📦 Node.js paketleri kontrol ediliyor...")
        
        # Node.js kurulu mu kontrol et (shell=True ile Windows uyumluluğu)
        try:
            result = subprocess.run(
                "node --version", 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                raise Exception("Node.js bulunamadı")
            logger.info(f"✅ Node.js kurulu: {result.stdout.strip()}")
        except:
            logger.error("❌ Node.js bulunamadı!")
            logger.error("   Node.js kurmanız gerekiyor:")
            logger.error("   1. https://nodejs.org/ adresini ziyaret edin")
            logger.error("   2. LTS versiyonunu indirin ve kurun")
            logger.error("   3. Bilgisayarı yeniden başlatın")
            logger.error("   4. Uygulamayı tekrar çalıştırın")
            return False
        
        node_modules = FRONTEND_DIR / "node_modules"
        if not node_modules.exists():
            logger.info("📥 Frontend paketleri yükleniyor (ilk kez - 5-10 dakika sürebilir)...")
            logger.info("   ⏳ Lütfen sabırla bekleyin...")
            
            try:
                original_dir = os.getcwd()
                os.chdir(FRONTEND_DIR)
                
                # Yarn'ı kontrol et (shell=True ile)
                yarn_check = subprocess.run(
                    "yarn --version",
                    shell=True,
                    capture_output=True,
                    timeout=5
                )
                
                if yarn_check.returncode == 0:
                    # Yarn var, onu kullan
                    logger.info("✅ Yarn bulundu, paketler yükleniyor...")
                    result = subprocess.run(
                        "yarn install",
                        shell=True,
                        timeout=900,  # 15 dakika (ilk yükleme için)
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        logger.error(f"Yarn hatası: {result.stderr}")
                        raise Exception("Yarn yükleme başarısız")
                else:
                    # npm kullan (shell=True ile Windows uyumluluğu)
                    # --legacy-peer-deps flag'i ile dependency conflict'leri çöz
                    logger.info("📦 npm ile paketler yükleniyor...")
                    result = subprocess.run(
                        "npm install --legacy-peer-deps",
                        shell=True,
                        timeout=900,  # 15 dakika (ilk yükleme için)
                        capture_output=False,  # Kullanıcı ilerlemeyi görsün
                        text=True
                    )
                    if result.returncode != 0:
                        raise Exception("npm yükleme başarısız")
                
                os.chdir(original_dir)
                logger.info("✅ Frontend paketleri yüklendi")
                
            except subprocess.TimeoutExpired:
                logger.error("❌ Paket yükleme zaman aşımına uğradı")
                logger.error("   İnternet bağlantınızı kontrol edin")
                os.chdir(original_dir)
                return False
            except Exception as e:
                logger.error(f"❌ Frontend paket yükleme hatası: {e}")
                logger.error("\n💡 Manuel yükleme için Command Prompt'ta:")
                logger.error(f"   cd {FRONTEND_DIR}")
                logger.error("   npm install --legacy-peer-deps")
                logger.error("\nVeya:")
                logger.error("   npm install --force")
                os.chdir(original_dir)
                return False
        else:
            logger.info("✅ Frontend paketleri mevcut")
        
        return True
    
    def setup_local_mongodb(self):
        """Yerleşik file-based MongoDB (mongita) ayarla"""
        logger.info("🗄️  Yerel veritabanı ayarlanıyor...")
        
        # .env dosyasını oluştur/güncelle
        env_file = BACKEND_DIR / ".env"
        
        # Windows path'lerini düzelt (\ yerine /)
        data_path = str(DATA_DIR.absolute()).replace('\\', '/')
        
        env_content = f"""# Yerleşik MongoDB (Mongita) - Dosya Tabanlı
MONGO_URL=mongita:///{data_path}/cabin_db
DB_NAME=smart_cabin_db
CORS_ORIGINS=*
"""
        try:
            env_file.write_text(env_content, encoding='utf-8')
            logger.info(f"✅ .env dosyası oluşturuldu: {env_file}")
            logger.info("✅ Veritabanı yapılandırıldı")
        except Exception as e:
            logger.error(f"⚠️  .env dosyası oluşturulamadı: {e}")
            logger.warning("Devam ediliyor...")
        
        return True
    
    def seed_database_if_needed(self):
        """İlk çalıştırmada veritabanını doldur"""
        seed_flag = DATA_DIR / ".db_seeded"
        
        if not seed_flag.exists():
            logger.info("📊 Veritabanı ilk kez dolduruluyor...")
            
            # Environment variables'ı set et
            data_path = str(DATA_DIR.absolute()).replace('\\', '/')
            os.environ['MONGO_URL'] = f"mongita:///{data_path}/cabin_db"
            os.environ['DB_NAME'] = "smart_cabin_db"
            os.environ['CORS_ORIGINS'] = "*"
            
            original_dir = os.getcwd()
            os.chdir(BACKEND_DIR)
            try:
                result = subprocess.run(
                    [sys.executable, "seed_data.py"],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode == 0:
                    seed_flag.touch()
                    logger.info("✅ Veritabanı dolduruldu")
                else:
                    logger.warning(f"⚠️  Seed uyarısı: {result.stderr}")
                    logger.info("Devam ediliyor...")
            except subprocess.TimeoutExpired:
                logger.warning("⚠️  Seed zaman aşımı (devam ediliyor)")
            except Exception as e:
                logger.warning(f"⚠️  Seed hatası (devam ediliyor): {e}")
            finally:
                os.chdir(original_dir)
        else:
            logger.info("✅ Veritabanı mevcut")
        
        return True
    
    def start_backend(self):
        """Backend sunucusunu başlat"""
        logger.info("🔧 Backend başlatılıyor...")
        
        # Environment variables'ı set et
        data_path = str(DATA_DIR.absolute()).replace('\\', '/')
        os.environ['MONGO_URL'] = f"mongita:///{data_path}/cabin_db"
        os.environ['DB_NAME'] = "smart_cabin_db"
        os.environ['CORS_ORIGINS'] = "*"
        
        # Backend dizinini sys.path'e ekle
        if str(BACKEND_DIR) not in sys.path:
            sys.path.insert(0, str(BACKEND_DIR))
        
        original_dir = os.getcwd()
        os.chdir(BACKEND_DIR)
        
        # Uvicorn'u thread içinde çalıştır
        def run_backend():
            import uvicorn
            uvicorn.run(
                "server:app",
                host="127.0.0.1",
                port=8001,
                log_level="warning",
                reload=False
            )
        
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Backend'in hazır olmasını bekle
        logger.info("⏳ Backend hazırlanıyor...")
        for i in range(30):
            try:
                import requests
                response = requests.get("http://127.0.0.1:8001/api/stats", timeout=1)
                if response.status_code in [200, 401, 403]:  # API çalışıyor (auth gerekli ama hazır)
                    self.backend_ready = True
                    logger.info("✅ Backend hazır (http://127.0.0.1:8001)")
                    break
            except:
                time.sleep(1)
        
        os.chdir(original_dir)
        
        if not self.backend_ready:
            logger.warning("⚠️  Backend başlatılamadı, devam ediliyor...")
        
        return self.backend_ready
    
    def start_frontend(self):
        """Frontend sunucusunu başlat"""
        logger.info("🎨 Frontend başlatılıyor...")
        
        original_dir = os.getcwd()
        os.chdir(FRONTEND_DIR)
        
        # .env.local dosyasını oluştur
        env_file = FRONTEND_DIR / ".env.local"
        env_content = """REACT_APP_BACKEND_URL=http://127.0.0.1:8001
PORT=3000
BROWSER=none
"""
        env_file.write_text(env_content)
        
        # React development server'ı başlat (shell=True ile Windows uyumluluğu)
        try:
            # Yarn varsa yarn kullan
            yarn_check = subprocess.run(
                "yarn --version",
                shell=True,
                capture_output=True,
                timeout=5
            )
            
            if yarn_check.returncode == 0:
                logger.info("📦 Yarn ile frontend başlatılıyor...")
                self.frontend_process = subprocess.Popen(
                    "yarn start",
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                # npm kullan
                logger.info("📦 npm ile frontend başlatılıyor...")
                self.frontend_process = subprocess.Popen(
                    "npm start",
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
        except Exception as e:
            logger.error(f"❌ Frontend başlatma hatası: {e}")
            os.chdir(original_dir)
            return False
        
        # Frontend'in hazır olmasını bekle
        logger.info("⏳ Frontend hazırlanıyor (20-30 saniye)...")
        for i in range(60):
            try:
                import requests
                response = requests.get("http://127.0.0.1:3000", timeout=1)
                if response.status_code == 200:
                    self.frontend_ready = True
                    logger.info("✅ Frontend hazır (http://127.0.0.1:3000)")
                    break
            except Exception as e:
                if i % 5 == 0:  # Her 5 saniyede bir durum göster
                    logger.debug(f"Frontend bekleniyor... ({i} saniye)")
                time.sleep(1)
        
        os.chdir(original_dir)
        
        if not self.frontend_ready:
            logger.warning("⚠️  Frontend başlatılamadı (timeout)")
            logger.info("💡 Frontend manuel başlatmak için:")
            logger.info(f"   cd {FRONTEND_DIR}")
            logger.info("   npm start")
            return False
        
        return True
    
    def open_app(self):
        """Uygulamayı aç"""
        logger.info("🌐 Uygulama açılıyor...")
        
        try:
            # pywebview ile native pencere aç
            import webview
            
            logger.info("✅ Native masaüstü penceresi açılıyor...")
            webview.create_window(
                title="🏢 Akıllı Kabin İzleme Sistemi",
                url="http://127.0.0.1:3000",
                width=1400,
                height=900,
                resizable=True,
                fullscreen=False,
                min_size=(1200, 800)
            )
            webview.start()
            
        except ImportError:
            # pywebview yoksa tarayıcıda aç
            logger.info("✅ Tarayıcıda açılıyor...")
            time.sleep(2)
            webbrowser.open("http://127.0.0.1:3000")
            
            # Kullanıcıya bilgi ver
            print("""
═══════════════════════════════════════════════════════════════
✅ SİSTEM ÇALIŞIYOR!
═══════════════════════════════════════════════════════════════

📊 Dashboard: http://127.0.0.1:3000
🔐 Giriş Bilgileri:
   Kullanıcı Adı: admin
   Şifre: admin123

📹 Kamera URL: http://192.168.3.210/capture
   (Ayarlar sayfasından kamerayı ekleyin)

⚠️  ÖNEMLİ: Bu pencereyi kapatmayın!
   Kapatırsanız sistem durur.

🛑 Durdurmak için: CTRL+C tuşlarına basın
═══════════════════════════════════════════════════════════════
""")
            
            # Sonsuz döngü - çalışmaya devam et
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("\n⏹️  Durdurma komutu alındı...")
    
    def cleanup(self):
        """Temizlik işlemleri"""
        logger.info("\n🛑 Sistem kapatılıyor...")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
            except:
                self.frontend_process.kill()
        
        logger.info("✅ Temizlik tamamlandı")
    
    def run(self):
        """Uygulamayı çalıştır"""
        try:
            # 1. Paket kontrolleri
            self.check_python_packages()
            
            if not self.check_node_packages():
                logger.error("\n❌ Frontend paketleri yüklenemedi!")
                logger.error("   Uygulama çalıştırılamıyor.")
                logger.error("\n💡 Yukarıdaki hata mesajlarını kontrol edin.")
                return False
            
            # 2. Veritabanı ayarla
            self.setup_local_mongodb()
            self.seed_database_if_needed()
            
            # 3. Backend başlat
            self.start_backend()
            
            # 4. Frontend başlat
            if not self.start_frontend():
                logger.error("❌ Frontend başlatılamadı!")
                return False
            
            # 5. Uygulamayı aç
            self.open_app()
            
            return True
            
        except KeyboardInterrupt:
            logger.info("\n⏹️  Kullanıcı tarafından durduruldu")
        except Exception as e:
            logger.error(f"\n❌ Hata: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
            logger.info("👋 Güle güle!\n")
        
        return False


def main():
    """Ana fonksiyon"""
    app = SmartCabinApp()
    
    # Windows'ta console encoding'i UTF-8 yap
    if sys.platform == 'win32':
        try:
            import locale
            if locale.getpreferredencoding() != 'UTF-8':
                sys.stdout.reconfigure(encoding='utf-8')
                sys.stderr.reconfigure(encoding='utf-8')
        except:
            pass
    
    success = app.run()
    
    if not success:
        input("\nHata oluştu. Çıkmak için Enter'a basın...")
        sys.exit(1)


if __name__ == "__main__":
    main()
