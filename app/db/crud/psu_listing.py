import pandas as pd
from sqlalchemy.orm import Session
from app.db.models import Ticker, PSUListing


def insert_psu_listings(db: Session, listings_df: pd.DataFrame):
    listings_df = listings_df.drop_duplicates(subset=["ticker", "index", "provider"])

    for _, row in listings_df.iterrows():
        ticker = (
            db.query(Ticker)
            .filter(Ticker.ticker == row["ticker"], Ticker.provider == row["provider"])
            .first()
        )
        il = (
            db.query(PSUListing)
            .filter(
                PSUListing.ticker == row["ticker"],
                PSUListing.index == row["index"],
                PSUListing.provider == row["provider"],
            )
            .first()
        )
        if il:
            continue
        if ticker:
            psu_listing = PSUListing(
                index=row["index"],
                ticker=row["ticker"],
                provider=row["provider"],
                ticker_id=ticker.id,
            )
            db.add(psu_listing)
        else:
            error_msg = (
                f"The ticker: {row['ticker']} were not found in the ticker table"
            )
            raise ValueError(error_msg)
    db.commit()
