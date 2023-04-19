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
                print("Data not found")

            except KeyError:
                print("Data not found")
        
        

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
                print("Data not found")
            except TypeError:
                print("Data not found")    
                

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
                if (roce > 15):
                    print(roce)
                    # cur.execute(
                    #     "INSERT INTO roce_table (tickers,roce) VALUES (?,?)", (symbol, roce))
                    # conn.commit()
                    continue

            except KeyError:
                print("data not found")

            except TypeError:
                print("Data not found")    


        
        
        

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

                except TypeError:
                    print("Data not found")    
        
        

    def pe_ratio(self):
        for symbol in self.symbols:
            try:    
                tickers=Ticker(symbol)
                share_price=tickers.financial_data[symbol]["currentPrice"]
                eps=tickers.key_stats[symbol]["trailingEps"]
                peratio=share_price/eps
                print(peratio)

            except KeyError:
                print("Data not found")
            except TypeError:
                print("Data not found")    
        


class ManagementFilter(stocks):
    def __init__(self, symbols):
        super().__init__(symbols)

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
                if (roce > 15):
                    print(roce)
                    # cur.execute(
                    #     "INSERT INTO roce_table (tickers,roce) VALUES (?,?)", (symbol, roce))
                    # conn.commit()
                    continue

            except KeyError:
                print("data not found")

            except TypeError:
                print("Data not found")
                    

    def current_ratio(self):
        for symbol in self.symbols:
            try:
                tickers=Ticker(symbol)
                current_ratio_values=tickers.financial_data[symbol]["currentRatio"]
                print(current_ratio_values)

            except KeyError:
                print("Data not found")    
            except TypeError:
                print("Data not found")    

    def piotrosky_score(self):
        for symbol in self.symbols:            
            try:
                tickers=Ticker(symbol)
                # Profitability F score calculation begin

                roa=tickers.financial_data[symbol]["returnOnAssets"]
                if(roa>0):
                    roa_score=1
                else:
                    roa_score=0
                    
                

                o_cashflow=tickers.cash_flow(trailing=False)["OperatingCashFlow"].values[-1]
                t_assets=tickers.balance_sheet(trailing=False)["TotalAssets"].values[-1]
                cfo=o_cashflow/t_assets
                if(cfo>0):
                    cfo_score=1   
                else:
                    cfo_score=0
                

                a=tickers.balance_sheet(trailing=False)["TotalAssets"].values
                list_length=len(a)
                list_sum=sum(a)
                average_totalassets=list_sum/list_length
                recent_net_income=tickers.cash_flow(trailing=False)["NetIncome"].values[-1]
                before_net_income=tickers.cash_flow(trailing=False)["NetIncome"].values[-2]
                change_in_roa=(recent_net_income/average_totalassets)-(before_net_income/average_totalassets)
                if(change_in_roa>0):
                    change_in_roa_score=1
                else:
                    change_in_roa_score=0
                


                if(cfo>roa):
                    accrual_score=1
                else:
                    accrual_score=0
                
                # Profitability F score calculation end


                #Leverage, Liquidity, and Source of Funds calculation begin

                recent_longTermDebt=tickers.balance_sheet(trailing=False)["LongTermDebt"].values[-1]
                before_longTermDebt=tickers.balance_sheet(trailing=False)["LongTermDebt"].values[-2]
                if((recent_longTermDebt/average_totalassets)>(before_longTermDebt-average_totalassets)):
                    levrage_score=1
                else:
                    levrage_score=0
                


                recent_currentAssets=tickers.balance_sheet(trailing=False)["CurrentAssets"].values[-1]
                before_currentAssets=tickers.balance_sheet(trailing=False)["CurrentAssets"].values[-2]
                recent_currentLiabities=tickers.balance_sheet(trailing=False)["CurrentLiabilities"].values[-1]
                before_currentLiabities=tickers.balance_sheet(trailing=False)["CurrentLiabilities"].values[-2]
                recent_currentratio=recent_currentAssets/recent_currentLiabities
                before_currentratio=before_currentAssets/before_currentLiabities
                if(recent_currentratio>before_currentratio):
                    currentRatio_score=1
                else:
                    currentRatio_score=0





                recent_commonEquity=tickers.balance_sheet(trailing=False)["CommonStockEquity"].values[-1]        
                before_commonEquity=tickers.balance_sheet(trailing=False)["CommonStockEquity"].values[-2]
                if(recent_commonEquity>before_commonEquity):
                    commonequity_score=1
                else:
                    commonequity_score=0

                #Leverage, Liquidity, and Source of Funds calculation end


                

                
                


                




            except TypeError:
                print("Data not found")                         
            except KeyError:
                print("Data not found")    
        


initial_obj=InitialFilter(symbols)
management_obj=ManagementFilter(symbols)

management_obj.piotrosky_score()

