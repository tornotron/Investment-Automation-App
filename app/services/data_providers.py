from abc import ABC, abstractmethod
import pandas as pd
import requests
import yfinance as yf
from datetime import datetime, timedelta

from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

from app.db import schemas, models
from app.db.crud import create_ohlc_data
from app.utils.constants import YFINANCE_CACHE_FILE
from app.utils.enums import (
    TradeType,
    YahooDataExtractionLib,
    YahooInterval,
    YahooPeroid,
    CacheValidity,
    UserAgent,
    DataRange,
)


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    # def request(self, method, url, *args, **kwargs):
    #     # Get the cached response, if available
    #     cached_response = self.cache.get_response_and_time(url)
    #     headers = kwargs.get("headers", {})

    #     if cached_response:
    #         etag = cached_response.headers["ETag"]
    #         headers["If-Modified-Since"] = cached_response.headers["Date"]

    #         if etag:
    #             headers["If-None-Match"] = etag
    #         kwargs["headers"] = headers

    #     response = super().request(method, url, *args, **kwargs)

    #     if response.status_code == 304:
    #         # Not modified, use the cached response
    #         response = cached_response[0]
    #     else:
    #         # Update the cache with the new response
    #         self.cache.save_response(response, cache_key=url)

    #     return response


class DataProvider(ABC):
    @abstractmethod
    def fetch_data(self, symbol: str) -> pd.DataFrame:
        pass

    def get_trend_favorability(self, symbol: str) -> bool:
        pass

    def get_index_trend_favorability(self, symbol: str) -> bool:
        pass

    def get_global_index_trend_favorability(self, symbol: str) -> bool:
        pass

    def get_market_trend_news_favorability(self, symbol: str) -> bool:
        pass

    def get_momentum_favorability(self, symbol: str) -> bool:
        pass

    def get_options_interest_favorablitiy(self, symbol: str) -> bool:
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

    def check_and_save_data(self, data: pd.DataFrame, table: models.Yahoo_OHLC_Base):
        """Add data to the database if not already present"""
        db: Session = Session()

        try:
            for index, row in data.iterrows():
                ticker = row["ticker"]
                date = index.to_pydatetime()
                open = row["open"]
                high = row["high"]
                low = row["low"]
                close = row["close"]
                volume = row["volume"]
                adjusted_close = row["adjusted_close"]
                dividends = row["dividends"]
                stock_splits = row["stock_splits"]
                repaired = row["repaired"]
                try:
                    ohlc_data = schemas.Yahoo_OHLC_Base(
                        ticker=ticker,
                        date=date,
                        open=open,
                        high=high,
                        low=low,
                        close=close,
                        volume=volume,
                        adjusted_close=adjusted_close,
                        dividends=dividends,
                        stock_splits=stock_splits,
                        repaired=repaired,
                    )
                    create_ohlc_data(db, ohlc_data, table=table)
                    print(f"Data for ticker {ticker} added to {table} table")

                except Exception as e:
                    print(e)
                    continue

        finally:
            db.close()

    def get_trend_favorability(self, symbol: str, trade_type: TradeType) -> bool:

        end_date = datetime.now()

        if trade_type == TradeType.INTRADAY:
            cache_validity = CacheValidity.INTRADAY.value
            session.headers["User-agent"] = UserAgent.INTRADAY.value
            start_date = end_date - timedelta(days=DataRange.INTRADAY.value)
            interval = YahooInterval.THIRTY_MIN.value
            ytable = models.Yahoo_30min60day
        elif trade_type == TradeType.SWING:
            cache_validity = CacheValidity.SWING.value
            session.headers["User-agent"] = UserAgent.SWING.value
            start_date = end_date - timedelta(days=DataRange.SWING.value)
            interval = YahooInterval.ONE_DAY.value
            ytable = models.Yahoo_1d730day
        elif trade_type == TradeType.POSITIONAL:
            cache_validity = CacheValidity.POSITIONAL.value
            session.headers["User-agent"] = UserAgent.POSITIONAL.value
            interval = YahooInterval.ONE_WEEK.value
            ytable = models.Yahoo_1wk_maxdays
        else:
            raise ValueError("Invalid trade type")

        session = CachedLimiterSession(
            limiter=Limiter(
                RequestRate(2, Duration.SECOND * 5)
            ),  # max 2 requests per 5 seconds
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache(YFINANCE_CACHE_FILE),
            expire_after=timedelta(days=cache_validity),
        )

        company = yf.Ticker(symbol, session=session)

        if trade_type != TradeType.POSITIONAL:
            data_ohlcv = company.history(
                interval=interval,
                start=start_date,
                end=end_date,
                actions=True,
                prepost=True,
                auto_adjust=True,
                repair=True,
            ).sort_index(inplace=True)
        else:
            data_ohlcv = company.history(
                interval=interval,
                period=YahooPeroid.MAX.value,
                actions=True,
                prepost=True,
                auto_adjust=True,
                repair=True,
            ).sort_index(inplace=True)

        self.check_and_save_data(data_ohlcv, ytable)

        # Calculate the 200 period  exponential moving average
        ema_200 = data_ohlcv["close"].ewm(span=200, adjust=False).mean()
        data_ohlcv["ema_200"] = ema_200
        data_ohlcv["Trend"] = data_ohlcv["close"] > data_ohlcv["ema_200"]

        # Check if the past 5 days have been bullish
        data_ohlcv["Bullish"] = data_ohlcv["close"] > data_ohlcv["ema_200"]
        data_ohlcv["Bearish"] = data_ohlcv["close"] < data_ohlcv["ema_200"]

        # Check the number of bullish days in the past 100 days
        is_bullish = (
            data_ohlcv["Bullish"].tail(10).sum() > 10
            and data_ohlcv["Bullish"].tail(100).sum() > 70
        )

        return is_bullish


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


class IEXCloudDataProvider(DataProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        url = f"https://api.anotherexample.com/stocks/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
