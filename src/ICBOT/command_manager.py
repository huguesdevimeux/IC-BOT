import typing
from abc import ABC

from discord import message

from ICBOT.bot_response import BotResponse
from ICBOT.constants.constants import ErrorMessages
from ICBOT.exceptions import InvalidCommandName
from ICBOT.standard_commands.commands import Help

__all__ = ["CommandManager"]


class CommandManager(ABC):
    """Handles the logic of dispatching the standard_commands under user's input.

    Raises
    ------
    NoArgument
        If the user didn't provide any argument.
    InvalidCommandName
        If the user provided a wrong command.
    """

    _MAP_COMMANDS = None

    @classmethod
    def get_command(cls, key: typing.Union[str, int]) -> BotResponse:
        """
        Returns the associated command, given its name.
        Parameters
        ----------
        key
            The command's name.
        Returns
        -------
            The command.
        Raises
        ------
        KeyError
            If there is no command for the given name.
        """

        return cls._MAP_COMMANDS[key]

    @classmethod
    def has_command(cls, command: str):
        """
        Check if a command is registered.
        Parameters
        ----------
        command
            The command to check
        Returns
        -------
            Whether the command is registered.
        """
        return command in cls._MAP_COMMANDS

    @classmethod
    async def parse_command(
            cls, args: typing.Iterable[str], message: message.Message
    ) -> BotResponse:
        """Given the list of arguments passed after the prefix, returns the corresponding Command.

        Parameters
        ----------
        args : typing.Iterable[str]
            The arguments.

        message : message.Message
            The discord message the command comes from.

        Returns
        -------
        Command
        """
        if len(args) == 0:
            args.append(Help.info.call_name)
        if not cls.has_command(args[0]):
            raise InvalidCommandName(
                message=ErrorMessages.COMMAND_NOT_FOUND.format(args[0])
            )
        return await cls.get_command(args[0]).build_with_args(args[1:], message)
