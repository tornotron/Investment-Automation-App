from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base import Base


class Trade(Base):
    __tablename__ = "trade"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"))
    portfolio = relationship("Portfolio", back_populates="trades")
    asset = Column(String, index=True)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    trade_type = Column(String, index=True)  # e.g., "buy" or "sell"
