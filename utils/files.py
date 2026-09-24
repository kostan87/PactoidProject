import json
import tomllib
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def load_json_file(data_path: Path) -> dict:
    data = json.loads(data_path.read_text(encoding="utf-8"))
    return data

@lru_cache(maxsize=1)
def load_config(path: Path) -> dict:
    with open(path, "rb") as file:
        return tomllib.load(file)