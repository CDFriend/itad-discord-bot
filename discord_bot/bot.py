import sys
import discord
import logging
from discord_bot.config import DISCORD_BOT_TOKEN

client = discord.Client()

# Configure logging
root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
root.addHandler(handler)


def get_client() -> discord.Client:
    """Gets the Discord client singleton."""
    return client


def is_mentioned(message) -> bool:
    """Returns true if our user is mentioned in a message. Excludes the @everyone role."""
    if client.user.id in message.raw_mentions:
        return True

    # Are any of my roles mentioned?
    if message.guild:
        roles = message.guild.me.roles
        for role in roles:
            # Ignore default @everyone role
            if role == message.guild.default_role:
                continue

            if role.id in message.raw_role_mentions:
                return True

    return False


@client.event
async def on_ready():
    logging.info(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if is_mentioned(message):
        await message.channel.send("sup")


if __name__ == "__main__":
    client.run(DISCORD_BOT_TOKEN)
