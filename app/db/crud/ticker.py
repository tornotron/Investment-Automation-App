import pandas as pd
from sqlalchemy import or_
from sqlalchemy.orm import Session, Mapper
from app.db import models
from app.db.models.ticker import Ticker
import yfinance as yf


def bulk_insert_tickers(db: Session, tickers_df: pd.DataFrame, provider: str = None):
    """First time bulk insert of tickers into the database."""
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
    """
    Delete tickers from the database by provider.

    Args:
        db (Session): The database session.
        provider (str): The provider of the tickers to be deleted.

    Returns:
        None
    """
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


def update_single_ticker(db: Session, updates: dict):
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
    """Insert new tickers into the database in a table that already has tickers."""
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


def get_tickers_with_null_vlaues(db: Session) -> list:
    return (
        db.query(models.Ticker)
        .filter(
            or_(
                Ticker.name.in_([None, "nan"]),
                Ticker.exchange.in_([None, "nan"]),
                Ticker.category_name.in_([None, "nan"]),
                Ticker.country.in_([None, "nan"]),
            )
        )
        .all()
    )


def get_missing_ticker_data(db: Session, ticker: Ticker, provider: str):
    if provider == "YAHOO":
        update_ticker_with_yahoo_data(db, ticker)
    else:
        raise ValueError(f"Provider {provider} not supported")


def update_ticker_with_yahoo_data(db: Session, ticker: Ticker):
    ticker_symbol = ticker.ticker
    try:
        yf_ticker = yf.Ticker(ticker_symbol)
        info = yf_ticker.info
        print(f"Fetched data for {ticker_symbol}")
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {str(e)}")
        return

    try:
        company_name = info.get("longName")
        if company_name is None:
            company_name = ticker.name
    except Exception as e:
        raise ValueError(f"Error fetching company name for {ticker_symbol}: {str(e)}")
    try:
        exchange = info.get("exchange")
        if exchange is None:
            exchange = ticker.exchange
    except Exception as e:
        raise ValueError(f"Error fetching exchange for {ticker_symbol}: {str(e)}")
    try:
        category_name = info.get("sector")
        if category_name is None:
            category_name = ticker.category_name
    except Exception as e:
        raise ValueError(f"Error fetching category name for {ticker_symbol}: {str(e)}")
    try:
        country = info.get("country")
        if country is None:
            country = ticker.country
    except Exception as e:
        raise ValueError(f"Error fetching country for {ticker_symbol}: {str(e)}")

    print(
        f"Updating values for {ticker_symbol}: name: {company_name}, exchange: {exchange}, category_name: {category_name}, country: {country}"
    )
    update_single_ticker(
        db,
        {
            "ticker": ticker_symbol,
            "name": company_name,
            "exchange": exchange,
            "category_name": category_name,
            "country": country,
            "provider": "YAHOO",
        },
    )
