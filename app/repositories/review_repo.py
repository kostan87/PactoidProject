from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.review import Review

def upsert_review(session:Session, review:dict) -> Review | None:
    product_at_db = session.scalar(select(Product).where(Product.id == review["nm_id"]))
    review_at_db = session.scalar(select(Review).where(Review.id == review["id"]))

    if product_at_db is None:
        return None

    if review_at_db is None: # INSERT
        review_at_db = Review(**review)
        session.add(review_at_db)
    else: # UPDATE
        review = {key:value for key,value in review.items() if key not in ["id", "nm_id"]}
        for key,value in review.items():
            setattr(review_at_db, key, value)
    return review_at_db