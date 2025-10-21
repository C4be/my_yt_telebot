from fastapi import APIRouter, HTTPException, Query
from utils.edit_video import video_processing_pipeline

router = APIRouter()

@router.post("/edit_video/")
async def get_video_link(db_url: str = Query(..., description="Ссылка на загрузку")):
    """Получает ссылку на видео из DataBase и загружает его оттуда
    Пока это будет ссылка на видео из локальной папки video"""

    video_processing_pipeline(db_url)

