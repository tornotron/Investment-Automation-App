from abc import ABC, abstractmethod
from typing import List
import pandas as pd
import requests
from enum import Enum
from app.db.models.index_listing import IndexListing
from sqlalchemy.orm import Session

from app.db.models.psu_listing import PSUListing


class YahooFinancialsExtractionLib(Enum):
    YFINANCE = "yfinance"
    YAHOO_FINANCIALS = "yahoofinancials"


class FinancialsProvider(ABC):
    @abstractmethod
    def fetch_data(self, symbol: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_tickers_from_index(self, db: Session, index: str) -> List[str]:
        pass

    @abstractmethod
    def get_psu_tickers_from_index(self, db: Session, index: str) -> List[str]:
        pass


class YahooFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str, extraction_lib: YahooFinancialsExtractionLib):
        self.api_key = api_key
        self.extraction_lib = extraction_lib

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.example.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)

    def get_tickers_from_index(self, db: Session, index: str) -> List[str]:
        if index == "NIFTY50":
            index = "^NSEI"
            tickers = (
                db.query(IndexListing)
                .filter(
                    IndexListing.index == index,
                    IndexListing.provider == "YAHOO",
                )
                .all()
            )
            return [ticker.ticker for ticker in tickers]

        else:
            raise ValueError(f"Index {index} not supported")

    def get_psu_tickers_from_index(self, db: Session, index: str) -> List[str]:
        if index == "NIFTY50":
            index = "^NSEI"

            tickers = (
                db.query(PSUListing)
                .filter(
                    PSUListing.index == index,
                    PSUListing.provider == "YAHOO",
                )
                .all()
            )
            return [ticker.ticker for ticker in tickers]

        else:
            raise ValueError(f"Index {index} not supported")


class AlphaVantageFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.example.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)


class FinaincialModelingGrepFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.example.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)


class StockRowFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.anotherexample.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)


class IBKRFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.anotherexample.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)


class AlpacaFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.anotherexample.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)


class ZerodhaFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.anotherexample.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)


class AngelOneFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.anotherexample.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)


class IEXCloudFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.anotherexample.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
