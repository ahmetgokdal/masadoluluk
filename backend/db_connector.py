"""
Veritabanı bağlantı modülü - MongoDB ve Mongita desteği
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient

def get_database():
    """
    MongoDB veya Mongita bağlantısı oluştur.
    MONGO_URL'e göre otomatik seçim yapar.
    """
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'smart_cabin_db')
    
    # Mongita mı MongoDB mu kontrol et
    if mongo_url.startswith('mongita://'):
        # Mongita - file-based
        from mongita import MongitaClientDisk
        db_path = mongo_url.replace('mongita:///', '').replace('mongita://', '')
        client = MongitaClientDisk(db_path)
        db = client[db_name]
        print(f"✅ Mongita (file-based) bağlantısı: {db_path}/{db_name}")
    else:
        # Motor - async MongoDB
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        print(f"✅ MongoDB bağlantısı: {mongo_url}/{db_name}")
    
    return db, client

# Global database instance
db, client = get_database()
