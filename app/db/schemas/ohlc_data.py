from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Yahoo_OHLC_Base(BaseModel):
    ticker: str = Field(..., max_length=10)
    date: datetime
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    volume: Optional[int]
    adjusted_close: Optional[float]
    dividends: Optional[int]
    stock_splits: Optional[int]
    repaired: Optional[bool]
