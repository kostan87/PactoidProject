from app.llm.analyze_batch import analyze_batch

from sqlalchemy import select, func

from app.db import SessionLocal
from app.models.database.review import Review
from app.models.database.review_analysis_cache import ReviewAnalysisCache
from app.llm.review_analysis import build_review_text
from app.repositories.review_analysis_repo import upsert_review_analysis_cache

with SessionLocal.begin() as session:
    reviews = session.scalars(select(Review).where(
        (Review.root == 513853400) & (
            ((Review.text != "NULL") & (func.length(Review.text) > 30)) |
            ((Review.cons != "NULL") & (func.length(Review.cons) > 10)) | 
            ((Review.pros != "NULL") & (func.length(Review.pros) > 10))
        )
    ).limit(14)).all()

    reviews = [r for r in reviews if (session.get(ReviewAnalysisCache, r.id) is None)] # ignore cached reviews
    reviews = [build_review_text(review) for review in reviews]
    reviews_batches = [reviews[x:x+5] for x in range(0, len(reviews), 5)]

    for batch in reviews_batches:
        print(batch)
        results = analyze_batch(batch)
        print("\nFINISH\n")
        for result in results:
            review_analysis = result.model_dump()
            upsert_review_analysis_cache(session, review_analysis)