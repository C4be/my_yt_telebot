import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from config import TOKEN
from handlers import start_router, help_router, link_router, video_router, echo_router

# Create logger
logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(link_router)  # Обработчик ссылок
    dp.include_router(video_router)  # Обработчик видео
    dp.include_router(echo_router)   # Обработчик обычных сообщений (должен быть последним)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())