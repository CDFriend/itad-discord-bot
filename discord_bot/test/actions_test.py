import pytest
from unittest import mock
import discord_bot.actions as actions


@pytest.fixture
def mocked_actions():
    action_dict = {
        "funcA": mock.MagicMock(),
        "funcB": mock.MagicMock()
    }

    # Replace the commands map with our map of mocks
    with mock.patch("discord_bot.actions.cmds_map", action_dict):
        yield action_dict


@pytest.mark.parametrize("cmd,expected_func,expected_arg_str", [
    ("funcA", "funcA", ""),              # Function with no args
    ("funcA a b c", "funcA", "a b c"),   # Function with args
    ("funcB", "funcB", ""),              # 2nd function, no args
    ("funcB 1 2abc", "funcB", "1 2abc")  # 2nd function with args
])
def test_handle_cmd_calls_functions(mocked_actions, cmd, expected_func, expected_arg_str):
    # Handle the command string
    actions.handle_command(cmd)

    # Was the correct function called? Were we given the correct argument string?
    mocked_actions[expected_func].assert_called_once_with(expected_arg_str)


@pytest.mark.parametrize("cmd", [
    "funcC",
    "some random input",
    ""
])
def test_handle_cmd_gives_unrecognized_cmd(mocked_actions, cmd):
    # Attempt to handle command string
    actions.handle_command(cmd)

    # None of the actions should be called
    for name, action in mocked_actions.items():
        action.assert_not_called()
