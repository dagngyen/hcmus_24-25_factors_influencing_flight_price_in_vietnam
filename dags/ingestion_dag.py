# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime, timedelta
# # Import module bạn vừa viết
# from src.etl.flight_etl import extract_flight_data, transform_flight_data, load_flight_data

# default_args = {
#     'owner': 'airflow',
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

# with DAG(
#     'flight_ingestion_v1',
#     default_args=default_args,
#     schedule_interval='@daily',
#     start_date=datetime(2025, 12, 12),
#     catchup=False
# ) as dag:

#     # Task 1: Extract
#     # Lưu ý: XCom được dùng ngầm định để truyền đường dẫn file giữa các task
#     t1_extract = PythonOperator(
#         task_id='extract_task',
#         python_callable=extract_flight_data,
#         op_kwargs={
#             'departure_cities': ['HAN', 'SGN'], # Ví dụ
#             'arrival_cities': ['SGN', 'HAN'],
#             'start_date': '{{ ds }}', # Lấy ngày chạy của Airflow
#             'end_date': '{{ ds }}',
#             'travel_classes': ['Economy', 'Business'],
#             'execution_date': '{{ ds_nodash }}' # Ví dụ: 20231027
#         }
#     )

#     # Task 2: Transform
#     t2_transform = PythonOperator(
#         task_id='transform_task',
#         python_callable=transform_flight_data,
#         op_kwargs={
#             # Lấy output (đường dẫn file raw) từ task t1
#             'raw_file_path': '{{ task_instance.xcom_pull(task_ids="extract_task") }}'
#         }
#     )

#     # Task 3: Load
#     t3_load = PythonOperator(
#         task_id='load_task',
#         python_callable=load_flight_data,
#         op_kwargs={
#             # Lấy output (đường dẫn file processed) từ task t2
#             'processed_file_path': '{{ task_instance.xcom_pull(task_ids="transform_task") }}',
#             'table_name': 'flight_prices'
#         }
#     )

#     # Luồng chạy
#     t1_extract >> t2_transform >> t3_load

###############
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
import pendulum # Thư viện xử lý thời gian chuẩn của Airflow

# Import module ETL của bạn
from src.etl.flight_etl import extract_flight_data, transform_flight_data, load_flight_data

# 1. Định nghĩa múi giờ GMT+7
local_tz = pendulum.timezone("Asia/Ho_Chi_Minh")

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'flight_ingestion_v2',
    default_args=default_args,
    schedule_interval='@daily',
    
    start_date=pendulum.today(local_tz), # Bắt đầu từ hôm qua theo múi giờ GMT+7
    
    catchup=False
) as dag:

    # Task 1: Extract
    t1_extract = PythonOperator(
        task_id='extract_task',
        python_callable=extract_flight_data,
        op_kwargs={
            'departure_cities': ['HAN', 'SGN'], 
            'arrival_cities': ['SGN', 'HAN'],
            
            'start_date': '{{ ds }}', 
            'end_date': '{{ macros.ds_add(ds, 30) }}',
            
            'travel_classes': ['Economy', 'Business'],
            'execution_date': '{{ ds_nodash }}'
        }
    )

    # Task 2: Transform
    t2_transform = PythonOperator(
        task_id='transform_task',
        python_callable=transform_flight_data,
        op_kwargs={
            'raw_file_path': '{{ task_instance.xcom_pull(task_ids="extract_task") }}'
        }
    )

    # Task 3: Load
    t3_load = PythonOperator(
        task_id='load_task',
        python_callable=load_flight_data,
        op_kwargs={
            'processed_file_path': '{{ task_instance.xcom_pull(task_ids="transform_task") }}',
            'table_name': 'flight_prices'
        }
    )

    # Luồng chạy
    t1_extract >> t2_transform >> t3_load