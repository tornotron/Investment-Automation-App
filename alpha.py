import os
import sqlite3
import csv
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv
import time
import requests
import logging

conn=sqlite3.connect('cashflowdata.db')
cur=conn.cursor()
load_dotenv()
API_KEY = os.getenv("API_KEY")


symbols = []

responses=[]                                                    

with open("ticker_test.csv", "r") as file:
    reader = csv.reader(file)
    # Skip the header row                                           
    next(reader, None)                                          
    for row in reader:                                          
        symbols.append(row[0])                                  


counter=0

for symbol in symbols:
        url = (
        "https://www.alphavantage.co/query?function=CASH_FLOW&symbol="
        + symbol
        + "&apikey="
        + API_KEY
              )
        
        r=requests.get(url)
        cash_flow_data = r.json()
        responses.append(cash_flow_data)
        cashflow=responses[counter]["quarterlyReports"][0]["operatingCashflow"]
        cur.execute("INSERT INTO cashflow_table (ticker,cashflow) VALUES (?,?)",(symbols[counter],cashflow,))        
        conn.commit()
        counter+=1
        print(counter)
        while counter%5==0:
             print(counter)
             time.sleep(75)
             break
             
        
        

conn.close()




