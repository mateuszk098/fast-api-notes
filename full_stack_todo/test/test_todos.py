from fastapi.testclient import TestClient
from starlette import status

from app.app import app
from app.core.database import get_db
from app.core.models import Todos
from app.routers.auth import get_current_user

from .utils import TestingSessionLocal, get_current_test_user, get_test_db, test_todo

app.dependency_overrides[get_db] = get_test_db
app.dependency_overrides[get_current_user] = get_current_test_user

client = TestClient(app)


def test_read_all(test_todo) -> None:
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread, and bananas",
            "priority": 3,
            "complete": False,
            "owner_id": 1,
        }
    ]


def test_read(test_todo) -> None:
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, eggs, bread, and bananas",
        "priority": 3,
        "complete": False,
        "owner_id": 1,
    }


def test_read_not_found() -> None:
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "TODO not found"}


def test_create(test_todo) -> None:
    request = {
        "title": "Buy coffee",
        "description": "Ground coffee beans",
        "priority": 5,
        "complete": False,
    }
    response = client.post("/todos/todo", json=request)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    # Fixture creates a first todo (id=1), and here the second is created (id=2).
    todo = db.query(Todos).filter_by(id=2).first()

    assert todo is not None
    assert todo.title == request.get("title")
    assert todo.description == request.get("description")
    assert todo.priority == request.get("priority")
    assert todo.complete == request.get("complete")


def test_update(test_todo) -> None:
    request = {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread, and bananas",
        "priority": 1,
        "complete": True,
    }
    response = client.put("/todos/todo/1", json=request)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    todo = db.query(Todos).filter_by(id=1).first()

    assert todo is not None
    assert todo.title == request.get("title")
    assert todo.description == request.get("description")
    assert todo.priority == request.get("priority")
    assert todo.complete == request.get("complete")


def test_update_not_found(test_todo) -> None:
    request = {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread, and bananas",
        "priority": 1,
        "complete": True,
    }
    response = client.put("/todos/todo/999", json=request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "TODO not found"}


def test_delete(test_todo) -> None:
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    todo = db.query(Todos).filter_by(id=1).first()

    assert todo is None


def test_delete_not_found(test_todo) -> None:
    response = client.delete("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "TODO not found"}
