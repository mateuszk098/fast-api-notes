import os
from datetime import UTC, datetime, timedelta

import pytest
from dotenv import find_dotenv, load_dotenv
from fastapi import HTTPException
from fastapi.testclient import TestClient
from jose import jwt
from starlette import status

from app.app import app
from app.core.database import get_db
from app.routers.auth import authenticate_user, create_access_token, get_current_user

from .utils import TestingSessionLocal, get_current_test_user, get_test_db, test_user

assert load_dotenv(
    find_dotenv()
), "Could not load the environment variables. Is the .env file missing?"

SECRET_KEY = os.getenv("SECRET_KEY", default="")
ALGORITHM = os.getenv("ALGORITHM", default="HS256")

app.dependency_overrides[get_db] = get_test_db
app.dependency_overrides[get_current_user] = get_current_test_user

client = TestClient(app)


def test_authenticate_user_success(test_user) -> None:
    db = TestingSessionLocal()
    user = authenticate_user(db, test_user.username, "password")
    assert user is not None


def test_authenticate_user_incorrent_password(test_user) -> None:
    db = TestingSessionLocal()
    with pytest.raises(HTTPException) as e:
        authenticate_user(db, test_user.username, "incorrect_password")
    assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert e.value.detail == "Incorrect password"


def test_authenticate_user_not_found() -> None:
    db = TestingSessionLocal()
    with pytest.raises(HTTPException) as e:
        authenticate_user(db, "unknown_user", "password")
    assert e.value.status_code == status.HTTP_404_NOT_FOUND
    assert e.value.detail == "User not found"


def test_create_access_token(test_user) -> None:
    token = create_access_token(
        test_user.username, test_user.id, test_user.role, timedelta(hours=1)
    )
    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False}
    )
    assert decoded_token["sub"] == test_user.username
    assert decoded_token["id"] == test_user.id
    assert decoded_token["role"] == test_user.role
    assert datetime.fromisoformat(decoded_token["expires"]) > datetime.now(UTC)


def test_get_current_user_valid_token() -> None:
    expires = datetime.now(UTC) + timedelta(hours=1)
    payload = {
        "sub": "mateusz",
        "id": 1,
        "role": "admin",
        "expires": expires.isoformat(sep=" ", timespec="seconds"),
    }
    token = jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)
    user = get_current_user(token)

    assert user["username"] == payload["sub"]
    assert user["id"] == payload["id"]
    assert user["role"] == payload["role"]


def test_get_current_user_invalid_token() -> None:
    with pytest.raises(HTTPException) as e:
        get_current_user("invalid_token")
    assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert e.value.detail == "Could not authenticate user"
