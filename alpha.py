import os
import csv
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv
import time
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")

# ts = TimeSeries(key="API_KEY")
# symbols = ["AAPL", "GOOG", "MSFT", "AMZN"]
symbols = []

with open("nasdaq_tickers.csv", "r") as file:
    reader = csv.reader(file)
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
    operating_cash_flow = float(
        cash_flow_data["quarterlyReports"][0]["operatingCashflow"]
    )
    print(operating_cash_flow)
    if operating_cash_flow > 0:
        print(f"Stock symbol: {symbol}")
        print(f"Operating cash flow: {operating_cash_flow}")
        print("")

time.sleep(5)
