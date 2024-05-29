import pandas as pd
from sqlalchemy.orm import Session
from app.db import models


def insert_tickers(db: Session, tickers_df: pd.DataFrame, provider: str):
    tickers_df["provider"] = provider
    tickers = tickers_df.to_dict(orient="records")
    db.bulk_insert_mappings(models.Ticker, tickers)
    db.commit()


def delete_tickers_by_provider(db: Session, provider: str):
    db.query(models.Ticker).filter(models.Ticker.provider == provider).delete()
    db.commit()
