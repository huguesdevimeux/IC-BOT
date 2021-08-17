import typing
from abc import ABC, abstractmethod

import discord
from discord.message import Message


class BotResponse(ABC):
    """Abstract class for all the bot responses."""

    @abstractmethod
    def to_message(self) -> discord.Embed:
        """Returns the embed message that will be sent.

        Returns
        -------
        discord.Embed
            The message.
        """

    @classmethod
    async def build_with_args(
        cls, args: typing.Iterable[str] = None, original_message: Message = None
    ) -> "BotResponse":
        """Build the bot response given the argument.

        Parameters
        ----------
        args : typing.Iterable[str]
            The arguments the user passed (i.e, every word after the command invocation).
            WARNING : args does not contains the command !
        original_message : Message
            The message the request comes from.
        """
        return cls()
