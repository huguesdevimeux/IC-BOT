import typing
from dataclasses import dataclass

from ICBOT.constants.constants import Constants

__all__ = ["StandardCommands"]


@dataclass
class CommandInfo:
    """Representation of a Command."""

    name: str
    call_name: str
    description: str
    usage: str = ""

    def __str__(self):
        return f"{self.name} {self.description}"

    @property
    def help_message(self):
        r = f"`{Constants.PREFIX} {self.call_name}` {self.description}"
        if len(self.usage) > 0:
            return r + f"\n\t_Usage_ : `{self.usage}`"
        return r


class StandardCommands:
    """Enumeration of all the standard_commands avaiable."""

    HELP = CommandInfo("Aide", "aide", "pour avoir la documentation.")
    DELEGATES = CommandInfo(
        "Délégués", "delegues", "pour savoir qui sont les délégués actuels."
    )
    DRIVE = CommandInfo(
        "Drive (BETA)",
        "drive",
        "pour chercher un document dans le drive de section (bon parfois ça marche ok ?)",
        f"{Constants.PREFIX} drive [matiere] [fichier à chercher (espaces autorisés)]",
    )
    RANDOMPANDA = CommandInfo(
        "Panda aléatoire",
        "pandalea",
        "pour avoir un émoji panda aléatoire",
    )
    RANDOMCOPIEPATE = CommandInfo(
        "Copie pâte aléatoire", "copiepate", "pour avoir un copie pate aléatoire."
    )
    RANDOMMEME = CommandInfo("Meme aléatoire", "meme", "Pour avoir un meme aléatoire.")
    METEO = CommandInfo(
        "La météo",
        "meteo",
        description="Pour avoir la météo.",
        usage=f"{Constants.PREFIX} meteo [ville=Lausanne]",
    )

    @classmethod
    def ALL(cls) -> typing.Iterable[CommandInfo]:
        """Returns all the commandes defined.

        Returns
        -------
        typing.Iterable[_Command]
            List of all the standard_commands.
        """
        return [m for _, m in vars(cls).items() if (isinstance(m, CommandInfo))]
