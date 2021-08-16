from discord import embeds
from discord import colour
from discord.colour import Colour
from abc import ABC
from .constants import Commands, Constants, Messages
import discord


class EmebedWithFile:
    def __init__(self, file_to_send: discord.File, embed: discord.Embed) -> None:
        self.file = file_to_send
        self.embed = embed


class AbstractMessage(discord.Embed, ABC):
    """Abstract class for all the embedded messages ICBOT can send."""

    def __init__(self, show_doc=True, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.show_doc = show_doc
        self._add_doc()

    def __str__(self):
        return f"{type(self).__name__} {self.description}"

    def _add_doc(self):
        if self.show_doc:
            super().add_field(name="Documentation :", value=Commands.HELP.help_message)


class StandardMessage(AbstractMessage):
    def __init__(self, title=None, content="", show_doc=True) -> None:
        super().__init__(
            colour=Colour.blue(), title=title, description=content, show_doc=show_doc
        )
        self.set_footer(text=Messages.CONTRIBUTION_MESSAGE_FOOTER)

    def add_field(self, *, name, value, inline=False):
        fields = self.fields
        # This is an override to ensure that the "documentation" part will always be at the bottom of the embed.
        if len(fields) == 0 or not "Documentation" in fields[-1].name:
            super().add_field(name=name, value=value, inline=inline)
            self._add_doc()
            return self

        # Remove the doc field and add it at the end.
        self.remove_field(len(fields) - 1)
        super().add_field(name=name, value=value, inline=inline)
        self._add_doc()
        return self


class ErrorMessage(AbstractMessage):
    def __init__(self, text, *args, **kwargs) -> None:
        super().__init__(
            colour=Colour.red(),
            title="ERREUR : ",
            description=f"**{text}**",
            *args,
            **kwargs,
        )
