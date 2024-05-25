from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    portfolios = relationship("Portfolio", back_populates="owner")
