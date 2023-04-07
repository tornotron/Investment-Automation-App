from yahooquery import Ticker
import csv
# import sqlite3

# conn=sqlite3.connect('cashflowdata.db')
# cur=conn.cursor()
symbols = []



with open("ticker_test.csv", "r") as file:
    reader = csv.reader(file)
    # Skip the header row
    next(reader, None)
    for row in reader:
        symbols.append(row[0])
print(len(symbols))
tickers=Ticker(symbols)
print(tickers)
dataframe=tickers.cash_flow()
cashflow_values = dataframe['OperatingCashFlow'].values
print(len(cashflow_values))
positive_cashflows=[]
for cashflow_value in cashflow_values:
    if cashflow_value>0:
        positive_cashflows.append(cashflow_value)
print(len(positive_cashflows))
# counter=0

# for symbol in symbols:
#     cur.execute("INSERT INTO cashflow_table (ticker,cashflow) VALUES (?,?)",(symbols[counter], positive_cashflows[counter],))
#     counter+=1
#     conn.commit()

# conn.close()