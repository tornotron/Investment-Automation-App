import sqlite3

conn = sqlite3.connect('cashflowdata.db')
cur = conn.cursor()
# cur.execute("""CREATE TABLE cashflow_table(
#                 tickers TEXT,
#                 cashflow REAL
#                 )"""
#             )
cur.execute("""CREATE TABLE roce_table(
                tickers TEXT,
                roce REAL
                )"""
            )


# cur.execute("""DROP TABLE cashflow_table
# """)

# cur.execute("""DROP TABLE roce_table
# """)


conn.commit()
conn.close()
