from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class PSUListing(Base):
    __tablename__ = "psu_listing"

    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    index = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    ticker_id = Column(Integer, ForeignKey("ticker.id"), nullable=False)

    ticker_model = relationship("Ticker", back_populates="psu_listings")
