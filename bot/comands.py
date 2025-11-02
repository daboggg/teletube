from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        # BotCommand(
        #     command='help',
        #     description='ururu'
        # ),
        BotCommand(
            command='start',
            description='нажмите для старта'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())