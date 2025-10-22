from utils import LogManager, read_metadata_json


_logger = LogManager.new_logger("HelpService")


async def _load_metadata():
    data = await read_metadata_json("metadata.json")
    return {
        "answers": data["handlers"]["command_help"]["answers"],
        "abilities": "\n".join(data["abilities"]),
    }


async def get_help_message() -> str:
    data = await _load_metadata()
    return data["answers"]["default"].format(abilities=data["abilities"])
