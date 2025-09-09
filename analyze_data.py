import pandas as pd
import sqlite3
import os

# Define the absolute file path for the database.
# Using the specific Windows path to avoid any issues with os.path.expanduser().
documents_path = 'C:\\Users\\V SRILEKHYA\\Documents'
db_file = os.path.join(documents_path, 'paypal_analytics.db')

print(f"Connecting to database: {db_file}...")

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    
    # Define the SQL queries
    queries = {
        "Total_Transactions": "SELECT COUNT(*) AS TotalTransactions FROM transactions;",
        "Total_Avg_Amount": "SELECT SUM(transaction_amount) AS TotalAmount, AVG(transaction_amount) AS AverageAmount FROM transactions;",
        "Transactions_by_Country": "SELECT country, COUNT(*) AS TransactionCount, SUM(transaction_amount) AS TotalAmount FROM transactions GROUP BY country ORDER BY TotalAmount DESC;",
        "Transactions_by_Payment_Method": "SELECT payment_method, COUNT(*) AS TransactionCount, SUM(transaction_amount) AS TotalAmount FROM transactions GROUP BY payment_method ORDER BY TotalAmount DESC;",
        "Transactions_by_Status": "SELECT status, COUNT(*) AS TransactionCount, SUM(transaction_amount) AS TotalAmount FROM transactions GROUP BY status;"
    }

    print("\nExecuting analytical queries...")
    for name, query in queries.items():
        print("-" * 50)
        print(f"Executing: {name}")
        
        # Use pandas to read the SQL query directly into a DataFrame
        df = pd.read_sql_query(query, conn)
        
        print(f"Results for '{name}':")
        print(df.to_string(index=False)) # Use to_string to avoid truncation
        print("-" * 50)

except sqlite3.OperationalError as e:
    print(f"A database error occurred: {e}")
    print("This may mean the 'transactions' table does not exist or the database file is not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("Database connection closed.")
