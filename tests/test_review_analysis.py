import threading
import pytest

from tests.factories import DELETE, make_expected_review
from app.models.database import Review, ReviewAnalysisCache
from app.models.review_analysis import Aspect, ReviewAnalysis, BatchAnalysis
from app.llm.review_analysis import build_review_text, form_messages_for_analysis, get_reviews_from_db, remove_cached_reviews, analyze_reviews_batches
from app.repositories.review_analysis_repo import upsert_review_analysis_cache

def test_build_review_text_full_review():
    review = Review(**make_expected_review())
    result = build_review_text(review)
    assert result == "[ID: StringID_reviewID] String_Text\nПлюсы: String_Pros\nМинусы: String_Cons"

def test_build_review_text_empty_review():
    review = Review(**make_expected_review(text=DELETE, pros=DELETE, cons=DELETE))
    result = build_review_text(review)
    assert result == "[ID: StringID_reviewID] (пусто)"

def test_get_reviews_from_db(session):
    review = Review(**make_expected_review())
    session.add(review)
    review_at_db = get_reviews_from_db(session, 153, 1)[0]
    assert review_at_db == review

def test_remove_cached_reviews(session):
    reviews = [
        Review(**make_expected_review(id="StringID_One")),
        Review(**make_expected_review(id="StringID_Two")),
        Review(**make_expected_review(id="StringID_Three"))
    ]
    cached_review = ReviewAnalysisCache(**{"id": "StringID_Two", "aspects": [], "summary": "", "overall_sentiment": ""})

    session.add(cached_review)
    session.flush()

    filtered_reviews = remove_cached_reviews(session, reviews)

    assert len(filtered_reviews) == 2
    assert reviews[1] not in filtered_reviews

def test_upsert_review_analysis_cache(session):
    review_analysis = {"id": "StringID_One", "aspects": [], "summary": "", "overall_sentiment": "positive"}

    upsert_review_analysis_cache(session, review_analysis)
    session.flush()

    review_analysis_cache = session.get(ReviewAnalysisCache, "StringID_One")
    assert review_analysis_cache.overall_sentiment == "positive"