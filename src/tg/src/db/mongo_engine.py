from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from collections.abc import AsyncGenerator
from core.config import MONGO_DB_URL, MONGO_DB_NAME

# Глобальные переменные для клиента и базы
client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


async def init_mongo() -> AsyncIOMotorDatabase:
    """
    Инициализирует подключение к MongoDB и возвращает объект базы данных.
    """
    global client, db

    if client is None:
        client = AsyncIOMotorClient(MONGO_DB_URL)
        db = client[MONGO_DB_NAME]
        print(f"✅ Подключено к MongoDB: {MONGO_DB_URL}/{MONGO_DB_NAME}")

    return db


async def get_mongo_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """
    Асинхронный генератор для получения подключения к MongoDB (аналог get_db_session)
    """
    if db is None:
        await init_mongo()
    yield db


async def close_mongo():
    """
    Закрывает соединение с MongoDB
    """
    global client
    if client:
        client.close()
        print("🧹 Соединение с MongoDB закрыто")
