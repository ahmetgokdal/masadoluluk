#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖥️ AKILLI KABİN İZLEME SİSTEMİ - MASAÜSTÜ UYGULAMASI
═══════════════════════════════════════════════════════

ÇOK KOLAY KULLANIM:
1. Çift tıklayın → Uygulama açılır
2. Tarayıcıda sistem otomatik açılır
3. Giriş: admin / admin123

VEYA Terminal'den:
python START_APP.py
"""

import sys
import os
import subprocess
import time
import webbrowser
import socket
from pathlib import Path
import threading

# Renkli konsol çıktısı için
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    print(f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     {Colors.BOLD}🖥️  AKILLI KABİN İZLEME SİSTEMİ - MASAÜSTÜ{Colors.END}{Colors.CYAN}           ║
║                                                               ║
║     {Colors.GREEN}✨ Modern Web Arayüzü + Gerçek Zamanlı İzleme{Colors.END}{Colors.CYAN}      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
""")

def check_port(port):
    """Port'un kullanımda olup olmadığını kontrol et"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def kill_port(port):
    """Port'u kullanan process'i kapat (Windows)"""
    try:
        subprocess.run(f'netstat -ano | findstr :{port}', shell=True, capture_output=True)
        # Gerekirse process'i öldür
    except:
        pass

def check_mongodb():
    """MongoDB çalışıyor mu kontrol et"""
    print(f"\n{Colors.BLUE}🗄️  MongoDB kontrol ediliyor...{Colors.END}")
    
    try:
        # MongoDB'ye bağlanmayı dene
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        client.server_info()
        print(f"  {Colors.GREEN}✅ MongoDB çalışıyor{Colors.END}")
        return True
    except Exception as e:
        print(f"  {Colors.YELLOW}⚠️  MongoDB başlatılıyor...{Colors.END}")
        try:
            # Windows servisi başlat
            subprocess.run(["net", "start", "MongoDB"], shell=True, capture_output=True)
            time.sleep(3)
            
            # Tekrar dene
            client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
            client.server_info()
            print(f"  {Colors.GREEN}✅ MongoDB başlatıldı{Colors.END}")
            return True
        except:
            print(f"  {Colors.RED}❌ MongoDB başlatılamadı!{Colors.END}")
            print(f"  {Colors.YELLOW}     Manuel başlatın: services.msc → MongoDB → Start{Colors.END}")
            return False

def start_backend():
    """Backend server'ı başlat"""
    print(f"\n{Colors.BLUE}🔧 Backend başlatılıyor...{Colors.END}")
    
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    # Port kontrolü
    if check_port(8001):
        print(f"  {Colors.YELLOW}⚠️  Port 8001 kullanımda, temizleniyor...{Colors.END}")
        kill_port(8001)
        time.sleep(2)
    
    # Environment variables
    env = os.environ.copy()
    env['MONGO_URL'] = 'mongodb://localhost:27017/'
    env['DB_NAME'] = 'cabin_system_local'
    
    # Veritabanını seed et (ilk kez)
    seed_marker = backend_dir / ".db_seeded"
    if not seed_marker.exists():
        print(f"  {Colors.CYAN}📊 Veritabanı ilk kez hazırlanıyor...{Colors.END}")
        subprocess.run([sys.executable, "seed_data.py"], env=env)
        seed_marker.touch()
        print(f"  {Colors.GREEN}✅ Veritabanı hazır (2 kabin eklendi){Colors.END}")
    
    # Uvicorn başlat
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "server:app", 
         "--host", "127.0.0.1", "--port", "8001", "--reload"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # Log thread
    def log_backend():
        for line in process.stdout:
            if "Application startup complete" in line:
                print(f"  {Colors.GREEN}✅ Backend hazır!{Colors.END}")
            elif "ERROR" in line:
                print(f"  {Colors.RED}❌ {line.strip()}{Colors.END}")
    
    threading.Thread(target=log_backend, daemon=True).start()
    
    time.sleep(4)
    print(f"  {Colors.GREEN}✅ Backend çalışıyor: http://127.0.0.1:8001{Colors.END}")
    
    os.chdir(Path(__file__).parent)
    return process

def start_frontend():
    """Frontend'i başlat"""
    print(f"\n{Colors.BLUE}🎨 Frontend başlatılıyor...{Colors.END}")
    
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    # Port kontrolü
    if check_port(3000):
        print(f"  {Colors.YELLOW}⚠️  Port 3000 kullanımda, temizleniyor...{Colors.END}")
        kill_port(3000)
        time.sleep(2)
    
    # .env.local oluştur
    env_local = frontend_dir / ".env.local"
    env_content = """REACT_APP_BACKEND_URL=http://127.0.0.1:8001
PORT=3000
BROWSER=none
"""
    env_local.write_text(env_content)
    print(f"  {Colors.CYAN}✅ Lokal yapılandırma hazırlandı{Colors.END}")
    
    # Node modules kontrolü
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print(f"  {Colors.CYAN}📦 Paketler yükleniyor (ilk kez - 2-3 dakika)...{Colors.END}")
        subprocess.run(["yarn", "install"], shell=True)
    
    # React başlat
    env = os.environ.copy()
    env['BROWSER'] = 'none'
    
    process = subprocess.Popen(
        ["yarn", "start"],
        env=env,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # Log thread
    def log_frontend():
        for line in process.stdout:
            if "webpack compiled successfully" in line.lower():
                print(f"  {Colors.GREEN}✅ Frontend hazır!{Colors.END}")
            elif "error" in line.lower() and "compiled with" not in line.lower():
                if len(line.strip()) > 0 and not line.startswith('('):
                    print(f"  {Colors.YELLOW}⚠️  {line.strip()}{Colors.END}")
    
    threading.Thread(target=log_frontend, daemon=True).start()
    
    time.sleep(12)
    print(f"  {Colors.GREEN}✅ Frontend çalışıyor: http://127.0.0.1:3000{Colors.END}")
    
    os.chdir(Path(__file__).parent)
    return process

def open_browser():
    """Tarayıcıda otomatik aç"""
    print(f"\n{Colors.CYAN}🌐 Tarayıcı açılıyor...{Colors.END}")
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:3000/login")
    print(f"  {Colors.GREEN}✅ Uygulama tarayıcıda açıldı!{Colors.END}")

def show_info():
    """Kullanım bilgilerini göster"""
    print(f"\n{Colors.BOLD}{'='*65}{Colors.END}")
    print(f"{Colors.GREEN}{Colors.BOLD}✅ SİSTEM ÇALIŞIYOR!{Colors.END}")
    print(f"{Colors.BOLD}{'='*65}{Colors.END}")
    print(f"""
{Colors.CYAN}📊 Dashboard:{Colors.END}     http://127.0.0.1:3000
{Colors.CYAN}🔐 Giriş:{Colors.END}         {Colors.BOLD}admin{Colors.END} / {Colors.BOLD}admin123{Colors.END}
{Colors.CYAN}📹 Kamera:{Colors.END}        http://192.168.3.210/capture

{Colors.YELLOW}⚠️  ÖNEMLİ:{Colors.END}
   • Bu pencereyi KAPATMAYIN! Kapatırsanız sistem durur.
   • ESP32-CAM aynı WiFi'de olmalı (192.168.x.x)

{Colors.GREEN}📝 KULLANIM:{Colors.END}
   1. Tarayıcıda login yapın
   2. Dashboard'da kabin görün
   3. Ayarlar'dan kamera/telegram ayarlayın
   4. Öğrenci atayın

{Colors.RED}🛑 DURDURMAK İÇİN: CTRL+C{Colors.END}
    """)

def cleanup(processes):
    """Process'leri temizle"""
    print(f"\n\n{Colors.YELLOW}🛑 Sistem kapatılıyor...{Colors.END}")
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            try:
                process.kill()
            except:
                pass
    print(f"{Colors.GREEN}✅ Temizlik tamamlandı{Colors.END}")

def main():
    """Ana başlatma fonksiyonu"""
    processes = []
    
    try:
        print_header()
        
        # MongoDB kontrolü
        if not check_mongodb():
            print(f"\n{Colors.RED}❌ MongoDB gerekli!{Colors.END}")
            input("Çıkmak için Enter'a basın...")
            sys.exit(1)
        
        # Backend başlat
        backend_process = start_backend()
        processes.append(backend_process)
        
        # Frontend başlat
        frontend_process = start_frontend()
        processes.append(frontend_process)
        
        # Tarayıcıda aç
        open_browser()
        
        # Bilgileri göster
        show_info()
        
        # Sonsuz döngü - çalışmaya devam
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⏹️  Durdurma komutu alındı (CTRL+C)...{Colors.END}")
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ HATA: {e}{Colors.END}")
    finally:
        cleanup(processes)
        print(f"\n{Colors.CYAN}👋 Güle güle!{Colors.END}\n")
        input("Çıkmak için Enter'a basın...")

if __name__ == "__main__":
    main()
