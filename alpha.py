import os
import csv
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv
import time
import requests
import logging

load_dotenv()
API_KEY = os.getenv("API_KEY")

# ts = TimeSeries(key="API_KEY")
# symbols = ["AAPL", "GOOG", "MSFT", "AMZN"]
symbols = []

with open("nasdaq_tickers.csv", "r") as file:
    reader = csv.reader(file)
    # Skip the header row
    next(reader, None)
    for row in reader:
        symbols.append(row[0])

for symbol in symbols:
    url = (
        "https://www.alphavantage.co/query?function=CASH_FLOW&symbol="
        + symbol
        + "&apikey="
        + API_KEY
    )

    cash_flow_data = requests.get(url).json()
    # cash_flow_data, cash_flow_metadata = ts.cash_flow(symbol=symbol)
    try:
        cash_flow = cash_flow_data["quarterlyReports"][0]["operatingCashflow"]
        if cash_flow is not None:
            operating_cash_flow = float(cash_flow)
        else:
            logging.error(f"Cash flow for {symbol} is None")
            continue
    except KeyError:
        logging.error(f"Could not find operating cash flow for {symbol}")
        continue
    print(operating_cash_flow)
    if operating_cash_flow is not None and operating_cash_flow > 0:
        print(f"Stock symbol: {symbol}")
        print(f"Operating cash flow: {operating_cash_flow}")
        print("")

time.sleep(5)
