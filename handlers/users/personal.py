from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

import keyboards
import texts
import states
from trade.binance_ import check_deposit
from loader import dp, db


@dp.message_handler(Text('Личный кабинет'), chat_type=ChatType.PRIVATE)
async def send_start_message(message: Message):
    response = await db.get_balance(message.from_user.id)
    balance = response['balance']
    await message.answer(f'Ваш баланс: {balance} $', reply_markup=keyboards.replenish_balance)


@dp.message_handler(Text('Пополнить баланс'), chat_type=ChatType.PRIVATE, state='*')
async def balance_handler(message: Message, state: FSMContext = None):
    if state: 
        await state.reset_data()
        await state.finish()
        
    await message.answer(text=texts.end_buy_deal, reply_markup=keyboards.back_to_menu)
    await states.ReplenishBalance.get_tx_id.set()


@dp.message_handler(state=states.ReplenishBalance.get_tx_id, chat_type=ChatType.PRIVATE)
async def update_balance(message: Message, state: FSMContext):
    amount = await check_deposit(message.text.strip())
    if amount:
        await db.update_transaction(message.from_user.id, message.text.strip())
        await db.plus_balance(message.from_user.id, amount)
        await message.answer(
            text=f'Ваш баланс успешно пополнен на {amount} $.',
            reply_markup=keyboards.start_keyboard
        )
        return await state.finish()

    await message.answer(text='Транзакция не найдена или же ей уже оплачивали.')
