import os
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

import bcrypt
from dotenv import find_dotenv, load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt  # type: ignore
from sqlalchemy.orm import Session
from starlette import status

from ..core.database import DBDependency
from ..core.models import Users
from ..core.utils import Tags
from ..core.validation import UserRequest

assert load_dotenv(
    find_dotenv()
), "Could not load the environment variables. Is the .env file missing?"

SECRET_KEY = os.getenv("SECRET_KEY", default="")
ALGORITHM = os.getenv("ALGORITHM", default="HS256")

router = APIRouter(prefix="/auth", tags=[Tags.AUTHENTICATION])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(db: DBDependency, user_request: UserRequest) -> None:
    user = Users(
        username=user_request.username,
        email=user_request.email,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        role=user_request.role,
        hashed_password=bcrypt.hashpw(
            user_request.password.encode("utf-8"),
            bcrypt.gensalt(),
        ),
    )
    db.add(user)
    db.commit()


@router.post("/token")
async def login(db: DBDependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(db, form_data.username, form_data.password)
    token = create_access_token(user.username, user.id, user.role, timedelta(hours=1))
    return {"user": user, "access_token": token}


def authenticate_user(db: Session, username: str, password: str) -> Users:
    user = db.query(Users).filter_by(username=username).first()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    if not bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    return user


def create_access_token(
    username: str, user_id: int, user_role: str, expiry_time: timedelta
) -> str:
    expires = datetime.now(UTC) + expiry_time
    payload = {
        "sub": username,
        "id": user_id,
        "role": user_role,
        "expires": expires.isoformat(sep=" ", timespec="seconds"),
    }
    return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Could not authenticate user")
    else:
        username = payload.get("sub")
        user_id = payload.get("id")
        user_role = payload.get("role")
        if any(x is None for x in (username, user_id, user_role)):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Could not authenticate user")
        return {"username": username, "id": user_id, "role": user_role}
