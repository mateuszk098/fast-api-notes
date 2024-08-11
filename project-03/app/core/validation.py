from pydantic import BaseModel, ConfigDict, Field


class TodoRequest(BaseModel):
    # We do not use the `id` because it is a primary key and should be auto-generated.
    title: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=10, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete: bool

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, and bananas",
                "priority": 3,
                "complete": False,
            }
        }
    )


class TodoResponse(TodoRequest):
    id: int


class User(BaseModel):
    # We do not use the `id` because it is a primary key and should be auto-generated.
    # And we do not use `is_active` because the user should be active by default.
    username: str = Field(min_length=5, max_length=50)
    email: str = Field(min_length=5, max_length=50)
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    role: str


class UserRequest(User):
    # We use `password` instead of `hashed_password` because the user
    # will send the password in plain text.
    password: str = Field(min_length=8, max_length=50)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "password",
                "role": "user",
            }
        }
    )


class UserResponse(User):
    id: int
    is_active: bool
    hashed_password: bytes
