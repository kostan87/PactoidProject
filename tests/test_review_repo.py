from sqlalchemy import select, inspect

from app.repositories.review_repo import upsert_review
from app.models.database.review import Review
from tests.factories import make_expected_review
from tests.assertions import assert_dict_subset

def test_repo_review_is_full(session):
    review = make_expected_review()

    upsert_review(session, review)
    session.flush()
    session.expire_all()

    review_at_db = session.get(Review, "StringID_reviewID")
    assert review_at_db is not None

    mapper = inspect(Review).mapper
    review_at_db = {col.key: getattr(review_at_db, col.key) for col in mapper.columns}
    assert_dict_subset(review_at_db, review)

def test_repo_review_update(session):
    review1 = make_expected_review()
    review2 = make_expected_review(votes_pluses=15, votes_minuses=14)

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

def test_repo_review_changed_nm_id(session):
    review1 = make_expected_review(nm_id=100)
    review2 = make_expected_review(nm_id=200)

    upsert_review(session, review1)
    session.flush()
    upsert_review(session, review2)
    session.flush()
    session.expire_all()

    mapper = inspect(Review).mapper
    review_at_db = session.get(Review, "StringID_reviewID")
    review_at_db = {col.key: getattr(review_at_db, col.key) for col in mapper.columns}
    assert_dict_subset(review_at_db, {"nm_id": 100})