from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from steampy.exceptions import ConfirmationExpected

import config
import texts
import keyboards
from loader import dp, db
from trade import offers, binance_
from states import BuyKey


@dp.message_handler(Text('Купить ключи'), chat_type=ChatType.PRIVATE)
async def start_buying_key(message: Message):
    await message.answer(
        text=texts.send_trade_url, 
        disable_web_page_preview=True,
        reply_markup=keyboards.back_to_menu
    )
    await BuyKey.get_trade_link.set()


@dp.message_handler(state=BuyKey.get_trade_link, chat_type=ChatType.PRIVATE)
async def get_trade_link(message: Message, state: FSMContext):
    trade_link = message.text.strip()
    if trade_link.startswith('https://steamcommunity.com/tradeoffer/new/'):   # Минимальная валидация ссылки.
        max_buy_keys, _ = offers.get_keys_in_inventory()
        await message.answer(text=texts.send_need_keys.format(keys_number=max_buy_keys))
        await state.update_data(trade_link=trade_link, keys_in_inventory=max_buy_keys)
        return await BuyKey.get_count_keys.set()

    await message.answer(text='Я не понимаю эту ссылку, попробуйте заново!')


@dp.message_handler(state=BuyKey.get_count_keys, chat_type=ChatType.PRIVATE)
async def get_count_keys(message: Message, state: FSMContext):
    state_data = await state.get_data()
    keys_in_inventory = state_data['keys_in_inventory']
    user_count_keys = message.text.strip()

    if not user_count_keys.isdigit():
        return await message.answer('Отправьте число')

    if int(user_count_keys) >= keys_in_inventory:
        return await message.answer(f'Вы не можете купить ключей больше чем {keys_in_inventory}')

    if int(user_count_keys) < 10:
        return await message.answer(f'Вы не можете купить меньше 10 ключей')

    values = await db.get_values()
    price_for_user = round(values.get('user_buy_price') * int(user_count_keys), 2)
    response = await db.get_balance(message.from_user.id)
    balance = response['balance']
    if balance >= price_for_user:
        try:
            await state.finish()
            await state.reset_data()
            offers.create_sell_trade(
                int(user_count_keys), state_data['trade_link']
            )
            await db.minus_balance(message.from_user.id, price_for_user)
        except ConfirmationExpected:
            return await message.answer('Мы не можем отправить вам трейд. Проверьте настройки аккаунта.')

        return await message.answer(text='Обмен отправлен!')

    need_balance = price_for_user - balance
    await message.answer(f'На балансе недостаточно средств, не хватет {need_balance} $', reply_markup=keyboards.replenish_balance)

