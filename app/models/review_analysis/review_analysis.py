from pydantic import BaseModel
from typing import Literal

from app.models.review_analysis.aspect import Aspect

class ReviewAnalysis(BaseModel):
    aspects: list[Aspect]
    summary: str
    overall_sentiment: Literal["positive", "negative", "mixed", "neutral"]