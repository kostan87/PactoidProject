import sys
import time
from threading import Event
from collections import Counter

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.database import Review, ReviewAnalysisCache
from app.models.review_analysis import Aspect, ReviewAnalysis
from app.repositories.review_analysis_repo import upsert_review_analysis_cache
from app.llm.analyze_batch import analyze_batch

def aggregate(aspects: list[Aspect]) -> dict:
    stats = {}
    for a in aspects:
        key = a.aspect
        stats.setdefault(key, {"pos": 0, "neg": 0, "defects": [], "advantages": []})
        if a.sentiment == "positive":
            stats[key]["pos"] += 1
        elif a.sentiment == "negative":
            stats[key]["neg"] += 1
        if a.type == "defect":
            stats[key]["defects"].append(a.detail)
        elif a.type == "advantage":
            stats[key]["advantages"].append(a.detail)
    return stats

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
        reviews = session.scalars(select(Review).where(
            (Review.root == 513853400) & (
                ((Review.text != "NULL") & (func.length(Review.text) > 30)) |
                ((Review.cons != "NULL") & (func.length(Review.cons) > 10)) | 
                ((Review.pros != "NULL") & (func.length(Review.pros) > 10))
            )
        ).limit(count)).all()
    return reviews

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