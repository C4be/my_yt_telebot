import io
from aiogram import Router, F
from aiogram.types import Message
from db.engine import get_db_session
from domain.services.video_service import VideoService
from core.logging import new_logger

__NAME: str = "video_handler"
__LOGGER = new_logger(__NAME, to_file=False)

router = Router(name=__NAME)


async def save_video_if_new(message: Message):
    if message.video is None:
        await message.answer("⚠️ Не смог поределеить ID видео в телеграм!")
        return

    tg_id = str(message.video.file_id)
    title = f"Видео от {message.from_user.username or message.from_user.id}"

    async for db in get_db_session():
        # Проверяем, есть ли уже такое видео
        existing_video = await VideoService.get_video_by_tg_id(db, tg_id)
        if existing_video:
            __LOGGER.info(f"Видео {tg_id} уже в системе")
            await message.answer(
                "⚠️ Это видео уже загружено в систему, повторно загружать нет смысла!"
            )
            return

        # Скачиваем видео в память
        video_io = io.BytesIO()
        try:
            bot = message.bot  # 1. Получаем экземпляр Bot
            file = await bot.get_file(
                tg_id
            )  # 2. Получаем информацию о файле по file_id
            await bot.download_file(
                file.file_path, destination=video_io
            )  # 3. Скачиваем файл
        except Exception as e:
            __LOGGER.error(f"Не удалось скачать файл {tg_id}: {e}")
            await message.answer(
                "❌ Произошла ошибка при скачивании файла с серверов Telegram."
            )
            return
        video_io.seek(0)  # очень важно

        # Сохраняем в Mongo + Postgres
        video_record = await VideoService.create_video_record(
            db=db,
            tg_id=tg_id,
            video_bytes=video_io.read(),
            filename=f"{tg_id}.mp4",
            title=title,
        )

    await message.answer(
        f"✅ Видео успешно сохранено!\nPostgres ID: {video_record.id}\nMongoDB ID: {video_record.mongo_db_id}"
    )


# ------------------------
# Хэндлеры
# ------------------------


@router.message(F.video & F.forward_from)
async def handle_forwarded_video(message: Message):
    await message.answer("📤 Это пересланное видео!")
    await save_video_if_new(message)


@router.message(F.video & F.forward_from_chat)
async def handle_forwarded_video_from_chat(message: Message):
    await message.answer("📤 Пересланное видео из чата!")
    await save_video_if_new(message)


@router.message(F.video)
async def handle_video(message: Message):
    await message.answer("📤 Это обычное видео!")
    await save_video_if_new(message)


@router.message(F.reply_to_message & F.reply_to_message.video)
async def handle_reply_with_video(message: Message):
    await message.answer("📤 Это ответ на сообщение с видео!")
    await save_video_if_new(message)
