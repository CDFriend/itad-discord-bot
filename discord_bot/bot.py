import sys
import discord
import logging
from typing import Set
from discord_bot.config import DISCORD_BOT_TOKEN
from discord_bot.actions import handle_message

client = discord.Client()

# Configure logging
root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
root.addHandler(handler)


def get_client() -> discord.Client:
    """Gets the Discord client singleton."""
    return client

@client.event
async def on_ready():
    logging.info(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    await handle_message(message, client)


if __name__ == "__main__":
    client.run(DISCORD_BOT_TOKEN)
