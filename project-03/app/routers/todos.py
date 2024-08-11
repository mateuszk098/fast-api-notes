from typing import Any

from fastapi import APIRouter, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from ..core.database import DBDependency
from ..core.models import Todos
from ..core.utils import Tags
from ..core.validation import TodoRequest, TodoResponse

router = APIRouter(prefix="/todos", tags=[Tags.TODOS])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[TodoResponse])
async def read_all(db: DBDependency) -> Any:
    return get_todos(db)


@router.get("/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoResponse)
async def read(db: DBDependency, todo_id: int = Path(ge=1)) -> Any:
    return get_todo(db, todo_id)


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create(db: DBDependency, todo_request: TodoRequest) -> None:
    todo = Todos(**todo_request.model_dump())
    db.add(todo)  # Add the data to the session.
    db.commit()  # Now commit the data to the database.


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(db: DBDependency, todo_request: TodoRequest, todo_id: int = Path(ge=1)) -> None:
    todo = get_todo(db, todo_id)
    for key, value in todo_request.model_dump().items():
        setattr(todo, key, value)
    db.add(todo)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(db: DBDependency, todo_id: int = Path(ge=1)) -> None:
    todo = get_todo(db, todo_id)
    db.delete(todo)
    db.commit()


def get_todos(db: Session) -> list[Todos]:
    return db.query(Todos).all()


def get_todo(db: Session, todo_id: int) -> Todos:
    data = db.query(Todos).filter_by(id=todo_id).first()
    if data is None:
        raise HTTPException(status_code=404, detail="TODO not found")
    return data
