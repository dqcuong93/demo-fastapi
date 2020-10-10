from pydantic import BaseModel


# Create a schema for DB - this is auto validation
class StockRequest(BaseModel):
    symbol: str
