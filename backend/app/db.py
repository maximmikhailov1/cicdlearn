import asyncpg
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import get_settings


async def get_pg_pool():
    settings = get_settings()
    return await asyncpg.create_pool(
        settings.postgres_dsn,
        min_size=1,
        max_size=5,
        command_timeout=10,
    )


def get_mongo_client():
    settings = get_settings()
    return AsyncIOMotorClient(settings.mongo_url)


def get_mongo_db():
    settings = get_settings()
    client = get_mongo_client()
    return client[settings.mongo_db]
