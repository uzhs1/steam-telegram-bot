from aiogram import executor

import handlers
from loader import dp, db


async def on_startup(dp):
    await db.create_table()
    await db.create_values_table()
    await db.create_table_offers()
    await db.insert_default_values()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
