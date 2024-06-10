from abc import ABC, abstractmethod
import pandas as pd
import requests
import yfinance as yf
from datetime import datetime, timedelta, date, time

from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

from app.db import schemas, models
from app.db.crud import create_ohlc_data
from app.utils.constants import YFINANCE_CACHE_FILE
from app.utils.enums import (
    TradeType,
    YahooExtractionLib,
    YahooInterval,
    YahooPeroid,
    CacheValidity,
    UserAgent,
    DataRange,
)
import pytz
from app.core.logger import iap_logger as logger

tz = pytz.timezone("Asia/Kolkata")


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

    def get_trend_favorability(self, db: Session, symbol: str) -> bool:
        pass

    def get_index_trend_favorability(self, db: Session, symbol: str) -> bool:
        pass

    def get_global_index_trend_favorability(self, db: Session, symbol: str) -> bool:
        pass

    def get_market_trend_news_favorability(self, db: Session, symbol: str) -> bool:
        pass

    def get_momentum_favorability(self, db: Session, symbol: str) -> bool:
        pass

    def get_options_interest_favorablitiy(self, db: Session, symbol: str) -> bool:
        pass


# Should not be used for commercial application. License restricted
class YahooDataProvider(DataProvider):
    def __init__(self, extraction_lib: YahooExtractionLib):
        self.extraction_lib = extraction_lib

    def fetch_data(
        self, symbol: str, interval: YahooInterval, peroid: YahooPeroid
    ) -> pd.DataFrame:
        company = yf.Ticker(
            symbol,
        )
        data = company.history(peroid=peroid, interval=interval)
        return data

    def save_data(
        self,
        db: Session,
        symbol: str,
        data: pd.DataFrame,
        table: models.Yahoo_OHLC_Base,
    ):
        """Add data to the database if not already present"""

        for index, row in data.iterrows():
            ticker = symbol
            ohlcvdatetime = index.to_pydatetime()
            open = row["Open"]
            high = row["High"]
            low = row["Low"]
            close = row["Close"]
            volume = row["Volume"]
            dividends = row["Dividends"]
            stock_splits = row["Stock Splits"]
            repaired = row["Repaired?"]
            try:
                ohlc_data = schemas.Yahoo_OHLC_Base(
                    ticker=ticker,
                    ohlcvdatetime=ohlcvdatetime,
                    open=open,
                    high=high,
                    low=low,
                    close=close,
                    volume=volume,
                    dividends=dividends,
                    stock_splits=stock_splits,
                    repaired=repaired,
                )
                create_ohlc_data(db, ohlc_data, table=table)

            except Exception as e:
                print(e)
                continue

        logger.info(f"Data for ticker {symbol} added to {table.__tablename__} table")

    def check_and_fetch_data_positional(self, db, symbol, ytable):
        data = (
            db.query(ytable)
            .filter(
                ytable.ticker == symbol,
            )
            .order_by(ytable.ohlcvdatetime)
            .all()
        )
        if not data:
            logger.info(f"No data found for {symbol} in {ytable.__tablename__}")
            return pd.DataFrame(), None
        else:
            latest_datetime = data[-1].ohlcvdatetime

            # Add timedelta to the latest date to avoid fetching duplicate data
            latest_datetime = latest_datetime + timedelta(days=7)

            # Convert SQLAlchemy models to a list of dictionaries
            data_dicts = [d.__dict__ for d in data]

            # Remove the SQLAlchemy internal state from the dictionaries
            for d in data_dicts:
                d.pop("_sa_instance_state", None)

            logger.info(f"Data found for {symbol} in {ytable.__tablename__}")
            data_df = pd.DataFrame(
                data_dicts,
            )

            # Rename columns
            data_df.rename(
                columns={
                    "ohlcvdatetime": "Datetime",
                    "open": "Open",
                    "high": "High",
                    "low": "Low",
                    "close": "Close",
                    "volume": "Volume",
                    "dividends": "Dividends",
                    "stock_splits": "Stock Splits",
                    "repaired": "Repaired?",
                },
                inplace=True,
            )

            # Select only the required columns
            data_df = data_df[
                [
                    "Datetime",
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Volume",
                    "Dividends",
                    "Stock Splits",
                    "Repaired?",
                ]
            ]

            data_df.set_index("Datetime", inplace=True)
            return data_df, latest_datetime

    def check_and_fetch_data(self, db, symbol, start_date, end_date, ytable):
        data = (
            db.query(ytable)
            .filter(
                ytable.ticker == symbol,
                ytable.ohlcvdatetime >= start_date,
                ytable.ohlcvdatetime <= end_date,
            )
            .order_by(ytable.ohlcvdatetime)
            .all()
        )
        if not data:
            logger.info(f"No data found for {symbol} in {ytable.__tablename__}")
            return pd.DataFrame(), start_date
        else:
            latest_datetime = data[-1].ohlcvdatetime
            # Add timedelta to the latest date to avoid fetching duplicate data
            if ytable == models.Yahoo_30min60day:
                latest_datetime = latest_datetime + timedelta(minutes=30)
            elif ytable == models.Yahoo_1d730day:
                latest_datetime = latest_datetime + timedelta(days=1)
            # Convert SQLAlchemy models to a list of dictionaries
            data_dicts = [d.__dict__ for d in data]

            # Remove the SQLAlchemy internal state from the dictionaries
            for d in data_dicts:
                d.pop("_sa_instance_state", None)

            logger.info(f"Data found for {symbol} in {ytable.__tablename__}")
            data_df = pd.DataFrame(
                data_dicts,
            )

            # Rename columns
            data_df.rename(
                columns={
                    "ohlcvdatetime": "Datetime",
                    "open": "Open",
                    "high": "High",
                    "low": "Low",
                    "close": "Close",
                    "volume": "Volume",
                    "dividends": "Dividends",
                    "stock_splits": "Stock Splits",
                    "repaired": "Repaired?",
                },
                inplace=True,
            )

            # Select only the required columns
            data_df = data_df[
                [
                    "Datetime",
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Volume",
                    "Dividends",
                    "Stock Splits",
                    "Repaired?",
                ]
            ]

            data_df.set_index("Datetime", inplace=True)
            return data_df, latest_datetime

    def get_trend_favorability(
        self, db: Session, symbol: str, trade_type: TradeType
    ) -> bool:

        end_datetime = datetime.now(tz)

        if trade_type == TradeType.INTRADAY:
            cache_validity = CacheValidity.INTRADAY.value
            start_datetime = end_datetime - timedelta(days=DataRange.INTRADAY.value)
            interval = YahooInterval.THIRTY_MIN.value
            ytable = models.Yahoo_30min60day
        elif trade_type == TradeType.SWING:
            cache_validity = CacheValidity.SWING.value
            start_datetime = end_datetime - timedelta(days=DataRange.SWING.value)
            interval = YahooInterval.ONE_DAY.value
            ytable = models.Yahoo_1d730day
        elif trade_type == TradeType.POSITIONAL:
            cache_validity = CacheValidity.POSITIONAL.value
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

        if trade_type == TradeType.INTRADAY:
            session.headers["User-agent"] = UserAgent.INTRADAY.value
        elif trade_type == TradeType.SWING:
            session.headers["User-agent"] = UserAgent.SWING.value
        elif trade_type == TradeType.POSITIONAL:
            session.headers["User-agent"] = UserAgent.POSITIONAL.value

        company = yf.Ticker(symbol, session=session)

        if trade_type != TradeType.POSITIONAL:
            data_ohlcv, start_datetime_updated = self.check_and_fetch_data(
                db,
                symbol,
                start_datetime,
                end_datetime,
                ytable,
            )
            fetch_condition = True
            # If the updated start date is yesterday and the time is after trading hours and if the request is made before 9:15 AM then no need to fetch data
            if (
                (
                    (end_datetime.date() - timedelta(days=1))
                    == start_datetime_updated.date()
                )
                and (start_datetime_updated.time() >= time(15, 30))
                and (end_datetime.time() < time(9, 15))
            ):
                fetch_condition = False
            # If the updated start date is today and the time is after trading hours then no need to fetch data
            if (end_datetime.date() == start_datetime_updated.date()) and (
                start_datetime_updated.time() >= time(15, 30)
            ):
                fetch_condition = False
            # If the updated start date is today and the request is made before 9:15 AM then no need to fetch data
            if (end_datetime.date() == start_datetime_updated.date()) and (
                end_datetime.time() < time(9, 15)
            ):
                fetch_condition = False
            # If the updated start datetime is greater than the end datetime then no need to fetch data
            if start_datetime_updated > end_datetime:
                fetch_condition = False
            if start_datetime_updated == start_datetime:
                logger.info(f"No data found for {symbol} in {ytable.__tablename__}")
                logger.info(
                    f"Fetching data for {symbol} in {ytable.__tablename__} from Yahoo"
                )
                data_ohlcv = company.history(
                    interval=interval,
                    start=start_datetime_updated,
                    end=end_datetime,
                    actions=True,
                    prepost=True,
                    auto_adjust=True,
                    repair=True,
                ).sort_index()
                self.save_data(db, symbol, data_ohlcv, ytable)
            elif fetch_condition:
                logger.info(
                    f"Updating latest data for {symbol} in {ytable.__tablename__}"
                )
                data_ohlcv_updated = company.history(
                    interval=interval,
                    start=start_datetime_updated,
                    end=end_datetime,
                    actions=True,
                    prepost=True,
                    auto_adjust=True,
                    repair=True,
                ).sort_index()
                if not data_ohlcv_updated.empty:
                    self.save_data(db, symbol, data_ohlcv_updated, ytable)
                    logger.info(
                        f"updated {len(data_ohlcv_updated)} rows in {ytable.__tablename__}"
                    )
                    data_ohlcv = pd.concat([data_ohlcv, data_ohlcv_updated])
        else:
            data_ohlcv, start_datetime_updated = self.check_and_fetch_data_positional(
                db,
                symbol,
                ytable,
            )
            fetch_condition = True
            # If the updated start date is last week and the time is after trading hours and if the request is made before 9:15 AM then no need to fetch data
            if (
                (
                    start_datetime_updated.date()
                    == (end_datetime.date() - timedelta(days=7))
                )
                and (end_datetime.time() < time(9, 15))
                and (start_datetime_updated.time() >= time(15, 30))
            ):
                fetch_condition = False
            if start_datetime_updated > end_datetime:
                fetch_condition = False
            if start_datetime_updated == None:
                logger.info(f"No data found for {symbol} in {ytable.__tablename__}")
                logger.info(
                    f"Fetching data for {symbol} in {ytable.__tablename__} from Yahoo"
                )
                data_ohlcv = company.history(
                    interval=interval,
                    period=YahooPeroid.MAX.value,
                    actions=True,
                    prepost=True,
                    auto_adjust=True,
                    repair=True,
                ).sort_index()
                self.save_data(db, symbol, data_ohlcv, ytable)
            elif fetch_condition:
                logger.info(
                    f"Updating latest data for {symbol} in {ytable.__tablename__}"
                )
                data_ohlcv_updated = company.history(
                    interval=interval,
                    start=start_datetime_updated,
                    end=end_datetime,
                    actions=True,
                    prepost=True,
                    auto_adjust=True,
                    repair=True,
                ).sort_index()
                if not data_ohlcv_updated.empty:
                    self.save_data(db, symbol, data_ohlcv_updated, ytable)
                    logger.info(
                        f"updated {len(data_ohlcv_updated)} rows in {ytable.__tablename__}"
                    )
                    data_ohlcv = pd.concat([data_ohlcv, data_ohlcv_updated])

        if data_ohlcv.empty:
            raise ValueError("No data found")

        # Calculate the 200 period  exponential moving average
        ema_200 = data_ohlcv["Close"].ewm(span=200, adjust=False).mean()
        data_ohlcv["EMA_200"] = ema_200
        data_ohlcv["Trend"] = data_ohlcv["Close"] > data_ohlcv["EMA_200"]

        # Check if the past 5 days have been bullish
        data_ohlcv["Bullish"] = data_ohlcv["Close"] > data_ohlcv["EMA_200"]
        data_ohlcv["Bearish"] = data_ohlcv["Close"] < data_ohlcv["EMA_200"]

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
