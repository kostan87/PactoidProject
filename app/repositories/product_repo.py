from typing import Optional, Any

from sqlalchemy import select, desc, ColumnElement
from sqlalchemy.orm import Session

from app.models.database import Product, PriceHistory, ProductAnalysisCache

def upsert_product(session: Session, product: dict) -> Product | None:
    current_product = {key:value for key,value in product.items() if key not in ("price_basic", "price_product")}
    product_at_db = session.scalar(select(Product).where(Product.id == product["id"]))
    latest_price = session.scalar(
        select(PriceHistory)
        .where(PriceHistory.product_id == product["id"])
        .order_by(PriceHistory.recorded_at.desc())
    )
    current_price = PriceHistory(
        price_basic=product["price_basic"],
        price_product=product["price_product"]
    )

    if product_at_db is None: # INSERT
        product_at_db = Product(**current_product)
        product_at_db.prices.append(current_price)
        session.add(product_at_db)
    else: # UPDATE
        for key, value in current_product.items():
            setattr(product_at_db, key, value)
        if latest_price is None or (current_price.price_basic != latest_price.price_basic or current_price.price_product != latest_price.price_product):
            product_at_db.prices.append(current_price)
    return product_at_db

def upsert_product_analysis_cache(session: Session, product_analysis: dict) -> ProductAnalysisCache | None:
    product_analysis_at_db = session.scalar(select(ProductAnalysisCache).where(ProductAnalysisCache.root == product_analysis["root"]))

    if product_analysis_at_db is None: # INSERT
        product_analysis_at_db = ProductAnalysisCache(**product_analysis)
        session.add(product_analysis_at_db)
    else: # UPDATE
        product_analysis = {key: value for key, value in product_analysis.items() if key not in ["root"]}
        for key, value in product_analysis.items():
            setattr(product_analysis_at_db, key, value)
    return product_analysis

def get_products_from_db(session: Session, count: Optional[int] = None, order_by: ColumnElement[Any] = None) -> list[Product]:
    request = select(Product)
    if count is not None:
        request = request.limit(count)
    if order_by is not None:
        request = request.order_by(order_by)
    return session.scalars(request).all()

def get_products_prices_from_db(session: Session, products: list[Product]) -> list[int]:
    products_ids = [p.id for p in products]
    rows = session.execute(
        select(PriceHistory.product_id, PriceHistory.price_product)
        .where(PriceHistory.product_id.in_(products_ids))
        .order_by(PriceHistory.product_id, desc(PriceHistory.recorded_at))
        .distinct(PriceHistory.product_id)
    ).all()
    return {product: int(price) for product, price in rows}