import os
import typing
from pathlib import Path

from dotenv import dotenv_values

from .utils.logging import logger

# This logic is to intended to keep all the potentially private variables outside git by storing them in a .env.shared
# at the root.

__all__ = [
    "AICC2_ID",
    "DSD_ID",
    "ANALYSE_ID",
    "DRIVE_LINK",
    "DELEGATES_SC",
    "DELEGATES_IN",
]

_config_shared = dotenv_values(Path(__file__).parents[2] / ".env.shared")
_config_secret = dotenv_values(Path(__file__).parents[2] / ".env.secret")


def _load_value(name: str, secret=False) -> str:
    try:
        if secret:
            return _config_secret[name]
        else:
            return _config_shared[name]
    except KeyError:
        logger.warning(f"{name} env variable non loaded.")
        return "NON_LOADED_DATA"


AICC2_ID = _load_value("AICC2_ID")
DSD_ID = _load_value("DSD_ID")
ANALYSE_ID = _load_value("ANALYSE_ID")
DRIVE_LINK = _load_value("DRIVE_LINK")
DELEGATES_IN = _load_value("DELEGATES_IN")
DELEGATES_SC = _load_value("DELEGATES_SC")

USER_MAIL = _load_value("USER_MAIL", secret=True)
PASSWORD_MAIL = _load_value("PASSWORD_MAIL", secret=True)
WEATHER_API_KEY = _load_value("WEATHER_API_KEY", secret=True)
