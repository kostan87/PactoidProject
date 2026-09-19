from app.db import Base, engine
from app.models.product import Product
from app.models.price_history import PriceHistory
from app.models.review import Review

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

print("DATABASE: tables created")