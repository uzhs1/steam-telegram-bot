import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from binance.client import Client

from steampy.client import SteamClient

import config
from db import Database

# Telegram bot
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s -%(name)s - %(message)s'
)

loop = asyncio.get_event_loop()

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# Binance
binance_client = Client(config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY)

# Steam
# steam_client = SteamClient(config.STEAM_API_KEY)
# steam_client.login(config.STEAM_LOGIN, config.STEAM_PASSWORD, 'steam_guard.json')

first_steam_acc = SteamClient(config.STEAM_FIRST_API_KEY)
first_steam_acc.login(config.STEAM_FIRST_LOGIN, config.STEAM_FIRST_PASSWORD, 'steam_1acc.json')

# second_steam_acc = SteamClient(config.STEAM_SECOND_API_KEY)
# second_steam_acc.login(config.STEAM_SECOND_LOGIN, config.STEAM_SECOND_PASSWORD, 'steam_1acc.json')

# Database
db = loop.run_until_complete(Database.create())
