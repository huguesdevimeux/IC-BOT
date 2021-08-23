import typing
from typing import List

import discord
from discord import Message

from ICBOT.bot_response import BotResponse
from ICBOT.constants.commands import CommandInfo, IcecoinCommands
from ICBOT.constants.constants import Messages, Constants, ErrorMessages
from ICBOT.exceptions import InvalidArgument
from ICBOT.icecoin import bank
from ICBOT.icecoin.exceptions import IceCoinException, CantMine
from ICBOT.icecoin.templates import StandardMessage

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
        resp = StandardMessage(
            f"AIDE {Constants.ICECOIN}:", content="\u200b", show_doc=False
        )
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

    def __init__(
            self,
            asker: discord.abc.User,
            bank_entry: bank.BankEntry,
    ):
        self.bank_entry = bank_entry
        self.asker = asker

    @classmethod
    async def build_with_args(
            cls, args: typing.Iterable[str] = None, original_message: Message = None
    ) -> "BotResponse":
        if len(original_message.mentions) != 1:
            raise InvalidArgument(ErrorMessages.NO_ONE_MENTIONED_INFOS)
        asker = original_message.mentions[0]
        if not bank.is_registered(asker.id):
            raise InvalidArgument(
                f"{asker.mention} n'a pas capitalisé de {Constants.ICECOIN}."
            )
        return cls(asker, bank.get_entry(asker.id))

    def to_message(self) -> discord.Embed:
        m = StandardMessage(
            title=f"Rapport banquier", content=f"De {self.asker.mention}"
        )
        m.add_field(
            name="Capital :",
            value=f"**{self.bank_entry} {Constants.ICECOIN}**",
        )
        m.set_footer(text="Vive le capitalisme")
        return m


@register_command
class Give(BotResponse):
    info: CommandInfo = IcecoinCommands.GIVE

    def __init__(self, amount_given: int, receiver: discord.abc.User):
        self.receiver = receiver
        self.amount_given = amount_given

    @classmethod
    async def build_with_args(
            cls, args: typing.Iterable[str] = None, original_message: Message = None
    ) -> "BotResponse":
        if len(original_message.mentions) != 1:
            raise InvalidArgument(ErrorMessages.NO_ONE_MENTIONED_DONATION)
        if len(args) != 2 or not args[0].isdigit():
            raise InvalidArgument(ErrorMessages.NO_AMOUNT_SPECIFIED_DONATION)
        if not bank.is_registered(original_message.author.id):
            raise InvalidArgument(
                f"{original_message.author.mention} n'a pas encore capitalisé de {Constants.ICECOIN}, et ne peut donc "
                f"pas en donner. "
            )
        if original_message.author.id == original_message.mentions[0].id:
            raise IceCoinException(
                message="Soit vous êtes con, soit vous vous faites uen fausse manipulation. Vous ne pouvez pas donner "
                        "de l'argent à vous même."
            )

        donnor = bank.get_entry(original_message.author.id)
        receiver = bank.get_entry(original_message.mentions[0].id)
        donnor.transfer(receiver, int(args[0]))
        bank.put_entry(donnor)
        bank.put_entry(receiver)

        return cls(int(args[0]), original_message.mentions[0])

    def to_message(self) -> discord.Embed:
        return StandardMessage(
            title="Succès",
            content=f"Donné {self.amount_given} {Constants.ICECOIN} à {self.receiver.mention}.",
        )


@register_command
class Mine(BotResponse):
    info: CommandInfo = IcecoinCommands.MINE

    def __init__(self, new_amount: int, miner: discord.abc.User):
        self.new_amount = new_amount
        self.miner = miner

    @classmethod
    async def build_with_args(
            cls, args: typing.Iterable[str] = None, original_message: Message = None
    ) -> "BotResponse":
        user_entry = bank.get_entry(original_message.author.id)
        if not user_entry.can_mine():
            raise CantMine
        user_entry.mine()
        bank.put_entry(user_entry)
        return cls(new_amount=user_entry.amount, miner=original_message.author)

    def to_message(self) -> discord.Embed:
        return StandardMessage(
            title="Vous avez miné !",
            content=f"{self.miner.mention} a maintenant {self.new_amount} {Constants.ICECOIN}",
        )
