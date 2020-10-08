from typing import Optional

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "test_var": 1993,
    })


@app.post("/stock")
def create_stock():
    return {
        "code": "success",
        "message": "Stock created"
    }
