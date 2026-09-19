from datetime import datetime

from sqlalchemy import BigInteger, Text, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

class Review(Base):
    __tablename__ = "reviews"
    product: Mapped["Product"] = relationship(back_populates="reviews")
    id: Mapped[str] = mapped_column(Text, primary_key=True, autoincrement=False)
    nm_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"))
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    pros: Mapped[str | None] = mapped_column(Text, nullable=True)
    cons: Mapped[str | None] = mapped_column(Text, nullable=True)
    product_valuation: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    global_user_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    votes_pluses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    votes_minuses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_excluded_from_rating: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    parent_feedback_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    child_feedback_id: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<Review("
            f"id={self.id!r}, "
            f"nm_id={self.nm_id}, "
            f"text={self.text!r}, "
            f"pros={self.pros!r}, "
            f"cons={self.cons!r}, "
            f"product_valuation={self.product_valuation}, "
            f"created_date={self.created_date!r}, "
            f"status_id={self.status_id}, "
            f"global_user_id={self.global_user_id!r}, "
            f"votes_pluses={self.votes_pluses}, "
            f"votes_minuses={self.votes_minuses}, "
            f"is_excluded_from_rating={self.is_excluded_from_rating}, "
            f"parent_feedback_id={self.parent_feedback_id!r}, "
            f"child_feedback_id={self.child_feedback_id!r}"
            f")>"
        )