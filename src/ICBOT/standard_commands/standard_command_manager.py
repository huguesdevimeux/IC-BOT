import typing

from ICBOT.bot_response import BotResponse
from ICBOT.command_manager import CommandManager
from ICBOT.standard_commands.commands import ALL_COMMANDS

__all__ = ["StandardCommandManager"]


class StandardCommandManager(CommandManager):
    _MAP_COMMANDS = {command.info.call_name: command for command in ALL_COMMANDS}

    @classmethod
    def get_command(cls, key: typing.Union[str, int]) -> BotResponse:
        return cls._MAP_COMMANDS[key]
