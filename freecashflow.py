from yahooquery import Ticker
import sqlite3

conn=sqlite3.connect("cashflowdata.db")
cur = conn.cursor()

cur.execute("SELECT tickers from cashflow_table")
db_rows = cur.fetchall()

symbols = [row[0] for row in db_rows]



for symbol in symbols:
        try:
            tickers= Ticker(symbol)
            recent_freecashflow= tickers.cash_flow(trailing=False)["FreeCashFlow"][-1]
            if(recent_freecashflow>0):
                cur.execute("INSERT INTO freecashflow_table(tickers, freecashflow) VALUES(?, ?)",(symbol, recent_freecashflow))
                conn.commit()
                continue

        except KeyError:
              print("data not found")    
           
conn.close()         
