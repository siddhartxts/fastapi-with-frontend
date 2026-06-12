from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import models
from database import engine

from routers import financenotes, watchlist

app = FastAPI()
templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html")


app.include_router(watchlist.router)
app.include_router(financenotes.router)
