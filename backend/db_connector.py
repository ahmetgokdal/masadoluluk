"""
Veritabanı bağlantı modülü - MongoDB ve Mongita desteği
Mongita'yı async uyumlu wrapper ile kullanır
"""
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

class AsyncMongitaWrapper:
    """Mongita için async wrapper - Motor API'si ile uyumlu"""
    
    def __init__(self, collection):
        self._collection = collection
    
    def find(self, *args, **kwargs):
        """find operasyonu - returns async cursor"""
        cursor = self._collection.find(*args, **kwargs)
        return AsyncMongitaCursor(cursor)
    
    async def find_one(self, *args, **kwargs):
        """find_one operasyonu"""
        return await asyncio.to_thread(self._collection.find_one, *args, **kwargs)
    
    async def insert_one(self, *args, **kwargs):
        """insert_one operasyonu"""
        return await asyncio.to_thread(self._collection.insert_one, *args, **kwargs)
    
    async def insert_many(self, *args, **kwargs):
        """insert_many operasyonu"""
        return await asyncio.to_thread(self._collection.insert_many, *args, **kwargs)
    
    async def update_one(self, filter_query, update_query, **kwargs):
        """update_one operasyonu"""
        # Mongita upsert desteği
        if kwargs.get('upsert'):
            existing = await asyncio.to_thread(self._collection.find_one, filter_query)
            if not existing:
                # Insert new document
                doc = filter_query.copy()
                if '$set' in update_query:
                    doc.update(update_query['$set'])
                return await asyncio.to_thread(self._collection.insert_one, doc)
        
        return await asyncio.to_thread(self._collection.update_one, filter_query, update_query, **kwargs)
    
    async def update_many(self, *args, **kwargs):
        """update_many operasyonu"""
        return await asyncio.to_thread(self._collection.update_many, *args, **kwargs)
    
    async def delete_one(self, *args, **kwargs):
        """delete_one operasyonu"""
        return await asyncio.to_thread(self._collection.delete_one, *args, **kwargs)
    
    async def delete_many(self, *args, **kwargs):
        """delete_many operasyonu"""
        return await asyncio.to_thread(self._collection.delete_many, *args, **kwargs)
    
    async def count_documents(self, *args, **kwargs):
        """count_documents operasyonu"""
        return await asyncio.to_thread(self._collection.count_documents, *args, **kwargs)
    
    async def aggregate(self, *args, **kwargs):
        """aggregate operasyonu"""
        result = await asyncio.to_thread(self._collection.aggregate, *args, **kwargs)
        return AsyncMongitaCursor(result)


class AsyncMongitaCursor:
    """Mongita cursor için async wrapper"""
    
    def __init__(self, cursor):
        self._cursor = cursor if isinstance(cursor, list) else list(cursor)
    
    async def to_list(self, length=None):
        """Cursor'dan liste oluştur"""
        return self._cursor[:length] if length else self._cursor


class AsyncMongitaDatabase:
    """Mongita database için async wrapper"""
    
    def __init__(self, db):
        self._db = db
    
    def __getattr__(self, name):
        """Collection erişimi"""
        collection = self._db[name]
        return AsyncMongitaWrapper(collection)
    
    def __getitem__(self, name):
        """Collection erişimi (dict syntax)"""
        collection = self._db[name]
        return AsyncMongitaWrapper(collection)


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
        try:
            from mongita import MongitaClientDisk
            db_path = mongo_url.replace('mongita:///', '').replace('mongita://', '')
            
            # Path'i normalize et
            if not os.path.isabs(db_path):
                db_path = os.path.abspath(db_path)
            
            # Dizini oluştur
            os.makedirs(db_path, exist_ok=True)
            
            client = MongitaClientDisk(db_path)
            raw_db = client[db_name]
            db = AsyncMongitaDatabase(raw_db)
            print(f"✅ Mongita (file-based) bağlantısı: {db_path}/{db_name}")
        except ImportError:
            print("⚠️  Mongita bulunamadı, MongoDB'ye geçiliyor...")
            client = AsyncIOMotorClient('mongodb://localhost:27017')
            db = client[db_name]
            print(f"✅ MongoDB bağlantısı (fallback): mongodb://localhost:27017/{db_name}")
    else:
        # Motor - async MongoDB
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        print(f"✅ MongoDB bağlantısı: {mongo_url}/{db_name}")
    
    return db, client

# Global database instance
db, client = get_database()
