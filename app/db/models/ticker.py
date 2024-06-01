from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.dialects.postgresql import JSON


class Ticker(Base):
    __tablename__ = "ticker"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True, nullable=False, unique=False)
    name = Column(String, nullable=True)
    exchange = Column(String, nullable=True)
    category_name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    provider = Column(String, nullable=False)
    index_listings = Column(JSON, nullable=True)
    index_listings = relationship(
        "IndexListing", back_populates="ticker_model", cascade="all, delete-orphan"
    )
    psu_listings = relationship(
        "PSUListing", back_populates="ticker_model", cascade="all, delete-orphan"
    )
