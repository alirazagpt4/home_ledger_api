import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# .env file se connection string load ho rahi hai
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB client initialize ho raha hai network certificates ke sath
client = AsyncIOMotorClient(
    MONGO_URI,
    tlsCAFile=certifi.where(),
    tlsAllowInvalidCertificates=True
)

# Database ka naam hum 'home_ledger' rakh rahe hain
db = client.get_database("homeledgerDB")

# Yeh function server start hote hi check karega ke database chal raha hai ya nahi
async def ping_database():
    try:
        await client.admin.command('ping')
        return True
    except Exception as e:
        print(f"❌ DB Connection Failed: {e}")
        return False