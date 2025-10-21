from fastapi import APIRouter, HTTPException
from fastapi import Query
from utils.video_loader import download_video

router = APIRouter()

@router.get("/load/")
async def load_video(url: str = Query(..., description="Ссылка на загрузку")):
    """
    Скачивает видео по ссылке и сохраняет его во временный файл.
    Возвращает id и путь к файлу.
    """
    try:
        video_id = await download_video(url)
        return {"id": video_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))