import uvicorn
from fastapi import FastAPI

from .core.database import Base, engine
from .routers.auth import router as auth_router
from .routers.todos import router as todos_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(todos_router)


def run() -> None:
    uvicorn.run(app, host="localhost", port=8000)
