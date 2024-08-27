from typing import Annotated, Any

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from ..core.database import DBDependency
from ..core.models import Users
from ..core.utils import Tags
from ..core.validation import UserPasswordResetRequest, UserResponse
from .auth import get_current_user

router = APIRouter(prefix="/user", tags=[Tags.USER])
UserDependency = Annotated[dict, Depends(get_current_user)]


@router.get("/info", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_info(db: DBDependency, user: UserDependency) -> Any:
    return retrieve_user(db, user["id"])


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(
    db: DBDependency, user: UserDependency, password: UserPasswordResetRequest
) -> None:
    user = retrieve_user(db, user["id"])
    if not bcrypt.checkpw(password.current_password.encode("utf-8"), user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    user.hashed_password = bcrypt.hashpw(password.new_password.encode("utf-8"), bcrypt.gensalt())
    db.add(user)
    db.commit()


@router.put("/phone-number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(db: DBDependency, user: UserDependency, phone_number: str) -> None:
    user = retrieve_user(db, user["id"])
    user.phone_number = phone_number
    db.add(user)
    db.commit()


def retrieve_user(db, user_id) -> Users:
    user = db.query(Users).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
