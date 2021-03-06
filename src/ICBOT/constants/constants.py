from ICBOT.var_env import *

_moodle_url = "https://moodle.epfl.ch/course/view.php?id={id}"

__all__ = ["Constants", "Messages", "ErrorMessages"]


class Constants:
    # TODO Change this name.
    PREFIX = "!ic"
    MAP_COURSE_TO_MOODLE_LINK = {
        "aicc2": _moodle_url.format(id=AICC2_ID),
        "dsd": _moodle_url.format(id=DSD_ID),
        "analyse": _moodle_url.format(id=ANALYSE_ID),
    }
    MAX_AMOUNT_PANDAS = 50
    SECTIONS = ["IN", "SC"]
    REFRESH_HOURS_WEATHER = 3


class ErrorMessages:
    COMMAND_NOT_FOUND = "`{}` n'est pas une commande enregistrée."
    NO_COMMAND = "Vous m'avez appelé sans commande !"
    INVALID_ARGUMENT = "{} n'est pas un argument valide"
    NO_ARGUMENT_GIVEN = "La commande `{}` a été appelée sans argument :/"
    MOODLE_NOT_FOUND = "Le cours {} n'a pas été trouvé sur moodle :/"
    DRIVE_NO_FILE_SPECIFIED = "Vous n'avez pas spécifié de fichier"
    CITY_NOT_FOUND = "J’ai cherché partout, mais je n’ai pas trouvé cet endroit :/"
    WEATHER_ERROR = (
        "Je dois être rouillé, je n’arrive pas à regarder dans ma boule de cristal :/"
    )


def _d(s):
    d = {}
    for c in (65, 97):
        for i in range(26):
            d[chr(i + c)] = chr((i + 13) % 26 + c)
    return "".join([d.get(c, c) for c in s])


class Messages:
    DELEGATES = (
        "Il y a quatre délégués (deux par section). N'hésitez pas à les contacter !"
    )
    DELEGATES_IN = DELEGATES_IN
    DELEGATES_SC = DELEGATES_SC
    DRIVE_MESSAGE = "Le lien du drive : \n{}. \n**VOUS DEVEZ VOUS CONNECTER AVEC VOTRE COMPTE EPFL.**".format(
        DRIVE_LINK
    )
    CONTRIBUTION_MESSAGE_FOOTER = (
        "Je suis open-source pour la promo ! Les contributions sont les bienvenues."
    )
    CONTRIBUTION_MESSAGE = "**C'est [ici](https://github.com/huguesdevimeux/IC-BOT)**"
    BONSOIR_NON = """**
    \uD83D\uDCF6SFR 4G                       \uD83C\uDF19\uD83D\uDD1256%\uD83D\uDD0B\n\n                      21:40\n              Samedi 17 mars\n\n\uD83D\uDCAC  MESSAGES                maintenant\nOumar Coach\n\nBonsoir non
    **"""
    METEO = "{emoji_weather} **{time_of_day}** : _{description}_ - Ressenti {feels_like}°C : - Prob. précipitations : {probability_precipitation}% - Nuages : {clouds}%."
    PRIVATE_MESSAGE_ANSWER = _d(
        "Gur zbbqyr grfg pbhagf sbe 40% bs rinyhngvba 1. Lbh pna tb gb lbhe zbbqyr grfg naq frr lbhe erfhygf. Gb pnyphyngr lbhe crepragntr fpberq sbe gur zbbqyr grfg: 23 cbvagf vg 50%. Vs lbh unir yrff guna 23 cbvagf lbhe crepragntr vf pnyphyngrq nf: ((lbhe cbvagf)/23)50%. Vs lbh unir 23 be zber cbvagf lbhe crepragntr vf pnyphyngrq nf: 50%(1+((lbhe cbvag-23)/4))."
    )
