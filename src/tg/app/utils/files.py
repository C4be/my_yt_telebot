from typing import Any
from pathlib import Path
import aiofiles
import json


async def read_metadata(path: Path) -> Any:
    async with aiofiles.open(path, mode="r", encoding="utf-8") as f:
        text = await f.read()
        data = json.loads(text)
    return data


# if __name__ == "__main__":
#     # Example Usage
#     import asyncio
#     async def main():
#         path = Path("metadata.json")
#         data = await read_metadata(path)
#         print(data)
#     asyncio.run(main())
