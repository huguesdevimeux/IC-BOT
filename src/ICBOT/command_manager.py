import typing
from abc import abstractclassmethod, abstractmethod

from discord import message

from ICBOT.bot_response import BotResponse
from ICBOT.constants.constants import ErrorMessages
from ICBOT.exceptions import InvalidCommandName
from ICBOT.standard_commands.commands import ALL_COMMANDS, Help


class CommandManager:
    """Handles the logic of dispatching the standard_commands under user's input.

    Raises
    ------
    NoArgument
        If the user didn't provide any argument.
    InvalidCommandName
        If the user provided a wrong command.
    """

    _MAP_COMMANDS = {command.info.call_name: command for command in ALL_COMMANDS}

    @classmethod
    @abstractmethod
    def get_commmand(cls, key: typing.Union[str, int]) -> BotResponse:
        """"""
        return cls._MAP_COMMANDS[key]

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
            return await Help.build_with_args()
        try:
            return await cls.get_commmand(args[0]).build_with_args(args[1:], message)
        except KeyError:
            raise InvalidCommandName(
                message=ErrorMessages.COMMAND_NOT_FOUND.format(args[0])
            )
