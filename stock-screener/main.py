import models
from database import engine, SessionLocal
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

app = FastAPI()

# Create table
models.Base.metadata.create_all(bind=engine)

# Define you template language and its directory
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    """
    This is the root path - home path
    :param request:
    :return:
    """
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "test_var": 1993,  # Call this variable in your template using Jinja2 syntax
        },
    )


@app.post("/stock")
def create_stock():
    # Return a JSON response
    return {"code": "success", "message": "Stock created"}
