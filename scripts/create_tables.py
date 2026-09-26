import app.models.database
from app.db import Base, engine

Base.metadata.create_all(engine)

print("DATABASE: tables created")