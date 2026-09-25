from datetime import datetime

from sqlalchemy import Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.db import Base
from utils.time import utcnow

class ReviewAnalysisCache(Base):
    __tablename__ = "review_analysis_cache"

    id: Mapped[str] = mapped_column(Text, primary_key=True, autoincrement=False)
    aspects: Mapped[list] = mapped_column(JSONB, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    overall_sentiment: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    def __repr__(self) -> str:
        return (
            f"<ReviewAnalysisCache("
            f"id={self.hash!r}, "
            f"aspects={self.analysis!r}, "
            f"summary={self.analysis!r}, "
            f"overall_sentiment={self.analysis!r}, "
            f"created_at={self.created_at!r}"
            f")>"
        )