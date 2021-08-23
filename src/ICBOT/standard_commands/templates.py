from discord import Colour

from ICBOT.abstract_templates import AbstractMessage, AbstractStandardMessage
from ICBOT.constants.commands import StandardCommands


class StandardMessage(AbstractStandardMessage):
    def __init__(
            self,
            title=None,
            content="",
            show_doc=True,
            colour=Colour.blue(),
    ) -> None:
        super().__init__(
            help_message=StandardCommands.HELP.help_message,
            colour=colour,
            title=title,
            content=content,
            show_doc=show_doc,
        )


class ErrorMessage(AbstractMessage):
    def __init__(self, text, *args, **kwargs) -> None:
        super().__init__(
            help_message=StandardCommands.HELP.help_message,
            colour=Colour.red(),
            title="ERREUR : ",
            description=f"**{text}**",
            *args,
            **kwargs,
        )
