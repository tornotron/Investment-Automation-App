import os
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv
import time
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")

# ts = TimeSeries(key="API_KEY")
symbols = ["AAPL", "GOOG", "MSFT", "AMZN"]

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
