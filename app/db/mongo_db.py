from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_DB_URL

client = AsyncIOMotorClient(MONGO_DB_URL)
db = client.cooling_system_db
temperature_collection = db.temperature
device_speed_collection = db.device_speed
