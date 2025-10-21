from moviepy import *
import os
import shutil
from random import randint as rnd


# Заменить на ffmpeg
def split_video(input_path: str, chunk_duration: int = 30, min_duration: int = 20) -> list[str]:
    """
    Делит исходное видео на клипы заданной длительности и возвращает 
    список путей к файлам, которые длиннее минимальной длительности.

    :param input_path: Путь к исходному видеофайлу.
    :param chunk_duration: Максимальная длительность одного фрагмента (в секундах).
    :param min_duration: Минимальная длительность фрагмента для включения в результат (в секундах).
    :return: Список путей к созданным клипам.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Исходный файл не найден: {input_path}")

    output_dir = os.path.join(os.path.dirname(input_path), "chunks")
    os.makedirs(output_dir, exist_ok=True)
    
    output_files = []

    with VideoFileClip(input_path) as clip:
        duration = clip.duration
        
        for i in range(0, int(duration), chunk_duration):
            start_time = i
            end_time = min(i + chunk_duration, duration)
            
            # Проверяем, что фрагмент достаточно длинный
            if (end_time - start_time) >= min_duration:
                # Определяем путь для сохранения фрагмента
                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_filename = f"{base_name}_chunk_{i:04d}s.mp4"
                output_path = os.path.join(output_dir, output_filename)
                
                # Создаем и сохраняем фрагмент
                try:
                    subclip = clip.subclipped(start_time, end_time)
                    subclip.write_videofile(
                        output_path, 
                        codec='libx264', 
                        audio_codec='aac', 
                        temp_audiofile='temp-audio.m4a', 
                        remove_temp=True, 
                        # N.B. threads=4, verbose=False можно добавить для оптимизации
                    )
                    output_files.append(output_path)
                except Exception as e:
                    print(f"Ошибка при обработке фрагмента {i}s: {e}")

    return output_files

## 2. Перевод видео из горизонтального в вертикальный формат

def convert_to_vertical(input_path: str, output_path: str, aspect_ratio: float = 9/16) -> str:
    """
    Конвертирует видео из горизонтального в вертикальный формат, 
    обрезая его по центру.

    :param input_path: Путь к исходному видеофайлу.
    :param output_path: Путь для сохранения вертикального видео.
    :param aspect_ratio: Требуемое соотношение сторон (по умолчанию 9/16).
    :return: Путь к сохраненному файлу.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Исходный файл не найден: {input_path}")

    with VideoFileClip(input_path) as clip:
        original_width, original_height = clip.size
        
        # 1. Рассчитываем новую высоту для вертикального формата (9:16)
        # Новая ширина = оригинальная высота (мы поворачиваем или берем высоту как базу)
        # Или, если мы хотим обрезать из центра:
        target_height = original_height
        target_width = int(target_height * aspect_ratio) # e.g., 1080 * 9/16 ≈ 607
        
        # 2. Определяем область для центральной обрезки
        # Координаты X для центральной части
        center_x = original_width / 2
        x1 = center_x - (target_width / 2)
        x2 = center_x + (target_width / 2)
        
        # 3. Обрезаем и сохраняем
        cropped_clip = clip.cropped(x1=x1, y1=0, x2=x2, y2=original_height)
        
        # Устанавливаем целевой размер (например, 1080x1920, если исходная высота 1080)
        final_size = (target_width, target_height)
        
        print(f"Конвертация: {clip.size} -> {final_size} (обрезка по центру)")

        cropped_clip.write_videofile(
            output_path + f"{rnd(1, 20)}" + ".mp4", 
            codec='libx264', 
            audio_codec='aac', 
            temp_audiofile='temp-vertical-audio.m4a',
            remove_temp=True,
            # Можно установить битрейт, чтобы избежать потери качества: bitrate='5000k'
        )

    return output_path

## 3. Пайплайн обработки видео

def video_processing_pipeline(input_video_path: str) -> list[str]:
    """
    Пайплайн: разбивает видео на 30-секундные клипы и конвертирует каждый в вертикальный формат.

    :param input_video_path: Путь к исходному видеофайлу.
    :return: Список путей к финальным вертикальным клипам.
    """
    if not os.path.exists(input_video_path):
        raise FileNotFoundError(f"Исходный файл не найден: {input_video_path}")

    base_dir = os.path.dirname(input_video_path)
    # Создаем директорию для финальных вертикальных клипов
    vertical_output_dir = os.path.join(base_dir, "vertical_clips")
    os.makedirs(vertical_output_dir, exist_ok=True)
    
    print(f"--- Шаг 1: Разбиение видео на фрагменты (мин. 20 секунд) ---")
    
    # Шаг 1: Разбиваем видео
    # Возвращает список путей к клипам в папке 'chunks'
    chunk_paths = split_video(input_video_path, chunk_duration=30, min_duration=20)
    
    if not chunk_paths:
        print("Не найдено фрагментов, подходящих по минимальной длительности (20 секунд).")
        return []

    final_vertical_paths = []
    
    print(f"\n--- Шаг 2: Конвертация {len(chunk_paths)} фрагментов в вертикальный формат ---")

    # Шаг 2: Последовательно конвертируем каждый фрагмент
    for i, chunk_path in enumerate(chunk_paths):
        print(f"Обработка фрагмента {i+1}/{len(chunk_paths)}: {os.path.basename(chunk_path)}")
        
        # Определяем имя для выходного вертикального файла
        base_name = os.path.splitext(os.path.basename(chunk_path))[0]
        vertical_filename = f"video/dog.mp4"
        vertical_output_path = f"video_shorts/file"
        
        try:
            # Конвертируем фрагмент
            result_path = convert_to_vertical(chunk_path, vertical_output_path)
            final_vertical_paths.append(result_path)
            print(f"Готово. Сохранено в: {os.path.basename(result_path)}")
            
        except Exception as e:
            print(f"Произошла ошибка при конвертации фрагмента {os.path.basename(chunk_path)}: {e}")
            
    # Очистка: Удаляем временную папку с горизонтальными фрагментами
    # Предполагая, что 'chunks' находится рядом с исходным видео
    chunks_dir = os.path.join(base_dir, "chunks")
    if os.path.exists(chunks_dir):
        shutil.rmtree(chunks_dir)
        print(f"\nОчистка: Удалена временная папка {chunks_dir}")

    print("\n--- Пайплайн завершен ---")
    return final_vertical_paths