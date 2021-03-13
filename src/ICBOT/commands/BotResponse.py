from abc import ABC, abstractclassmethod, abstractmethod
import typing

import discord


class BotResponse(ABC):
    """Abstract class for all the bot responses."""

    @abstractmethod
    def to_embed(self) -> discord.Embed:
        """Returns the embed message that will be sent.

        Returns
        -------
        discord.Embed
            The message.
        """
        pass

    @classmethod
    def build_with_args(cls, args: typing.Iterable[str] = None) -> "BotResponse":
        """Build the bot response given the argument.

        Parameters
        ----------
        args : typing.Iterable[str]
            The arguments the user passed (i.e, every word after the command invocation).
            WARNING : args does not contains the command !
        """
        return cls()
