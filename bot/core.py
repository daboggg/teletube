from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage

from settings import settings


bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode='HTML', link_preview_is_disabled=True))
dp = Dispatcher(storage=MemoryStorage())
