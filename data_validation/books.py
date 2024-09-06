from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    """Represents a book."""

    def __init__(self, id: int, title: str, author: str, description: str, rating: int) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(
        id=1,
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        description="A classic novel about the American Dream.",
        rating=4,
    ),
    Book(
        id=2,
        title="Don Quixote",
        author="Miguel de Cervantes",
        description="A Spanish novel about what it means to be a knight.",
        rating=5,
    ),
]


# Request model used for validating incoming data.
# BaseModel is a Pydantic class that provides data validation and serialization.
# Field is a Pydantic class that provides additional validation for the fields.
class RequestBook(BaseModel):
    id: int | None = Field(description="Unique identifier for the book. Optional", default=None)
    title: str = Field(min_length=1, max_length=50)
    author: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=10, max_length=100)
    rating: int = Field(ge=1, le=5)

    # The model_config property is used to provide additional configuration for the model.
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A classic novel about the American Dream.",
                "rating": 4,
            }
        }
    }


#
@app.get("/books", status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_rating(rating: int = Query(ge=1, le=5)):
    return list(book for book in BOOKS if book.rating == rating)


@app.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Path(ge=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


# This function includes data validation using the RequestBook model,
# which ensures that the incoming data meets the specified requirements.
# If the data does not meet the requirements, FastAPI will return an error response.
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: RequestBook) -> None:
    book = Book(**book_request.model_dump())
    book.id = create_unique_id()
    BOOKS.append(book)


@app.put("/books/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: RequestBook, book_id: int = Query(ge=0)) -> None:
    for book in BOOKS:
        if book.id == book_id:
            book.title = book_request.title
            book.author = book_request.author
            book.description = book_request.description
            book.rating = book_request.rating
            return
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(ge=0)) -> None:
    for book in reversed(BOOKS):
        if book.id == book_id:
            BOOKS.remove(book)
            return
    raise HTTPException(status_code=404, detail="Book not found")


def create_unique_id() -> int:
    return 1 + max((book.id for book in BOOKS), default=0)
