import json
from pathlib import Path

from app.parsers.wb_parser import parse_products

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "app" / "data" / "wb_phones_raw.json"

data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

print(parse_products(data))