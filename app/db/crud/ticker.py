import pandas as pd
from sqlalchemy.orm import Session, Mapper
from app.db import models


def bulk_insert_tickers(db: Session, tickers_df: pd.DataFrame, provider: str = None):
    if len(tickers_df.columns) < 5:
        raise ValueError("All required columns are not present in tickers_df.")
    elif len(tickers_df.columns) > 6:
        raise ValueError("Extra columns present in tickers_df.")
    elif len(tickers_df.columns) == 5 and provider is None:
        raise ValueError("Provider name is required when file has no provider column.")
    elif len(tickers_df.columns) == 5:
        tickers_df["provider"] = provider
    tickers_df.columns = [
        "ticker",
        "name",
        "exchange",
        "category_name",
        "country",
        "provider",
    ]
    tickers_df = tickers_df.drop_duplicates(subset=["ticker", "provider"])
    tickers = tickers_df.to_dict(orient="records")
    db.bulk_insert_mappings(models.Ticker, tickers)
    db.commit()


def delete_tickers_by_provider(db: Session, provider: str):
    db.query(models.Ticker).filter(models.Ticker.provider == provider).delete()
    db.commit()


def ticker_exists(db: Session, ticker: str, provider: str) -> bool:
    return (
        db.query(models.Ticker)
        .filter(models.Ticker.ticker == ticker, models.Ticker.provider == provider)
        .first()
        is not None
    )


def insert_single_ticker(db: Session, ticker_row: dict):
    ticker = models.Ticker(**ticker_row)
    db.add(ticker)
    db.commit()
    db.refresh(ticker)
    return ticker


def update_ticker(db: Session, updates: dict):
    ticker_model = (
        db.query(models.Ticker)
        .filter(
            models.Ticker.ticker == updates["ticker"],
            models.Ticker.provider == updates["provider"],
        )
        .first()
    )
    if ticker_model:
        for key, value in updates.items():
            if key != "ticker" and key != "provider":
                setattr(ticker_model, key, value)
        db.commit()
        db.refresh(ticker_model)
        return ticker_model
    return None


def bulk_insert_new_tickers(db: Session, tickers_df: pd.DataFrame, provider: str):
    tickers_df["provider"] = provider
    # Remove duplicates within the DataFrame
    tickers_df = tickers_df.drop_duplicates(subset=["ticker", "provider"])

    # Fetch existing tickers for the provider from the database
    existing_tickers = (
        db.query(models.Ticker.ticker).filter(models.Ticker.provider == provider).all()
    )
    existing_tickers_set = set([ticker[0] for ticker in existing_tickers])

    # Filter out tickers that already exist in the database
    new_tickers_df = tickers_df[~tickers_df["ticker"].isin(existing_tickers_set)]
    new_tickers = new_tickers_df.to_dict(orient="records")

    # Insert new tickers
    db.bulk_insert_mappings(models.Ticker, new_tickers)
    db.commit()


def bulk_update_tickers(db: Session, tickers_df: pd.DataFrame):

    fields = [col for col in tickers_df.columns if col not in ["ticker", "provider"]]

    for field in fields:
        # Ensure the field to update exists in the Ticker model
        if not hasattr(models.Ticker, field):
            raise ValueError(f"Field '{field}' does not exist in the Ticker model.")

    # Iterate over the DataFrame and update each ticker
    for index, row in tickers_df.iterrows():
        ticker = (
            db.query(models.Ticker)
            .filter(
                models.Ticker.ticker == row["ticker"],
                models.Ticker.provider == row["provider"],
            )
            .first()
        )
        if ticker:
            for field in fields:
                setattr(ticker, field, row[field])
            db.commit()
            db.refresh(ticker)
