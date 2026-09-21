from pathlib import Path

from app.parsers.wb_parser import parse_products
from app.repositories.wb_product_repo import upsert_wb_product
from utils.files import load_json_file
from utils.database import process_batch

base_dir = Path(__file__).resolve().parents[1] 
data_path = base_dir / "app" / "data" / "wb_phones_raw.json"
data = load_json_file(data_path)
products = parse_products(data)
process_batch(products, upsert_wb_product)