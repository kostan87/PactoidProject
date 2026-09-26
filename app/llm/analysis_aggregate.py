from collections import Counter

from sqlalchemy import select

from app.db import SessionLocal
from app.models.database import ReviewAnalysisCache
from app.models.review_analysis import Aspect

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

def load_review_analysis_from_db() -> list[ReviewAnalysisCache]:
    with SessionLocal.begin() as session:
        result = session.scalars(select(ReviewAnalysisCache)).all()
    return result

reviews_analysis = load_review_analysis_from_db()

aspects = []
for review_analysis in reviews_analysis:
    aspects += [Aspect(**aspect) for aspect in review_analysis.aspects]
    
print(aggregate(aspects))