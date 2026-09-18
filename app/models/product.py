from decimal import Decimal

from datetime import datetime, timezone

from sqlalchemy import BigInteger, Text, Integer, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.utils.time import utcnow

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(Text)
    brand: Mapped[str | None] = mapped_column(Text, nullable=True)
    supplier: Mapped[str | None] = mapped_column(Text, nullable=True)
    subject_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    feedbacks_count: Mapped[int] = mapped_column(Integer, default=0)
    supplier_rating: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), nullable=True)
    rating: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), nullable=True)
    review_rating: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)