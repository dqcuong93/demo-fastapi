import models
from database import SessionLocal, engine
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Stock

app = FastAPI()

# Create table
models.Base.metadata.create_all(bind=engine)

# Define you template language and its directory
templates = Jinja2Templates(directory="templates")


# Create a schema for DB - this is auto validation
class StockRequest(BaseModel):
    symbol: str


# Make sure we can connect to DB
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


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
def create_stock(stock_request: StockRequest, db: Session = Depends(get_db)):
    # Return a JSON response

    stock = Stock()
    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()
    return {"code": "success", "message": "Stock created"}
