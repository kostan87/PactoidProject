from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.price_history import PriceHistory

def upsert_product(session:Session, product:dict) -> Product | None:
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
        for key,value in current_product.items():
            setattr(product_at_db, key, value)
        if latest_price is None or (current_price.price_basic != latest_price.price_basic or current_price.price_product != latest_price.price_product):
            product_at_db.prices.append(current_price)
    return product_at_db