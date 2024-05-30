from sqlalchemy.orm import Session
from app.db import models, schemas


def get_portfolio(db: Session, portfolio_id: int):
    return (
        db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    )


def get_portfolios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Portfolio).offset(skip).limit(limit).all()


def create_portfolio(db: Session, portfolio: schemas.PortfolioCreate, owner_id: int):
    db_portfolio = models.Portfolio(**portfolio.model_dump(), owner_id=owner_id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio
