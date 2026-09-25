from collections import Counter

from app.models.review_analysis import Aspect

def aggregate(aspects: list[Aspect]) -> dict:
    stats = {}
    for a in aspects:
        key = a.aspect
        stats.setdefault(key, {"pos": 0, "neg": 0, "defects": [], "advantages": []})
        if a.sentiment == "positive":
            stats[key]["pos"] += 1
        elif a.sentiment == "negative":
            stats[key]["neg"] += 1
        if a.type == "defect":
            stats[key]["defects"].append(a.detail)
        elif a.type == "advantage":
            stats[key]["advantages"].append(a.detail)
    return stats

def build_review_text(review: dict) -> str:
    parts = [f"[ID: {review.id}]"]
    if review.text:
        parts.append(review.text.strip())
    if review.pros:
        parts.append(f"Плюсы: {review.pros.strip()}")
    if review.cons:
        parts.append(f"Минусы: {review.cons.strip()}")
    return "\n".join(parts) if parts else "(пусто)"