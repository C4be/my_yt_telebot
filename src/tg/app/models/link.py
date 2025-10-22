from pydantic import BaseModel, HttpUrl, ValidationError


class LinkModel(BaseModel):
    link: HttpUrl


if __name__ == "__main__":
    try:
        data = LinkModel(link="https://example.com/test")
        print("Корректно:", data.link)
    except ValidationError as e:
        print("Ошибка:", e)
