from discord import Colour

from ICBOT.constants.commands import IcecoinCommands
from ICBOT.abstract_templates import AbstractMessage, AbstractStandardMessage


class StandardMessage(AbstractStandardMessage):
    def __init__(self, title=None, content="", show_doc=True, colour=Colour.greyple(), ) -> None:
        super().__init__(help_message=IcecoinCommands.HELP.help_message,
                         colour=colour, title=title, content=content, show_doc=show_doc,
                         )


class ErrorMessage(AbstractMessage):
    def __init__(self, text, *args, **kwargs) -> None:
        super().__init__(help_message=IcecoinCommands.HELP.help_message,
                         colour=Colour.red(),
                         title="ERREUR : ",
                         description=f"**{text}**",
                         *args,
                         **kwargs,
                         )
