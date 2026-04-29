from sqlmodel import SQLModel, Field
from datetime import datetime

class StockPrices(SQLModel, table=True):
    __tablename__ = 'stock_prices'
    __table_args__ = {'schema':'raw'}
    ticker: str | None = Field(default=None, primary_key=True)
    timestamp: datetime | None = Field(default=None, primary_key=True)
    open: float
    high: float
    low: float
    close: float
    volume: int

class CryptoPrices(SQLModel, table=True):
    __tablename__ = 'crypto_prices'
    __table_args__ = {'schema':'raw'}
    symbol: str | None = Field(default=None, primary_key=True)
    timestamp: datetime | None = Field(default=None, primary_key=True)
    price: float
    total_volume: int
    market_cap: float
    high_24h: float
    low_24h: float