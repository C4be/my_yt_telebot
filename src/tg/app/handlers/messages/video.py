from aiogram import Router, F
from aiogram.types import Message, Video

router = Router()

@router.message(F.video)
async def video_handler(message: Message):
    video: Video = message.video

    # Выводим информацию о видео
    await message.answer(
        f"🎬 Видео получено!\n"
        f"Файл ID: {video.file_id}\n"
        f"Размер: {video.file_size / (1024*1024):.2f} MB\n"
        f"Длительность: {video.duration} секунд\n"
        f"Ширина/Высота: {video.width}x{video.height}"
    )

    # --- Запал под дальнейшую обработку ---
    # Например, скачивание видео и отправка на FastAPI
    # file = await message.video.download(destination=f"{video.file_id}.mp4")
    # result = await send_video_to_service(file.name)
    # await message.answer(f"Ответ от сервиса: {result}")
