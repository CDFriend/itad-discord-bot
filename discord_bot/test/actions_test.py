import pytest
from unittest import mock
import discord_bot.actions as actions
from discord_bot.game_prices import GamePrice


@pytest.fixture
def mocked_actions():
    action_dict = {
        "funcA": mock.AsyncMock(),
        "funcB": mock.AsyncMock()
    }

    # Replace the commands map with our map of mocks
    with mock.patch("discord_bot.actions.cmds_map", action_dict):
        yield action_dict


@pytest.fixture
def mock_messenger():
    messenger = mock.AsyncMock()
    yield messenger


@pytest.fixture
def mock_game_prices():
    with mock.patch("discord_bot.actions.game_prices") as mock_game_prices:
        yield mock_game_prices


@pytest.mark.asyncio
@pytest.mark.parametrize("cmd,expected_func,expected_arg_str", [
    ("funcA", "funcA", ""),              # Function with no args
    ("funcA a b c", "funcA", "a b c"),   # Function with args
    ("funcB", "funcB", ""),              # 2nd function, no args
    ("funcB 1 2abc", "funcB", "1 2abc")  # 2nd function with args
])
async def test_handle_cmd_calls_functions(mocked_actions, mock_messenger, cmd, expected_func, expected_arg_str):
    # Handle the command string
    await actions.handle_command(cmd, mock_messenger)

    # Was the correct function called? Were we given the correct argument string?
    mocked_actions[expected_func].assert_called_once_with(expected_arg_str, mock_messenger)


@pytest.mark.asyncio
@pytest.mark.parametrize("cmd", [
    "funcC",
    "some random input",
    ""
])
async def test_handle_cmd_gives_unrecognized_cmd(mocked_actions, mock_messenger, cmd):
    # Attempt to handle command string
    await actions.handle_command(cmd, mock_messenger)

    # None of the actions should be called
    for name, action in mocked_actions.items():
        action.assert_not_called()

    # Should send unrecognized command message
    mock_messenger.send_unknown_command.assert_called_once()


@pytest.mark.asyncio
async def test_track_game_finds_lowest_price(mock_messenger, mock_game_prices):
    # Track game should find the lowest price for a game and relay that to the user.
    mock_game_prices.get_id_from_game_title.return_value = "gameid"
    mock_game_prices.get_prices_for_games.return_value = {
        "gameid": [
            GamePrice(price_new=12.04),
            GamePrice(price_new=2.24),
            GamePrice(price_new=5.00)
        ]
    }

    await actions.cmds_map["track"]("test game", mock_messenger)

    # Should notify user that the best price for the game is 2.24
    mock_messenger.send_price_found.assert_called_once_with("test game", 2.24)


@pytest.mark.asyncio
@pytest.mark.parametrize("game_price_result", [
    {},             # No results returned for game
    {"gameid": []}  # Empty list returned for game
])
async def test_track_game_notifies_no_price(mock_messenger, mock_game_prices, game_price_result):
    # If ITAD doesn't return a price for a game (even if we got a plain) then we should notify the user.
    mock_game_prices.get_id_from_game_title.return_value = "gameid"
    mock_game_prices.get_prices_for_games.return_value = game_price_result

    await actions.cmds_map["track"]("test game", mock_messenger)

    # User should be notified that we couldn't find a price
    mock_messenger.send_no_price_found.assert_called_once_with("test game")


@pytest.mark.asyncio
async def test_track_game_notifies_no_game_id(mock_messenger, mock_game_prices):
    # If no plain ID is found for a game, user should be notified
    mock_game_prices.get_id_from_game_title.return_value = None

    await actions.cmds_map["track"]("test game", mock_messenger)

    mock_messenger.send_no_game_found.assert_called_once_with("test game")
