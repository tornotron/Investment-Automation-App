from abc import ABC, abstractmethod
from typing import List
from enum import Enum
from app.db.models.index_listing import IndexListing
from sqlalchemy.orm import Session

from app.db.models.psu_listing import PSUListing
from app.db.models.ticker import Ticker
from app.db.crud.ticker import update_single_ticker
import yfinance as yf


class YahooFinancialsExtractionLib(Enum):
    YFINANCE = "yfinance"
    YAHOO_FINANCIALS = "yahoofinancials"


class FinancialsProvider(ABC):
    @abstractmethod
    def get_tickers_from_index(self, db: Session, index: str) -> List[str]:
        pass

    @abstractmethod
    def get_psu_tickers_from_index(self, db: Session, index: str) -> List[str]:
        pass

    def unsupported_method(self, method_name: str):
        raise NotImplementedError(
            f"This method is not yet supported by the {self.__class__.__name__} provider"
        )


class YahooFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str, extraction_lib: YahooFinancialsExtractionLib):
        self.api_key = api_key
        self.extraction_lib = extraction_lib

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

    def get_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_tickers_from_index")

    def get_psu_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_psu_tickers_from_index")


class FinaincialModelingGrepFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_tickers_from_index")

    def get_psu_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_psu_tickers_from_index")


class StockRowFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_tickers_from_index")

    def get_psu_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_psu_tickers_from_index")


class IBKRFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_tickers_from_index")

    def get_psu_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_psu_tickers_from_index")


class AlpacaFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_tickers_from_index")

    def get_psu_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_psu_tickers_from_index")


class ZerodhaFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_tickers_from_index")

    def get_psu_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_psu_tickers_from_index")


class AngelOneFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_tickers_from_index")

    def get_psu_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_psu_tickers_from_index")


class IEXCloudFinancialsProvider(FinancialsProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_tickers_from_index")

    def get_psu_tickers_from_index(self, db: Session, index: str) -> List[str]:
        return self.unsupported_method("get_psu_tickers_from_index")
