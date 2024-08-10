from dataclasses import dataclass

from fastapi import Body, FastAPI

app = FastAPI()


@dataclass(kw_only=True)
class Book:
    """Represents a book with a title, author, and category."""

    title: str
    author: str
    category: str


BOOKS = [
    Book(title="The Great Gatsby", author="F. Scott Fitzgerald", category="Fiction"),
    Book(title="The Da Vinci Code", author="Dan Brown", category="Thriller"),
    Book(title="The Catcher in the Rye", author="J.D. Salinger", category="Fiction"),
    Book(title="The Alchemist", author="Paulo Coelho", category="Fantasy"),
    Book(title="The Hobbit", author="J.R.R. Tolkien", category="Fantasy"),
]

# ORDER OF ROUTES MATTERS. FIRST MATCHED ROUTE WILL BE EXECUTED.


# This decorator is used to define a route in a web application.
# In this case, it's defining the root route ("/"). When a GET request
# is made to the root URL of the application (something like "http://localhost:8000/"),
# the function decorated with @app.get("/") will be executed.
@app.get("/books")
async def get_books() -> list[Book]:
    return BOOKS


# This route is similar to the previous one, but it includes a path parameter.
# The path parameter is specified in curly braces in the route definition ("/books/{author}").
# The value of the path parameter will be passed to the function as an argument.
# Type hints can be used to specify the type of the parameter.
# In this case, the author parameter is expected to be a string.
# If user passes different type, FastAPI will return an error.
@app.get("/books/{author}")
async def get_books_by_author(author: str) -> list[Book]:
    return list(book for book in BOOKS if book.author.casefold() == author.casefold())


# This route includes a query parameter.
# Query parameters are specified in the URL after a question mark (?).
# The query parameter is passed to the function as an argument.
# For example "/books/?category=Fiction" will return all books with the category "Fiction".
@app.get("/books/")
async def get_books_by_query_category(category: str) -> list[Book]:
    return list(book for book in BOOKS if book.category.casefold() == category.casefold())


# This route includes a path parameter and a query parameter.
# The path parameter is specified first, followed by the query parameter.
# The example URL may be something like "/books/Fiction/?author=J.D.%20Salinger".
@app.get("/books/{category}/")
async def get_books_by_category_and_author(category: str, author: str) -> list[Book]:
    return list(
        book
        for book in BOOKS
        if book.category.casefold() == category.casefold()
        and book.author.casefold() == author.casefold()
    )


# This route includes a request body.
# The request body is passed to the function as an argument.
# The request body is expected to be a JSON object that can be converted to a Book object.
# FastAPI will automatically parse the request body and convert it to the specified type.
@app.post("/books/create_book")
async def create_book(new_book: Book = Body()) -> None:
    BOOKS.append(new_book)


# The PUT method is used to update an existing resource.
# This route includes a request body with a Book object.
# The Book object is used to update an existing book in the BOOKS list.
@app.put("/books/update_book")
async def update(updated_book: Book = Body()) -> None:
    for book in BOOKS:
        if book.title.casefold() == updated_book.title.casefold():
            book.author = updated_book.author
            book.category = updated_book.category


# The DELETE method is used to delete a resource.
# This route includes a path parameter for the title of the book to be deleted.
@app.delete("/books/delete_book/{title}")
async def delete(book_title: str) -> None:
    for book in reversed(BOOKS):
        if book.title.casefold() == book_title.casefold():
            BOOKS.remove(book)
