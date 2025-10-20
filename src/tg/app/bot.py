import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from config import TOKEN
from handlers import start_router, help_router, link_router

# Create logger
logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(link_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())