from app.db import SessionLocal
from app.repositories.product_repo import get_products_from_db, upsert_product_analysis_cache
from app.repositories.review_repo import get_reviews_for_products
from app.llm.product_analysis import aggregate, get_reviews_analysis_from_db, get_aspects_from_reviews_analysis

with SessionLocal() as session:
    products = get_products_from_db(session, 1000)
    reviews_for_products = get_reviews_for_products(session, products)
    reviews_for_products = {root: reviews for root, reviews in reviews_for_products.items() if reviews}

    for root, reviews_for_product in reviews_for_products.items():
        reviews_analysis_for_product = get_reviews_analysis_from_db(session, reviews_for_product)
        aspects = get_aspects_from_reviews_analysis(reviews_analysis_for_product)
        product_analysis_cache = {
            "root": root,
            "aggregate": aggregate(aspects),
            "reviews_count": len(reviews_analysis_for_product)
        }
        upsert_product_analysis_cache(session, product_analysis_cache)
        session.commit()