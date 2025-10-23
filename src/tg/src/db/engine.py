from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from collections.abc import AsyncGenerator
from core.config import DATABASE_URL

Base = declarative_base()

# Пример: DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Создает и возвращает асинхронную сессию базы данных
    """
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    """
    Инициализирует базу данных, создавая все таблицы (асинхронно)
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
