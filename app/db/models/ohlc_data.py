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
from sqlalchemy.ext.declarative import declared_attr


class Yahoo_OHLC_Base(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(20), nullable=False)
    ohlcvdatetime = Column(DateTime(timezone=True), nullable=False)
    open = Column(Numeric(10, 2))
    high = Column(Numeric(10, 2))
    low = Column(Numeric(10, 2))
    close = Column(Numeric(10, 2))
    volume = Column(BigInteger)
    dividends = Column(Numeric(10, 2))
    stock_splits = Column(Numeric(10, 2))
    repaired = Column(Boolean)

    @declared_attr
    def __table_args__(cls):
        return (
            UniqueConstraint(
                "ticker", "ohlcvdatetime", name=f"_{cls.__tablename__}_ticker_date_uc"
            ),
        )


class Yahoo_30min60day(Yahoo_OHLC_Base):
    __tablename__ = "yahoo_30min60day"


class Yahoo_1d730day(Yahoo_OHLC_Base):
    __tablename__ = "yahoo_1d730day"


class Yahoo_1wk_maxdays(Yahoo_OHLC_Base):
    __tablename__ = "yahoo_1wk_maxdays"
