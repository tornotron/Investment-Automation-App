import pandas as pd
from sqlalchemy.orm import Session
from app.db.models import IndexListing, Ticker


def insert_index_listings(db: Session, listings_df: pd.DataFrame):
    listings_df = listings_df.drop_duplicates(subset=["ticker", "index", "provider"])

    for index, row in listings_df.iterrows():
        ticker = (
            db.query(Ticker)
            .filter(Ticker.ticker == row["ticker"], Ticker.provider == row["provider"])
            .first()
        )
        il = (
            db.query(IndexListing)
            .filter(
                IndexListing.ticker == row["ticker"],
                IndexListing.index == row["index"],
                IndexListing.provider == row["provider"],
            )
            .first()
        )
        if il:
            continue
        if ticker:
            index_listing = IndexListing(
                index=row["index"],
                ticker=row["ticker"],
                provider=row["provider"],
                ticker_id=ticker.id,
            )
            db.add(index_listing)
        else:
            error_msg = (
                f"The ticker: {row['ticker']} were not found in the ticker table"
            )
            raise ValueError(error_msg)
    db.commit()
