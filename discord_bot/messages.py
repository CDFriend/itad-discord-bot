from discord.abc import Messageable


class Messenger:
    """Allows functions to respond to a message on a given channel."""
    def __init__(self, channel: Messageable):
        self._channel = channel

    async def send_unknown_command(self):
        await self._send_message("Sorry, I didn't recognize that command.")

    async def send_no_game_found(self, title: str):
        await self._send_message(f"Sorry, I couldn't find the game '{title}' on the IsThereAnyDeal server.")

    async def send_no_price_found(self, title: str):
        await self._send_message(f"Welp, something funky's going on here. The game '{title}' appears to be "
                                 "present on IsThereAnyDeal, but no prices are available.")

    async def send_price_found(self, title: str, price: float):
        await self._send_message(f"Nice, I found the game {title} on IsThereAnyDeal. "
                                 f"The best price I found is ${price}")

    async def _send_message(self, msg: str):
        await self._channel.send(msg)
