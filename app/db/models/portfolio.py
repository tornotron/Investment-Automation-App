from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="portfolios")
    trades = relationship("Trade", back_populates="portfolio")
