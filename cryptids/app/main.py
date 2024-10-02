import uvicorn
from fastapi import FastAPI

from app.web.creature import router as creature_router
from app.web.explorer import router as explorer_router

app = FastAPI()
app.include_router(explorer_router)
app.include_router(creature_router)


@app.get("/")
def top():
    return "Top"


@app.get("/echo/{thing}")
def echo(thing: str):
    return f"Show {thing}"


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
