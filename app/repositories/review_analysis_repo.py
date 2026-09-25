from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.database.review_analysis_cache import ReviewAnalysisCache

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