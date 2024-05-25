from sqlalchemy.orm import Session
from app.db import models, schemas


def get_trade(db: Session, trade_id: int):
    return db.query(models.Trade).filter(models.Trade.id == trade_id).first()


def get_trades(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Trade).offset(skip).limit(limit).all()


def create_trade(db: Session, trade: schemas.TradeCreate):
    db_trade = models.Trade(**trade.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade
