from app.parsers.wb_parser import parse_product, parse_products

def test_parse_product_full():
    raw = {
        "id": 1,
        "subjectId": 123,
        "name": "TestProductName",
        "brand": "TestBrandBrand",
        "supplier": "TestSupplierName",
        "supplierRating": 4.5,
        "rating": 3.2,
        "reviewRating": 5.0,
        "feedbacks": 22,
        "sizes": [
            {
                "price": {
                    "basic": 25000,
                    "product": 12000
                }
            }
        ]
    }

    result = parse_product(raw)
    assert result["id"] == 1
    assert result["subject_id"] == 123
    assert result["name"] == "TestProductName"
    assert result["brand"] == "TestBrandBrand"
    assert result["supplier"] == "TestSupplierName"
    assert result["supplier_rating"] == 4.5
    assert result["rating"] == 3.2
    assert result["review_rating"] == 5.0
    assert result["feedbacks_count"] == 22
    assert result["price_basic"] == 250.00
    assert result["price_product"] == 120.00

def test_parse_no_sizes():
    raw = {
        "id": 123456789,
        "subjectId": 234567891,
        "name": "TestProductName",
        "brand": "TestBrandBrand",
        "supplier": "TestSupplierName",
        "supplierRating": 345678912,
        "rating": 456789123,
        "reviewRating": 56789123,
        "feedbacks": 678912345
    }

    result = parse_product(raw)
    assert result["price_basic"] == 0
    assert result["price_product"] == 0

def test_parse_sizes_is_empty():
    raw = {
        "id": 123456789,
        "subjectId": 234567891,
        "name": "TestProductName",
        "brand": "TestBrandBrand",
        "supplier": "TestSupplierName",
        "supplierRating": 345678912,
        "rating": 456789123,
        "reviewRating": 56789123,
        "feedbacks": 678912345,
        "sizes": []
    }

    result = parse_product(raw)
    assert result["price_basic"] == 0
    assert result["price_product"] == 0

def test_parse_prices_is_zero():
    raw = {
        "id": 123456789,
        "subjectId": 234567891,
        "name": "TestProductName",
        "brand": "TestBrandBrand",
        "supplier": "TestSupplierName",
        "supplierRating": 345678912,
        "rating": 456789123,
        "reviewRating": 56789123,
        "feedbacks": 678912345,
        "sizes": [
            {
                "price": {
                    "basic": 0,
                    "product": 0
                }
            }
        ]
    }

    result = parse_product(raw)
    assert result["price_basic"] == 0
    assert result["price_product"] == 0

def test_parse_price_is_empty():
    raw = {
        "id": 123456789,
        "subjectId": 234567891,
        "name": "TestProductName",
        "brand": "TestBrandBrand",
        "supplier": "TestSupplierName",
        "supplierRating": 345678912,
        "rating": 456789123,
        "reviewRating": 56789123,
        "feedbacks": 678912345,
        "sizes": [
            {
                "price": {}
            }
        ]
    }

    result = parse_product(raw)
    assert result["price_basic"] == 0
    assert result["price_product"] == 0

def test_parse_no_price_key():
    raw = {
        "id": 123456789,
        "subjectId": 234567891,
        "name": "TestProductName",
        "brand": "TestBrandBrand",
        "supplier": "TestSupplierName",
        "supplierRating": 345678912,
        "rating": 456789123,
        "reviewRating": 56789123,
        "feedbacks": 678912345,
        "sizes": [{}]
    }

    result = parse_product(raw)
    assert result["price_basic"] == 0
    assert result["price_product"] == 0

def test_parse_brand_is_empty():
    raw = {
        "id": 123456789,
        "subjectId": 234567891,
        "name": "TestProductName",
        "brand": "",
        "supplier": "TestSupplierName",
        "supplierRating": 345678912,
        "rating": 456789123,
        "reviewRating": 56789123,
        "feedbacks": 678912345,
        "sizes": [
            {
                "price": {
                    "basic": 789123456,
                    "product": 891234567
                }
            }
        ]
    }

    result = parse_product(raw)
    assert result["brand"] is None

def test_parse_supplier_is_empty():
    raw = {
        "id": 123456789,
        "subjectId": 234567891,
        "name": "TestProductName",
        "brand": "TestBrandName",
        "supplier": "",
        "supplierRating": 345678912,
        "rating": 456789123,
        "reviewRating": 56789123,
        "feedbacks": 678912345,
        "sizes": [
            {
                "price": {
                    "basic": 789123456,
                    "product": 891234567
                }
            }
        ]
    }

    result = parse_product(raw)
    assert result["supplier"] is None

def test_parse_feedbacks_is_zero():
    raw = {
        "id": 123456789,
        "subjectId": 234567891,
        "name": "TestProductName",
        "brand": "TestBrandName",
        "supplier": "",
        "supplierRating": 345678912,
        "rating": 456789123,
        "reviewRating": 56789123,
        "feedbacks": 0,
        "sizes": [
            {
                "price": {
                    "basic": 789123456,
                    "product": 891234567
                }
            }
        ]
    }

    result = parse_product(raw)
    assert result["feedbacks_count"] == 0

def test_parse_rating_is_zero():
    raw = {
        "id": 123456789,
        "subjectId": 234567891,
        "name": "TestProductName",
        "brand": "TestBrandName",
        "supplier": "",
        "supplierRating": 345678912,
        "rating": 0,
        "reviewRating": 56789123,
        "feedbacks": 678912345,
        "sizes": [
            {
                "price": {
                    "basic": 789123456,
                    "product": 891234567
                }
            }
        ]
    }

    result = parse_product(raw)
    assert result["rating"] == 0

def test_parse_no_id():
    raw = {
        "subjectId": 234567891,
        "name": "TestProductName",
        "brand": "TestBrandBrand",
        "supplier": "TestSupplierName",
        "supplierRating": 345678912,
        "rating": 456789123,
        "reviewRating": 56789123,
        "feedbacks": 678912345,
        "sizes": [
            {
                "price": {
                    "basic": 789123456,
                    "product": 891234567
                }
            }
        ]
    }

    assert (parse_product(raw) is None)

def test_parse_product_without_id_at_products():
    raw = {
        "products": [
            {
                "id": 123456789,
                "subjectId": 234567891,
                "name": "TestProductName",
                "brand": "TestBrandBrand",
                "supplier": "TestSupplierName",
                "supplierRating": 345678912,
                "rating": 456789123,
                "reviewRating": 56789123,
                "feedbacks": 678912345,
                "sizes": [
                    {
                        "price": {
                            "basic": 789123456,
                            "product": 891234567
                        }
                    }
                ]
            },
            {
                "subjectId": 234567891,
                "name": "TestProductName",
                "brand": "TestBrandBrand",
                "supplier": "TestSupplierName",
                "supplierRating": 345678912,
                "rating": 456789123,
                "reviewRating": 56789123,
                "feedbacks": 678912345,
                "sizes": [
                    {
                        "price": {
                            "basic": 789123456,
                            "product": 891234567
                        }
                    }
                ]
            }
        ]
    }

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
    raw = {
        "products": [
            {
                "id": 123456789,
                "subjectId": 234567891,
                "name": "TestProductName",
                "brand": "TestBrandBrand",
                "supplier": "TestSupplierName",
                "supplierRating": 345678912,
                "rating": 456789123,
                "reviewRating": 56789123,
                "feedbacks": 678912345,
                "sizes": [
                    {
                        "price": {
                            "basic": 789123456,
                            "product": 891234567
                        }
                    }
                ]
            },
            "TestWrongItem"
        ]
    }
    assert len(parse_products(raw)) == 1