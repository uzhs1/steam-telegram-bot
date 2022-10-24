from typing import Optional

from steampy.client import Asset
from steampy.utils import GameOptions, get_key_value_from_url, account_id_to_steam_id

from loader import steam_client

GAME = GameOptions.TF2
MARKET_HASH_NAME = 'Mann Co. Supply Crate Key'


class UserDontHaveKeys(Exception):
   pass


def get_inventory_items(user_offer_link: Optional[str | None] = None) -> dict:
   if user_offer_link:
      partner_account_id = get_key_value_from_url(user_offer_link, 'partner', True)
      partner_steam_id = account_id_to_steam_id(partner_account_id)
      return steam_client.get_partner_inventory(partner_steam_id, GAME)
   return steam_client.get_my_inventory(GAME)


def get_keys_in_inventory(user_offer_link: Optional[str | None] = None) -> tuple:
   inventory = get_inventory_items(user_offer_link)
   count_keys = 0
   keys_list = []
   for item in inventory.values():
      if item['market_hash_name'] == MARKET_HASH_NAME:
         count_keys += 1
         keys_list.append(item['id'])
   return count_keys, keys_list


def check_trade_accepted(count_keys_before: int, new_count_keys: int) -> bool:
   count_keys_after, _ = get_keys_in_inventory()
   return count_keys_before <= (count_keys_after - new_count_keys)


def create_sell_trade(my_keys: int, user_offer_link: str) -> None:
   _, my_keys_id = get_keys_in_inventory()
   my_asset_list = [Asset(key_id, game=GAME) for key_id in my_keys_id[:my_keys]]
   user_asset_list = []
   result = steam_client.make_offer_with_url(my_asset_list, user_asset_list, user_offer_link)
   print(result)
   

def create_buy_trade(user_keys: int, user_offer_link: str) -> None:
   count_keys, keys_list = get_keys_in_inventory(user_offer_link)
   if user_keys > count_keys:
      raise UserDontHaveKeys('На аккаунте меньше ключей чем вы указали.')

   my_asset_list = []
   user_asset_list = [Asset(key_id, game=GAME) for key_id in keys_list[:user_keys]]
   steam_client.make_offer_with_url(my_asset_list, user_asset_list, user_offer_link)
   return [key_id for key_id in keys_list[:user_keys]]


def check_trade():
   pass