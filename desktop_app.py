#!/usr/bin/env python3
"""
Akıllı Kabin İzleme Sistemi - Desktop Uygulaması
Tek dosya - Her şey burada!
"""
import sys
import os
import subprocess
import time
import webbrowser
from pathlib import Path

print("""
╔═══════════════════════════════════════════════════════════╗
║   🖥️  AKILLI KABİN İZLEME SİSTEMİ - MASAÜSTÜ           ║
╚═══════════════════════════════════════════════════════════╝
""")

# Dizinler
BASE_DIR = Path(__file__).parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"

# Process'leri sakla
processes = []

def check_dependencies():
    """Gerekli programları kontrol et"""
    print("📦 Gereksinimler kontrol ediliyor...")
    
    # MongoDB
    try:
        subprocess.run(["mongod", "--version"], capture_output=True, check=True)
        print("  ✅ MongoDB kurulu")
    except:
        print("  ⚠️  MongoDB bulunamadı")
        print("     https://www.mongodb.com/try/download/community adresinden kurun")
        return False
    
    # Node.js
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
        print("  ✅ Node.js kurulu")
    except:
        print("  ⚠️  Node.js bulunamadı")
        print("     https://nodejs.org adresinden kurun")
        return False
    
    # Python packages
    try:
        import fastapi
        import uvicorn
        import motor
        import cv2
        print("  ✅ Python paketleri kurulu")
    except ImportError as e:
        print(f"  ⚠️  Python paketi eksik: {e}")
        print("     backend klasöründe: pip install -r requirements.txt")
        return False
    
    return True

def start_mongodb():
    """MongoDB'yi başlat"""
    print("\n🗄️  MongoDB başlatılıyor...")
    try:
        # Windows'ta MongoDB genelde servis olarak çalışır
        result = subprocess.run(
            ["sc", "query", "MongoDB"], 
            capture_output=True, 
            text=True,
            shell=True
        )
        if "RUNNING" in result.stdout:
            print("  ✅ MongoDB zaten çalışıyor")
            return True
        else:
            # Servisi başlat
            subprocess.run(["net", "start", "MongoDB"], shell=True)
            time.sleep(2)
            print("  ✅ MongoDB başlatıldı")
            return True
    except Exception as e:
        print(f"  ⚠️  MongoDB başlatılamadı: {e}")
        print("     Manuel başlatın: net start MongoDB")
        return False

def start_backend():
    """Backend server'ı başlat"""
    print("\n🔧 Backend başlatılıyor...")
    
    os.chdir(BACKEND_DIR)
    
    # Veritabanını seed et (ilk kez)
    seed_file = BACKEND_DIR / ".seeded"
    if not seed_file.exists():
        print("  📊 Veritabanı ilk kez dolduruluyor...")
        subprocess.run([sys.executable, "seed_data.py"])
        seed_file.touch()
    
    # Uvicorn başlat
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "server:app", 
         "--host", "127.0.0.1", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    processes.append(process)
    
    print("  ⏳ Backend hazırlanıyor...")
    time.sleep(5)
    print("  ✅ Backend çalışıyor (http://127.0.0.1:8001)")
    
    os.chdir(BASE_DIR)
    return process

def start_frontend():
    """Frontend'i başlat"""
    print("\n🎨 Frontend başlatılıyor...")
    
    os.chdir(FRONTEND_DIR)
    
    # yarn install (ilk kez)
    node_modules = FRONTEND_DIR / "node_modules"
    if not node_modules.exists():
        print("  📦 Paketler yükleniyor (ilk kez - 2-3 dakika)...")
        subprocess.run(["yarn", "install"], shell=True)
    
    # .env.local oluştur
    env_file = FRONTEND_DIR / ".env.local"
    env_content = """REACT_APP_BACKEND_URL=http://127.0.0.1:8001
PORT=3000
BROWSER=none
"""
    env_file.write_text(env_content)
    
    # React başlat
    process = subprocess.Popen(
        ["yarn", "start"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    processes.append(process)
    
    print("  ⏳ Frontend hazırlanıyor...")
    time.sleep(10)
    print("  ✅ Frontend çalışıyor (http://127.0.0.1:3000)")
    
    os.chdir(BASE_DIR)
    return process

def open_browser():
    """Tarayıcıda aç"""
    print("\n🌐 Tarayıcı açılıyor...")
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:3000")
    print("  ✅ Uygulama açıldı!")

def cleanup():
    """Temizlik - process'leri kapat"""
    print("\n\n🛑 Uygulama kapatılıyor...")
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
    print("  ✅ Temizlik tamamlandı")

def main():
    """Ana fonksiyon"""
    try:
        # Kontroller
        if not check_dependencies():
            print("\n❌ Gereksinimler karşılanmadı!")
            input("Çıkmak için Enter'a basın...")
            sys.exit(1)
        
        # MongoDB başlat
        if not start_mongodb():
            print("\n⚠️  MongoDB olmadan devam ediliyor...")
        
        # Backend başlat
        start_backend()
        
        # Frontend başlat
        start_frontend()
        
        # Tarayıcıda aç
        open_browser()
        
        # Bilgi
        print("\n" + "="*60)
        print("✅ SİSTEM ÇALIŞIYOR!")
        print("="*60)
        print("""
📊 Dashboard: http://127.0.0.1:3000
🔐 Giriş: admin / admin123
📹 Kamera URL: http://192.168.3.210/capture (lokal network)

⚠️  BU PENCEREYI KAPATMAYIN!
    Kapatırsanız sistem durur.

🛑 Durdurmak için: CTRL+C
        """)
        
        # Sonsuz döngü - çalışmaya devam et
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Durdurma komutu alındı...")
    except Exception as e:
        print(f"\n\n❌ HATA: {e}")
    finally:
        cleanup()
        print("\n👋 Güle güle!")
        input("Çıkmak için Enter'a basın...")

if __name__ == "__main__":
    main()
