import pandas as pd
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
import logging
from app.utils.constants import APP_LOG_LEVEL
from app.db import crud


logging.basicConfig(level=APP_LOG_LEVEL)
logger = logging.getLogger(__name__)


class AssetsManager:

    def bulk_upload_tickers(
        self,
        provider: str,
        file_path: str,
    ):
        db: Session = SessionLocal()
        try:
            file_type = file_path.split(".")[-1]
            if file_type not in ["csv", "xlsx"]:
                raise Exception("Unsupported file type")
            tickers_df = self.parse_ticker_file(file_path, file_type)
            crud.delete_tickers_by_provider(db, provider)
            crud.bulk_insert_tickers(db, tickers_df, provider)
            logger.info("Tickers uploaded successfully")
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        finally:
            db.close()

    def upload_single_ticker(
        self,
        provider: str,
        ticker: str,
        name: str,
        exchange: str,
        category_name: str,
        country: str,
    ):
        db: Session = SessionLocal()
        try:
            ticker_row = {
                "ticker": ticker,
                "name": name,
                "exchange": exchange,
                "category_name": category_name,
                "country": country,
                "provider": provider,
            }

            if crud.ticker_exists(db, ticker, provider):
                logger.warning(
                    f"Ticker {ticker} already exists for provider {provider}"
                )
                return
            else:
                new_ticker = crud.insert_single_ticker(db, ticker_row)
                logger.info(f"Ticker {new_ticker.ticker} uploaded successfully")
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        finally:
            db.close()

    def update_single_ticker(
        self,
        ticker: str,
        provider: str,
        field: str,
        value: str,
    ):
        db: Session = SessionLocal()
        try:
            updates = {field: value, "ticker": ticker, "provider": provider}
            ticker = crud.update_single_ticker(db, updates)
            if ticker:
                logger.info(f"Ticker {ticker.ticker} updated successfully")
            else:
                logger.warn("Ticker not found")
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        finally:
            db.close()

    def bulk_update_tickers(
        self,
        file_path: str,
    ):
        """Bulk update tickers in the database based on a given field."""
        db: Session = SessionLocal()
        try:
            file_type = file_path.split(".")[-1]
            if file_type not in ["csv", "xlsx"]:
                raise Exception("Unsupported file type")
            tickers_df = self.parse_ticker_file(file_path, file_type)
            crud.bulk_update_tickers(db, tickers_df)
            logger.info("Tickers updated successfully")
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        finally:
            db.close()

    def upload_index_listings(file_path: str):
        """Upload index listings from a file and insert them into the database."""
        db: Session = SessionLocal()
        try:
            file_type = file_path.split(".")[-1]
            if file_type not in ["csv", "xlsx"]:
                raise Exception("Unsupported file type")
            listings_df = (
                pd.read_csv(file_path)
                if file_type == "csv"
                else pd.read_excel(file_path)
            )

            # Check if required columns are present
            required_columns = {"ticker", "index", "provider"}
            if not required_columns.issubset(set(listings_df.columns)):
                raise Exception(
                    f"File must contain the following columns: {required_columns}"
                )

            crud.insert_index_listings(db, listings_df)
            logger.info("Index listings uploaded successfully")
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        finally:
            db.close()

    def upload_psu_listings(file_path: str):
        """Upload PSU listings from a file and insert them into the database."""
        db: Session = SessionLocal()
        try:
            file_type = file_path.split(".")[-1]
            if file_type not in ["csv", "xlsx"]:
                raise Exception("Unsupported file type")
            listings_df = (
                pd.read_csv(file_path)
                if file_type == "csv"
                else pd.read_excel(file_path)
            )

            # Check if required columns are present
            required_columns = {"ticker", "index", "provider"}
            if not required_columns.issubset(set(listings_df.columns)):
                raise Exception(
                    f"File must contain the following columns: {required_columns}"
                )

            crud.insert_psu_listings(db, listings_df)
            logger.info("PSU listings uploaded successfully")
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        finally:
            db.close()

    def fetch_and_update_missing_ticker_info(provider: str):
        """Fetch and update missing ticker information from the provider."""
        db: Session = SessionLocal()
        try:
            tickers = crud.get_tickers_with_null_vlaues(db)
            for ticker in tickers:
                crud.get_missing_ticker_data(db, ticker, provider)
            logger.info("Missing ticker information updated successfully")
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        finally:
            db.close()

    def parse_ticker_file(self, file_path: str, file_type: str) -> pd.DataFrame:
        if file_type == "csv":
            # Read the CSV file without header
            df = pd.read_csv(file_path, header=None)

            # Extract the first row to use as column names
            new_column_names = df.iloc[0].tolist()

            # Set the new column names
            df.columns = new_column_names

            # Drop the first row which was used as column names
            df = df.drop(df.index[0])
        elif file_type == "xlsx":
            # Read the Excel file without header
            df = pd.read_excel(file_path, header=None, dtype=str)

            # Extract the first row to use as column names
            new_column_names = df.iloc[0].tolist()

            # Set the new column names
            df.columns = new_column_names

            # Drop the first row which was used as column names
            df = df.drop(df.index[0]).reset_index(drop=True)
        else:
            raise ValueError("Unsupported file type")

        # Drop rows where all values are null
        df = df.dropna(axis=0, how="all")

        # Convert all data types to string
        df = df.astype(str)

        return df
