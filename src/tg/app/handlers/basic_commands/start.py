from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import logging

router = Router()

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


@router.message(Command('start'))
async def start_handler(message: Message) -> None:
    logging.INFO(f'\help команда от {message.from_user.id}')
    await message.answer(
        "Привет, я бот, через который ты сможешь грузить и загружать видео на YT/TT автоматически!"
    )

