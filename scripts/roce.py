from yahooquery import Ticker
import sqlite3

conn = sqlite3.connect("cashflowdata.db")
cur = conn.cursor()

cur.execute("SELECT tickers from freecashflow_table")
db_rows=cur.fetchall()


symbols = [row[0] for row in db_rows]


for symbol in symbols:
    try:
        tickers = Ticker(symbol)

        dataframe_ebit = tickers.income_statement(trailing=False)
        ebit_values = dataframe_ebit["EBIT"].values
        
        dataframe_totalassets = tickers.balance_sheet(trailing=False)
        totalassets_values = dataframe_totalassets["TotalAssets"].values

        dataframe_currentliabilities = tickers.balance_sheet(trailing=False)
        currentliabilities_values = dataframe_currentliabilities["CurrentLiabilities"].values

        
        recent_values_ebit = float(ebit_values[-1])
        recent_values_totalassets = float(totalassets_values[-1])
        recent_values_currentliabilities = float(currentliabilities_values[-1])
        
        capitolemployed=recent_values_totalassets-recent_values_currentliabilities
        roce=(recent_values_ebit/capitolemployed)*100
        print(symbol,":",roce,"%")
        if(roce>15):
            cur.execute("INSERT INTO roce_table (tickers,roce) VALUES (?,?)",(symbol, roce))
            conn.commit()
            continue



        

    except KeyError:
        print("data not found")   

conn.close() 
# aapl=Ticker('aapl')
# earnings_dataframe=aapl.earnings

# print(earnings_dataframe["aapl"]["financialsChart"]
#       ["yearly"][-1]["revenue"])
