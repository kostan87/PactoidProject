from sqlalchemy import select, inspect

from app.repositories.wb_product_repo import upsert_wb_product
from app.repositories.review_repo import upsert_review

from app.models.review import Review

from tests.factories import make_expected_product, make_expected_review
from tests.assertions import assert_dict_subset

def test_repo_review_is_full(session):
    product = make_expected_product()
    review = make_expected_review()

    upsert_wb_product(session, product)
    upsert_review(session, review)
    session.flush()
    session.expire_all()

    review_at_db = session.get(Review, "StringID_reviewID")
    assert review_at_db is not None

    mapper = inspect(Review).mapper
    review_at_db = {col.key: getattr(review_at_db, col.key) for col in mapper.columns}
    assert_dict_subset(review_at_db, review)

def test_repo_review_update(session):
    product = make_expected_product()
    review1 = make_expected_review()
    review2 = make_expected_review(votes_pluses=15, votes_minuses=14)

    upsert_wb_product(session, product)
    upsert_review(session, review1)
    session.flush()
    upsert_review(session, review2)
    session.flush()
    session.expire_all()

    reviews_at_db = session.scalars(select(Review).where(Review.nm_id == 1)).all()
    assert len(reviews_at_db) == 1

    mapper = inspect(Review).mapper
    review_at_db = {col.key: getattr(reviews_at_db[0], col.key) for col in mapper.columns}
    assert_dict_subset(review_at_db, {"votes_pluses": 15, "votes_minuses": 14})

def test_repo_review_without_product(session):
    review = make_expected_review()

    assert upsert_review(session, review) is None
    session.flush()
    session.expire_all()

    review_at_db = session.scalar(select(Review).where(Review.nm_id == 1))
    assert review_at_db is None

def test_repo_review_changed_nm_id(session):
    product1 = make_expected_product(id=100)
    product2 = make_expected_product(id=200)
    review1 = make_expected_review(nm_id=100)
    review2 = make_expected_review(nm_id=200)

    upsert_wb_product(session, product1)
    upsert_review(session, review1)
    session.flush()
    upsert_wb_product(session, product2)
    upsert_review(session, review2)
    session.flush()
    session.expire_all()

    mapper = inspect(Review).mapper
    review_at_db = session.get(Review, "StringID_reviewID")
    review_at_db = {col.key: getattr(review_at_db, col.key) for col in mapper.columns}
    assert_dict_subset(review_at_db, {"nm_id": 100})