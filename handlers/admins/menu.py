from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import Text, CommandStart
from aiogram.dispatcher.storage import FSMContext

import states
import config
import keyboards
from loader import dp, db


admins_id = [628554250, 675402103]


@dp.message_handler(
    CommandStart(),
    user_id=admins_id
)
async def start_admin(message: Message):
    await message.answer(
        text='Привет хозяин!',
        reply_markup=keyboards.admin_keyboard
    )


@dp.message_handler(
    Text('Изменить цену продажи ключа'), 
    chat_type=ChatType.PRIVATE,
    user_id=admins_id
)
async def change_sell_price(message: Message):
    await message.answer(text='Отправьте новую цену')
    await states.ChangeSellPrice.get_new_price.set()


@dp.message_handler(
    state=states.ChangeSellPrice.get_new_price,
    chat_type=ChatType.PRIVATE,
    user_id=admins_id
)
async def new_price_set(message: Message, state: FSMContext):
    new_price = float(message.text)
    await db.update_user_sell_price(new_price)
    await message.answer(text='Цена успешно изменена.')
    await state.finish()


@dp.message_handler(
    Text('Изменить цену покупки ключа'), 
    chat_type=ChatType.PRIVATE,
    user_id=admins_id
)
async def change_buy_price(message: Message):
    await message.answer(text='Отправьте новую цену')
    await states.ChangeBuyPrice.get_new_price.set()


@dp.message_handler(
    state=states.ChangeBuyPrice.get_new_price,
    chat_type=ChatType.PRIVATE,
    user_id=admins_id
)
async def new_buy_price_set(message: Message, state: FSMContext):
    new_price = float(message.text)
    await db.update_user_buy_price(new_price)
    await message.answer(text='Цена успешно изменена.')
    await state.finish()


@dp.message_handler(
    Text('Изменить максимальное число ключей для покупки'),
    chat_type=ChatType.PRIVATE,
    user_id=admins_id
)
async def change_sell_price(message: Message):
    await message.answer(text='Отправьте новую число')
    await states.ChangeMaxBuyKeys.get_new_number.set()


@dp.message_handler(
    state=states.ChangeMaxBuyKeys.get_new_number,
    chat_type=ChatType.PRIVATE,
    user_id=admins_id
)
async def new_price_set(message: Message, state: FSMContext):
    new_number = float(message.text)
    await db.update_user_max_buy(new_number)
    await message.answer(text='Количество успешно изменено.')
    await state.finish()


@dp.message_handler(
    Text('Изменить максимальное число ключей для продажи'),
    chat_type=ChatType.PRIVATE,
    user_id=admins_id
)
async def change_buy_price(message: Message):
    await message.answer(text='Отправьте новую цену')
    await states.ChangeMaxSellKeys.get_new_number.set()


@dp.message_handler(
    state=states.ChangeMaxSellKeys.get_new_number,
    chat_type=ChatType.PRIVATE,
    user_id=admins_id
)
async def new_buy_price_set(message: Message, state: FSMContext):
    new_number = float(message.text)
    await db.update_user_max_buy(new_number)
    await message.answer(text='Количество успешно изменено.')
    await state.finish()

