from decimal import Decimal

from sqlalchemy import select, inspect

from app.repositories.product_repo import upsert_product

from app.models.product import Product
from app.models.price_history import PriceHistory

from tests.factories import DELETE, make_expected_product
from tests.assertions import assert_dict_subset

def test_repo_product_is_full(session):
    product = make_expected_product()

    upsert_product(session, product)
    session.flush()
    session.expire_all()

    product_at_db = session.get(Product, 1)
    assert product_at_db is not None

    mapper = inspect(Product).mapper
    product_at_db = {col.key: getattr(product_at_db, col.key) for col in mapper.columns}
    product_expected = make_expected_product(
        supplier_rating=Decimal("4.5"),
        rating=Decimal("3.2"),
        review_rating=Decimal("5.0"),
        price_basic=DELETE,
        price_product=DELETE
    )
    assert_dict_subset(product_at_db, product_expected)

    price_at_db = session.scalar(select(PriceHistory).where(PriceHistory.product_id == 1))
    assert price_at_db is not None

def test_repo_product_price_changed(session):
    product1 = make_expected_product(price_basic=500, price_product=350)
    product2 = make_expected_product(price_basic=400, price_product=250)
    
    upsert_product(session, product1)
    session.flush()
    upsert_product(session, product2)
    session.flush()
    session.expire_all()

    products_at_db = session.scalars(select(Product).where(Product.id == 1)).all()
    assert len(products_at_db) == 1

    prices_at_db = session.scalars(select(PriceHistory).where(PriceHistory.product_id == 1)).all()
    assert len(prices_at_db) == 2
    
    assert {price.price_basic for price in prices_at_db} == {Decimal("500"), Decimal("400")}
    assert {price.price_product for price in prices_at_db} == {Decimal("350"), Decimal("250")}

def test_repo_product_price_unchanged(session):
    product = make_expected_product(price_basic=500, price_product=350)

    upsert_product(session, product)
    session.flush()
    upsert_product(session, product)
    session.flush()
    session.expire_all()

    products_at_db = session.scalars(select(Product).where(Product.id == 1)).all()
    assert len(products_at_db) == 1

    prices_at_db = session.scalars(select(PriceHistory).where(PriceHistory.product_id == 1)).all()
    assert len(prices_at_db) == 1

def test_repo_product_without_price_record(session):
    product_without_price = make_expected_product(price_basic=DELETE, price_product=DELETE)
    product_with_price = make_expected_product(price_basic=500, price_product=350)
    
    product_at_db = Product(**product_without_price)
    session.add(product_at_db)
    upsert_product(session, product_with_price)
    session.flush()
    session.expire_all()

    product_at_db = session.get(Product, 1)
    assert product_at_db is not None

    price_at_db = session.scalar(select(PriceHistory).where(PriceHistory.product_id == 1))
    assert price_at_db is not None