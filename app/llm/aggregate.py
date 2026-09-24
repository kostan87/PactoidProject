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