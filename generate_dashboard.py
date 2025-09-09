import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Define the absolute file path for the database and output image.
# Using a single, explicit path string to avoid any issues with os.path.join()
db_file = 'C:\\Users\\V SRILEKHYA\\Documents\\paypal_analytics.db'
output_file = 'C:\\Users\\V SRILEKHYA\\Documents\\paypal_analytics_dashboard.png'

print(f"Connecting to database: {db_file}...")

if not os.path.exists(db_file):
    print(f"Error: Database file not found at '{db_file}'.")
    print("Please ensure the 'paypal_analytics.db' file is in your Documents folder.")
else:
    try:
        conn = sqlite3.connect(db_file)
        
        # Define the queries for visualization
        queries = {
            "Total_Transactions_by_Country": "SELECT country, COUNT(*) as count FROM transactions GROUP BY country ORDER BY count DESC;",
            "Total_Transactions_by_Payment_Method": "SELECT payment_method, COUNT(*) as count FROM transactions GROUP BY payment_method ORDER BY count DESC;",
            "Total_Transactions_by_Status": "SELECT status, COUNT(*) as count FROM transactions GROUP BY status ORDER BY count DESC;",
            "Total_Amount_by_Country": "SELECT country, SUM(transaction_amount) as total_amount FROM transactions GROUP BY country ORDER BY total_amount DESC;",
            "Average_Amount_by_Country": "SELECT country, AVG(transaction_amount) as avg_amount FROM transactions GROUP BY country ORDER BY avg_amount DESC;"
        }

        print("\nExecuting queries and generating dashboard...")
        
        # Set the style for the plots
        sns.set_theme(style="whitegrid")
        
        # Create the figure for the dashboard with a 3x2 grid of subplots
        fig, axes = plt.subplots(3, 2, figsize=(18, 15))
        fig.suptitle('PayPal Transaction Analysis Dashboard', fontsize=24, weight='bold', y=1.02)
        plt.subplots_adjust(hspace=0.5, wspace=0.3)
        
        # Flatten the axes array for easy iteration
        axes_flat = axes.flatten()
        
        # Plot 1: Transactions by Country (Count)
        df_country_count = pd.read_sql_query(queries["Total_Transactions_by_Country"], conn)
        sns.barplot(x='country', y='count', data=df_country_count, ax=axes_flat[0], palette='viridis')
        axes_flat[0].set_title('Transaction Count by Country', fontsize=16)
        axes_flat[0].set_ylabel('Transaction Count')
        axes_flat[0].set_xlabel('Country')
        
        # Plot 2: Transactions by Payment Method (Count)
        df_method_count = pd.read_sql_query(queries["Total_Transactions_by_Payment_Method"], conn)
        sns.barplot(x='payment_method', y='count', data=df_method_count, ax=axes_flat[1], palette='magma')
        axes_flat[1].set_title('Transaction Count by Payment Method', fontsize=16)
        axes_flat[1].set_ylabel('Transaction Count')
        axes_flat[1].set_xlabel('Payment Method')
        
        # Plot 3: Transactions by Status (Count)
        df_status_count = pd.read_sql_query(queries["Total_Transactions_by_Status"], conn)
        sns.barplot(x='status', y='count', data=df_status_count, ax=axes_flat[2], palette='cividis')
        axes_flat[2].set_title('Transaction Count by Status', fontsize=16)
        axes_flat[2].set_ylabel('Transaction Count')
        axes_flat[2].set_xlabel('Status')
        
        # Plot 4: Total Transaction Amount by Country
        df_country_amount = pd.read_sql_query(queries["Total_Amount_by_Country"], conn)
        sns.barplot(x='country', y='total_amount', data=df_country_amount, ax=axes_flat[3], palette='inferno')
        axes_flat[3].set_title('Total Transaction Amount by Country', fontsize=16)
        axes_flat[3].set_ylabel('Total Amount (USD)')
        axes_flat[3].set_xlabel('Country')

        # Plot 5: Average Transaction Amount by Country
        df_country_avg_amount = pd.read_sql_query(queries["Average_Amount_by_Country"], conn)
        sns.barplot(x='country', y='avg_amount', data=df_country_avg_amount, ax=axes_flat[4], palette='plasma')
        axes_flat[4].set_title('Average Transaction Amount by Country', fontsize=16)
        axes_flat[4].set_ylabel('Average Amount (USD)')
        axes_flat[4].set_xlabel('Country')
        
        # Hide the empty subplot
        axes_flat[5].axis('off')
        
        # Save the figure to a file
        plt.savefig(output_file, bbox_inches='tight', dpi=100)
        print("\nDashboard saved successfully to:", output_file)
        
    except sqlite3.OperationalError as e:
        print(f"A database error occurred: {e}")
        print("This may mean the 'transactions' table does not exist or the database file is not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("Database connection closed.")
