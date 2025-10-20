from aiogram import Router, F
from aiogram.types import Message, Document
import os
import logging

router = Router()
logger = logging.getLogger(__name__)

# Список поддерживаемых расширений файлов
SUPPORTED_EXTENSIONS = [".txt"]

# Обрабатываем документы с поддерживаемыми расширениями
@router.message(
    (F.document & F.document.file_name.regexp(r'\.txt$')) | 
    (F.forward_from.as_("forwarded") & F.document & F.document.file_name.regexp(r'\.txt$'))
)
async def file_handler(message: Message):
    document: Document = message.document
    file_name = document.file_name
    file_extension = os.path.splitext(file_name)[1].lower()
    
    # Определяем, пересланный это документ или нет
    forwarded = "(пересланный)" if message.forward_from else ""
    
    # Выводим информацию о файле
    await message.answer(
        f"📄 Файл получен! {forwarded}\n"
        f"Имя файла: {file_name}\n"
        f"Тип: {document.mime_type}\n"
        f"Размер: {document.file_size / 1024:.2f} KB"
    )
    
    # Разная обработка в зависимости от типа файла
    if file_extension == ".txt":
        await message.answer("Обрабатываю текстовый файл...")
        # Здесь можно добавить скачивание и обработку текстового файла
        # file = await message.document.download()
        # with open(file.name, 'r', encoding='utf-8') as f:
        #     content = f.read()
        # await message.answer(f"Содержимое файла: {content[:100]}...")
    
    logger.info(f"Получен файл {file_name} от пользователя {message.from_user.username or message.from_user.id}")