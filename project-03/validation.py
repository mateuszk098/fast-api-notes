from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    # We do not use the `id` because it is a primary key and should be auto-generated.
    title: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=10, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, and bananas",
                "priority": 3,
                "complete": False,
            }
        }
    }


class TodoResponse(TodoRequest):
    id: int
