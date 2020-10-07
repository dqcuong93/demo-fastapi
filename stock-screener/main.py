from typing import Optional

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get("/")
def dashboard():
    return templates.TemplateResponse("dashboard.html")


@app.post("/stock")
def create_stock():
    return {
        "code": "success",
        "message": "Stock created"
    }
