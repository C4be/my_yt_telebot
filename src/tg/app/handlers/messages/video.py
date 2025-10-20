from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(
    F.video |
    (F.forward_from | F.forward_from_chat) & (F.video | F.document) |
    (F.reply_to_message & (F.reply_to_message.video | F.reply_to_message.document))
)
async def video_handler(message: Message):
    # Сначала берём видео
    video = message.video or message.document
    if not video:
        await message.answer("❌ Видео не найдено")
        return

    file_id = getattr(video, "file_id", None)
    file_size = getattr(video, "file_size", 0)
    duration = getattr(video, "duration", 0)
    width = getattr(video, "width", 0)
    height = getattr(video, "height", 0)

    await message.answer(
        f"🎬 Видео получено!\n"
        f"Файл ID: {file_id}\n"
        f"Размер: {file_size / (1024*1024):.2f} MB\n"
        f"Длительность: {duration} секунд\n"
        f"Ширина/Высота: {width}x{height}"
    )

    # --- Запал под дальнейшую обработку ---
    # file = await video.download(destination=f"{file_id}.mp4")
    # result = await send_video_to_service(file.name)
    # await message.answer(f"Ответ от сервиса: {result}")
