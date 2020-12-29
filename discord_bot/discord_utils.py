from typing import Set
from discord import Message, Client


def find_mentions(message: Message, client: Client) -> Set[str]:
    """Returns any mention strings referring to our client. Excludes the @everyone role."""
    mentions = set()

    if client.user.id in message.raw_mentions:
        mentions.add("@" + client.user.name)

    # Are any of my roles mentioned?
    if message.guild:
        roles = message.guild.me.roles
        for role in roles:
            # Ignore default @everyone role
            if role == message.guild.default_role:
                continue

            if role.id in message.raw_role_mentions:
                mentions.add("@" + role.name)

    return mentions
