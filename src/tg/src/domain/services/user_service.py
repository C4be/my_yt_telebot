from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.user import User
from core.logging import new_logger


class UserService:
    """
    Сервис для работы с пользователями (асинхронно)
    """

    __NAME = "UserService"
    __LOGGER = new_logger(__NAME)

    @staticmethod
    async def create_user(
        db: AsyncSession,
        tg_id: int,
        nickname: str | None = None,
        age: int | None = None,
    ) -> User:
        """
        Создает нового пользователя в базе данных
        """
        user = User(tg_id=tg_id, nickname=nickname, age=age)
        db.add(user)
        try:
            await db.commit()
            await db.refresh(user)
            UserService.__LOGGER.info(f"Пользователь {user} создан")
            return user
        except IntegrityError:
            await db.rollback()
            UserService.__LOGGER.warning(f"Пользователь {user} уже существует")
            existing_user = await UserService.get_user_by_tg_id(db, tg_id)
            return existing_user

    @staticmethod
    async def get_user_by_tg_id(db: AsyncSession, tg_id: int) -> User | None:
        """
        Получает пользователя по его Telegram ID
        """
        stmt = select(User).where(User.tg_id == tg_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def update_user(db: AsyncSession, tg_id: int, **kwargs) -> User | None:
        """
        Обновляет данные пользователя
        """
        user = await UserService.get_user_by_tg_id(db, tg_id)
        if not user:
            UserService.__LOGGER.warning(f"Пользователь с tg_id={tg_id} не найден")
            return None

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def ban_user(db: AsyncSession, tg_id: int) -> User | None:
        """
        Блокирует пользователя
        """
        UserService.__LOGGER.info(f"Бан tg_id={tg_id}")
        return await UserService.update_user(db, tg_id, is_banned=True)

    @staticmethod
    async def unban_user(db: AsyncSession, tg_id: int) -> User | None:
        """
        Разблокирует пользователя
        """
        UserService.__LOGGER.info(f"Разбан tg_id={tg_id}")
        return await UserService.update_user(db, tg_id, is_banned=False)
