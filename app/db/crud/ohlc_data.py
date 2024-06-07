from sqlalchemy.orm import Session
from app.db import models, schemas
from datetime import datetime


def create_ohlc_data(db: Session, ohlc_data: schemas.Yahoo_OHLC_Base, table: str):
    if table == "yahoo_30min60day":
        db_ohlc = models.Yahoo_30min60day(**ohlc_data.to_dict())
    elif table == "yahoo_60min730day":
        db_ohlc = models.Yahoo_60min730day(**ohlc_data.to_dict())
    elif table == "yahoo_1dmaxdays":
        db_ohlc = models.Yahoo_1dmaxdays(**ohlc_data.to_dict())
    db.add(db_ohlc)
    db.commit()
    db.refresh(db_ohlc)
    return db_ohlc


def get_ohlc_data(db: Session, ticker: str, date: datetime, table: str):
    if table == "yahoo_30min60day":
        db_model = models.Yahoo_30min60day
    elif table == "yahoo_60min730day":
        db_model = models.Yahoo_60min730day
    elif table == "yahoo_1dmaxdays":
        db_model = models.Yahoo_1dmaxdays
    else:
        return None
    return (
        db.query(db_model)
        .filter(db_model.ticker == ticker, db_model.date == date)
        .first()
    )


def update_ohlc_data(
    db: Session, ticker: str, date: datetime, updates: dict, table: str
):
    if table == "yahoo_30min60day":
        db_model = models.Yahoo_30min60day
    elif table == "yahoo_60min730day":
        db_model = models.Yahoo_60min730day
    elif table == "yahoo_1dmaxdays":
        db_model = models.Yahoo_1dmaxdays
    else:
        return None
    db_ohlc = (
        db.query(db_model)
        .filter(db_model.ticker == ticker, db_model.date == date)
        .first()
    )
    if db_ohlc:
        for key, value in updates.items():
            setattr(db_ohlc, key, value)
        db.commit()
        db.refresh(db_ohlc)
    return db_ohlc


def delete_ohlc_data(db: Session, ticker: str, date: datetime, table: str):
    if table == "yahoo_30min60day":
        db_model = models.Yahoo_30min60day
    elif table == "yahoo_60min730day":
        db_model = models.Yahoo_60min730day
    elif table == "yahoo_1dmaxdays":
        db_model = models.Yahoo_1dmaxdays
    else:
        return None
    db_ohlc = (
        db.query(db_model)
        .filter(db_model.ticker == ticker, db_model.date == date)
        .first()
    )
    if db_ohlc:
        db.delete(db_ohlc)
        db.commit()
    return db_ohlc
