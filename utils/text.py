import hashlib

def build_review_text(review: dict) -> str:
    parts = []
    if review.text:
        parts.append(review.text.strip())
    if review.pros:
        parts.append(f"Плюсы: {review.pros.strip()}")
    if review.cons:
        parts.append(f"Минусы: {review.cons.strip()}")
    return "\n".join(parts) if parts else "(пусто)"

def get_hash(text: str) -> str:
    return hashlib.sha256(text.strip().lower().encode()).hexdigest()