from typing import Any, Optional
from pathlib import Path
import aiofiles
import json
from utils.my_log import LogManager


_logger = LogManager.new_logger("FileManager", to_file=True)


async def read_metadata_json(path: Path) -> Optional[Any]:
    """
    Безопасно читает JSON-файл и возвращает его содержимое.
    Возвращает None, если файл не найден или повреждён.
    """
    try:
        async with aiofiles.open(path, mode="r", encoding="utf-8") as f:
            text = await f.read()
            data = json.loads(text)
            _logger.info(f"Файл `{path}` успешно загружен!")
            return data

    except FileNotFoundError:
        _logger.error(f"Файл `{path}` не найден.")
    except json.JSONDecodeError as e:
        _logger.error(f"Ошибка парсинга JSON (`{path}`): {e}")
    except Exception as e:
        _logger.exception(f"Неизвестная ошибка при чтении `{path}`: {e}")

    return None
