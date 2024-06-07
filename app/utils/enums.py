from enum import Enum


class YahooDataExtractionLib(Enum):
    YFINANCE = "yfinance"
    YAHOO_FINANCIALS = "yahoofinancials"


class YahooPeroid(Enum):
    ONE_DAY = "1d"
    FIVE_DAY = "5d"
    ONE_MON = "1mo"
    THREE_MON = "3mo"
    SIX_MON = "6mo"
    ONE_YEAR = "1yr"
    TWO_YEAR = "2yr"
    FIVE_YEAR = "5yr"
    TEN_YEAR = "10yr"
    YTD = "ytd"
    MAX = "max"


class YahooInterval(Enum):
    ONE_MIN = "1m"
    TWO_MIN = "2m"
    FIVE_MIN = "5m"
    FIFTEEN_MIN = "15m"
    THIRTY_MIN = "30m"
    SIXTY_MIN = "60m"
    NINTEY_MIN = "90m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    FIVE_DAY = "5d"
    ONE_WEEK = "1wk"
    ONE_MONTH = "1mo"
    THREE_MONTH = "3mo"


class TableNames(Enum):
    YAHOO_30MIN60DAY = "yahoo_30min60day"
    YAHOO_1D730DAY = "yahoo_1d730day"
    YAHOO_1WK_MAXDAYS = "yahoo_1wk_maxdays"


class TradeType(Enum):
    INTRADAY = "intraday"
    SWING = "swing"
    POSITIONAL = "positional"


class CacheValidity(Enum):
    INTRADAY = 1
    SWING = 10
    POSITIONAL = 30


class DataRange(Enum):
    INTRADAY = 60 - 1
    SWING = 730 - 1
    POSITIONAL = 365 * 5 - 1


class UserAgent(Enum):
    INTRADAY = "Tornotron-Trading-Client-Intraday/1.0"
    SWING = "Tornotron-Trading-Client-Swing/1.0"
    POSITIONAL = "Tornotron-Trading-Client-Positional/1.0"


class SelectionCriteria(Enum):
    NIFTY50_LOW_BY10TO15_FROM_52WH = "Stocks that are part of NIFTY50 index and are down by 10 to 15% from the 52 week high"
    NIFTY50_PSUS = "The PSUs listed in NIFTY50 index"
    NIFTY50_TOP5_BY_MC = "The top 5 stocks in NIFTY50 by market capitalization"
    STREAK_RECOMMENDED = "Stocks that are recommended by the streak scanner"
    NEWS_RECOMMENDED = "Stocks that are recommended in news having a positive sentiment"
    HIGH_VOL = "High volume stocks from NSE Website"
    HIGH_MOVEMENT = "High movement stocks from NSE Website"
    VOL_SHOCKERS = "Get volume shockers from MoneyControl Website"


# Implementation needs LLM based analysis
class FundamentalsCriteria(Enum):
    IS_MANAGEMENT_SKILLS_GOOD = "Management should be good"
    IS_BUSINESS_MODEL_GOOD = "Business model should be good"
    IS_COMPANY_GROWING = "Company should be growing"
    IS_COMPANY_MAKING_PROFIT = "Company should be making profit"
    IS_COMPANY_UNDERVALUED = "Company should be undervalued"


class ValidationCriteria(Enum):
    TREND_INTRADAY = (
        "Stocks should have consistent bullish or bearish trend in intraday"
    )
    TREND_SWING = "Stocks should have consistent bullish or bearish trend swing"
    TREND_POSITIONAL = (
        "Stocks should have consistent bullish or bearish trend in positional"
    )
    TREND_INTR_MATCH_SWING = "Intraday trend should match with swing trend"
    TREND_INTR_MATCH_POS = "Intraday trend should match with positional trend"
    TREND_SWING_MATCH_POS = "Swing trend should match with positional trend"
    INDEX_TREND = "Stocks should have a positive trend in the index for respective exchanges"  # NSE, BSE, SGX_NIFTY etc... in case of Indian stocks
    GLOBAL_INDEX_TREND = "Global indexes should have a postive trend before trading"
    MARKET_TREND_NEWS = "Markets should have a positive trend based on news"
    MOMENTUM = "Stocks should have high values for momentum indicators"
    OPTIONS_INTEREST = "Stocks should have an open interest in options"


class FilteredLists(Enum):
    FINAL_LIST = "Final list of filtered stocks"
