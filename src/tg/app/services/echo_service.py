from aiogram.types import Message

from utils import LogManager, read_metadata_json


_logger = LogManager.new_logger("EchoService")


async def _load_metadata():
    data = await read_metadata_json("metadata.json")
    echo_handler_words = data["handlers"]["echo_handler"]
    return {
        "answer": echo_handler_words["answer"],
        "types": echo_handler_words["types"],
    }


async def get_echo_answer(message: Message) -> str:
    words = await _load_metadata()
    answer, types = words["answer"], words["types"]

    message_type = types["unknown"]
    if message.photo:
        message_type = types["photo"]
    elif message.sticker:
        message_type = types["sticker"]
    elif message.voice:
        message_type = types["voice"]
    elif message.audio:
        message_type = types["audio"]
    elif message.animation:
        message_type = types["animation"]
    elif message.location:
        message_type = types["location"]

    return answer.format(type=message_type)
