import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs

from config_data.config import load_config, Config
from handlers.user_handlers import user_router
from dialogs.start_dialog.dialogs import start_dialog
from dialogs.admin_dialog.dialogs import admin_dialog
from database.db_conf import database

format = '[{asctime}] #{levelname:8} {filename}:' \
         '{lineno} - {name} - {message}'

logging.basicConfig(
    level=logging.DEBUG,
    format=format,
    style='{'
)

#db = database('users')
#db.delete_data()

logger = logging.getLogger(__name__)

config: Config = load_config()


async def main():
    bot = Bot(token=config.bot.token, parse_mode='HTML')
    dp = Dispatcher()

    # подключаем роутеры
    dp.include_routers(user_router, admin_dialog, start_dialog)
    # подключаем middleware

    # запуск

    await bot.delete_webhook(drop_pending_updates=True)
    setup_dialogs(dp)
    logger.info('Bot start polling')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())