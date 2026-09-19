import pytest

from app.db import SessionLocal

@pytest.fixture
def session():
    # setup
    s = SessionLocal()
    yield s
    # teardown
    s.rollback()
    s.close()