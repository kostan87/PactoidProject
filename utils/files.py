import json
from pathlib import Path

def load_json_file(data_path: Path) -> dict:
    data = json.loads(data_path.read_text(encoding="utf-8"))
    return data