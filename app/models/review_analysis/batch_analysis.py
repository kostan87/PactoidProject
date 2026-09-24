from pydantic import BaseModel

from app.models.review_analysis.review_analysis import ReviewAnalysis

class BatchAnalysis(BaseModel):
    results: list[ReviewAnalysis]