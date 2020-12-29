from discord.abc import Messageable


class Messenger:
    """Allows functions to respond to a message on a given channel."""
    def __init__(self, channel: Messageable):
        self._channel = channel

    async def send_unknown_command(self):
        await self._channel.send("Sorry, I didn't recognize that command.")
