# Login PostgreSQL client
import psycopg2
from psycopg2 import sql
from psycopg2 import OperationalError
from psycopg2.extras import execute_values

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

if __name__ == "__main__":
    conn = connect_db()
    if conn:
        print("Connection to PostgreSQL DB successful")
        conn.close()
    else:
        print("Failed to connect to PostgreSQL DB")
# Additional functions for database operations can be added here