import random
import typing
from abc import ABC, abstractclassmethod, abstractmethod
from pathlib import Path
from typing import overload

import discord
from discord import emoji
from discord.emoji import Emoji
from fuzzywuzzy import process

from ..constants import Commands, Constants, ErrorMessages, Messages
from ..utils.data_loader import ALL_FILES_DRIVE, COPIE_PATES, DRIVE_PATH
from ..utils.logging import logger
from ..BotResponse import BotResponse
from ..exceptions import InvalidArgument, NoArgument
from ..templates import EmebedWithFile, StandardMessage


class Help(BotResponse):
    def to_message(self) -> discord.Embed:
        resp = StandardMessage("AIDE :", content="", show_doc=False)
        for command in Commands.ALL():
            resp.add_field(name=command.name, value=command.help_message)
        resp.add_field(name="Contribuer :", value=Messages.CONTRIBUTING_MESSAGE)
        return resp

    @staticmethod
    def _generate_help():
        return "\n".join([command.help_message for command in Commands.ALL()])


class Delegates(BotResponse):
    def to_message(self) -> None:
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

    def to_message(self) -> discord.Embed:
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
    def build_with_args(cls, args: typing.Iterable[str], *argments) -> "BotResponse":
        if len(args) == 0:
            return cls()
        arg = args[0].lower()
        if arg not in Constants.MAP_COURSE_TO_MOODLE_LINK:
            raise InvalidArgument(ErrorMessages.MOODLE_NOT_FOUND.format(args[0]))
        return cls(arg, Constants.MAP_COURSE_TO_MOODLE_LINK[args[0]])


class Drive(BotResponse):
    def __init__(self, files_names: typing.Iterable[typing.Tuple[str, int]]) -> None:
        self.files_names = files_names

    # TODO, drive features.
    def to_message(self) -> discord.Embed:
        print(self.files_names)
        temp_path = self.files_names[0].replace("\n", "")[2:]
        embed = StandardMessage(
            title="Drive :",
            content="Résultats : ```"
            + "\n".join([f"{c}" for c in self.files_names])
            + "```",
        )
        file_ = discord.File(Path.joinpath(DRIVE_PATH, temp_path), filename=temp_path)
        return EmebedWithFile(file_, embed)

    @classmethod
    def build_with_args(
        cls, args: typing.Iterable[str], original_message: discord.Message
    ) -> "BotResponse":
        if len(args) == 0:
            raise NoArgument(Commands.DRIVE.name)
        logger.info("Searching for " + " ".join(args))
        import difflib

        return cls(
            difflib.get_close_matches("".join(args), ALL_FILES_DRIVE, cutoff=0.1)
        )


class RandomPanda(BotResponse):
    def __init__(self, emojis: typing.Iterable[Emoji]) -> None:
        self.emojis = emojis

    def to_message(self) -> discord.Embed:
        return " ".join([str(e) for e in self.emojis])

    @classmethod
    def build_with_args(
        cls, args: typing.Iterable[str], message: discord.Message
    ) -> "BotResponse":
        amount_of_pandas = 1
        if len(args) > 0:
            try:
                amount_of_pandas = int(args[0])
            except ValueError:
                pass
        amount_of_pandas = min(max(1, amount_of_pandas), Constants.MAX_AMOUNT_PANDAS)
        pandas = list(
            filter(lambda e: e.name.startswith("panda"), message.guild.emojis)
        )
        pandas_resp = []
        for i in range(amount_of_pandas):
            pandas_resp.append(random.choice(pandas))
        return cls(pandas_resp)


class RandomCopiePate(BotResponse):
    def __init__(self, copiepate: str, submitter: str):
        self.copiepate = copiepate
        self.submitter = submitter

    def to_message(self) -> discord.Embed:
        resp = f"**{self.copiepate}** \n\n_Soumis par_ <@{self.submitter}>"
        return StandardMessage(content=resp, show_doc=False)

    @classmethod
    def build_with_args(
        cls, args: typing.Iterable[str], original_message: discord.Message
    ) -> "BotResponse":
        copie_pate = random.choice(COPIE_PATES)
        return cls(copie_pate["content"], copie_pate["author"]["id"])
