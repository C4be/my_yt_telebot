from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.my_log import LogManager
from services.help_service import get_help_message

# Настройка логгера
_logger = LogManager.new_logger("HelpHandler")

router = Router()

@router.message(Command('help'))
async def start_handler(message: Message) -> None:
    _logger.info(f'\help команда от {message.from_user.id}')
    answer = await get_help_message()
    await message.answer(
        answer
    )
