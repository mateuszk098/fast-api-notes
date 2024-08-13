import uvicorn
from fastapi import FastAPI

from .core.database import Base, engine
from .routers.admin import router as admin_router
from .routers.auth import router as auth_router
from .routers.todos import router as todos_router
from .routers.user import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(todos_router)
app.include_router(admin_router)
app.include_router(user_router)


def run() -> None:
    uvicorn.run(app, host="localhost", port=8000)
