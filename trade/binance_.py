from binance.exceptions import BinanceAPIException
from typing import Optional

from loader import binance_client, db


async def _check_last_tx_ids(tx_id: str) -> bool:
    response = await db.check_transactions(tx_id)
    return response.split()[-1] != '0'


def _format_amount(amount: str) -> bool:
    try:
        amount = int(amount)
    except ValueError:
        amount = float(amount)
    return amount


async def check_deposit(tx_id: str) -> Optional[bool | None]:
    have_txid = await _check_last_tx_ids(tx_id)
    print(have_txid)
    if not have_txid:
        all_deposits = binance_client.get_deposit_history(coin='USDT')
        for deposit in all_deposits:
            print(deposit)
            if deposit['txId'] == tx_id:
                amount = _format_amount(deposit['amount'])
                return amount


async def get_balance() -> float:
    balances = binance_client.get_account()
    for balance in balances['balances']:
        if balance['asset'] == 'USDT':
            return float(balance['free'])


async def send_money(money: float, address: str) -> bool:
    try:
        result = binance_client.withdraw(
            coin='USDT',
            address=address,
            amount=money,
            network='TRX',
            transactionFeeFlag=True
        )
        print(result)
    except BinanceAPIException as e:
        print(e)
        return False
    return True


