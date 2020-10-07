from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def dashboard():
    return {"Dashboard": "Home Page"}


@app.post("/stock")
def create_stock():
    return {
        "code": "success",
        "message": "Stock created"
    }
