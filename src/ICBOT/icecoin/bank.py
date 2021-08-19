import dataclasses
from dataclasses import dataclass
from pathlib import Path

import tinydb
from tinydb import TinyDB, Query

from ICBOT.constants.constants import Constants

_path_db = Path(__file__).parents[3] / "data" / "bank.json"

_db = TinyDB(_path_db)
_BankEntryQuery = Query()


@dataclass(order=True)
class BankEntry:
    id_discord: str = dataclasses.field(compare=False)
    amount: int

    def __str__(self):
        return f"{self.amount} {Constants.ICECOIN}"


def is_registered(id_discord: str) -> bool:
    """
    Checks whether the id is registered at the bank.
    Parameters
    ----------
    id_discord
        The id of check.
    Returns
    -------
        Whether the id is registered.
    """
    return _db.contains(cond=_BankEntryQuery["id_discord"] == id_discord)


def get_entry(id_discord: str) -> BankEntry:
    """
    Gets the bank entry of the id.

    Parameters
    ----------
    id_discord
        The id.
    Returns
    -------
        The entry.

    Raises
    ------

    """
    ret = _db.search(_BankEntryQuery["id_discord"] == id_discord)
    if len(ret) == 0:
        raise KeyError("There are no entry with that id.")
    if len(ret) > 1:
        raise KeyError("There are several entries with that id.")
    return BankEntry(**ret[0])


def put_entry(entry: BankEntry) -> BankEntry:
    """
    Put (or update if existing) an entry.
    Parameters
    ----------
    entry
        The new entry.
    Returns
    -------
        The entry.
    """
    _db.upsert(vars(entry), cond=_BankEntryQuery["id_discord"] == entry.id_discord)
    return entry
