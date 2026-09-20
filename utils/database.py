from typing import Callable

from sqlalchemy.orm import Session

from app.db import SessionLocal

def process_batch(
        data: list[dict],
        action: Callable[[Session, dict], None],
        session_factory=SessionLocal
    ) -> None:
    with SessionLocal() as session:
        with session_factory.begin() as session:
            for item in data:
                action(session, item)