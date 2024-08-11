from typing import Annotated, Any

from fastapi import Depends, FastAPI, Path
from sqlalchemy.orm import Session
from starlette import status

from .database import Base, engine, get_db
from .models import Todos, get_todo, get_todos
from .validation import TodoRequest, TodoResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()
DBDependency = Annotated[Session, Depends(get_db)]


@app.get("/todos", status_code=status.HTTP_200_OK, response_model=list[TodoResponse])
async def read_all(db: DBDependency) -> Any:
    return get_todos(db)


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoResponse)
async def read(db: DBDependency, todo_id: int = Path(ge=1)) -> Any:
    return get_todo(db, todo_id)


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create(db: DBDependency, todo_request: TodoRequest) -> None:
    todo = Todos(**todo_request.model_dump())
    db.add(todo)  # Add the data to the session.
    db.commit()  # Now commit the data to the database.


@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(db: DBDependency, todo_request: TodoRequest, todo_id: int = Path(ge=1)) -> None:
    todo = get_todo(db, todo_id)
    for key, value in todo_request.model_dump().items():
        setattr(todo, key, value)
    db.add(todo)
    db.commit()


@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(db: DBDependency, todo_id: int = Path(ge=1)) -> None:
    todo = get_todo(db, todo_id)
    db.delete(todo)
    db.commit()
