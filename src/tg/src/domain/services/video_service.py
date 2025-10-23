import io
from bson import ObjectId
import gridfs
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from domain.models.video import Video
from db.mongo_engine import get_mongo_db
from core.logging import new_logger


class VideoService:
    __NAME = "VideoService"
    __LOGGER = new_logger(__NAME)

    # -----------------------------
    # CREATE
    # -----------------------------
    @staticmethod
    async def create_video_record(
        db: AsyncSession, tg_id: str, video_bytes: bytes, filename: str, title: str
    ) -> Video:
        """
        Сохраняет видео в MongoDB и Postgres.
        Если видео с tg_id уже существует, возвращает существующее.
        """
        # Проверяем в Postgres
        existing_video = await VideoService.get_video_by_tg_id(db, tg_id)
        if existing_video:
            VideoService.__LOGGER.info(f"Видео с tg_id={tg_id} уже существует")
            return existing_video

        # --- Сохраняем в Mongo ---
        async for mongo in get_mongo_db():
            # fs = gridfs.AsyncIOMotorGridFSBucket(mongo)
            fs = AsyncIOMotorGridFSBucket(mongo)
            mongo_file_id = await fs.upload_from_stream(
                filename, io.BytesIO(video_bytes)
            )
            VideoService.__LOGGER.info(
                f"Видео сохранено в MongoDB с ID: {mongo_file_id}"
            )

        # --- Сохраняем запись в Postgres ---
        video = Video(tg_id=tg_id, mongo_db_id=str(mongo_file_id), title=title)
        db.add(video)
        try:
            await db.commit()
            await db.refresh(video)
            VideoService.__LOGGER.info(
                f"Метаданные видео сохранены в Postgres: {video}"
            )
            return video
        except IntegrityError:
            await db.rollback()
            VideoService.__LOGGER.warning(f"Видео с tg_id={tg_id} уже существует")
            return await VideoService.get_video_by_tg_id(db, tg_id)

    # -----------------------------
    # READ
    # -----------------------------
    @staticmethod
    async def get_video_by_tg_id(db: AsyncSession, tg_id: str) -> Video | None:
        """
        Получает видео из Postgres по tg_id
        """
        result = await db.execute(select(Video).where(Video.tg_id == tg_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_video_by_title(db: AsyncSession, title: str) -> list[Video]:
        """
        Получает все видео с заданным названием
        """
        result = await db.execute(select(Video).where(Video.title == title))
        return result.scalars().all()

    # -----------------------------
    # DELETE
    # -----------------------------
    @staticmethod
    async def delete_video_by_tg_id(db: AsyncSession, tg_id: str) -> bool:
        """
        Удаляет видео из MongoDB и Postgres по tg_id
        """
        video = await VideoService.get_video_by_tg_id(db, tg_id)
        if not video:
            VideoService.__LOGGER.warning(f"Видео с tg_id={tg_id} не найдено")
            return False

        # --- Удаляем из Mongo ---
        async for mongo in get_mongo_db():
            fs = gridfs.AsyncIOMotorGridFSBucket(mongo)
            try:
                await fs.delete(ObjectId(video.mongo_db_id))
                VideoService.__LOGGER.info(
                    f"Видео с MongoDB ID={video.mongo_db_id} удалено"
                )
            except Exception as e:
                VideoService.__LOGGER.error(f"Ошибка при удалении видео из Mongo: {e}")

        # --- Удаляем из Postgres ---
        await db.delete(video)
        await db.commit()
        VideoService.__LOGGER.info(
            f"Запись о видео с tg_id={tg_id} удалена из Postgres"
        )
        return True
