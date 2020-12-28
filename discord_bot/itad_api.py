import requests
import discord_bot.config as config

ITAD_API_URL = "https://api.isthereanydeal.com/"


class ITADApi:
    """IsThereAnyDeal.com API binding"""
    def __init__(self):
        self._api_key = config.ITAD_API_KEY

    def get_plain(self, title: str) -> requests.Response:
        return self._send_request("v02/game/plain", {"title": title})

    def get_prices(self, plains: str) -> requests.Response:
        return self._send_request("v01/game/prices", {"plains": plains})

    def _send_request(self, route: str, payload: dict) -> requests.Response:
        """Sends a request to ITAD with the appropriate auth info."""
        payload["key"] = self._api_key
        return requests.get(ITAD_API_URL + route)
