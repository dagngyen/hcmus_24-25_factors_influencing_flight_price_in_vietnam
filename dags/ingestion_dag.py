from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# Thêm đường dẫn src để Airflow nhận diện module
sys.path.append('/opt/airflow')
from src.etl.flight_etl import run_pipeline

default_args = {
    'owner': 'user',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='flight_price_ingestion',
    default_args=default_args,
    schedule_interval='0 7 * * *', # Chạy 7h sáng mỗi ngày
    start_date=datetime(2023, 1, 1),
    catchup=False
) as dag:
    
    task_crawl_and_load = PythonOperator(
        task_id='crawl_flight_data',
        python_callable=run_pipeline
    )