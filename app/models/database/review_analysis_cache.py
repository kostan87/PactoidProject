from datetime import datetime

from sqlalchemy import Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from utils.time import utcnow

class ReviewAnalysisCache(Base):
    __tablename__ = "review_analysis_cache"

    hash: Mapped[str] = mapped_column(Text, primary_key=True, autoincrement=False)
    analysis: Mapped[dict] = mapped_column(JSON, nullable=False)
    model: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    def __repr__(self) -> str:
        return (
            f"<ReviewAnalysisCache("
            f"hash={self.hash!r}, "
            f"analysis={self.analysis!r}, "
            f"model={self.model!r}, "
            f"created_at={self.created_at!r}"
            f")>"
        )