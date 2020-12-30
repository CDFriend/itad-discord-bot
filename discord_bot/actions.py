from types import FunctionType
from typing import Dict
from discord import Message, Client
from discord_bot.discord_utils import find_mentions
from discord_bot.messages import Messenger
import discord_bot.game_prices as game_prices

cmds_map: Dict[str, FunctionType] = {}


async def handle_message(message: Message, client: Client):
    """Command structure: <command> <arg str>"""
    # Find any mentions of us. If none exist, ignore the message.
    mentions = find_mentions(message, client)

    if len(mentions) > 0:
        msg_content = message.clean_content

        # Strip out mentions of the bot and pass to handle_cmd
        for mention in mentions:
            msg_content = msg_content.replace(mention, "")

        # Strip whitespace
        msg_content = msg_content.strip()

        # Build messenger and handle command
        messenger = Messenger(message.channel)
        await handle_command(msg_content, messenger)


async def handle_command(cmd: str, messenger: Messenger):
    # Get command name from first token
    split_cmd = cmd.split(" ", 1)

    cmd_name = split_cmd[0]
    if cmd_name in cmds_map:
        arg_str = "" if len(split_cmd) == 1 else split_cmd[1]

        await cmds_map[cmd_name](arg_str, messenger)
    else:
        await messenger.send_unknown_command()
        pass


def bot_command(name: str):
    def wrapper(fn):
        cmds_map[name] = fn
    return wrapper


@bot_command("track")
async def track_game(arg_str: str, messenger: Messenger):
    """Keeps track of the price of a game on IsThereAnyDeal. If we can find the game on
    ITAD, send a price back to the user immediately.
    """

    # Try and find a game with the given title (arg string) on ITAD.
    id = game_prices.get_id_from_game_title(arg_str)

    if id:
        # Find current price for game
        prices = game_prices.get_prices_for_games([id])

        if id in prices and len(prices[id]) > 0:
            price_list = prices[id]

            best_price = min(price_list, key=lambda price: price.price_new)
            await messenger.send_price_found(arg_str, best_price.price_new)
        else:
            await messenger.send_no_price_found(arg_str)
    else:
        # Notify user we couldn't find game
        await messenger.send_no_game_found(arg_str)
