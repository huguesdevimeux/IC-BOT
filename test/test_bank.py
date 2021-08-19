import pytest
from tinydb import TinyDB

import ICBOT.icecoin.bank as bank
import tinydb


@pytest.fixture()
def patch_db(monkeypatch, tmp_path):
    # monkeypatching automatically reset at the end.
    monkeypatch.setattr(bank, "_db", TinyDB(tmp_path / "test.json"))


def test_is_registered(patch_db):
    assert not bank.is_registered("1")
    bank.put_entry(bank.BankEntry("1", 69))
    assert bank.is_registered("1")


def test_entries_management(patch_db):
    entry = bank.BankEntry("1", 78)
    bank.put_entry(entry)
    assert bank.get_entry("1") == entry
    entry.amount = 88
    bank.put_entry(entry)
    assert bank.get_entry("1").amount == 88
    assert bank.get_entry("1") == entry


def test_get_entry(patch_db):
    with pytest.raises(KeyError, match="no entry"):
        bank.get_entry("1")
    entry = bank.BankEntry("1", 78)
    bank.put_entry(entry)
    assert bank.get_entry("1") == entry
