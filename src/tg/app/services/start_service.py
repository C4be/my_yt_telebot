from utils.files import read_metadata_json
from utils.my_log import LogManager


_logger = LogManager.new_logger("StartServiceLogger")


USERS = []


async def _load_metadata():
    data = await read_metadata_json("metadata.json")
    return {
        "answers": data["handlers"]["command_start"]["answers"],
        "abilities": "\n".join(data["abilities"]),
        "thanks": data["authors"]["thanks"],
        "authors": ",".join([el["name"] for el in data["authors"]["list"]])
    }


async def get_hello_message(user_id: int) -> str:
    is_first_time = False
    data = await _load_metadata()
    if user_id not in USERS:
        USERS.append(user_id)
        _logger.info(f"Пользователь {user_id} в первый раз!")
        is_first_time = True
    
    thanks = data["thanks"].format(authors_list = data["authors"])
    
    if is_first_time:
        return data["answers"]["first_time"].format(
            abilities = data["abilities"], 
            authors_info = thanks
        )
        
    return data["answers"]["returning_user"].format(
        name = user_id, 
        abilities = data["abilities"], 
        authors_info = thanks
    )
        

