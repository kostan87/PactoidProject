from app.parsers.wb_parser import parse_product, parse_products, parse_review, parse_reviews

from tests.factories import DELETE, make_raw_product, make_expected_product, make_raw_review, make_expected_review

from tests.assertions import assert_dict_subset

# PRODUCT TESTS

def test_parse_product_full():
    result = parse_product(make_raw_product())
    assert_dict_subset(result, make_expected_product())

def test_parse_no_sizes():
    result = parse_product(make_raw_product(sizes=DELETE))
    assert_dict_subset(result, {"price_basic": 0, "price_product": 0})

def test_parse_sizes_is_empty():
    result = parse_product(make_raw_product(sizes=[]))
    assert_dict_subset(result, {"price_basic": 0, "price_product": 0})

def test_parse_prices_is_zero():
    result = parse_product(make_raw_product(sizes=[{"price": {"basic": 0,"product": 0}}]))
    assert_dict_subset(result, {"price_basic": 0, "price_product": 0})

def test_parse_price_is_empty():
    result = parse_product(make_raw_product(sizes=[{"price": {}}]))
    assert_dict_subset(result, {"price_basic": 0, "price_product": 0})

def test_parse_no_price_key():
    result = parse_product(make_raw_product(sizes=[{}]))
    assert_dict_subset(result, {"price_basic": 0, "price_product": 0})

def test_parse_brand_is_empty():
    result = parse_product(make_raw_product(brand=""))
    assert result["brand"] is None

def test_parse_supplier_is_empty():
    result = parse_product(make_raw_product(supplier=""))
    assert result["supplier"] is None

def test_parse_feedbacks_is_zero():
    result = parse_product(make_raw_product(feedbacks=0))
    assert_dict_subset(result, {"feedbacks_count": 0})

def test_parse_rating_is_zero():
    result = parse_product(make_raw_product(rating=0))
    assert_dict_subset(result, {"rating": 0})

def test_parse_no_id():
    result = parse_product(make_raw_product(id=DELETE))
    assert result is None

# PRODUCTS TESTS

def test_parse_product_without_id_at_products():
    raw = {"products": [make_raw_product(), make_raw_product(id=DELETE)]}
    assert len(parse_products(raw)) == 1

def test_parse_products_is_empty():
    raw = {"products": []}
    assert parse_products(raw) == []

def test_parse_no_products_key():
    raw = {}
    assert parse_products(raw) == []

def test_parse_products_is_not_dict():
    raw = ["No products"]
    assert parse_products(raw) == []

def test_parse_not_dict_at_products():
    raw = {"products": [make_raw_product(), "TestWrongItem"]}
    assert len(parse_products(raw)) == 1

# REVIEW TESTS

def test_parse_review_full():
    result = parse_review(make_raw_review(), 153)
    assert_dict_subset(result, make_expected_review())

def test_parse_review_without_id():
    result = parse_review(make_raw_review(id=DELETE), 153)
    assert result is None

def test_parse_review_without_nmId():
    result = parse_review(make_raw_review(nmId=DELETE), 153)
    assert result is None

def test_parse_review_without_createdDate():
    result = parse_review(make_raw_review(createdDate=DELETE), 153)
    assert result is None

def test_parse_review_without_votes():
    result = parse_review(make_raw_review(votes=DELETE), 153)
    assert_dict_subset(result, {"votes_pluses": 0, "votes_minuses": 0})

def test_parse_review_without_excludedFromRating():
    result = parse_review(make_raw_review(excludedFromRating=DELETE), 153)
    assert_dict_subset(result, {"is_excluded_from_rating": False})

def test_parse_review_with_empty_text():
    result = parse_review(make_raw_review(text="", pros="", cons=""), 153)
    assert_dict_subset(result, {"text": None, "pros": None, "cons": None})

def test_parse_review_without_product_valuation():
    result = parse_review(make_raw_review(productValuation=DELETE), 153)
    assert_dict_subset(result, {"product_valuation": None})

# REVIEWS TESTS

def test_parse_reviews_feedbacks_is_empty():
    raw = {"feedbacks": []}
    assert parse_reviews(raw, 153) == []

def test_parse_reviews_no_feedbacks_key():
    raw = {}
    assert parse_reviews(raw, 153) == []

def test_parse_reviews_is_not_dict():
    raw = ["No views"]
    assert parse_reviews(raw, 153) == []

def test_parse_not_dict_at_reviews():
    raw = {"feedbacks": [make_raw_review(),"TestWrongItem"]}
    assert len(parse_reviews(raw, 153)) == 1