from sqlalchemy.orm import Session
from datetime import date
from app.db import models
from typing import List


def get_daily_filtered_stocks(db: Session, filter_date: date, reason: str):
    return (
        db.query(models.DailyStockFilter)
        .filter(models.DailyStockFilter.filter_date == filter_date)
        .filter(models.DailyStockFilter.reason == reason)
        .all()
    )


def create_daily_filtered_stocks(
    db: Session, filtered_stocks: List[models.DailyStockFilter]
):
    for stock_filter in filtered_stocks:
        is_present = (
            db.query(models.DailyStockFilter)
            .filter(
                models.DailyStockFilter.stock_symbol == stock_filter.stock_symbol,
                models.DailyStockFilter.filter_date == stock_filter.filter_date,
            )
            .first()
            is not None
        )
        if not is_present:
            db.add(stock_filter)
            db.commit()
            db.refresh(stock_filter)
