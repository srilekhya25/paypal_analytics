import pandas as pd
import sqlite3
import os

# Define the file paths
# IMPORTANT: The script will now look for the file in your Documents directory
# regardless of where the script is executed from.
documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
csv_file = os.path.join(documents_path, 'paypal_transactions.csv')
db_file = 'paypal_analytics.db'

print(f"Connecting to database: {db_file}...")

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Read the data from the CSV file into a Pandas DataFrame
    print(f"Reading data from {csv_file}...")
    df = pd.read_csv(csv_file)

    # Rename the 'amount' column to 'transaction_amount' to match the SQL schema
    # This is a temporary fix based on your previous queries
    df.rename(columns={'amount': 'transaction_amount'}, inplace=True)

    # Load the DataFrame into the 'transactions' table in the database
    # 'if_exists="append"' adds new rows to the existing table
    print(f"Loading {len(df)} rows into the 'transactions' table...")
    df.to_sql('transactions', conn, if_exists='append', index=False)
    
    # Commit the changes and close the connection
    conn.commit()
    print("Data loading complete!")
    print(f"{len(df)} rows have been successfully loaded into the 'transactions' table.")

except FileNotFoundError:
    print(f"Error: The file '{csv_file}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("Database connection closed.")
