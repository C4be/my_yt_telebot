import logging
from aiogram import Router, F
from aiogram.types import Message
from pydantic import ValidationError

from models.link import LinkModel
# from services.api_client import ping_fastapi_server

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

router = Router()


@router.message(
    F.text.regexp(r"^https?://")
    | (F.forward_from.as_("forwarded") & F.text.regexp(r"^https?://"))
    | (F.reply_to_message & F.reply_to_message.text.regexp(r"^https?://"))
)
async def links_handler(message: Message) -> None:
    try:
        link_data = LinkModel(link=message.text)
    except ValidationError as e:
        await message.answer("❌ Неверный формат ссылки. Пример: https://example.com")
        logger.warning(
            f"Ошибка валидации ссылки от пользователя {message.from_user.id}: {e}"
        )
        return

    logger.info(
        f"Получена корректная ссылка от {message.from_user.username or message.from_user.id}: {link_data.link}"
    )
    await message.answer(f"✅ Ссылка корректна: {link_data.link}")

    # --- Запал под запрос к FastAPI ---
    # try:
    #     result = await ping_fastapi_server("http://127.0.0.1:8000/api/check", str(link_data.link))
    #     logger.info(f"Ответ от сервера: {result}")
    # except Exception as e:
    #     logger.error(f"Ошибка при запросе к серверу: {e}")
