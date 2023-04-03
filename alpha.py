from alpha_vantage.timeseries import TimeSeries
import time

# ts=TimeSeries(key)
symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

for symbol in symbols:
    cash_flow_data, cash_flow_metadata = ts.CASH_FLOW(symbol=symbol)
    operating_cash_flow = float( cash_flow_data['quarterlyReports'][0]['operatingCashflow'])
    if operating_cash_flow > 0:
        print(f"Stock symbol: {symbol}")
        print(f"Operating cash flow: {operating_cash_flow}")
        print("")

time.sleep(15)

