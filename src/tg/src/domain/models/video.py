from sqlalchemy import Column, Integer, String, DateTime, func
from db.engine import Base


class Video(Base):
    """
    Модель видеоролика в базе данных
    """

    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(String, unique=True, index=True, nullable=False)
    mongo_db_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)  # новое поле
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Video(id={self.id}, tg_id={self.tg_id}, title={self.title}, mongo_db_id={self.mongo_db_id})>"
