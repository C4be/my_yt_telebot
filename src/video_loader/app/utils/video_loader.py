from yt_dlp import YoutubeDL
import os
import asyncio
import re # Добавляем для очистки имени файла

# 1. Определяем постоянную директорию для сохранения видео
DOWNLOAD_DIR = 'video' 

# Создаем директорию, если она еще не существует
os.makedirs(DOWNLOAD_DIR, exist_ok=True) 

def clean_filename(filename):
    """Удаляет недопустимые символы из имени файла."""
    # Заменяем все символы, кроме букв, цифр, -, _ и . на пустое место
    # Это важно, так как yt-dlp может менять название видео, и мы должны
    # использовать логику, похожую на его.
    return re.sub(r'[\\/:*?"<>|]', '', filename)

async def download_video(url: str) -> str:
    """
    Скачивает видео по URL в постоянную директорию 'video/' и возвращает
    фактический путь к скачанному файлу.

    :param url: URL видео (например, YouTube).
    :return: Полный путь к скачанному файлу.
    """
    
    # 2. Используем шаблон с ID для гарантированной уникальности
    output_template = os.path.join(DOWNLOAD_DIR, '%(title)s-%(id)s.%(ext)s')

    ydl_opts = {
        'outtmpl': output_template,
        # Используем более надежный формат, требующий слияния (если есть FFmpeg)
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 
        
        # Оставляем verbose для отладки, но обычно лучше использовать True
        'verbose': True, 
        'noprogress': True, 
        
        'keepvideo': True, 
        'noplaylist': True,
    }

    print("--- ЗАПУСК YT-DLP ---")
    
    # 3. Выполняем загрузку и получаем info_dict
    info_dict = await asyncio.to_thread(_perform_download_and_get_info, url, ydl_opts)
    
    print("--- КОНЕЦ ЛОГОВ YT-DLP ---")
    
    # 4. НАДЕЖНЫЙ ПОИСК ФИНАЛЬНОГО ПУТИ
    final_file_path = info_dict.get('_filename')
    
    if final_file_path and os.path.exists(final_file_path):
        print(f"Файл успешно скачан (из _filename): {final_file_path}")
        return final_file_path

    # --- FALLBACK: Если _filename не установлен (ваша текущая проблема) ---
    
    # Извлекаем необходимые данные для формирования пути
    video_title = info_dict.get('title', 'unknown_title')
    video_id = info_dict.get('id', 'unknown_id')
    # yt-dlp часто сам определяет расширение mp4, если мы указали его в format
    video_ext = info_dict.get('ext', 'mp4') 

    # Создаем ожидаемое имя файла, как в шаблоне: 'video/%(title)s-%(id)s.%(ext)s'
    # Применяем очистку, чтобы имитировать логику yt-dlp
    cleaned_title = clean_filename(video_title)
    expected_filename = f"{cleaned_title}-{video_id}.{video_ext}"
    final_file_path = os.path.join(DOWNLOAD_DIR, expected_filename)
    
    # Проверяем, существует ли файл по этому рассчитанному пути
    if os.path.exists(final_file_path):
        print(f"Файл успешно скачан (FALLBACK): {final_file_path}")
        return final_file_path
    else:
        # Если файл не найден даже по ожидаемому пути, значит, загрузка/слияние точно провалились.
        print(f"Файл не найден по пути: {final_file_path}")
        print("Проверьте, установлена ли программа 'ffmpeg' и доступна ли она в PATH.")
        raise FileNotFoundError(f"Файл не был найден после загрузки. Проверьте логи yt-dlp.")


def _perform_download_and_get_info(url: str, ydl_opts: dict) -> dict:
    """
    Синхронная функция для загрузки видео и возврата info_dict. 
    """
    with YoutubeDL(ydl_opts) as ydl:
        # download=True: выполняет загрузку, пост-процессинг и слияние
        info_dict = ydl.extract_info(url, download=True) 
        return info_dict