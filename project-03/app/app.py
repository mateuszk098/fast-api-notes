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


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "Healthy"}


def run(*, host: str = "localhost", port: int = 8000) -> None:
    uvicorn.run(app, host=host, port=port)
