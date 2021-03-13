from ICBOT.commands.exceptions import InvalidArgument, NoArgument
from abc import ABC, abstractclassmethod, abstractmethod
from typing import overload
import typing

import discord
from ICBOT.commands.templates import StandardMessage

from ..constants import Commands, Constants, ErrorMessages, Messages
from .BotResponse import BotResponse


class Help(BotResponse):
    def to_embed(self) -> discord.Embed:
        resp = StandardMessage("AIDE :", content="", show_doc=False)
        for command in Commands.ALL():
            resp.add_field(name=command.name, value=command.help_message)
        resp.add_field(name="Contribuer :", value=Messages.CONTRIBUTING_MESSAGE)
        return resp

    @staticmethod
    def _generate_help():
        return "\n".join([command.help_message for command in Commands.ALL()])


class Delegates(BotResponse):
    def to_embed(self) -> None:
        return (
            StandardMessage("Délégués :", content=Messages.DELEGATES, show_doc=False)
            .add_field(name="IN", value=Messages.DELEGATES_IN)
            .add_field(name="SC", value=Messages.DELEGATES_SC)
        )


class Moodle(BotResponse):
    def __init__(
        self, chosen_cours_name=None, chosen_course_url: typing.Union[None, str] = None
    ) -> None:
        super().__init__()
        self.chosen_cours_name = chosen_cours_name
        self.chosen_course_url = chosen_course_url

    def to_embed(self) -> discord.Embed:
        if self.chosen_course_url != None:
            return StandardMessage(title="Lien Moodle :", content=" ").add_field(
                name=self.chosen_cours_name.upper(), value=self.chosen_course_url
            )
        else:
            r = StandardMessage(title="Liens Moodle : ")
            for course_name, course_url in Constants.MAP_COURSE_TO_MOODLE_LINK.items():
                r.add_field(name=course_name.upper(), value=course_url)
            return r

    @classmethod
    def build_with_args(cls, args: typing.Iterable[str]) -> "BotResponse":
        if len(args) == 0:
            return cls()
        arg = args[0].lower()
        if arg not in Constants.MAP_COURSE_TO_MOODLE_LINK:
            raise InvalidArgument(ErrorMessages.MOODLE_NOT_FOUND.format(args[0]))
        return cls(arg, Constants.MAP_COURSE_TO_MOODLE_LINK[args[0]])


class Drive(BotResponse):
    # TODO, drive features.
    def to_embed(self) -> discord.Embed:
        return StandardMessage(
            title="Drive :",
            content=Messages.DRIVE_MESSAGE
            + "\n\n la fonction recherche arrivera un jour ..",
        )
