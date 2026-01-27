from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from models import Account


async def startup():
    client = AsyncIOMotorClient(settings.DB_URI)
    await init_beanie(client["acl"], document_models=[Account])
