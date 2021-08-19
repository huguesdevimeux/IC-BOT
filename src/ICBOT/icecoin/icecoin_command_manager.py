import typing

from ICBOT.bot_response import BotResponse
from ICBOT.command_manager import CommandManager

__all__ = ["IcecoinCommandManager"]

from ICBOT.icecoin.commands import ALL_COMMANDS


class IcecoinCommandManager(CommandManager):
    _MAP_COMMANDS = {command.info.call_name: command for command in ALL_COMMANDS}

    @classmethod
    def get_command(cls, key: typing.Union[str, int]) -> BotResponse:
        return cls._MAP_COMMANDS[key]
