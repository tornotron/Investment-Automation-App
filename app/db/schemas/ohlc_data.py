from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Yahoo_OHLC_Base(BaseModel):
    ticker: str = Field(..., max_length=20)
    ohlcvdatetime: datetime
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    volume: Optional[int]
    dividends: Optional[float]
    stock_splits: Optional[float]
    repaired: Optional[bool]
