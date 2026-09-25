from app.llm.analyze_batch import analyze_batch

from sqlalchemy import select, func

from app.db import SessionLocal
from app.models.database.review import Review
from app.models.review_analysis.batch_analysis import BatchAnalysis
from utils.text import build_review_text, review_hash

with SessionLocal.begin() as session:
    reviews = session.scalars(select(Review).where(
        (Review.root == 513853400) & (
            ((Review.text != "NULL") & (func.length(Review.text) > 30)) |
            ((Review.cons != "NULL") & (func.length(Review.cons) > 10)) | 
            ((Review.pros != "NULL") & (func.length(Review.pros) > 10))
        )
    ).limit(2)).all()

    reviews = [build_review_text(review) for review in reviews]

results = analyze_batch(reviews)
print(f"\n{reviews}\n→")
for review in results:
    print(review.model_dump_json(indent=2))