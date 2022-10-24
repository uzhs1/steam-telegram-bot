from aiogram.types import Message, ChatType, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from steampy.exceptions import ConfirmationExpected

import config
import texts
import keyboards as key
from loader import dp, db
from states import SellKey
from trade import offers, binance_


@dp.message_handler(Text('Продать ключи'), chat_type=ChatType.PRIVATE)
async def sell_keys_start(message: Message):
    await message.answer(
        text=texts.send_trade_url, 
        disable_web_page_preview=True,
        reply_markup=key.back_to_menu
    )
    await SellKey.get_trade_link.set()


@dp.message_handler(state=SellKey.get_trade_link, chat_type=ChatType.PRIVATE)
async def get_link(message: Message, state: FSMContext):
    trade_link = message.text.strip()
    if trade_link.startswith('https://steamcommunity.com/tradeoffer/new/'):   # Минимальная валидация ссылки.
        count_keys_before_trade, _ = offers.get_keys_in_inventory()
        
        values = await db.get_values()
        user_sell_price = values.get('user_sell_price')

        balance = await binance_.get_balance()
        can_buy_number = round(balance // user_sell_price, 2)
        
        await message.answer(
            text=texts.send_need_keys.format(keys_number=can_buy_number)
        )
        await state.update_data(
            trade_link=trade_link,
            can_buy_keys=can_buy_number,
            count_keys_before_trade=count_keys_before_trade
        )
        return await SellKey.get_count_keys.set()

    await message.answer(text='Я не понимаю эту ссылку, попробуйте заново!')


@dp.message_handler(state=SellKey.get_count_keys, chat_type=ChatType.PRIVATE)
async def get_count_keys(message: Message, state: FSMContext):
    state_data = await state.get_data()
    can_buy_keys = state_data['can_buy_keys']
    user_count_keys = message.text.strip()

    if not user_count_keys.isdigit():
        return await message.answer('Отправьте число')

    if int(user_count_keys) >= can_buy_keys:
        return await message.answer(f'Вы не можете продать ключей больше чем {can_buy_keys}')

    if int(user_count_keys) < 10:
        return await message.answer(f'Вы не можете продать меньше 10 ключей')

    values = await db.get_values()
    price_for_user = round(values.get('user_sell_price') * int(user_count_keys), 2)
    await state.update_data(price_for_user=price_for_user, new_count_keys=int(user_count_keys))
    await message.answer(
        text=texts.end_sell_deal.format(
            keys_number=user_count_keys,
            price=price_for_user,
        )
    )
    return await SellKey.get_wallet.set()


@dp.message_handler(state=SellKey.get_wallet, chat_type=ChatType.PRIVATE)
async def get_wallet_handler(message: Message, state: FSMContext):
    wallet = message.text.strip()
    data = await state.get_data()
    new_count_keys = data['new_count_keys']
    try:
        user_asset_list = offers.create_buy_trade(new_count_keys, data['trade_link'])
        await state.update_data(
            user_wallet=wallet,
        )
    except (ConfirmationExpected, offers.UserDontHaveKeys) as e:
        print(e)
        await state.reset_data()
        await state.finish()
        return await message.answer(text='Мы не можем отправить вам трейд. Проверьте количество ключей на аккаунте или настройки приватности')

    await message.answer(
        f'Мы отправили вам обмен на {new_count_keys}, примите его.',
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Обмен подтвержден')]], resize_keyboard=True)
    )
    await SellKey.send_money.set()


@dp.message_handler(
    text='Обмен подтвержден',
    state=SellKey.send_money,
    chat_type=ChatType.PRIVATE
)
async def send_money(message: Message, state: FSMContext):
    data = await state.get_data()
    print(data['count_keys_before_trade'], data['new_count_keys'])
    trade_was_accepted = offers.check_trade_accepted(data['count_keys_before_trade'], data['new_count_keys'])
    if trade_was_accepted:
        money_was_send = await binance_.send_money(data['price_for_user'], data['user_wallet'])

        await state.reset_data()
        await state.finish()

        msg_text = 'В течении 10 минут средства поступят на ваш адрес! (Без учета комиссии)' \
            if money_was_send else 'Ошибка с отправкой средств. Обратитесь в поддержку'
        return await message.answer(msg_text, reply_markup=key.start_keyboard)
        
    return await message.answer('Трейд не подтвержден. Проверьте данные')
            