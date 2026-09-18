import json
from pathlib import Path

from app.db import SessionLocal
from app.parsers.wb_parser import parse_products
from app.repositories.product_repo import upsert_product

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "app" / "data" / "wb_phones_raw.json"

data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

products = parse_products(data)

with SessionLocal() as session:
    try:
        for productData in products:
            product = upsert_product(session, productData)
        session.commit()
        print(f"Imported {len(products)} objects")
    except Exception:
        session.rollback()
        raise