import typing
from pathlib import Path
import json

_data_path = Path(__file__).parents[3] / "data"

def _load_drive_files_names() -> typing.Iterable[str]: 
   if not _data_path.is_dir(): 
       return ["NON_LOADED_DATA"]
   with open(_data_path / "drive" / "files.txt", "r") as f: 
       return f.readlines()

def _load_drive_path() -> Path: 
    if not _data_path.is_dir(): 
        return "NON_LOADED_DATA"
    return _data_path / "drive"

def _load_copie_pates() -> dict:
    if not _data_path.is_dir(): 
        return "NON_LOADED_DATA"
    return json.load(open(_data_path / "copie-pates.json"))["messages"]

DRIVE_PATH = _load_drive_path()
ALL_FILES_DRIVE = _load_drive_files_names()
COPIE_PATES = _load_copie_pates()
