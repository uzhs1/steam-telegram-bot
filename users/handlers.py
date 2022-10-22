from aiogram import Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Text

from .services import create_user

router = Router()

start_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton('Купить ключи'), types.KeyboardButton('Продать ключи')],
        [types.KeyboardButton('Цена ключа')],
        [types.KeyboardButton('Помощь')]
    ]
)

send_help_text = '''
Если не приходит обмен:
1. Проверьте настройки приватности, инвентарь должен быть Открытый.
2. При продаже ключей нашему боту, посмотрите не находятся ли ваши ключи в трейдбане.

Если также не приходят обмены или другие проблемы с ботом - обращаться к  @OrienS1
'''


@router.message(CommandStart())
async def send_welcome(message: types.Message, state: FSMContext):
    await state.clear()
    await create_user(message.from_user.id, message.from_user.username)
    await message.answer(text='Привет!', reply_markup=start_keyboard)


@router.message(Text(text='Помощь', ignore_case=True))
async def send_help_info(message: types.Message):
    await message.answer(text=send_help_text)
