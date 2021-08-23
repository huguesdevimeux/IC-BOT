import dataclasses
import datetime
import inspect
from dataclasses import dataclass
from pathlib import Path

from tinydb import TinyDB, Query

from ICBOT.constants.constants import Constants
from ICBOT.icecoin.exceptions import NotEnoughMoney

_path_db = Path(__file__).parents[3] / "data" / "bank.json"

_db = TinyDB(_path_db)
_BankEntryQuery = Query()


def _check_can_withdraw_amount(func):
    def wrapper(self, *args, **kwargs):
        amount = int(inspect.getcallargs(func, self, *args, **kwargs)["amount"])
        if amount > self.amount:
            raise NotEnoughMoney()
        return func(self, *args, **kwargs)

    return wrapper


@dataclass(order=True)
class BankEntry:
    id_discord: int = dataclasses.field(compare=False)
    amount: int = 0

    _last_mined_ser: str = dataclasses.field(
        default=datetime.datetime.isoformat(datetime.datetime.min), compare=False
    )

    @property
    def _last_mined(self) -> datetime.datetime:
        # This is used to serialize and deserialize on the fly _last_mined, since a raw datetime object can't be JSOn
        # serialized (-_-) and thus raises an error in the db.
        return datetime.datetime.fromisoformat(self._last_mined_ser)

    @_last_mined.setter
    def _last_mined(self, value: datetime.datetime):
        self._last_mined_ser = value.isoformat()

    def __str__(self):
        return f"{self.amount} {Constants.ICECOIN}"

    @_check_can_withdraw_amount
    def transfer(self, receiver: "BankEntry", amount: int):
        """
        Transfers to amount from self to receiver.
        Parameters
        ----------
        receiver
            The receiver.
        amount
            The amount.
        Returns
        -------
            self, for chaining.
        """
        self.withdraw(amount)
        receiver.add(amount)
        return self

    @_check_can_withdraw_amount
    def withdraw(self, amount: int) -> "BankEntry":
        """
        Withdraw amount icécoin from the entry. Returns false and does not do anything if there is not enough money.
        Parameters
        ----------
        amount
            The amount to withdraw.
        """
        self.amount -= amount
        return self

    def add(self, amount: int) -> "BankEntry":
        self.amount += amount
        return self

    def can_mine(self):
        """Whether the user can mine."""
        return (datetime.datetime.now() - self._last_mined).total_seconds() > 10

    def mine(self):
        assert self.can_mine()
        self.add(Constants.AMOUNT_MINING)
        self._last_mined = datetime.datetime.now()
        return self


def is_registered(id_discord: int) -> bool:
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


def get_entry(id_discord: int) -> BankEntry:
    """
    Gets the bank entry of the id. Returns a fresh one if it is not registered.

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
        return BankEntry(id_discord, 0)
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


def put_entries(*entries: BankEntry):
    [put_entry(entry) for entry in entries]
