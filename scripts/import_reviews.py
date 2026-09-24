from pathlib import Path

from app.parsers.wb_parser import parse_reviews
from app.repositories.review_repo import upsert_review
from utils.files import load_json_file
from utils.database import process_batch

base_dir = Path(__file__).resolve().parents[1] 
data_path = base_dir / "app" / "data" / "reviews"
for path in data_path.glob("*.json"):
    root = int(path.stem.split("_")[-1])
    data = load_json_file(path)
    products = parse_reviews(data, root)
    print(path.name)
    process_batch(products, upsert_review)