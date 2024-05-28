from abc import ABC, abstractmethod
import pandas as pd
import requests
from enum import Enum
import yfinance as yf


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


class DataProvider(ABC):
    @abstractmethod
    def fetch_data(self, symbol: str) -> pd.DataFrame:
        pass


# Should not be used for commercial application. License restricted
class YahooDataProvider(DataProvider):
    def __init__(self, api_key: str, extraction_lib: YahooDataExtractionLib):
        self.api_key = api_key
        self.extraction_lib = extraction_lib

    def fetch_data(
        self, symbol: str, interval: YahooInterval, peroid: YahooPeroid
    ) -> pd.DataFrame:
        company = yf.Ticker(
            symbol,
        )
        data = company.history(peroid=peroid, interval=interval)
        return data


class AlphaVantageDataProvider(DataProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.example.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)


class FinaincialModelingGrepDataProvider(DataProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.example.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)


class StockRowDataProvider(DataProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.anotherexample.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)


class IBKRDataProvider(DataProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.anotherexample.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)


class AlpacaDataProvider(DataProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.anotherexample.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)


class ZerodhaDataProvider(DataProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.anotherexample.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)


class AngelOneDataProvider(DataProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.anotherexample.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
