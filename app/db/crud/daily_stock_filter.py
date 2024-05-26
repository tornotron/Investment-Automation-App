from sqlalchemy.orm import Session
from datetime import date
from app.db import models, schemas


def get_daily_filtered_stocks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DailyStockFilter).offset(skip).limit(limit).all()


def get__daily_filtered_stocks_by_date(db: Session, filter_date: date):
    return (
        db.query(models.DailyStockFilter)
        .filter(models.DailyStockFilter.filter_date == filter_date)
        .all()
    )


def create_daily_stock_filter(
    db: Session, stock_filter: schemas.DailyStockFilterCreate
):
    db_stock_filter = models.DailyStockFilter(**stock_filter.dict())
    db.add(db_stock_filter)
    db.commit()
    db.refresh(db_stock_filter)
    return db_stock_filter
