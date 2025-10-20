import aiohttp

async def send_link_to_service(
    service_url: str, 
    link: str
) -> dict:
    """Отправляет ссылку на FastAPI сервер и возвращает ответ JSON"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(service_url, json={"link": link}, timeout=10) as response:
                if response.status == 200:
                    return await response.json()
                return {"error": f"Server returned {response.status}"}
        except aiohttp.ClientError as e:
            return {"error": f"Connection error: {e}"}
        except Exception as e:
            return {"error": str(e)}