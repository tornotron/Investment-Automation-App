from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Ticker(Base):
    __tablename__ = "ticker"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    exchange = Column(String, nullable=False)
    category_name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    provider = Column(String, nullable=False)
