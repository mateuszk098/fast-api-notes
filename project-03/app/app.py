import pathlib

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import APP_DIR

from .core.database import Base, engine
from .core.utils import Tags
from .routers.admin import router as admin_router
from .routers.auth import router as auth_router
from .routers.todos import router as todos_router
from .routers.user import router as user_router

templates = Jinja2Templates(directory=pathlib.Path(APP_DIR, "templates/"))

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(todos_router)
app.include_router(admin_router)
app.include_router(user_router)
app.mount("/static", StaticFiles(directory=pathlib.Path(APP_DIR, "static/")), name="static")


@app.get("/health", tags=[Tags.HEALTHCHECK], include_in_schema=False)
def health_check() -> dict[str, str]:
    return {"status": "Healthy"}


@app.get("/", tags=[Tags.HOME], include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


def run(*, host: str = "localhost", port: int = 8000) -> None:
    uvicorn.run(app, host=host, port=port)
