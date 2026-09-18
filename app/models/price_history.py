from decimal import Decimal

from datetime import datetime

from sqlalchemy import BigInteger, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.utils.time import utcnow

class PriceHistory(Base):
    __tablename__ = "price_history"
    product: Mapped["Product"] = relationship(back_populates="prices")
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"))
    price_basic: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    price_product: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    recorded_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    def __repr__(self) -> str:
        return (
            f"<PriceHistory("
            f"id={self.id}, "
            f"product_id={self.product_id}, "
            f"price_basic={self.price_basic}, "
            f"price_product={self.price_product}, "
            f"recorded_at={self.recorded_at}"
            f")>"
        )