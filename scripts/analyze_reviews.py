from app.db import SessionLocal
from app.llm.review_analysis import build_review_text, get_reviews_from_db, remove_cached_reviews, analyze_reviews_batches

with SessionLocal() as session:
    reviews_from_db = get_reviews_from_db(session, 513853400, 500)
    reviews_for_analysis = remove_cached_reviews(session, reviews_from_db)
    reviews_text = [build_review_text(review) for review in reviews_for_analysis]
    reviews_batches = [reviews_text[x:x+5] for x in range(0, len(reviews_text), 5)]
    analyze_reviews_batches(session, reviews_batches)