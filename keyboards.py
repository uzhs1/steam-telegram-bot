from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton('Купить ключи'), KeyboardButton('Продать ключи')],
        [KeyboardButton('Личный кабинет')],
        [KeyboardButton('Цена ключа')],
        [KeyboardButton('Помощь')]
    ],
    resize_keyboard=True
)

replenish_balance = ReplyKeyboardMarkup(
    [
        [KeyboardButton('Пополнить баланс')],
        [KeyboardButton('Главное меню')]
    ],
    resize_keyboard=True
)

back_to_menu = ReplyKeyboardMarkup(
    [
        [KeyboardButton('Главное меню')]
    ],
    resize_keyboard=True
)

accept_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton('Подтвердить оплату')]], resize_keyboard=True
)

admin_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton('Изменить цену продажи ключа'), KeyboardButton('Изменить цену покупки ключа')],
        [
            KeyboardButton('Изменить максимальное число ключей для покупки'),
            KeyboardButton('Изменить максимальное число ключей для продажи')
        ],
        [KeyboardButton('Заработали за день'), KeyboardButton('Заработали за месяц')]
    ],
    resize_keyboard=True
)