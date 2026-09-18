from decimal import Decimal

from datetime import datetime

from sqlalchemy import BigInteger, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.utils.time import utcnow

class PriceHistory(Base):
    __tablename__ = "price_history"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"))
    price_basic: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    price_product: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    recorded_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)