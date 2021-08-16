import typing

from discord import message

from ICBOT.utils.data_loader import COPIE_PATES

from ..constants import Commands, Constants, ErrorMessages
from .commands import (
    Drive,
    Help,
    Delegates,
    Meteo,
    RandomCopiePate,
    RandomMeme,
    RandomPanda,
)
from ..BotResponse import BotResponse
from ..exceptions import InvalidCommandName, NoArgument, NoCommand


class CommandManager:
    """Handles the logic of dispatching the commands under user's input.

    Raises
    ------
    NoArgument
        If the user didn't provide any argument.
    InvalidCommandName
        If the user provided a wrong command.
    """

    _MAP_COMMANDS = {
        Commands.HELP.call_name: Help,
        Commands.DELEGATES.call_name: Delegates,
        Commands.DRIVE.call_name: Drive,
        Commands.RANDOMPANDA.call_name: RandomPanda,
        Commands.RANDOMCOPIEPATE.call_name: RandomCopiePate,
        Commands.RANDOMMEME.call_name: RandomMeme,
        Commands.METEO.call_name: Meteo,
    }

    @classmethod
    def _get_commmand(cls, key: typing.Union[str, int]) -> BotResponse:
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
            return await cls._get_commmand(args[0]).build_with_args(args[1:], message)
        except KeyError:
            raise InvalidCommandName(
                message=ErrorMessages.COMMAND_NOT_FOUND.format(args[0])
            )
