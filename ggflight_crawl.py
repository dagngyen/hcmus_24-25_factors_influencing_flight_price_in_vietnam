from ggflight_selenium import *
from ggflight_sql import *
from ggflight_dataframe import *

# Import necessary libraries
import datetime

# Login PostgreSQL client
import psycopg2
from psycopg2 import sql
from psycopg2 import OperationalError

# Connect to PostgreSQL database
def connect_db():
    try:
        connection = psycopg2.connect(
            dbname="ggflight",
            user="user",
            password="00000000",
            host="localhost",
            port="5432"
        )
        return connection
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None
    
# Check exsistence of table, if not exist create new table
def create_table(connection, table_name="flight"):
    cursor = connection.cursor()
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        departure_city VARCHAR(10),
        arrival_city VARCHAR(10),
        travel_class VARCHAR(20),
        departure_date DATE,
        return_date DATE,
        price DECIMAL,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    try:
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error creating table: {e}")
        return False
    
if __name__ == "__main__":
    # Main script execution
    # First, we need to connect to the PostgreSQL database
    mydb = connect_db()
    if mydb:
        print("Connection to PostgreSQL DB successful")
    else:
        print("Failed to connect to PostgreSQL DB")
        exit(1)

    # Next, we need to create a table in the database to store the flight data
    if create_table(mydb):
        print("Table created successfully!")
    else:
        print("Table is already exsist!")

    # Next, we need to scrape the flight data
    departure_city = ['SGN', 'SGN', 'SGN']
    arrival_city = ['HAN', 'DAD', 'CXR']
    travel_class = ['Economy', 'Business']
    start_date = '2024-12-01'
    end_date = '2025-02-28'

    flight_df = multi_scrape(None, departure_city, arrival_city, start_date, end_date, travel_class)

    # Next, we need to save the flight data to a CSV file
    file_name = f"flight_data_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv"
    save_df_to_csv(flight_df, file_name)

    # Next, we need to append the flight data to the table in the database
    if append_flight_df_to_table(mydb, flight_df):
        print("Data appended to table successfully!")
    else:
        print("Data appended to table failed!")

    # Next, we need to close the connection to the Azure SQL database
    mydb.close()