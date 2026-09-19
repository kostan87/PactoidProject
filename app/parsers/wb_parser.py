from datetime import datetime

def parse_product(raw: dict) -> dict | None:
    wb_id = raw.get("id")
    if not wb_id:
        return None
    
    brand = raw.get("brand") or None
    supplier = raw.get("supplier") or None

    sizes = raw.get("sizes") or []
    first = sizes[0] if sizes else None
    price = (first or {}).get("price") or {}
    price_basic = (price.get("basic") or 0) / 100
    price_product = (price.get("product") or 0) / 100

    return {
        "id": wb_id,
        "subject_id": raw.get("subjectId"),
        "name": raw.get("name"),
        "brand": brand,
        "supplier": supplier,
        "supplier_rating": raw.get("supplierRating"),
        "rating": raw.get("rating"),
        "review_rating": raw.get("reviewRating"),
        "feedbacks_count": raw.get("feedbacks") or 0,
        "price_basic": price_basic,
        "price_product": price_product
    }

def parse_products(data: dict) -> list[dict]:
    if not isinstance(data, dict):
        return []

    products = []
    for product in (data.get("products") or []):
        if isinstance(product, dict):
            parsed_product = parse_product(product)
            if parsed_product is not None:
                products.append(parsed_product)
    return products

def parse_review(raw: dict) -> dict | None:
    review_id = raw.get("id") or None
    nm_id = raw.get("nmId") or None
    created_date = raw.get("createdDate") or None
    if not review_id or not nm_id or not created_date:
        return None

    created_date = datetime.fromisoformat(created_date)

    votes = raw.get("votes") or {}  
    votes_pluses = votes.get("pluses") or 0
    votes_minuses = votes.get("minuses") or 0

    excluded_from_rating = raw.get("excludedFromRating") or {}
    excluded_from_rating = excluded_from_rating.get("isExcluded") or False

    return {
        "id": review_id,
        "nm_id": nm_id,
        "text": raw.get("text") or None,
        "pros": raw.get("pros") or None,
        "cons": raw.get("cons") or None,
        "product_valuation": raw.get("productValuation") or None,
        "created_date": created_date,
        "status_id": raw.get("statusId") or None,
        "global_user_id": raw.get("globalUserId") or None,
        "votes_pluses": votes_pluses,
        "votes_minuses": votes_minuses,
        "is_excluded_from_rating": excluded_from_rating,
        "parent_feedback_id": raw.get("parentFeedbackId") or None,
        "child_feedback_id": raw.get("childFeedbackId") or None
    }

def parse_reviews(data: dict) -> list[dict]:
    if not isinstance(data, dict):
        return []

    reviews = []
    for review in (data.get("feedbacks") or []):
        if isinstance(review, dict):
            parsed_review = parse_review(review)
            if parsed_review is not None:
                reviews.append(parsed_review)
    return reviews