from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import logging

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

router = Router()

@router.message(Command('help'))
async def start_handler(message: Message) -> None:
    logging.info(f'\help команда от {message.from_user.id}')
    await message.answer(
        "Я пока не написал этот раздел"
    )
