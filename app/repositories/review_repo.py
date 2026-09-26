from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.database.review import Review


from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.database import Review, ReviewAnalysisCache
from app.models.review_analysis import ReviewAnalysis

def upsert_review(session:Session, review:dict) -> Review | None:
    review_at_db = session.scalar(select(Review).where(Review.id == review["id"]))

    if review_at_db is None: # INSERT
        review_at_db = Review(**review)
        session.add(review_at_db)
    else: # UPDATE
        review = {key:value for key,value in review.items() if key not in ["id", "nm_id"]}
        for key,value in review.items():
            setattr(review_at_db, key, value)
    return review_at_db

def upsert_review_analysis_cache(session:Session, review_analysis:dict) -> ReviewAnalysisCache | None:
    review_analysis_at_db = session.scalar(select(ReviewAnalysisCache).where(ReviewAnalysisCache.id == review_analysis["id"]))

    if review_analysis_at_db is None: # INSERT
        review_analysis_at_db = ReviewAnalysisCache(**review_analysis)
        session.add(review_analysis_at_db)
    else: # UPDATE
        review_analysis = {key:value for key,value in review_analysis.items() if key not in ["id"]}
        for key,value in review_analysis.items():
            setattr(review_analysis_at_db, key, value)
    return review_analysis_at_db

def get_reviews_from_db(session: Session, root: int, count: str) -> list[Review]:
    return session.scalars(select(Review).where(Review.root == root).limit(count)).all()

def remove_cached_reviews(session: Session, reviews: list[Review]) -> list[Review]:
    return [r for r in reviews if (session.get(ReviewAnalysisCache, r.id) is None)]

def save_reviews_analysis_to_db(session: Session, results: list[ReviewAnalysis]) -> None:
    for result in results:
        upsert_review_analysis_cache(session, result.model_dump())