from aiogram import Router, F
from aiogram.types import Message

router = Router()

# Обрабатываем обычные текстовые сообщения
@router.message(F.text)
async def echo_handler(message: Message):
    # Проверяем, пересланное ли это сообщение
    if message.forward_from:
        await message.answer(f"Это пересланное сообщение от {message.forward_from.first_name}: {message.text}")
    else:
        await message.answer(f"Вы написали: {message.text}")

# Обработчик для всех остальных типов сообщений
@router.message()
async def unknown_message_handler(message: Message):
    # Определяем тип сообщения для более информативного ответа
    message_type = "неизвестный тип"
    if message.photo:
        message_type = "фото"
    elif message.sticker:
        message_type = "стикер"
    elif message.voice:
        message_type = "голосовое сообщение"
    elif message.audio:
        message_type = "аудио"
    elif message.animation:
        message_type = "анимация"
    elif message.location:
        message_type = "геолокация"
    
    await message.answer(f"Получено сообщение типа '{message_type}'. Я обрабатываю только текст, ссылки, видео и документы.")