from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import CommandStart

from asyncpg.exceptions import UniqueViolationError

from keyboards import start_keyboard
from loader import dp, db


@dp.message_handler(CommandStart(), chat_type=ChatType.PRIVATE)
async def send_start_message(message: Message):
    try:
        await db.create_user(message.from_user.id)
    except UniqueViolationError:
        return await message.answer('И снова здравствуйте!', reply_markup=start_keyboard)
    await message.answer('Привет!', reply_markup=start_keyboard)
