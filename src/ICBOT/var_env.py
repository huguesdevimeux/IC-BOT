import os
import typing
from dotenv import dotenv_values
from pathlib import Path

# This logic is to intended to all the potntatially private information outside git by storing them in a .env.shared
# at the root.

__all__ = [
    "AICC2_ID",
    "DSD_ID",
    "ANALYSE_ID",
    "DRIVE_LINK",
    "DELEGATES_SC",
    "DELEGATES_IN",
]

_config = dotenv_values(Path(__file__).parents[2] / ".env.shared")


def _load_value(name: str) -> str:
    try:
        return _config[name]
    except KeyError:
        return "NON_LOADED_DATA"


AICC2_ID = _load_value("AICC2_ID")
DSD_ID = _load_value("DSD_ID")
ANALYSE_ID = _load_value("ANALYSE_ID")
DRIVE_LINK = _load_value("DRIVE_LINK")
DELEGATES_IN = _load_value("DELEGATES_IN")
DELEGATES_SC = _load_value("DELEGATES_SC")
