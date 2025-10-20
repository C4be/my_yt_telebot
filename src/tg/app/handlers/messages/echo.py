from aiogram import Router, F
from aiogram.types import Message

router = Router()

# Этот обработчик будет вызываться для всех текстовых сообщений, которые не являются ссылками
@router.message(F.text)
async def echo_handler(message: Message):
    await message.answer(f"Вы написали: {message.text}")

# Обработчик для всех остальных типов сообщений (стикеры, аудио, документы и т.д.)
@router.message()
async def unknown_message_handler(message: Message):
    await message.answer("Я понимаю только текст, ссылки и видео.")