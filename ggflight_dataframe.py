# Import necessary libraries
import pandas as pd
import datetime
import os

# Function to save dataframe to csv
def save_df_to_csv(df, file_name=None, path="./data/daily_flight_data"):
    try:
        if path[-1] == '/':
            path = path[:-1]
        if not os.path.exists(f"{path}"):
            os.makedirs(f"{path}")
        if file_name == "" or file_name is None:
            file_name = f"flight_data_{datetime.datetime.now().strftime("%Y-%m-%d")}.csv"
        df.to_csv(f"{path}/{file_name}", index=False, encoding='utf-8')
        return True
    except Exception as e:
        print(e)
        return False
    
# Function to load dataframe from csv
def load_df_from_csv(file_name, path="./data/daily_flight_data"):
    try:
        if path[-1] == '/':
            path = path[:-1]
        if file_name == "" or file_name is None:
            file_name = f"flight_data_{datetime.datetime.now().strftime("%Y-%m-%d")}.csv"
        return pd.read_csv(f"{path}/{file_name}")
    except Exception as e:
        print(e)
        return None