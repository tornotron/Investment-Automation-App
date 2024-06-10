from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict
from app.utils.enums import SelectionCriteriaKeys, ValidationCriteriaKeys


class DailyStockFilterBase(BaseModel):
    stock_symbols: List[str]
    provider: str


class DailyStockFilter(DailyStockFilterBase):
    date: datetime = None
    reason: str = None


class DailyStockFilterGenerate(BaseModel):
    selection_criteria: List[SelectionCriteriaKeys]
    validation_criteria: List[ValidationCriteriaKeys]


class DailyStockFilterResponse(BaseModel):
    filtered_stocks: Dict[str, Dict[str, float]]
