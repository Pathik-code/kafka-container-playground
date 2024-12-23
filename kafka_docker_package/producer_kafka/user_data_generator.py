import pandas as pd # type: ignore
import numpy as np
from faker import Faker
import psycopg2
import os
import time
import subprocess
from kafka_configuration import TopicCreation, KafkaProducerClient, KafkaConsumerClient, KafkaAdminClient, bootstrap_servers, TOPICS

# Initialize Faker
fake = Faker()

# Set random seed for reproducibility
np.random.seed(42)

# Define the number of users
n_users = 100000
chunk_size = 1000

# Database connection details
DB_DETAILS = {
    "dbname": "postgres",  # Replace with your database name
    "user": "postgres",         # Replace with your PostgreSQL username
    "password": "postgres",     # Replace with your PostgreSQL password
    "host": "localhost",             # Host for local PostgreSQL
    "port": "5432"                   # Default PostgreSQL port
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

# Function to fetch category data and short forms
def fetch_category_data(connection):
    try:
        # Empty list for category data
        cat = []
        cursor = connection.cursor()
        # Execute the query to fetch CategoryName and ShortForm
        cursor.execute("SELECT CategoryName, ShortForm FROM DataCreation.TradingCategories;")
        category_details = cursor.fetchall()  # Fetch all results
        
        # Print the fetched data
        print("CategoryName and ShortForm:")
        for row in category_details:
            print(f"Category: {row[0]}, ShortForm: {row[1]}")
            cat.append(row[1])
        
        return cat
    
    except psycopg2.Error as e:
        print(f"Error fetching data: {e}")

# Function to connect to the database and use the COPY command
def copy_csv_to_postgres(csv_file, table_name, connection):
    try:
        # Path to your CSV file

        # Construct the psql \copy command
        psql_command = f"PGPASSWORD={DB_DETAILS['password']} psql -h {DB_DETAILS['host']} -U {DB_DETAILS['user']} -d {DB_DETAILS['dbname']} -c \"\\copy {table_name} (userid, name, age, city, tradingcategories, accountbalance, experiencelevel) FROM '{csv_file}' DELIMITER ',' CSV HEADER;\""

        # Run the command using subprocess
        # subprocess.run(psql_command, shell=True, check=True)
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
    print("Connection Details:", conn)
    
    # Create Kafka topics
    topic_creator = TopicCreation(bootstrap_servers)
    for topic in TOPICS:
        topic_creator.create_topic(topic)
    topic_creator.close()

    # Initialize Kafka producer
    producer = KafkaProducerClient(bootstrap_servers)
    
    # Fetch category data if needed
    cat = fetch_category_data(conn)
    
    # Data insertion loop
    for _ in range(0, n_users, chunk_size):
        # Define user data (only generating data for each chunk)
        user_data = {
            "UserID": [fake.uuid4()[:8] for _ in range(chunk_size)],  # Unique user IDs
            "Name": [fake.name() for _ in range(chunk_size)],         # User names
            "Age": np.random.randint(20, 60, size=chunk_size),        # Random age between 20 and 60
            "City": [fake.city() for _ in range(chunk_size)],         # User's city
            "TradingCategories": [np.random.choice(cat, size=np.random.randint(1, 4), replace=False).tolist() for _ in range(chunk_size)],  # Random trading categories
            "AccountBalance": np.random.uniform(10000, 1000000, size=chunk_size).round(2),  # Account balance
            "ExperienceLevel": np.random.choice(["Beginner", "Intermediate", "Expert"], size=chunk_size)  # Experience level
        }

        # Convert to DataFrame
        user_df = pd.DataFrame(user_data)

        # Expand TradingCategories into multiple rows for users with multiple categories
        user_df = user_df.explode("TradingCategories").reset_index(drop=True)

        # Save the DataFrame to a CSV file
        csv_file_path = "synthetic_trading_users.csv"  # Define the CSV file path
        csv_file_path = os.path.abspath(csv_file_path)

        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
        user_df.to_csv(csv_file_path, index=False)  # Save without index

        # Change file permissions to allow reading by everyone (read permission)
        os.chmod(csv_file_path, 0o644)  # This gives read/write permissions for the owner, and read permission for others

        # Insert the data into PostgreSQL in chunks
        copy_csv_to_postgres(csv_file_path, 'datacreation.userdata', conn)

        # Push data to Kafka
        for _, row in user_df.iterrows():
            producer.produce_message("user-data", row.to_dict())

        time.sleep(10)

    # Close the Kafka producer
    producer.close()

    # Close the connection after all operations
    close_connection(conn)




