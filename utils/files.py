import json
import tomllib
from pathlib import Path
from functools import lru_cache, wraps

from utils.text import get_hash

@lru_cache(maxsize=1)
def load_json_file(data_path: Path) -> dict:
    data = json.loads(data_path.read_text(encoding="utf-8"))
    return data

@lru_cache(maxsize=1)
def load_config(path: Path) -> dict:
    with open(path, "rb") as file:
        return tomllib.load(file)

def llm_cache(fn):
    @wraps(fn)
    def wrapper(client, messages: list[dict], response_model, **kwargs):
        CACHE_DIR = Path(__file__).resolve().parent / "cache" / "llm"
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        key = get_hash(json.dumps({"messages": messages, "model": response_model.__name__}, sort_keys=True, ensure_ascii=False))
        path = CACHE_DIR / f"{key}.json"

        if path.exists():
            return response_model.model_validate_json(path.read_text(encoding="utf-8"))

        result = fn(client, messages, response_model, **kwargs)
        path.write_text(result.model_dump_json(), encoding="utf-8")
        return result

    return wrapper