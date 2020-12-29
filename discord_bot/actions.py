from types import FunctionType
from typing import Dict

cmds_map: Dict[str, FunctionType] = {}


def handle_command(cmd: str):
    """Command structure: <command> <arg str>"""

    # Get command name from first token
    split_cmd = cmd.split(" ", 1)

    cmd_name = split_cmd[0]
    if cmd_name in cmds_map:
        arg_str = "" if len(split_cmd) == 1 else split_cmd[1]

        cmds_map[cmd_name](arg_str)
    else:
        # TODO: unrecognized command
        pass


def track_game(arg_str: str):
    pass
