#!/usr/bin/env python3
"""
Mongita async wrapper test script
"""
import asyncio
import os
import sys
from pathlib import Path

# Test için .env ayarla
os.environ['MONGO_URL'] = f'mongita:///{Path(__file__).parent.absolute()}/data/cabin_db_test'
os.environ['DB_NAME'] = 'test_db'

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from db_connector import db

async def test_mongita():
    """Mongita async wrapper'ı test et"""
    
    print("\n🧪 Mongita Async Wrapper Test Başlıyor...\n")
    
    # 1. Insert test
    print("1️⃣  Insert test...")
    test_data = {
        "_id": "test_1",
        "name": "Test Cabin",
        "status": "active"
    }
    await db.test_collection.insert_one(test_data)
    print("   ✅ Insert başarılı")
    
    # 2. Find test
    print("\n2️⃣  Find test...")
    result = await db.test_collection.find_one({"_id": "test_1"})
    print(f"   ✅ Find başarılı: {result}")
    
    # 3. Update test
    print("\n3️⃣  Update test...")
    await db.test_collection.update_one(
        {"_id": "test_1"},
        {"$set": {"status": "updated"}}
    )
    result = await db.test_collection.find_one({"_id": "test_1"})
    print(f"   ✅ Update başarılı: status = {result['status']}")
    
    # 4. Insert many test
    print("\n4️⃣  Insert many test...")
    many_data = [
        {"_id": f"test_{i}", "value": i} for i in range(2, 6)
    ]
    await db.test_collection.insert_many(many_data)
    print("   ✅ Insert many başarılı")
    
    # 5. Find all test
    print("\n5️⃣  Find all test...")
    cursor = await db.test_collection.find({})
    results = await cursor.to_list(100)
    print(f"   ✅ Find all başarılı: {len(results)} kayıt")
    
    # 6. Delete test
    print("\n6️⃣  Delete test...")
    await db.test_collection.delete_many({})
    cursor = await db.test_collection.find({})
    results = await cursor.to_list(100)
    print(f"   ✅ Delete başarılı: {len(results)} kayıt kaldı")
    
    print("\n🎉 Tüm testler başarılı!\n")

if __name__ == "__main__":
    asyncio.run(test_mongita())
