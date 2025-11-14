"""
Seed initial data for Smart Cabin Monitoring System
"""
import asyncio
import os
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import random

ROOT_DIR = Path(__file__).parent

# .env dosyasını yükle (varsa)
env_file = ROOT_DIR / '.env'
if env_file.exists():
    load_dotenv(env_file)
else:
    print(f"⚠️  .env dosyası bulunamadı: {env_file}")
    print("Varsayılan değerler kullanılıyor...")

try:
    from db_connector import db, client
except ImportError:
    # Fallback to MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'smart_cabin_db')
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

async def seed_cabins():
    """Seed empty database - NO pre-filled cabins (users add manually)"""
    print("Checking cabins...")
    
    # Check if cabins already exist
    existing_count = await db.cabins.count_documents({})
    
    if existing_count > 0:
        print(f"⚠️  {existing_count} kabins already exist - skipping seed")
        return
    
    # Only create if database is completely empty
    print("✅ No cabins found - database ready for manual setup")

async def seed_sessions():
    """Seed session history"""
    print("Seeding sessions...")
    
    # Clear existing sessions
    await db.sessions.delete_many({})
    
    sessions = []
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Generate sessions for last 7 days
    for cabin_no in range(1, 51):
        # Random number of sessions per day (0-5)
        for day in range(7):
            date = today - timedelta(days=day)
            num_sessions = random.randint(0, 5)
            
            for _ in range(num_sessions):
                start_hour = random.randint(8, 18)
                duration = random.randint(1800, 7200)  # 30 min to 2 hours
                
                session = {
                    "_id": f"session_{cabin_no}_{day}_{_}",
                    "cabin_no": cabin_no,
                    "student_id": f"STU{str(cabin_no).zfill(3)}",
                    "student_name": f"Öğrenci {cabin_no}",
                    "start_time": date.replace(hour=start_hour, minute=random.randint(0, 59)),
                    "end_time": date.replace(hour=start_hour, minute=random.randint(0, 59)) + timedelta(seconds=duration),
                    "duration": duration,
                    "detection_method": random.choice(["mediapipe", "motion", "yolo"]),
                    "created_at": datetime.now(timezone.utc)
                }
                sessions.append(session)
    
    await db.sessions.insert_many(sessions)
    print(f"✅ Seeded {len(sessions)} sessions")

async def seed_alerts():
    """Seed some alerts"""
    print("Seeding alerts...")
    
    # Clear existing alerts
    await db.alerts.delete_many({})
    
    alerts = [
        {
            "_id": "alert_1",
            "type": "long_break",
            "cabin_no": 5,
            "student_name": "Öğrenci 5",
            "message": "2 saattir uzun molada",
            "severity": "warning",
            "resolved": False,
            "created_at": datetime.now(timezone.utc) - timedelta(hours=2)
        },
        {
            "_id": "alert_2",
            "type": "no_data",
            "cabin_no": 12,
            "student_name": "Öğrenci 12",
            "message": "24 saattir veri yok",
            "severity": "critical",
            "resolved": False,
            "created_at": datetime.now(timezone.utc) - timedelta(hours=24)
        },
        {
            "_id": "alert_3",
            "type": "camera_offline",
            "cabin_no": 23,
            "student_name": None,
            "message": "Kamera bağlantısı kesildi",
            "severity": "error",
            "resolved": False,
            "created_at": datetime.now(timezone.utc) - timedelta(hours=1)
        }
    ]
    
    await db.alerts.insert_many(alerts)
    print(f"✅ Seeded {len(alerts)} alerts")

async def seed_reports():
    """Seed some mock reports"""
    print("Seeding reports...")
    
    # Clear existing reports
    await db.reports.delete_many({})
    
    reports = [
        {
            "_id": "report_1",
            "type": "daily",
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "cabin_no": 1,
            "student_name": "Öğrenci 1",
            "total_hours": 6.5,
            "sessions_count": 3,
            "filename": f"report_daily_cabin1_{datetime.now().strftime('%Y-%m-%d')}.pdf",
            "file_path": "/app/backend/reports/report_daily_cabin1.pdf",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "_id": "report_2",
            "type": "weekly",
            "date": (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d"),
            "cabin_no": None,
            "student_name": "Tüm Öğrenciler",
            "total_hours": 145.2,
            "sessions_count": 78,
            "filename": f"report_weekly_all_{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')}.pdf",
            "file_path": "/app/backend/reports/report_weekly_all.pdf",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "_id": "report_3",
            "type": "monthly",
            "date": "2025-01-01",
            "cabin_no": None,
            "student_name": "Tüm Öğrenciler",
            "total_hours": 580.5,
            "sessions_count": 312,
            "filename": "report_monthly_all_2025-01.pdf",
            "file_path": "/app/backend/reports/report_monthly_all.pdf",
            "created_at": datetime.now(timezone.utc)
        }
    ]
    
    await db.reports.insert_many(reports)
    print(f"✅ Seeded {len(reports)} reports")

async def seed_telegram_config():
    """Seed default Telegram configuration"""
    print("Seeding Telegram config...")
    
    config = {
        "_id": "telegram_config",
        "bot_token": "",
        "weekly_recipients": [],
        "cabin_recipients": {},
        "updated_at": datetime.now(timezone.utc)
    }
    
    await db.telegram_config.update_one(
        {"_id": "telegram_config"},
        {"$set": config},
        upsert=True
    )
    print("✅ Seeded Telegram config")

async def main():
    print("🌱 Starting database seeding...")
    print(f"Database: {os.environ['DB_NAME']}")
    
    await seed_cabins()
    await seed_sessions()
    await seed_alerts()
    await seed_reports()
    await seed_telegram_config()
    
    print("\n✨ Database seeding completed successfully!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
