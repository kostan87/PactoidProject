from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.database import Review, ReviewAnalysisCache
from app.models.review_analysis import Aspect

def get_reviews_analysis_from_db(session: Session, reviews: list[Review]) -> list[ReviewAnalysisCache]:
    reviews_ids = [review.id for review in reviews]
    return session.scalars(select(ReviewAnalysisCache).where(ReviewAnalysisCache.id.in_(reviews_ids))).all()

def get_aspects_from_reviews_analysis(reviews_analysis_for_product: list[ReviewAnalysisCache]) -> list[Aspect]:
    result = []
    for review_analysis in reviews_analysis_for_product:
        result += [Aspect(**aspect) for aspect in review_analysis.aspects]
    return result

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