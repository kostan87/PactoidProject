import sys
import time
from threading import Event

from sqlalchemy import select

from app.db import SessionLocal
from app.models.database import Review, ReviewAnalysisCache
from app.models.review_analysis import ReviewAnalysis
from app.repositories.review_analysis_repo import upsert_review_analysis_cache
from app.llm.analyze_batch import analyze_batch

def build_review_text(review: dict) -> str:
    parts = [f"[ID: {review.id}]"]
    if review.text:
        parts.append(review.text.strip())
    if review.pros:
        parts.append(f"Плюсы: {review.pros.strip()}")
    if review.cons:
        parts.append(f"Минусы: {review.cons.strip()}")
    return "\n".join(parts) if parts else "(пусто)"

def get_reviews_from_db(count: str) -> list[Review]:
    with SessionLocal.begin() as session:
        result = session.scalars(select(Review).where(Review.root == 513853400).limit(count)).all()
    return result

def remove_cached_reviews(reviews: list[Review]) -> list[Review]:
    with SessionLocal.begin() as session:
        result = [r for r in reviews if (session.get(ReviewAnalysisCache, r.id) is None)]
    return result

def save_reviews_analysis_to_db(results: list[ReviewAnalysis]) -> None:
    with SessionLocal.begin() as session:
        for result in results:
            upsert_review_analysis_cache(session, result.model_dump())

def analyze_reviews_batch(threadEvent: Event, reviews_batch: list[str]) -> None:
    try:
        save_reviews_analysis_to_db(analyze_batch(reviews_batch))
    finally:
        threadEvent.set()

def start_timer(threadEvent: Event) -> None:
    start_time = time.time()
    while not threadEvent.is_set():
        elapsed = time.time() - start_time
        sys.stdout.write(f"\rРаботаю... {elapsed:6.1f} сек")
        sys.stdout.flush()
        threadEvent.wait(timeout=0.5)
    sys.stdout.write(f"\n")