from fastapi import HTTPException
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Session

from .database import Base


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)


def get_todos(db: Session) -> list[Todos]:
    return db.query(Todos).all()


def get_todo(db: Session, todo_id: int) -> Todos:
    data = db.query(Todos).filter_by(id=todo_id).first()
    if data is None:
        raise HTTPException(status_code=404, detail="TODO not found")
    return data
