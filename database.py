from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["ethiopian_food_db"]
food_collection = db["foods"]
drink_collection = db["drinks"]
user_collection = db["users"]