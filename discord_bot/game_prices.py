"""
Interacts with the IsThereAnyDeal API to get game prices.
"""

from typing import Optional, Dict, List
from discord_bot.itad_api import ITADApi

api = ITADApi()


class GamePrice:
    def __init__(self, **kwargs):
        # ITAD sometimes gives us prices with more than 2 decimal places, so round em
        self.price_new: float = self._round_price(kwargs.get("price_new"))
        self.price_old: float = self._round_price(kwargs.get("price_old"))
        self.percent_off: int = kwargs.get("price_cut")
        self.url: str = kwargs.get("url")

    @staticmethod
    def _round_price(price: Optional[float]) -> Optional[float]:
        if price:
            return round(price, 2)
        return None


def get_id_from_game_title(title: str) -> Optional[str]:
    """Gets the 'plain' ID from ITAD for a given game title.
    :return Plain ID if found, otherwise None.
    :raises Exception if ITAD API is unresponsive or returns unexpected response.
    """
    resp = api.get_plain(title)
    resp_data = resp.json()

    if resp_data[".meta"]["match"] == "title":
        return resp_data["data"]["plain"]
    else:
        return None


def get_prices_for_games(plains: List[str]) -> Dict[str, List[GamePrice]]:
    """Gets a list of prices from various stores for games.
    :return Map of plain strings to a list of game prices from various stores.
    :throws Exception if ITAD API is unavailable.
    """
    resp = api.get_prices(",".join(plains))
    resp_data = resp.json()

    game_data = {}
    for plain in plains:
        game_prices = resp_data["data"][plain]["list"]

        price_list = []
        for price_data in game_prices:
            price_list.append(GamePrice(**price_data))

        game_data[plain] = price_list

    return game_data
