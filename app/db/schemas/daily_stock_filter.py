from pydantic import BaseModel
from datetime import date


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
