from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

import keyboards
from loader import dp


@dp.message_handler(
    Text('Главное меню'), 
    state='*', 
    chat_type=ChatType.PRIVATE
)
async def back_to_menu(message: Message, state: FSMContext = None):
    if state:
        await state.reset_data()
        await state.finish()

    return await message.answer(
        text='Возвращаюсь в главное меню',
        reply_markup=keyboards.start_keyboard
    )