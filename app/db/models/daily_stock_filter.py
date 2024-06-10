from sqlalchemy import Column, Integer, String, Date
from app.db.base import Base


class DailyStockFilter(Base):
    __tablename__ = "daily_stock_filter"

    id = Column(Integer, primary_key=True, index=True)
    stock_symbol = Column(String, index=True, nullable=False)
    provider = Column(String, nullable=False)
    filter_date = Column(Date, nullable=False)
    reason = Column(String, nullable=True)
