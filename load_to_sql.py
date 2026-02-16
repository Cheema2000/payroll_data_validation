import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('payroll.db')

# Load data
df = pd.read_csv('data/clean_payroll.csv')

# Create table
df.to_sql('payroll', conn, if_exists='replace', index=False)

# Verify
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM payroll")
print(f"Loaded {cursor.fetchone()[0]} records to payroll.db")

conn.close()
print("Data loaded to SQLite successfully!")
