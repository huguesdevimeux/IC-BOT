import typing
from typing import List

import discord
from discord import Message

from ICBOT.bot_response import BotResponse
from ICBOT.constants.commands import CommandInfo, IcecoinCommands
from ICBOT.constants.constants import Messages, Constants
from ICBOT.templates import StandardMessage

ALL_COMMANDS: List[BotResponse] = []


def register_command(cls: BotResponse):
    """
    Decorator that registers a command as, well, a command

    Parameters
    ----------
    cls
        The command
    Returns
    -------
        The same command.
    """
    ALL_COMMANDS.append(cls)
    return cls


@register_command
class Help(BotResponse):
    info: CommandInfo = IcecoinCommands.HELP

    def to_message(self) -> discord.Embed:
        resp = StandardMessage(f"AIDE {Constants.ICECOIN}:", content="\u200b", show_doc=False)
        for command in ALL_COMMANDS:
            resp.add_field(name=command.info.name, value=command.info.help_message)
        resp.add_field(
            name="Voir le code / Contribuer :", value=Messages.CONTRIBUTION_MESSAGE
        )
        return resp

    @staticmethod
    def _generate_help():
        return "\n".join([command.info.help_message for command in ALL_COMMANDS])


@register_command
class Info(BotResponse):
    info: CommandInfo = IcecoinCommands.INFO

    @classmethod
    def build_with_args(
            cls, args: typing.Iterable[str] = None, original_message: Message = None
    ) -> "BotResponse":
        return super(Give, cls).build_with_args()

    def to_message(self) -> discord.Embed:
        return super(Give, self).to_message()


@register_command
class Give(BotResponse):
    info: CommandInfo = IcecoinCommands.GIVE

    @classmethod
    def build_with_args(
            cls, args: typing.Iterable[str] = None, original_message: Message = None
    ) -> "BotResponse":
        return super(Give, cls).build_with_args()

    def to_message(self) -> discord.Embed:
        return super(Give, self).to_message()
