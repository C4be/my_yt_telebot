from fastapi import FastAPI
from routers.video_router import router as video_router
import uvicorn

my_app = FastAPI(
    title="Video Loader API",
    version="1.0.0",
)

# Подключаем роутер сразу (так надёжнее)
my_app.include_router(video_router, prefix="/video", tags=["video"])


def main():
    """Точка входа при запуске из командной строки"""
    uvicorn.run("main:my_app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
