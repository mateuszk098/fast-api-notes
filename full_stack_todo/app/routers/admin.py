from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from ..core.database import DBDependency
from ..core.models import Todos
from ..core.utils import Tags
from ..core.validation import TodoResponse
from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=[Tags.ADMIN])
UserDependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todos", status_code=status.HTTP_200_OK, response_model=list[TodoResponse])
async def read_all(db: DBDependency, user: UserDependency) -> Any:
    if user["role"] != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return db.query(Todos).all()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(db: DBDependency, user: UserDependency, todo_id: int = Path(ge=1)) -> None:
    if user["role"] != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Permission denied")
    todo = db.query(Todos).filter_by(id=todo_id).first()
    if todo is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="TODO not found")
    db.delete(todo)
    db.commit()
