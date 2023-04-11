from yahooquery import Ticker
import sqlite3

conn = sqlite3.connect("cashflowdata.db")
cur = conn.cursor()

cur.execute("SELECT tickers from roce_table")
db_rows=cur.fetchall()

symbols = [row[0] for row in db_rows]


for symbol in symbols:
    try:
        tickers = Ticker(symbol)
        recent_stockholdersequity=tickers.balance_sheet(trailing=False)["StockholdersEquity"].values[-1]
        if(recent_stockholdersequity>20):
            cur.execute("INSERT INTO roe_table (tickers,roe) VALUES (?,?)", (symbol, recent_stockholdersequity))
            conn.commit()
            continue
    except KeyError:
        print("Data not found")

conn.close()