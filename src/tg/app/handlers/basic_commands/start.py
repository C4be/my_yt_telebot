from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils import LogManager
from services import get_hello_message

_logger = LogManager.new_logger("StartHandler")

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    _logger.info(f"\help команда от {message.from_user.id}")
    answer = await get_hello_message(message.from_user.id)
    await message.answer(answer)
