import asyncio
import logging

from aiogram import Bot, Dispatcher

from db import base, models
from config import app_config
from users import handlers

# Basic bot configuration
logging.basicConfig(level=logging.INFO)
bot = Bot(token=app_config.bot_token.get_secret_value())
dp = Dispatcher()


async def main():
    dp.include_router(handlers.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
