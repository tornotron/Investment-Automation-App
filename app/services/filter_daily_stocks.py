import pandas as pd
from typing import List, Dict
from datetime import date
from enum import Enum
from app.services.financials_providers import FinancialsProvider

# fmt: off
class SelectionCriteria(Enum):
    NIFTY50_LOW_BY10TO15_FROM_52WH = "Stocks that are part of NIFTY50 index and are down by 10 to 15% from the 52 week high"
    NIFTY50_PSUS = "The PSUs listed in NIFTY50 index"
    NIFTY50_TOP5_BY_MC = "The top 5 stocks in NIFTY50 by market capitalization"
    STREAK_RECOMMENDED = "Stocks that are recommended by the streak scanner"
    NEWS_RECOMMENDED = "Stocks that are recommended in news having a positive sentiment"
    HIGH_VOL = "High volume stocks from NSE Website"
    HIGH_MOVEMENT = "High movement stocks from NSE Website"
    VOL_SHOCKERS = "Get volume shockers from MoneyControl Website"


class ValidationCriteria(Enum):
    TREND = "Stocks should have matching trend in postional, swing and intraday windows"
    MOMENTUM = "Stocks should have high values for momentum indicators"
    OPTIONS_INTEREST = "Stocks should have an open interest in options"
    INDEX_TREND = "The NASDAQ SGX_NIFTY and NIFTY50 trends should be positive before trading"
    
class FilteredLists(Enum):
    FINAL_LIST = "Final list of filtered stocks"
# fmt: on

CriteriaWeightage = {
    ValidationCriteria.TREND: 2,
    ValidationCriteria.MOMENTUM: 2,
    ValidationCriteria.OPTIONS_INTEREST: 2,
    ValidationCriteria.INDEX_TREND: 2,
    SelectionCriteria.NIFTY50_LOW_BY10TO15_FROM_52WH: 1,
    SelectionCriteria.NIFTY50_PSUS: 1,
    SelectionCriteria.NIFTY50_TOP5_BY_MC: 1,
    SelectionCriteria.STREAK_RECOMMENDED: 2,
    SelectionCriteria.NEWS_RECOMMENDED: 1,
    SelectionCriteria.HIGH_VOL: 1,
    SelectionCriteria.HIGH_MOVEMENT: 1,
    SelectionCriteria.VOL_SHOCKERS: 1,
}

TickerBuckets = {
    SelectionCriteria.NIFTY50_LOW_BY10TO15_FROM_52WH: [],
    SelectionCriteria.NIFTY50_PSUS: [],
    SelectionCriteria.NIFTY50_TOP5_BY_MC: [],
    SelectionCriteria.STREAK_RECOMMENDED: [],
    SelectionCriteria.NEWS_RECOMMENDED: [],
    SelectionCriteria.HIGH_VOL: [],
    SelectionCriteria.HIGH_MOVEMENT: [],
    SelectionCriteria.VOL_SHOCKERS: [],
    FilteredLists.FINAL_LIST: [],
}


class StockSelectionService:
    def __init__(self, data: date):
        self.date = date

    def update_nifty_50_low_by10to15_from_52wh(fp: FinancialsProvider):
        SelectionCriteria.NIFTY50_LOW_BY10TO15_FROM_52WH = fp.get_tickers_from_index(
            "NIFTY50"
        )

    def update_nifty_50_psus(fp: FinancialsProvider):
        SelectionCriteria.NIFTY50_PSUS = fp.get_psu_tickers_from_index("NIFTY50")


class StockFilteringService:

    def get_daily_filtered_stocks(
        self,
    ) -> Dict[str, pd.DataFrame]:
        filtered_stocks = {}
        filtered_data = self.apply_criteria(tickers, criteria[symbol])
        if not filtered_data.empty:
            rank = self.rank_stocks(filtered_data, criteria[symbol])
            filtered_stocks[symbol] = pd.DataFrame(
                {"ticker": [symbol] * len(rank), "rank": rank}
            )
        return filtered_stocks

    def apply_criteria(self, data: List[str], criteria: str) -> pd.DataFrame:
        # Implement criteria-based filtering logic here
        # Placeholder logic: return all data
        return data

    def rank_stocks(self, data: pd.DataFrame, criteria: str) -> List[float]:
        # Implement ranking logic based on criteria
        # Placeholder logic: return dummy ranks
        return [1.0] * len(data)
