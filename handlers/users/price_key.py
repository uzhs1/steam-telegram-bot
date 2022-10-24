from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import Text

import config
import texts
from loader import dp, db
from trade import offers, binance_


@dp.message_handler(Text('Цена ключа'), chat_type=ChatType.PRIVATE)
async def key_price_info(message: Message):
    values = await db.get_values()
    user_buy_price = values.get('user_buy_price')
    user_sell_price = values.get('user_sell_price')
    count_keys, _ = offers.get_keys_in_inventory()
    balance = await binance_.get_balance()
    can_buy_number = round(balance // user_sell_price, 2)
    await message.answer(
        text=texts.price_key.format(
            user_sell_price=user_sell_price,
            user_buy_price=user_buy_price,
            can_buy=can_buy_number,
            have_keys=count_keys
        )
    )
