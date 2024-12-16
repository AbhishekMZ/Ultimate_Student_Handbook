# app/db/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import asyncio
from app.db.models import __beanie_models__  # Import list of models

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(database=client[settings.DATABASE_NAME], document_models=__beanie_models__)

asyncio.run(init_db())