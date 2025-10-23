from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from domain.models.user import User
from core.logging import new_logger

class UserService:
    """
    Сервис для работы с пользователями
    """
    __NAME = "UserService"
    __LOGGER = new_logger(__NAME)
    
    @staticmethod
    async def create_user(db: Session, tg_id: int, nickname: str = None, age: int = None) -> User:
        """
        Создает нового пользователя в базе данных
        
        Args:
            db: Сессия базы данных
            tg_id: Telegram ID пользователя
            nickname: Никнейм пользователя
            age: Возраст пользователя
            
        Returns:
            User: Созданный пользователь
        """
        user = User(tg_id=tg_id, nickname=nickname, age=age)
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
            UserService.__LOGGER.info(f"Пользователь {user} создан")
            return user
        except IntegrityError:
            db.rollback()
            UserService.__LOGGER.warning(f"Пользователь {user} уже существует")
            return await UserService.get_user_by_tg_id(db, tg_id)

    @staticmethod
    async def get_user_by_tg_id(db: Session, tg_id: int) -> User:
        """
        Получает пользователя по его Telegram ID
        
        Args:
            db: Сессия базы данных
            tg_id: Telegram ID пользователя
            
        Returns:
            User: Найденный пользователь или None
        """
        return db.query(User).filter(User.tg_id == tg_id).first()

    @staticmethod
    async def update_user(db: Session, tg_id: int, **kwargs) -> User:
        """
        Обновляет данные пользователя
        
        Args:
            db: Сессия базы данных
            tg_id: Telegram ID пользователя
            **kwargs: Поля для обновления
            
        Returns:
            User: Обновленный пользователь или None
        """
        user = await UserService.get_user_by_tg_id(db, tg_id)
        if not user:
            UserService.__LOGGER.warning(f"Пользователь с tg_id={tg_id} не найден")
            return None
            
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
                
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    async def ban_user(db: Session, tg_id: int) -> User:
        """
        Блокирует пользователя
        
        Args:
            db: Сессия базы данных
            tg_id: Telegram ID пользователя
            
        Returns:
            User: Заблокированный пользователь или None
        """
        UserService.__LOGGER.info(f"Бан tg_id={tg_id}")
        return await UserService.update_user(db, tg_id, is_banned=True)

    @staticmethod
    async def unban_user(db: Session, tg_id: int) -> User:
        """
        Разблокирует пользователя
        
        Args:
            db: Сессия базы данных
            tg_id: Telegram ID пользователя
            
        Returns:
            User: Разблокированный пользователь или None
        """
        UserService.__LOGGER.info(f"Разбан tg_id={tg_id}")
        return await UserService.update_user(db, tg_id, is_banned=False)