from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class IndexListing(Base):
    __tablename__ = "index_listing"

    id = Column(Integer, primary_key=True, index=True)
    index = Column(String, nullable=False)
    ticker = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    ticker_id = Column(Integer, ForeignKey("ticker.id"), nullable=False)

    ticker_model = relationship("Ticker", back_populates="index_listings")
