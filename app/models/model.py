from decimal import Decimal

from datetime import datetime

from sqlalchemy import BigInteger, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from utils.time import utcnow

class Model(Base):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    brand: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    wb_products: Mapped[list["WBProduct"]] = relationship(back_populates="model")
    reviews: Mapped[list["Review"]] = relationship(back_populates="model")

    def __repr__(self) -> str:
        return (
            f"<Model("
            f"id={self.id}, "
            f"name={self.name!r}, "
            f"brand={self.brand!r}, "
            f"created_at={self.created_at!r}, "
            f"updated_at={self.updated_at!r}"
            f")>"
        )