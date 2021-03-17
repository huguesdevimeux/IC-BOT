from asyncio import constants
import typing
from collections import namedtuple
from enum import Enum
import inspect

from attr import dataclass

from .var_env import *

_moodle_url = "https://moodle.epfl.ch/course/view.php?id={id}"


class Constants:
    # TODO Change this name.
    PREFIX = "!ic"
    MAP_COURSE_TO_MOODLE_LINK = {
        "aicc2": _moodle_url.format(id=AICC2_ID),
        "dsd": _moodle_url.format(id=DSD_ID),
        "analyse": _moodle_url.format(id=ANALYSE_ID),
    }
    MAX_AMOUNT_PANDAS = 50


class ErrorMessages:
    COMMAND_NOT_FOUND = "`{}` n'est pas une commande enregistrée."
    NO_COMMAND = "Vous m'avez appelé sans commande !"
    INVALID_ARGUMENT = "{} n'est pas un argument valide"
    NO_ARGUMENT_GIVEN = "La commande `{}` a été appelée sans argument :/"
    MOODLE_NOT_FOUND = "Le cours {} n'a pas été trouvé sur moodle :/"


class Messages:
    DELEGATES = (
        "Il y a quatre délégués (deux par section). N'hésitez pas à les contacter !"
    )
    DELEGATES_IN = DELEGATES_IN
    DELEGATES_SC = DELEGATES_SC
    DRIVE_MESSAGE = "Le lien du drive : \n{}. \n**VOUS DEVEZ VOUS CONNECTER AVEC VOTRE COMPTE EPFL.**".format(
        DRIVE_LINK
    )
    CONTRIBUTING_MESSAGE_FOOTER = (
        "J'appartiens à toute la promo. Les contributions sont la bienvenue !"
    )
    CONTRIBUTING_MESSAGE = "**Tu veux ajouter une fonctionnalité et devenir _cool_ ? C'est [ici](https://github.com/huguesdevimeux/IC-BOT)**"
    BONSOIR_NON = """**
    \uD83D\uDCF6SFR 4G                       \uD83C\uDF19\uD83D\uDD1256%\uD83D\uDD0B\n\n                      21:40\n              Samedi 17 mars\n\n\uD83D\uDCAC  MESSAGES                maintenant\nOumar Coach\n\nBonsoir non
    **"""


@dataclass
class _Command:
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


class Commands:
    """Enumeration of all the commands avaiable."""

    HELP = _Command("Aide", "aide", "pour avoir la documentation.")
    MOODLE = _Command(
        "Moodle",
        "moodle",
        "Les divers liens pour des cours en ligne.",
        f"{Constants.PREFIX} moodle [optionnel : nom du cours (AICC2, etc)]",
    )
    DELEGATES = _Command(
        "Délégués", "delegues", "pour savoir qui sont les délégués actuels."
    )
    DRIVE = _Command(
        "Drive (BETA)",
        "drive",
        "pour chercher un document dans le drive de section (très peu efficace, version alpha)",
    )
    RANDOMPANDA = _Command(
        "Panda aléatoire",
        "pandalea",
        "pour avoir un émoji panda aléatoire",
    )
    RANDOMCOPIEPATE = _Command(
        "Copie pâte aléatoire", "copiepate", "pour avoir un copie pate aléatoire."
    )

    @classmethod
    def ALL(cls) -> typing.Iterable[_Command]:
        """Returns all the commandes defined.

        Returns
        -------
        typing.Iterable[_Command]
            List of all the commands.
        """
        return [m for _, m in vars(cls).items() if (isinstance(m, _Command))]
