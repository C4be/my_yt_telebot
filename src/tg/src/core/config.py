import os
from pathlib import Path
from dotenv import load_dotenv

# ===== Paths =====
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
LOGS_BASE_DIR: Path = BASE_DIR / "logs"

# ===== Load secrets =====
if os.getenv("FROM_DOCKER", "NO") == "YES":
    load_dotenv(BASE_DIR / "secrets" / "bot.env", override=True)
    load_dotenv(BASE_DIR / "secrets" / "db.env", override=True)

# ===== Telegram =====
BOT_TOKEN: str | None = os.getenv("BOT_TOKEN", None)
if not BOT_TOKEN:
    raise ValueError("❌ Не найден BOT_TOKEN в *.env или переменных окружения")

# ===== Logs =====
LOGS_DATE_DIR_FORMAT: str = "%d-%m-%Y"  # формат имени директории логов
LOGS_DATE_TIME_FROMAT: str = "%Y-%m-%d %H:%M:%S"  # формат метки времени в логе
LOGS_LOG_FROMAT: str = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
LOGS_ENCODING: str = "utf-8"

# ===== DB =====
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "yt_telebot")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ===== Strings Templates =====
COMMAND_USE: str = "Команда {command} поступила от {user_name}[{user_id}]"
START_INFO: str = """
Привет! Я тебя ещё не знаю, но надеюсь, что смогу тебе помочь! 💪

Я умею делать разные вещи:

1. Пришли мне ссылку на ролик.
2. Пришли мне видео ролик.
3. Можешь мне переслать видео или ссылку из другого чата.
4. /start — начать диалог.
5. /help — список основных команд.
6. /status — статус выполнения задач.
7. /link_channel — подключение канала загрузки.
8. /unlink_channel — отвязывание канала загрузки.
9. /links - основные ссылки

Давай начнём наше приключение!

Большое спасибо разработчикам: Dmitry Gimazetdinov, что создали меня!
"""
HELP_INFO: str = """
Привет, я твой помошник!
"""
CONTACTS_INFO: str = """
Контакты
Автор: "Dmitry Gimazetdinov"
TG: @C4be74
TG Channel: @devwhoami
YT: ...
"""
