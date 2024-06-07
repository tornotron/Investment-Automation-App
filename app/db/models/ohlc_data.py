from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    BigInteger,
    DateTime,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Yahoo_30min60day(Base):
    table_name = "yahoo_30min60day"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    open = Column(Numeric(10, 2))
    high = Column(Numeric(10, 2))
    low = Column(Numeric(10, 2))
    close = Column(Numeric(10, 2))
    volume = Column(BigInteger)
    adjusted_close = Column(Numeric(10, 2))
    dividends = Column(Numeric(10, 2))
    stock_splits = Column(Numeric(10, 2))
    repaired = Column(Boolean)
    __table_args__ = (UniqueConstraint("ticker", "date", name="_ticker_date_uc"),)


class Yahoo_60min730day(Base):
    table_name = "yahoo_60min730day"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    open = Column(Numeric(10, 2))
    high = Column(Numeric(10, 2))
    low = Column(Numeric(10, 2))
    close = Column(Numeric(10, 2))
    volume = Column(BigInteger)
    adjusted_close = Column(Numeric(10, 2))
    dividends = Column(Numeric(10, 2))
    stock_splits = Column(Numeric(10, 2))
    repaired = Column(Boolean)
    __table_args__ = (UniqueConstraint("ticker", "date", name="_ticker_date_uc"),)


class Yahoo_1dmaxdays(Base):
    table_name = "yahoo_1dmaxdays"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    open = Column(Numeric(10, 2))
    high = Column(Numeric(10, 2))
    low = Column(Numeric(10, 2))
    close = Column(Numeric(10, 2))
    volume = Column(BigInteger)
    adjusted_close = Column(Numeric(10, 2))
    dividends = Column(Numeric(10, 2))
    stock_splits = Column(Numeric(10, 2))
    repaired = Column(Boolean)
    __table_args__ = (UniqueConstraint("ticker", "date", name="_ticker_date_uc"),)
