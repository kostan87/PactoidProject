import json
from pathlib import Path

from app.db import SessionLocal
from app.parsers.wb_parser import parse_reviews
from app.repositories.review_repo import upsert_review

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "app" / "data" / "wb_reviews_raw.json"

data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

reviews = parse_reviews(data)

with SessionLocal() as session:
    try:
        for reviewData in reviews:
            review = upsert_review(session, reviewData)
        session.commit()
    except Exception:
        session.rollback()
        raise