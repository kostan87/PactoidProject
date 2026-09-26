from pydantic import BaseModel, Field
from typing import Literal

from app.models.review_analysis.aspect import Aspect

class ReviewAnalysis(BaseModel):
    id: str = Field(description="ID отзыва в виде строки. ID отзывов указаны в сообщении пользователя, сохраняй эти ID для конкретного отзыва.")
    aspects: list[Aspect]
    summary: str
    overall_sentiment: Literal["positive", "negative", "mixed", "neutral"]