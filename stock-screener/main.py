import models
import schemas
import yfinance  # This is Yahoo Finance package
from database import SessionLocal, engine
from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from models import Stock
from sqlalchemy.orm import Session

app = FastAPI()

# Create table
models.Base.metadata.create_all(bind=engine)

# Define you template language and its directory
templates = Jinja2Templates(directory="templates")


# Dependency
# Make sure we can connect to DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(
    request: Request,
    forward_pe=None,
    dividend_yield=None,
    ma50=None,
    ma200=None,
    db: Session = Depends(get_db),
):
    """
    This is the root path - home path

    :param db:
    :param ma200:
    :param ma50:
    :param dividend_yield:
    :param forward_pe:
    :param request:
    :return:
    """

    # Create query object
    stocks = db.query(Stock)

    if forward_pe:
        stocks = stocks.filter(Stock.forward_pe < forward_pe)
    if dividend_yield:
        stocks = stocks.filter(Stock.dividend_yield > dividend_yield)
    if ma50:
        stocks = stocks.filter(Stock.price > Stock.ma50)
    if ma200:
        stocks = stocks.filter(Stock.price > Stock.ma200)

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "stocks": stocks,
            "forward_pe": forward_pe,
            "dividend_yield": dividend_yield,
            "ma50": ma50,
            "ma200": ma200,
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

    stock.ma200 = yahoo_data.info["twoHundredDayAverage"]
    stock.ma50 = yahoo_data.info["fiftyDayAverage"]
    stock.price = yahoo_data.info["previousClose"]
    stock.forward_pe = yahoo_data.info["forwardPE"]
    stock.forward_eps = yahoo_data.info["forwardEps"]

    if yahoo_data.info["dividendYield"] is not None:
        stock.dividend_yield = yahoo_data.info["dividendYield"] * 100

    db.add(stock)
    db.commit()


@app.post("/stock")
async def create_stock(
    stock_request: schemas.StockRequest,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db),
):
    # Return a JSON response

    stock = Stock()
    stock.symbol = stock_request.symbol

    db.add(stock)
    db.commit()

    # Run background task after DB committed
    background_task.add_task(fetch_stock_data, stock.id)

    return {"code": "success", "message": "Stock created"}
