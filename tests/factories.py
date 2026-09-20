from datetime import datetime, timezone

class _Delete:
    def __repr__(self):
        return "DELETE"

DELETE = _Delete()


def make_raw_product(**overrides):
    base = {
        "id": 1,
        "subjectId": 165,
        "name": "TestProductName",
        "brand": "TestBrandBrand",
        "supplier": "TestSupplierName",
        "supplierRating": 4.5,
        "rating": 3.2,
        "reviewRating": 5.0,
        "feedbacks": 22,
        "sizes": [{"price": {"basic": 25000, "product": 12000}}],
    }
    for key, value in overrides.items():
        if isinstance(value, _Delete):
            base.pop(key, None)
        else:
            base[key] = value
    return base

def make_expected_product(**overrides):
    base = {
        "id": 1,
        "subject_id": 165,
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
    for key, value in overrides.items():
        if isinstance(value, _Delete):
            base.pop(key, None)
        else:
            base[key] = value
    return base

def make_raw_review(**overrides):
    base = {
        "id": "StringID_reviewID",
        "globalUserId": "StringID_globalUserId",
        "nmId": 1,
        "text": "String_Text",
        "pros": "String_Pros",
        "cons": "String_Cons",
        "productValuation": 5,
        "createdDate": "2025-11-19T09:36:04Z",
        "votes": {
            "pluses": 3,
            "minuses": 0
        },
        "statusId": 16,
        "parentFeedbackId": "StringID_parent",
        "childFeedbackId": "StringID_child",
        "excludedFromRating": {
            "isExcluded": True,
            "reasons": [
                "hasIncludedChild"
            ]
        }
    }
    for key, value in overrides.items():
        if isinstance(value, _Delete):
            base.pop(key, None)
        else:
            base[key] = value
    return base

def make_expected_review(**overrides):
    base = {
        "id": "StringID_reviewID",
        "nm_id": 1,
        "text": "String_Text",
        "pros": "String_Pros",
        "cons": "String_Cons",
        "product_valuation":5,
        "created_date": datetime(2025, 11, 19, 9, 36, 4, tzinfo=timezone.utc),
        "status_id": 16,
        "global_user_id": "StringID_globalUserId",
        "votes_pluses": 3,
        "votes_minuses": 0,
        "is_excluded_from_rating": True,
        "parent_feedback_id": "StringID_parent",
        "child_feedback_id": "StringID_child"
    }
    for key, value in overrides.items():
        if isinstance(value, _Delete):
            base.pop(key, None)
        else:
            base[key] = value
    return base