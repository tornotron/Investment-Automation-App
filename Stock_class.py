import csv
import sqlite3
from yahooquery import Ticker
symbols = []

# conn = sqlite3.connect("cashflowdata.db")
# cur = conn.cursor()

with open("ticker_test.csv", "r") as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
        symbols.append(row[0])
        

class stocks:
    def __init__(self, symbols):
        self.symbols = symbols




class InitialFilter(stocks):

    def __init__(self, symbols):
        super().__init__(symbols)

    def operating_cashflow(self):
        for symbol in self.symbols:
            try:
                tickers = Ticker(symbol)
                dataframe = tickers.cash_flow(trailing=False)
                cashflow_values = dataframe["OperatingCashFlow"].values
                recent_cashflow = float(cashflow_values[-1])
                if recent_cashflow > 0:
                    print(recent_cashflow)
                    # cur.execute(
                    #     "INSERT INTO cashflow_table (tickers,cashflow) VALUES (?,?)",
                    #     (symbol, recent_cashflow),
                    # )
                    # conn.commit()
                    continue

            except TypeError:
                print("data not found")

            except KeyError:
                print("data not found")
        
        

    def free_cashflow(self):
        for symbol in self.symbols:
            try:
                tickers = Ticker(symbol)
                recent_freecashflow = tickers.cash_flow(
                    trailing=False)["FreeCashFlow"][-1]
                if (recent_freecashflow > 0):
                    print(recent_freecashflow)
                    # cur.execute(
                    #     "INSERT INTO freecashflow_table(tickers, freecashflow) VALUES(?, ?)", (symbol, recent_freecashflow))
                    # conn.commit()
                    continue

            except KeyError:
                print("data not found")
                

    def roce(self):

        for symbol in self.symbols:
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

                capitolemployed = recent_values_totalassets-recent_values_currentliabilities
                roce = (recent_values_ebit/capitolemployed)*100
                print(symbol, ":", roce, "%")
                if (roce > 15):
                    print(roce)
                    # cur.execute(
                    #     "INSERT INTO roce_table (tickers,roce) VALUES (?,?)", (symbol, roce))
                    # conn.commit()
                    continue

            except KeyError:
                print("data not found")


        
        
        

    def roe(self):

        for symbol in self.symbols:
                try:
                    tickers = Ticker(symbol)
                    recent_stockholdersequity = tickers.balance_sheet(
                        trailing=False)["StockholdersEquity"].values[-1]
                    if (recent_stockholdersequity > 20):
                        print(recent_stockholdersequity)
                        # cur.execute("INSERT INTO roe_table (tickers,roe) VALUES (?,?)",
                        #             (symbol, recent_stockholdersequity))
                        # conn.commit()
                        continue
                except KeyError:
                    print("Data not found")
        
        

    def pe_ratio(self):
        
        pass


class ManagementFilter(stocks):
    def __init__(self, symbols):
        super().__init__(symbols)

    def roce(self):
        pass            

    def current_ratio(self):
        pass

    def piotrosky_score(self):
        pass


s=InitialFilter(symbols)

operating_cf=s.operating_cashflow()

print(operating_cf)