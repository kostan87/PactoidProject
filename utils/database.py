from typing import Callable

from sqlalchemy.orm import Session

from app.db import SessionLocal

def process_batch(
        data: list[dict],
        action: Callable[[Session, dict], None],
        session_factory=SessionLocal
    ) -> None:
    total = len(data)
    saved = 0
    with session_factory.begin() as session:
        for item in data:
            if action(session, item) is not None:
                saved += 1
    print(f"saved {saved}/{total}")