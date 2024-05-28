from abc import ABC, abstractmethod
import pandas as pd
import requests
from enum import Enum


class YahooFinancialsExtractionLib(Enum):
    YFINANCE = "yfinance"
    YAHOO_FINANCIALS = "yahoofinancials"


class FinancialsProvider(ABC):
    @abstractmethod
    def fetch_data(self, symbol: str) -> pd.DataFrame:
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
