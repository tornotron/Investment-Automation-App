from pydantic import BaseModel
from datetime import date
from typing import List, Dict


class DailyStockFilterBase(BaseModel):
    stock_symbol: str
    filter_date: date
    reason: str = None


class DailyStockFilterCreate(DailyStockFilterBase):
    pass


class DailyStockFilter(DailyStockFilterBase):
    id: int

    class Config:
        from_attributes = True


class StockFilterRequest(BaseModel):
    date: date
    criteria: Dict[str, str]


class StockFilterResponse(BaseModel):
    filtered_stocks: Dict[str, List[str]]
    details: Dict[str, Dict[str, float]]


class DailyFilterResult(BaseModel):
    ticker: str
    rank: float
