from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import BigInteger

from db.connection import Base

class User(Base):
    """
    Модель пользователя в базе данных
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, unique=True, index=True, nullable=False)
    nickname = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    is_banned = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, tg_id={self.tg_id}, nickname={self.nickname})>"