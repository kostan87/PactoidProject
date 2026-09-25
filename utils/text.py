import hashlib

def get_hash(text: str) -> str:
    return hashlib.sha256(text.strip().lower().encode()).hexdigest()