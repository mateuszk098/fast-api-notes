from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from ..core.database import DBDependency
from ..core.models import Todos
from ..core.utils import Tags
from ..core.validation import TodoRequest, TodoResponse
from .auth import get_current_user

router = APIRouter(prefix="/todos", tags=[Tags.TODOS])
UserDependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[TodoResponse])
async def read_all(db: DBDependency, user: UserDependency) -> Any:
    return get_todos(db, user["id"])


@router.get("/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoResponse)
async def read(db: DBDependency, user: UserDependency, todo_id: int = Path(ge=1)) -> Any:
    return get_todo(db, user["id"], todo_id)


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create(db: DBDependency, user: UserDependency, todo_request: TodoRequest) -> None:
    todo = Todos(**todo_request.model_dump(), owner_id=user.get("id"))
    db.add(todo)  # Add the data to the session.
    db.commit()  # Now commit the data to the database.


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(
    db: DBDependency, todo_request: TodoRequest, user: UserDependency, todo_id: int = Path(ge=1)
) -> None:
    todo = get_todo(db, user["id"], todo_id)
    for key, value in todo_request.model_dump().items():
        setattr(todo, key, value)
    db.add(todo)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(db: DBDependency, user: UserDependency, todo_id: int = Path(ge=1)) -> None:
    todo = get_todo(db, user["id"], todo_id)
    db.delete(todo)
    db.commit()


def get_todos(db: Session, user_id: int) -> list[Todos]:
    return db.query(Todos).filter_by(owner_id=user_id).all()


def get_todo(db: Session, user_id: int, todo_id: int) -> Todos:
    data = db.query(Todos).filter_by(owner_id=user_id, id=todo_id).first()
    if data is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="TODO not found")
    return data
