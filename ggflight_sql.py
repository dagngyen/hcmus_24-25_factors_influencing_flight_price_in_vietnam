# Azure SQL imports
import pyodbc

# Pandas imports
import pandas as pd

# SQL
# Function to connect to Azure SQL
def connect_db():
    server = 'hcmus-intelhunter-ggflight.database.windows.net'  # Tên máy chủ
    database = 'google-flight'  # Tên cơ sở dữ liệu
    username = 'dagngyen'  # Tên người dùng
    password = 'Abc12345'  # Mật khẩu, hãy thay thế bằng mật khẩu thực tế
    port = '1433'  # Cổng

    # Tạo chuỗi kết nối
    connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server},{port};Database={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;"

    try:
        # Kết nối đến cơ sở dữ liệu
        conn = pyodbc.connect(connection_string)
        print("Connected to Azure SQL database successfully!")
        return conn
    except Exception as e:
        print("Error connecting to Azure SQL database.")
        print(e)
        return None
    
# Function to create table in Azure SQL
def create_table(mydb, table_name="flight"):
    if mydb == None:
        mydb = connect_db()
    cursor = mydb.cursor()
    cursor.execute(f"SELECT name FROM sys.tables WHERE name = '{table_name}'")
    if cursor.fetchone() is None:
        create_table = f"""
        CREATE TABLE {table_name} (
            scrape_date DATE,
            id_departure CHAR(4),
            id_arrival CHAR(4),
            departure_datetime DATETIME,
            arrival_datetime DATETIME,
            airline NTEXT,
            travel_class NTEXT,
            is_nonstop NTEXT,
            price FLOAT,
        )"""
        cursor.execute(create_table)
        cursor.commit()
        return True
    return False

# Function to delete table in Azure SQL
def delete_table(mydb, table_name="flight"):
    if mydb == None:
        mydb = connect_db()
    cursor = mydb.cursor()
    cursor.execute(f"SELECT name FROM sys.tables WHERE name = '{table_name}'")
    if cursor.fetchone() != None:
        try:
            cursor.execute(f"DROP TABLE {table_name}")
            cursor.commit()
            return True
        except Exception as e:
            print(e)
    return False

# Function to insert data into Azure SQL
def insert_flight_df_row_to_table(cursor, row, table_name="flight"):
    sql_template = f"""
            INSERT INTO {table_name}(
                scrape_date, 
                id_departure, 
                id_arrival, 
                departure_datetime, 
                arrival_datetime, 
                airline, 
                travel_class, 
                is_nonstop, 
                price)
            VALUES (?,?,?,?,?,?,?,?,?)
            """
    
    cursor.execute(sql_template, 
        row["scrape_date"], 
        row["id_departure"], 
        row["id_arrival"], 
        row["departure_datetime"], 
        row["arrival_datetime"], 
        row["airline"], 
        row["travel_class"], 
        row["is_nonstop"],
        row["price"]
    )
    
# Append dataframe to table
def append_flight_df_to_table(mydb, df, table_name="flight"):
    # Check connection
    if mydb is None:
        mydb = connect_db()
        
    # Check dataframe is exsist
    if df is None:
        print("Dataframe is not exsist!")
        return False
    
    # Check flight table is exsist
    cursor = mydb.cursor()
    cursor.execute(f"SELECT name FROM sys.tables WHERE name = '{table_name}'")
    if cursor.fetchone() == None:
        print("{} table is not exsist!".format(table_name))
        # Create table
        create_table(mydb, table_name)
    
    # Append dataframe to table
    for _, row in df.iterrows():
        insert_flight_df_row_to_table(cursor, row, table_name)
        
    cursor.commit()
    return True

# Function to load dataframe from Azure SQL
def load_df_from_azure_sql(mydb, table_name="flight"):
    # Check connection
    if mydb is None:
        mydb = connect_db()
    # cursor = mydb.cursor()
    # cursor.execute(f"SELECT * FROM {table_name}")
    return pd.read_sql(f"SELECT * FROM {table_name}",mydb)