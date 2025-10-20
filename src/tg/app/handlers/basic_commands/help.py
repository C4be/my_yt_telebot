from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command('help'))
async def start_handler(message: Message) -> None:
    await message.answer(
        "Я пока не написал этот раздел"
    )
