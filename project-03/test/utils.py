from typing import Any, Generator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.core.models import Todos

# We use PostgreSQL for production, but still we can use SQLite for testing.
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"  # SQLite.

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    # In unit testing, only one connection is needed at a time.
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_test_db() -> Generator[Session, Any, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_test_user() -> dict[str, Any]:
    return {"username": "mateusz", "id": 1, "role": "admin"}


@pytest.fixture()
def test_todo() -> Generator[Todos, Any, None]:
    todo = Todos(
        title="Buy groceries",
        description="Milk, eggs, bread, and bananas",
        priority=3,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()

    try:
        yield todo
    finally:
        with engine.connect() as connection:
            connection.execute(text("DELETE FROM todos;"))
            connection.commit()
