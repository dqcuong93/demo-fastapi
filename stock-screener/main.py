import models
import yfinance  # This is Yahoo Finance package
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates
from models import Stock
from pydantic import BaseModel
from sqlalchemy.orm import Session

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


def fetch_stock_data(id: int):
    # New DB session
    db = SessionLocal()

    # Get first queried instance
    stock = db.query(Stock).filter(Stock.id == id).first()

    # Set attribute manually for testing if background task is running or not
    # stock.forward_pe = 10

    yahoo_data = yfinance.Ticker(stock.symbol)

    stock.ma200 = yahoo_data.info['twoHundredDayAverage']
    stock.ma50 = yahoo_data.info['fiftyDayAverage']
    stock.price = yahoo_data.info['previousClose']
    stock.forward_pe = yahoo_data.info['forwardPE']
    stock.forward_eps = yahoo_data.info['forwardEps']

    if yahoo_data.info['dividendYield'] is not None:
        stock.dividend_yield = yahoo_data.info['dividendYield'] * 100

    db.add(stock)
    db.commit()


@app.post("/stock")
async def create_stock(stock_request: StockRequest, background_task: BackgroundTasks,
                       db: Session = Depends(get_db)):
    # Return a JSON response

    stock = Stock()
    stock.symbol = stock_request.symbol

    db.add(stock)
    db.commit()

    # Run background task after DB committed
    background_task.add_task(fetch_stock_data, stock.id)

    return {"code": "success", "message": "Stock created"}
