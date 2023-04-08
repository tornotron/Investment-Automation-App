from yahooquery import Ticker
import csv
import sqlite3

conn=sqlite3.connect('cashflowdata.db')
cur=conn.cursor()
symbols = []



with open("ticker_test.csv", "r") as file:
    reader = csv.reader(file)
    # Skip the header row
    next(reader, None)
    for row in reader:
        symbols.append(row[0])

cashflow_values=[]
recent_cashflow=0

for symbol in symbols:
    try:            
        tickers=Ticker(symbol)     
        dataframe=tickers.cash_flow(trailing=False)
        cashflow_values=dataframe['OperatingCashFlow'].values        
        recent_cashflow=(float(cashflow_values[-1]))
        print(recent_cashflow)
        if(recent_cashflow>0):        
            cur.execute("INSERT INTO cashflow_table (tickers,cashflow) VALUES (?,?)", (symbol,recent_cashflow))
            conn.commit()
            continue

        
    except TypeError:
        print("data not found")
conn.close()