from aiogram.dispatcher.filters.state import State, StatesGroup


class BuyKey(StatesGroup):
    get_trade_link = State()
    get_count_keys = State()
    get_txid = State()


class SellKey(StatesGroup):
    get_trade_link = State()
    get_count_keys = State()
    get_wallet = State()
    send_money = State()


class ChangeSellPrice(StatesGroup):
    get_new_price = State()


class ChangeBuyPrice(StatesGroup):
    get_new_price = State()


class ChangeMaxBuyKeys(StatesGroup):
    get_new_number = State()


class ChangeMaxSellKeys(StatesGroup):
    get_new_number = State()


class ReplenishBalance(StatesGroup):
    get_tx_id = State()
