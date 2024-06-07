import sys
import os

# Ensure the app module is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import click
from app.services import AssetsManager


@click.group()
def cli():
    click.echo("Admin CLI")


@cli.command()
@click.option("--provider", help="The provider name.")
@click.option(
    "--file-path",
    type=click.Path(exists=True),
    required=True,
    help="The path to the CSV or Excel file.",
)
def bulk_upload_tickers(provider: str, file_path: str):
    assets_manager = AssetsManager()
    try:
        assets_manager.bulk_upload_tickers(provider, file_path)
        click.echo("Tickers uploaded successfully")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        assets_manager.close()


@cli.command()
@click.option("--provider", required=True, help="The provider name.")
@click.option("--ticker", required=True, help="The ticker symbol.")
@click.option("--name", required=True, help="The name of the company.")
@click.option(
    "--exchange", required=True, help="The exchange where the ticker is listed."
)
@click.option("--category-name", required=True, help="The category name of the ticker.")
@click.option("--country", required=True, help="The country of the ticker.")
def upload_single_ticker(
    provider: str,
    ticker: str,
    name: str,
    exchange: str,
    category_name: str,
    country: str,
):
    assets_manager = AssetsManager()
    try:
        assets_manager.upload_single_ticker(
            provider, ticker, name, exchange, category_name, country
        )
    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        assets_manager.close()


@cli.command()
@click.option("--ticker", required=True, help="The ticker symbol.")
@click.option("--provider", required=True, help="The provider name.")
@click.option("--field", required=True, help="The field to update.")
@click.option("--value", required=True, help="The new value.")
def update_single_ticker(ticker: str, provider: str, field: str, value: str):
    assets_manager = AssetsManager()
    try:
        assets_manager.update_single_ticker(ticker, provider, field, value)
    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        assets_manager.close()


@cli.command()
@click.option(
    "--file-path",
    type=click.Path(exists=True),
    required=True,
    help="Path to the CSV or Excel file containing tickers to update.",
)
def bulk_update_tickers(file_path: str):
    """Bulk update tickers in the database based on a given field."""
    assets_manager = AssetsManager()
    try:
        assets_manager.bulk_update_tickers(file_path)
        click.echo("Tickers updated successfully")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        assets_manager.close()


@cli.command()
@click.option(
    "--file-path",
    type=click.Path(exists=True),
    required=True,
    help="Path to the CSV or Excel file containing index listings.",
)
def upload_index_listings(file_path: str):
    """Upload index listings from a file and insert them into the database."""
    assets_manager = AssetsManager()
    try:
        assets_manager.upload_index_listings(file_path)
        click.echo("Index listings uploaded successfully")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        assets_manager.close()


@cli.command()
@click.option(
    "--file-path",
    type=click.Path(exists=True),
    required=True,
    help="Path to the CSV or Excel file containing PSU listings.",
)
def upload_psu_listings(file_path: str):
    """Upload PSU listings from a file and insert them into the database."""
    assets_manager = AssetsManager()
    try:
        assets_manager.upload_psu_listings(file_path)
        click.echo("PSU listings uploaded successfully")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        assets_manager.close()


@cli.command()
@click.option(
    "--provider",
    required=True,
    help="The name of the provider to fetch missing ticker information.",
)
def fetch_and_update_missing_ticker_info(provider: str):
    """Fetch and update missing ticker information from the provider."""
    assets_manager = AssetsManager()
    try:
        assets_manager.fetch_and_update_missing_ticker_info(provider)
        click.echo("Missing ticker information updated successfully")
    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        assets_manager.close()


if __name__ == "__main__":
    cli()
