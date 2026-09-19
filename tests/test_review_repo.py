from datetime import datetime, timezone

from sqlalchemy import select

from app.repositories.product_repo import upsert_product
from app.repositories.review_repo import upsert_review

from app.models.review import Review

def test_repo_review_is_full(session):
    product = { 
        "id": 100222230,
        "subject_id": 123,
        "name": "TestProductName",
        "brand": "TestBrandBrand",
        "supplier": "TestSupplierName",
        "supplier_rating": 4.5,
        "rating": 3.2,
        "review_rating": 5.0,
        "feedbacks_count": 22,
        "price_basic": 250.00,
        "price_product": 120.00
    }

    review = {
        "id": "StringID_reviewID",
        "nm_id": 100222230,
        "text": "String_Text",
        "pros": "String_Pros",
        "cons": "String_Cons",
        "product_valuation": 5,
        "created_date": datetime(2025, 11, 19, 9, 36, 4, tzinfo=timezone.utc),
        "status_id": 16,
        "global_user_id": "StringID_globalUserId",
        "votes_pluses": 3,
        "votes_minuses": 0,
        "is_excluded_from_rating": True,
        "parent_feedback_id": "StringID_parent",
        "child_feedback_id": "StringID_child"
    }

    upsert_product(session, product)
    upsert_review(session, review)
    session.flush()
    session.expire_all()

    review_at_db = session.get(Review, "StringID_reviewID")

    assert review_at_db is not None

    assert review_at_db.id == "StringID_reviewID"
    assert review_at_db.nm_id == 100222230
    assert review_at_db.text == "String_Text"
    assert review_at_db.pros == "String_Pros"
    assert review_at_db.cons == "String_Cons"
    assert review_at_db.product_valuation == 5
    assert review_at_db.created_date == datetime(2025, 11, 19, 9, 36, 4, tzinfo=timezone.utc)
    assert review_at_db.status_id == 16
    assert review_at_db.global_user_id == "StringID_globalUserId"
    assert review_at_db.votes_pluses == 3
    assert review_at_db.votes_minuses == 0
    assert review_at_db.is_excluded_from_rating == True
    assert review_at_db.parent_feedback_id == "StringID_parent"
    assert review_at_db.child_feedback_id == "StringID_child"

def test_repo_review_update(session):
    product = { 
        "id": 200222230,
        "subject_id": 123,
        "name": "TestProductName",
        "brand": "TestBrandBrand",
        "supplier": "TestSupplierName",
        "supplier_rating": 4.5,
        "rating": 3.2,
        "review_rating": 5.0,
        "feedbacks_count": 22,
        "price_basic": 250.00,
        "price_product": 120.00
    }

    review1 = {
        "id": "StringID_reviewID",
        "nm_id": 200222230,
        "text": "String_Text",
        "pros": "String_Pros",
        "cons": "String_Cons",
        "product_valuation": 5,
        "created_date": datetime(2025, 11, 19, 9, 36, 4, tzinfo=timezone.utc),
        "status_id": 16,
        "global_user_id": "StringID_globalUserId",
        "votes_pluses": 3,
        "votes_minuses": 0,
        "is_excluded_from_rating": True,
        "parent_feedback_id": "StringID_parent",
        "child_feedback_id": "StringID_child"
    }

    review2 = {
        "id": "StringID_reviewID",
        "nm_id": 200222230,
        "text": "String_Text",
        "pros": "String_Pros",
        "cons": "String_Cons",
        "product_valuation": 5,
        "created_date": datetime(2025, 11, 19, 9, 36, 4, tzinfo=timezone.utc),
        "status_id": 16,
        "global_user_id": "StringID_globalUserId",
        "votes_pluses": 15,
        "votes_minuses": 14,
        "is_excluded_from_rating": True,
        "parent_feedback_id": "StringID_parent",
        "child_feedback_id": "StringID_child"
    }

    upsert_product(session, product)
    upsert_review(session, review1)
    session.flush()
    upsert_review(session, review2)
    session.flush()
    session.expire_all()

    review_at_db = session.scalars(select(Review).where(Review.nm_id == 200222230)).all()
    
    assert len(review_at_db) == 1

    assert review_at_db[0].votes_pluses == 15
    assert review_at_db[0].votes_minuses == 14

def test_repo_review_without_product(session):
    review = {
        "id": "StringID_reviewID",
        "nm_id": 300222230,
        "text": "String_Text",
        "pros": "String_Pros",
        "cons": "String_Cons",
        "product_valuation": 5,
        "created_date": datetime(2025, 11, 19, 9, 36, 4, tzinfo=timezone.utc),
        "status_id": 16,
        "global_user_id": "StringID_globalUserId",
        "votes_pluses": 3,
        "votes_minuses": 0,
        "is_excluded_from_rating": True,
        "parent_feedback_id": "StringID_parent",
        "child_feedback_id": "StringID_child"
    }

    assert upsert_review(session, review) is None
    session.flush()
    session.expire_all()

    review_at_db = session.scalar(select(Review).where(Review.nm_id == 300222230))
    
    assert review_at_db is None

def test_repo_review_changed_nm_id(session):
    product1 = { 
        "id": 400222230,
        "subject_id": 123,
        "name": "TestProductName",
        "brand": "TestBrandBrand",
        "supplier": "TestSupplierName",
        "supplier_rating": 4.5,
        "rating": 3.2,
        "review_rating": 5.0,
        "feedbacks_count": 22,
        "price_basic": 250.00,
        "price_product": 120.00
    }

    product2 = { 
        "id": 400222277,
        "subject_id": 123,
        "name": "TestProductName",
        "brand": "TestBrandBrand",
        "supplier": "TestSupplierName",
        "supplier_rating": 4.5,
        "rating": 3.2,
        "review_rating": 5.0,
        "feedbacks_count": 22,
        "price_basic": 250.00,
        "price_product": 120.00
    }


    review1 = {
        "id": "StringID_reviewID",
        "nm_id": 400222230,
        "text": "String_Text",
        "pros": "String_Pros",
        "cons": "String_Cons",
        "product_valuation": 5,
        "created_date": datetime(2025, 11, 19, 9, 36, 4, tzinfo=timezone.utc),
        "status_id": 16,
        "global_user_id": "StringID_globalUserId",
        "votes_pluses": 3,
        "votes_minuses": 0,
        "is_excluded_from_rating": True,
        "parent_feedback_id": "StringID_parent",
        "child_feedback_id": "StringID_child"
    }

    review2 = {
        "id": "StringID_reviewID",
        "nm_id": 400222277,
        "text": "String_Text",
        "pros": "String_Pros",
        "cons": "String_Cons",
        "product_valuation": 5,
        "created_date": datetime(2025, 11, 19, 9, 36, 4, tzinfo=timezone.utc),
        "status_id": 16,
        "global_user_id": "StringID_globalUserId",
        "votes_pluses": 15,
        "votes_minuses": 14,
        "is_excluded_from_rating": True,
        "parent_feedback_id": "StringID_parent",
        "child_feedback_id": "StringID_child"
    }

    upsert_product(session, product1)
    upsert_review(session, review1)
    session.flush()
    upsert_product(session, product2)
    upsert_review(session, review2)
    session.flush()
    session.expire_all()

    review_at_db = session.get(Review, "StringID_reviewID")
    assert review_at_db.nm_id == 400222230
    assert review_at_db.votes_pluses == 15
    assert review_at_db.votes_minuses == 14