import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN

from handlers import (
    start_router,
    help_router,
    link_router,
    video_router,
    file_router,
    echo_router,
)

# Create logger
logging.basicConfig(level=logging.INFO)


def init_dispatcher() -> Dispatcher:
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(start_router)  # Команды /start
    dp.include_router(help_router)  # Команды /help
    dp.include_router(link_router)  # Обработчик ссылок
    dp.include_router(video_router)  # Обработчик видео
    dp.include_router(file_router)  # Обработчик файлов
    dp.include_router(
        echo_router
    )  # Обработчик обычных сообщений (должен быть последним)
    return dp


async def main():
    bot = Bot(token=TOKEN)
    dp = init_dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
