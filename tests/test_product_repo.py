from decimal import Decimal

from sqlalchemy import select

from app.db import SessionLocal

from app.repositories.product_repo import upsert_product

from app.models.product import Product
from app.models.price_history import PriceHistory

def test_repo_product_is_full():
    product = {
        "id": 100999000999000,
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

    with SessionLocal() as session:
        upsert_product(session, product)
        session.flush()
        session.expire_all()

        product_at_db = session.get(Product, 100999000999000)

        assert product_at_db is not None

        assert product_at_db.subject_id == 123
        assert product_at_db.name == "TestProductName"
        assert product_at_db.brand == "TestBrandBrand"
        assert product_at_db.supplier == "TestSupplierName"
        assert product_at_db.supplier_rating == Decimal("4.5")
        assert product_at_db.rating == Decimal("3.2")
        assert product_at_db.review_rating == Decimal("5.0")
        assert product_at_db.feedbacks_count == 22

        price_at_db = session.scalar(select(PriceHistory).where(PriceHistory.product_id == 100999000999000))

        assert price_at_db is not None

        session.rollback()

def test_repo_product_price_changed():
    product1 = {
        "id": 200999000999000,
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
        "id": 200999000999000,
        "subject_id": 123,
        "name": "TestProductName",
        "brand": "TestBrandBrand",
        "supplier": "TestSupplierName",
        "supplier_rating": 4.5,
        "rating": 3.2,
        "review_rating": 5.0,
        "feedbacks_count": 22,
        "price_basic": 150.00,
        "price_product": 120.00
    }

    with SessionLocal() as session:
        upsert_product(session, product1)
        session.flush()
        upsert_product(session, product2)
        session.flush()
        session.expire_all()

        products_at_db = session.scalars(select(Product).where(Product.id == 200999000999000)).all()

        assert len(products_at_db) == 1

        prices_at_db = session.scalars(select(PriceHistory).where(PriceHistory.product_id == 200999000999000)).all()

        assert len(prices_at_db) == 2
        
        assert {p.price_basic for p in prices_at_db} == {Decimal("250"), Decimal("150")}

        session.rollback()

def test_repo_product_price_unchanged():
    product1 = {
        "id": 300999000999000,
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
        "id": 300999000999000,
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

    with SessionLocal() as session:
        upsert_product(session, product1)
        session.flush()
        upsert_product(session, product2)
        session.flush()
        session.expire_all()

        products_at_db = session.scalars(select(Product).where(Product.id == 300999000999000)).all()

        assert len(products_at_db) == 1

        prices_at_db = session.scalars(select(PriceHistory).where(PriceHistory.product_id == 300999000999000)).all()

        assert len(prices_at_db) == 1

        session.rollback()

def test_repo_product_without_price_record():
    product = {
        "id": 400999000999000,
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

    with SessionLocal() as session:
        current_product = {key:value for key,value in product.items() if key not in ("price_basic", "price_product")}
        product_at_db = Product(**current_product)
        session.add(product_at_db)

        upsert_product(session, product)
        session.flush()
        session.expire_all()

        product_at_db = session.get(Product, 400999000999000)
        
        assert product_at_db is not None

        price_at_db = session.scalar(select(PriceHistory).where(PriceHistory.product_id == 400999000999000))

        assert price_at_db is not None

        session.rollback()