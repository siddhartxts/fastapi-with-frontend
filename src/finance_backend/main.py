from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import models
from .database import engine
from .routers import finance_notes, watchlist

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html")


app.include_router(watchlist.router)
app.include_router(finance_notes.router)
