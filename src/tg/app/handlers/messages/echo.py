from aiogram import Router, F
from aiogram.types import Message

from services import get_echo_answer

router = Router()


# Обрабатываем обычные текстовые сообщения
@router.message(F.text)
async def echo_handler(message: Message):
    # Проверяем, пересланное ли это сообщение
    if message.forward_from:
        await message.answer(
            f"Это пересланное сообщение от {message.forward_from.first_name}: {message.text}"
        )
    else:
        await message.answer(f"Вы написали: {message.text}")


# Обработчик для всех остальных типов сообщений
@router.message()
async def unknown_message_handler(message: Message):
    answer = await get_echo_answer(message)
    await message.answer(answer)
