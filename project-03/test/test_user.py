from fastapi.testclient import TestClient
from starlette import status

from app import app
from app.core.database import get_db
from app.core.models import Users
from app.routers.auth import get_current_user

from .utils import TestingSessionLocal, get_current_test_user, get_test_db, test_user

app.dependency_overrides[get_db] = get_test_db
app.dependency_overrides[get_current_user] = get_current_test_user

client = TestClient(app)


def test_get_user(test_user) -> None:
    response = client.get("/user/info")
    assert response.status_code == status.HTTP_200_OK

    content = response.json()
    assert content["username"] == "mateusz"
    assert content["email"] == "mateusz@gmail.com"
    assert content["first_name"] == "Mateusz"
    assert content["last_name"] == "Kowalczyk"
    assert content["role"] == "user"
    assert content["phone_number"] == "123-456-789"
    # Hashed password is not testable.


def test_reset_password_success(test_user) -> None:
    request = {
        "current_password": "password",
        "new_password": "new_password",
    }
    response = client.put("/user/password", json=request)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_reset_password_fail(test_user) -> None:
    request = {
        "current_password": "incorrect_password",
        "new_password": "new_password",
    }
    response = client.put("/user/password", json=request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_phone_number(test_user) -> None:
    request = "987-654-321"
    response = client.put(f"/user/phone-number/{request}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    user = db.query(Users).filter_by(id=1).first()

    assert user is not None
    assert user.phone_number == request
