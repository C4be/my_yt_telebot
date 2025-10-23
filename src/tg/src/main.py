# standart imports
import asyncio
import logging
from aiogram import Bot, Dispatcher

# my imports
from bot.handlers import start_router, video_router
from core.config import BOT_TOKEN
from core.logging import ensure_log_directories
from db import init_db, init_mongo

__ROUTERS = [
    start_router,
    video_router,
]


async def main():
    # Настройка логирования (создание директорий и хендлеров)
    ensure_log_directories()
    logging.basicConfig(level=logging.INFO)

    # Инициализация базы данных
    await init_db()
    logging.getLogger("startup").info("🐘 База данных инициализирована")
    await init_mongo()
    logging.getLogger("startup").info("🗂️ База данных MONGO инициализирована")

    # Инициализация компонентов
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация хэндлеров
    dp.include_routers(*__ROUTERS)

    # Запуск
    logging.getLogger("startup").info("🚀 Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
