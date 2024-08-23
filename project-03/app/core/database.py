import os
from typing import Annotated, Any, Generator

from dotenv import find_dotenv, load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

assert load_dotenv(
    find_dotenv()
), "Could not load the environment variables. Is the .env file missing?"

POSTGRES_USER = os.getenv("POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="password")
POSTGRES_DB = os.getenv("POSTGRES_DB", default="TodoAppDB")

pattern = "postgresql://{}:{}@localhost/{}"
SQLALCHEMY_DATABASE_URL = pattern.format(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"  # SQLite.

# PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)  # PostgreSQL.
# SQLite
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()


def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBDependency = Annotated[Session, Depends(get_db)]
