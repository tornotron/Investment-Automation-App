import sqlite3

conn = sqlite3.connect('cashflowdata.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE cashflow_table(
                ticker TEXT,
                cashflow REAL
                )"""
            )
# cur.execute("""DROP TABLE cashflow_table
# """)

conn.commit()
conn.close()