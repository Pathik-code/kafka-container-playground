import pandas as pd
import numpy as np
from faker import Faker
import psycopg2
import os
import time
import subprocess
from kafka_configuration import TopicCreation, KafkaProducerClient, KafkaConsumerClient, KafkaAdminClient, bootstrap_servers

# Initialize Faker
fake = Faker()

# Set random seed for reproducibility
np.random.seed(42)

# Define the list of stocks and number of records
stocks = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "META", "NFLX", "NVDA"]
n_records = 1000000
chunk_size = 3000

# Database connection details
DB_DETAILS = {
    "dbname": "postgres",  # Replace with your database name
    "user": "postgres",    # Replace with your PostgreSQL username
    "password": "postgres",  # Replace with your PostgreSQL password
    "host": "localhost",   # Host for local PostgreSQL
    "port": "5432"         # Default PostgreSQL port
}

# Function to connect to the database
def connect_to_postgres(db_details):
    try:
        # Establish the connection
        connection = psycopg2.connect(
            dbname=db_details["dbname"],
            user=db_details["user"],
            password=db_details["password"],
            host=db_details["host"],
            port=db_details["port"]
        )
        print("Connection to PostgreSQL established successfully!")
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# Function to close the connection
def close_connection(connection):
    if connection:
        connection.close()
        print("PostgreSQL connection closed.")

# Function to connect to the database and use the COPY command
def copy_csv_to_postgres(csv_file, table_name, connection):
    try:
        # Construct the psql \copy command
        psql_command = f"PGPASSWORD={DB_DETAILS['password']} psql -h {DB_DETAILS['host']} -U {DB_DETAILS['user']} -d {DB_DETAILS['dbname']} -c \"\\copy {table_name} (StockSymbol, TradeDate, OpenPrice, HighPrice, LowPrice, ClosePrice, Volume) FROM '{csv_file}' DELIMITER ',' CSV HEADER;\""

        # Run the command using subprocess
        print(psql_command)
        result = subprocess.run(psql_command, shell=True, check=True, capture_output=True, text=True)

        # Print the output
        print("Command Output:")
        print(result.stdout)

        # Print any error output if it occurs
        if result.stderr:
            print("Command Error Output:")
            print(result.stderr)

    except psycopg2.Error as e:
        print(f"Error copying data: {e}")

# Main execution
if __name__ == "__main__":
    # Connect to the database
    conn = connect_to_postgres(DB_DETAILS)
    
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT version();")
        print(f"PostgreSQL version: {cur.fetchone()}")

        conn.commit()
        print("Connection Details:", conn)
    
    iteratio_number = 0

    # Initialize Kafka producer
    producer = KafkaProducerClient(bootstrap_servers)
    
    # Data insertion loop
    for _ in range(0, n_records, chunk_size):
        # Generate synthetic stock data for each chunk
        stock_data = {
            "StockSymbol": [np.random.choice(stocks) for _ in range(chunk_size)],  # Randomly choose stock symbols
            "TradeDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(chunk_size)],  # Random dates
            "OpenPrice": np.random.uniform(50, 2000, size=chunk_size).round(2),  # Random open prices
            "HighPrice": [(lambda x: (x + np.random.uniform(0, 50)).round(2))(x) for x in np.random.uniform(50, 2000, size=chunk_size)],  # High price based on open price
            "LowPrice": [(lambda x: (x - np.random.uniform(0, 50)).round(2))(x) for x in np.random.uniform(50, 2000, size=chunk_size)],   # Low price based on open price
            "ClosePrice": [(lambda x: (x + np.random.uniform(-20, 20)).round(2))(x) for x in np.random.uniform(50, 2000, size=chunk_size)],  # Close price near open price
            "Volume": np.random.randint(1000, 1000000, size=chunk_size)       # Random trade volumes
        }
        # Create the DataFrame
        stock_df = pd.DataFrame(stock_data)

        # Save the DataFrame to a CSV file
        csv_file_path = "synthetic_stock_prices.csv"  # Define the CSV file path
        csv_file_path = os.path.abspath(csv_file_path)

        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
        stock_df.to_csv(csv_file_path, index=False)  # Save without index

        # Change file permissions to allow reading by everyone
        os.chmod(csv_file_path, 0o644)  # Read/write for owner, read for others

        # Insert the data into PostgreSQL in chunks
        copy_csv_to_postgres(csv_file_path, 'stockanalysis.stockdata', conn)

        # Convert TradeDate to string
        stock_df['TradeDate'] = stock_df['TradeDate'].astype(str)

        # Initialize Kafka producer
        producer = KafkaProducerClient(bootstrap_servers)
        # Push data to Kafka
        for _, row in stock_df.iterrows():
            producer.produce_message("stock-data", row.to_dict())

        time.sleep(10)  # Optional: Pause between chunks

    # Close the connection after all operations
    close_connection(conn)
