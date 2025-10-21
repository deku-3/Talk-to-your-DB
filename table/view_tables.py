import sqlite3
import pandas as pd

# Connect to the DB
conn = sqlite3.connect('sales.db')

# Query all tables
df = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables:", df)

# View data from a specific table
sales_df = pd.read_sql_query("SELECT * FROM sales ;", conn)
print(sales_df)

conn.close()
