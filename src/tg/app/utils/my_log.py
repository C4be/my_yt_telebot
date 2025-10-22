import shutil
import logging
from pathlib import Path
from datetime import datetime


class LogManager:
    """
    Утилитарный класс для создания логгеров.
    Автоматически создаёт директории:
      logs/<DD-MM-YYYY>/<logger_name>.log
    """

    _BASE_DIR = Path("logs")
    _TIME_FROMAT = "%d-%m-%Y"
    _DATE_TIME_FROMAT = "%Y-%m-%d %H:%M:%S"
    _LOG_FROMAT = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
    _ENCODING = "utf-8"

    @staticmethod
    def _get_daily_log_dir() -> Path:
        """Возвращает директорию текущего дня, создавая её при необходимости."""
        date_str = datetime.now().strftime(LogManager._TIME_FROMAT)
        daily_dir = LogManager._BASE_DIR / date_str
        daily_dir.mkdir(parents=True, exist_ok=True)
        return daily_dir

    @staticmethod
    def new_logger(
        name: str, to_file: bool = True, level: int = logging.INFO
    ) -> logging.Logger:
        """
        Создаёт новый логгер с именем `name`.

        :param name: Имя логгера
        :param to_file: Если True — создаёт лог-файл
        :param level: Уровень логирования
        :return: logging.Logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Не добавляем дублирующиеся хендлеры
        if logger.handlers:
            return logger

        formatter = logging.Formatter(
            LogManager._LOG_FROMAT,
            datefmt=LogManager._DATE_TIME_FROMAT,
        )

        # === Консольный вывод ===
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # === Файловый вывод (если требуется) ===
        if to_file:
            daily_dir = LogManager._get_daily_log_dir()
            log_path = daily_dir / f"{name}.log"

            file_handler = logging.FileHandler(log_path, encoding=LogManager._ENCODING)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    @staticmethod
    def clear_old_logs() -> None:
        """Удаляет все логи, кроме сегодняшней директории."""
        today = datetime.now().strftime(LogManager._TIME_FROMAT)

        if not LogManager._BASE_DIR.exists():
            print("Папка logs не существует — ничего не удалено.")
            return

        for directory in LogManager._BASE_DIR.iterdir():
            if directory.is_dir() and directory.name != today:
                shutil.rmtree(directory, ignore_errors=True)
                print(f"🗑️ Удалена папка логов: {directory.name}")

        print("✅ Старые логи очищены, сегодняшние сохранены.")
