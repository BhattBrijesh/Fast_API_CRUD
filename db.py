from collections.abc import Iterator
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


load_dotenv(Path(__file__).with_name(".env"))

# Environment variables take precedence over values loaded from .env.
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("Set DATABASE_URL in .env or the process environment before importing db.py.")

# Check pooled connections before reuse so stale connections can be replaced.
engine = create_engine(database_url, pool_pre_ping=True)

# Create a session factory for requests and a shared base for ORM models.
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db() -> Iterator[Session]:
    # FastAPI uses the yielded session for the request and closes it on cleanup.
    with SessionLocal() as session:
        yield session
