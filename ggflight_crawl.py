from ggflight_selenium import *
from ggflight_sql import *
from ggflight_dataframe import *

# Import necessary libraries
import datetime

# Main function
# First, we need to connect to the Azure SQL database
mydb = connect_db()
if mydb is None:
    print("Connection to Azure SQL failed!")
    exit()

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