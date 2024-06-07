from sqlalchemy.orm import Session
from app.db import models, schemas
from datetime import datetime


def create_ohlc_data(
    db: Session, ohlc_data: schemas.Yahoo_OHLC_Base, table: models.Yahoo_OHLC_Base
):
    db_ohlc = table(**ohlc_data.to_dict())
    db.add(db_ohlc)
    db.commit()
    db.refresh(db_ohlc)
    return db_ohlc


def get_ohlc_data(
    db: Session,
    ticker: str,
    date: datetime,
    table: models.Yahoo_OHLC_Base,
):
    return db.query(table).filter(table.ticker == ticker, table.date == date).first()


def update_ohlc_data(
    db: Session,
    ticker: str,
    date: datetime,
    updates: dict,
    table: models.Yahoo_OHLC_Base,
):

    ohlc_data = (
        db.query(table).filter(table.ticker == ticker, table.date == date).first()
    )
    if ohlc_data:
        for key, value in updates.items():
            setattr(ohlc_data, key, value)
        db.commit()
        db.refresh(ohlc_data)
    return ohlc_data


def delete_ohlc_data(
    db: Session,
    ticker: str,
    date: datetime,
    table: models.Yahoo_OHLC_Base,
):
    ohlc_data = (
        db.query(table).filter(table.ticker == ticker, table.date == date).first()
    )
    if ohlc_data:
        db.delete(ohlc_data)
        db.commit()
    return ohlc_data
