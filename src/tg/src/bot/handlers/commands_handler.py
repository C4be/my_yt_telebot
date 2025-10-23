from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.logging import new_logger, get_command_use_str
from core.config import START_INFO, HELP_INFO, CONTACTS_INFO
from db import get_db_session
from domain.services import UserService

# constants
__COMMAND: str = "commands"
__NAME: str = f"{__COMMAND}_handler"
__LOGGER: str = new_logger(name=__NAME, to_file=False)

router = Router(name=__NAME)


@router.message(Command("start"))
async def start_message(message: Message) -> None:
    # log info about command
    __LOGGER.info(get_command_use_str(command="__COMMAND[\start]", message=message))

    # add user
    async for db_session in get_db_session():
        user = await UserService.create_user(
            db=db_session,
            tg_id=message.from_user.id,
            nickname=message.from_user.username or f"user_{message.from_user.id}",
            age=None,
        )
        __LOGGER.info(f"Добавлен или уже есть пользователь {user}")
        break

    await message.answer(START_INFO)


@router.message(Command("help"))
async def help_message(message: Message) -> None:
    # log info about command
    __LOGGER.info(get_command_use_str(command="__COMMAND[\help]", message=message))
    await message.answer(HELP_INFO)


@router.message(Command("contacts"))
async def contact_message(message: Message) -> None:
    # log info about command
    __LOGGER.info(get_command_use_str(command="__COMMAND[\contacts]", message=message))
    await message.answer(CONTACTS_INFO)
