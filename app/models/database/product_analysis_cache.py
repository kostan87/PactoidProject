from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.db import Base
from utils.time import utcnow

class ProductAnalysisCache(Base):
    __tablename__ = "product_analysis_cache"

    root: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    aggregate: Mapped[dict] = mapped_column(JSONB, nullable=False)
    reviews_count: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    def __repr__(self) -> str:
        return (
            f"<ProductAnalysisCache("
            f"root={self.root}, "
            f"aggregate ={self.aggregate !r}, "
            f"reviews_count={self.reviews_count!r}, "
            f"created_at={self.created_at!r}, "
            f"updated_at={self.updated_at!r}"
            f")>"
        )