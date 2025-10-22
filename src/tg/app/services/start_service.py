from aiogram.types import Message
from utils import LogManager, read_metadata_json
from database import upsert_user

_logger = LogManager.new_logger("StartServiceLogger")

USERS = []


async def _load_metadata():
    data = await read_metadata_json("metadata.json")
    return {
        "answers": data["handlers"]["command_start"]["answers"],
        "abilities": "\n".join(data["abilities"]),
        "thanks": data["authors"]["thanks"],
        "authors": ",".join([el["name"] for el in data["authors"]["list"]]),
    }


async def get_hello_message(user_id: int) -> str:
    is_first_time = False
    data = await _load_metadata()
    if user_id not in USERS:
        USERS.append(user_id)
        _logger.info(f"Пользователь {user_id} в первый раз!")
        is_first_time = True

    thanks = data["thanks"].format(authors_list=data["authors"])

    if is_first_time:
        return data["answers"]["first_time"].format(
            abilities=data["abilities"], authors_info=thanks
        )

    return data["answers"]["returning_user"].format(
        name=user_id, abilities=data["abilities"], authors_info=thanks
    )


async def add_user(db, message: Message):
    tg_id = message.from_user.id
    username = message.from_user.username
    full_name = f"{message.from_user.last_name or ''} {message.from_user.first_name or ''}".strip()
    birthday = None
    await upsert_user(db, tg_id, username, full_name, birthday)
