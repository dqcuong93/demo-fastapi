from typing import Optional

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Define you template language and its directory
templates = Jinja2Templates(directory='templates')


@app.get("/")
def home(request: Request):
    """
    This is the root path - home path
    :param request:
    :return:
    """
    return templates.TemplateResponse("home.html", {
        "request": request,
        "test_var": 1993,  # Call this variable in your template using Jinja2 syntax
    })


@app.post("/stock")
def create_stock():
    # Return a JSON response
    return {
        "code": "success",
        "message": "Stock created"
    }
