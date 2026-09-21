from datetime import datetime

from sqlalchemy import BigInteger, Text, Integer, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("marketplace", "marketplace_review_id", name="uq_marketplace_review"),
    )
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    model_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("models.id", ondelete="SET NULL"), nullable=True)
    marketplace: Mapped[str] = mapped_column(Text, nullable=False)
    marketplace_review_id: Mapped[str] = mapped_column(Text, nullable=False)
    marketplace_product_id : Mapped[str] = mapped_column(Text, nullable=False)
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

    model: Mapped["Model"] = relationship(back_populates="reviews")

    def __repr__(self) -> str:
        return (
            f"<Review("
            f"id={self.id!r}, "
            f"model_id={self.model_id!r}, "
            f"marketplace={self.marketplace!r}, "
            f"marketplace_review_id={self.marketplace_review_id!r}, "
            f"marketplace_product_id={self.marketplace_product_id!r}, "
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