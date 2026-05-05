from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import MONGODB_URL, DATABASE_NAME
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db_instance = MongoDB()

async def connect_to_mongo():
    logger.info("Connecting to MongoDB...")
    db_instance.client = AsyncIOMotorClient(MONGODB_URL)
    db_instance.db = db_instance.client[DATABASE_NAME]
    
    # Create Indexes for query performance
    await db_instance.db["products"].create_index("category")
    await db_instance.db["products"].create_index("price")
    logger.info("Connected to MongoDB & Indexes Verified")

async def close_mongo_connection():
    logger.info("Closing MongoDB connection...")
    if db_instance.client:
        db_instance.client.close()
        logger.info("MongoDB disconnected")

def get_database():
    return db_instance.db