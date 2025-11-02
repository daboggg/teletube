import asyncio
import logging

from bot.comands import set_commands
from bot.core import dp, bot
from bot.handlers.cmd import cmd_router
from bot.handlers.main import main_router
from settings import settings


async def start_bot():
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')


async def stop_bot():
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s - %(name)s - '
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'

                        )
    logger = logging.getLogger(__name__)


    # подключение роутеров
    dp.include_routers(
        cmd_router,
        main_router
    )

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    logger.info("Бот запущен!")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
