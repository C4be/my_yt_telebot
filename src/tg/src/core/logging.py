import asyncio
import shutil
import logging
from typing import List, Tuple
from pathlib import Path
from datetime import datetime
from aiogram.types import Message

from core.config import (
    LOGS_ENCODING,
    LOGS_DATE_TIME_FROMAT,
    LOGS_BASE_DIR,
    LOGS_LOG_FROMAT,
    LOGS_DATE_DIR_FORMAT,
    COMMAND_USE,
)

_LOGGER_CACHE: dict[str, logging.Logger] = {}


def ensure_log_directories() -> None:
    """
    Синхронно создаёт базовую директорию для логов и
    директорию текущего дня (если их нет).
    Вызывать один раз при старте приложения.
    """
    base_dir = Path(LOGS_BASE_DIR)
    daily_dir = base_dir / datetime.now().strftime(LOGS_DATE_DIR_FORMAT)
    base_dir.mkdir(parents=True, exist_ok=True)
    daily_dir.mkdir(parents=True, exist_ok=True)


def _get_daily_log_dir() -> Path:
    """Возвращает директорию для текущего дня."""
    date_str = datetime.now().strftime(LOGS_DATE_DIR_FORMAT)
    return Path(LOGS_BASE_DIR) / date_str


def new_logger(
    name: str, to_file: bool = True, level: int = logging.INFO
) -> logging.Logger:
    """
    Создаёт и возвращает настроенный логгер для компонента.
    Использовать через: `logger = new_logger(__name__)`
    """
    if name in _LOGGER_CACHE:
        return _LOGGER_CACHE[name]

    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(LOGS_LOG_FROMAT, datefmt=LOGS_DATE_TIME_FROMAT)

    # === Консоль ===
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # === Файл ===
    if to_file:
        try:
            daily_dir = _get_daily_log_dir()
            log_path = daily_dir / f"{name}.log"
            file_handler = logging.FileHandler(log_path, encoding=LOGS_ENCODING)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except OSError as e:
            logger.warning(f"⚠️ Не удалось создать файл логов {log_path}: {e}")

    _LOGGER_CACHE[name] = logger
    return logger


async def clear_old_logs(keep_days: int = 1) -> Tuple[str, bool]:
    """
    Асинхронно удаляет старые директории логов, оставляя последние `keep_days`.
    """
    base = Path(LOGS_BASE_DIR)
    if not base.exists():
        return "Папка логов отсутствует — ничего не удалено.", False

    dirs = sorted(
        [d for d in base.iterdir() if d.is_dir()], key=lambda p: p.name, reverse=True
    )
    today = datetime.now().strftime(LOGS_DATE_DIR_FORMAT)
    deleted: List[str] = []

    loop = asyncio.get_running_loop()

    for directory in dirs[keep_days:]:
        if directory.name != today:
            try:
                await loop.run_in_executor(None, shutil.rmtree, directory)
                deleted.append(f"🗑️ Удалена папка логов: {directory.name}")
            except Exception as e:
                deleted.append(f"⚠️ Ошибка при удалении {directory.name}: {e}")

    deleted.append("✅ Очистка завершена.")
    return "\n".join(deleted), True


def get_command_use_str(command: str, message: Message) -> str:
    user_name: str = message.from_user.username
    user_id: int = message.from_user.id
    return COMMAND_USE.format(
        command=command,
        user_name=user_name,
        user_id=user_id,
    )
