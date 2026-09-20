from pathlib import Path

from app.parsers.wb_parser import parse_products
from app.parsers.wb_parser import parse_reviews
from utils.files import load_json_file

base_dir = Path(__file__).resolve().parents[1] / "app" / "data" 

data_path = base_dir / "wb_phones_raw.json"
data = load_json_file(data_path)
print(parse_products(data)[0])

data_path = base_dir / "reviews" / "wb_reviews_raw_513853400.json"
data = load_json_file(data_path)
print(parse_reviews(data)[0])