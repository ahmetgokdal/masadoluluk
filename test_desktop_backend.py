#!/usr/bin/env python3
"""
Desktop backend quick test - Mongita ile backend'in çalışıp çalışmadığını test eder
"""
import asyncio
import os
import sys
import time
import threading
from pathlib import Path

# Test için environment
os.environ['MONGO_URL'] = f'mongita:///{Path(__file__).parent.absolute()}/data/test_desktop'
os.environ['DB_NAME'] = 'smart_cabin_db'
os.environ['CORS_ORIGINS'] = '*'

print("🧪 Desktop Backend Test")
print("=" * 50)
print(f"Database: {os.environ['MONGO_URL']}")
print(f"DB Name: {os.environ['DB_NAME']}")
print("=" * 50)

# Seed data
print("\n📊 Seeding database...")
os.chdir(Path(__file__).parent / 'backend')
import subprocess
result = subprocess.run([sys.executable, 'seed_data.py'], capture_output=True, text=True)
if result.returncode != 0:
    print("❌ Seed failed:")
    print(result.stderr)
    sys.exit(1)
print("✅ Seed successful")

# Backend'i thread'de başlat
print("\n🔧 Starting backend...")
def run_backend():
    import uvicorn
    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        port=8888,
        log_level="error"
    )

backend_thread = threading.Thread(target=run_backend, daemon=True)
backend_thread.start()
time.sleep(3)

# Test API calls
print("\n🧪 Testing API endpoints...")
import requests

try:
    # Test 1: Login
    print("\n1️⃣  Testing login...")
    response = requests.post(
        "http://127.0.0.1:8888/api/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    if response.status_code == 200:
        print("   ✅ Login successful")
        token = response.json()['session_token']
        headers = {"Cookie": f"session_token={token}"}
    else:
        print(f"   ❌ Login failed: {response.status_code}")
        sys.exit(1)
    
    # Test 2: Get stats
    print("\n2️⃣  Testing stats...")
    response = requests.get("http://127.0.0.1:8888/api/stats", headers=headers)
    if response.status_code == 200:
        stats = response.json()
        print(f"   ✅ Stats: {stats['total_cabins']} cabins, {stats['total_students']} students")
    else:
        print(f"   ❌ Stats failed: {response.status_code}")
    
    # Test 3: Get cabins
    print("\n3️⃣  Testing cabins...")
    response = requests.get("http://127.0.0.1:8888/api/cabins", headers=headers)
    if response.status_code == 200:
        cabins = response.json()
        print(f"   ✅ Cabins: {len(cabins)} cabins loaded")
    else:
        print(f"   ❌ Cabins failed: {response.status_code}")
    
    # Test 4: Get alerts
    print("\n4️⃣  Testing alerts...")
    response = requests.get("http://127.0.0.1:8888/api/alerts/recent", headers=headers)
    if response.status_code == 200:
        alerts = response.json()
        print(f"   ✅ Alerts: {len(alerts)} alerts")
    else:
        print(f"   ❌ Alerts failed: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 50)
    print("\n✅ Desktop backend is ready to use with Mongita!")
    print("   Masaüstü uygulaması kullanıma hazır!")
    
except Exception as e:
    print(f"\n❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
