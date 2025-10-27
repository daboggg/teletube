import logging

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

logger = logging.getLogger(__name__)
cmd_router = Router()


# отрабатывает по команде /start
@cmd_router.message(CommandStart())
async def start_cmd(message:Message) -> None:
    await message.answer('ку-ку')


# # отрабатывает по команде /help
@cmd_router.message(Command(commands="help"))
async def list_reminders(message:Message) -> None:
    await message.answer('какая-то помощь :)')
