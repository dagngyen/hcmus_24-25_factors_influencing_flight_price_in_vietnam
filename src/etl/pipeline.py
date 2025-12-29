import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from src.scraping.ggflight_scraper import GGFlightScraper
from src.database.db_client import PostgresClient
from src.kafka.producer import FlightKafkaProducer
from src.kafka.consumer import FlightKafkaConsumer
import json
import datetime
import pytz

# Tên topic quy định chung
KAFKA_TOPIC = "flight_data_pipeline"

def extract_flight_data(
    departure_cities: list, 
    arrival_cities: list, 
    start_date: str, 
    end_date: str, 
    travel_classes: list
):
    """
    Task Extract: Gọi Selenium Scraper và publish kết quả Raw lên Kafka.
    execution_date: Dùng để định danh tên file theo ngày chạy (từ Airflow truyền vào).
    """
    print(f"--- Bắt đầu Extract từ {start_date} đến {end_date} ---")

    # 1. Gọi hàm Scraper có sẵn
    df_result = GGFlightScraper(
        flight_df=None,
        departure_city=departure_cities,
        arrival_city=arrival_cities,
        start_date=start_date,
        end_date=end_date,
        travel_class=travel_classes
    )

    if df_result is not None and not df_result.empty:
        try:
            # 2. Load dataframe into PostgreSQL Raw Table
            db_client = PostgresClient()
            db_client.load_data(df_result, table_name='flight_raw')

            # # 3. Announce event via Kafka
            # producer = FlightKafkaProducer()
            
            # # Payload chỉ chứa thông tin metadata (nhẹ)
            # payload = {
            #     "start_date": start_date,
            #     "end_date": end_date,
            #     "record_count": len(df_result),
            #     "source": "ggflight",
            #     "status": "ready_for_transform"
            # }
            
            # producer.send_event(topic=KAFKA_TOPIC, event_type="RAW_DATA_SAVED", payload=payload)
            # producer.close()
        except Exception as e:
            print(f"--- Lỗi Critical: {e} ---")
            raise e
    else:
        print("--- Không cào được dữ liệu nào! ---")

def transform_load_flight_data():
    """
    Task Transform: Nghe Kafka -> Lấy data Raw -> Clean -> Lưu Clean
    """
    # consumer = FlightKafkaConsumer(topic=KAFKA_TOPIC)
    
    # # Lấy message (chờ tối đa 10s, nếu không có tin nhắn nào thì coi như không có việc để làm)
    # messages = consumer.consume_once(timeout_ms=10000)
    
    # if not messages:
    #     print("--- Không có sự kiện mới từ Kafka. Skip transform. ---")
    #     return

    db_client = PostgresClient()

    # for msg in messages:
    #     event_type = msg.get('event_type')
    #     payload = msg.get('payload')

    #     if event_type == "RAW_DATA_SAVED":
    #         print(f"--- Nhận tín hiệu xử lý data: {payload} ---")
    current_date = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d")
    
    # 1. Query dữ liệu từ Raw Table dựa trên payload (Ví dụ lấy data vừa cào)
    # Logic đơn giản: Lấy data có timestamp cùng date (%Y-%m-%d) với now()
    query = f"""
        SELECT * FROM flight_raw 
        WHERE timestamp LIKE '{current_date}%'
    """
    df_raw = db_client.fetch_data(query) 

    if df_raw.empty:
        print("--- Data raw trống, bỏ qua ---")
        return

    # 2. Transform Logic (Clean Data)
    print("--- Đang transform dữ liệu... ---")
    # Remove duplicates
    df_clean = df_raw.copy().drop_duplicates()
    # Convert data types
    df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], format='%Y-%m-%d', errors='coerce')
    df_clean['departure_datetime'] = pd.to_datetime(df_clean['departure_datetime'], format='%Y-%m-%d %H:%M', errors='coerce')
    df_clean['arrival_datetime'] = pd.to_datetime(df_clean['arrival_datetime'], format='%Y-%m-%d %H:%M', errors='coerce')
    df_clean['price'] = pd.to_numeric(df_clean['price'], errors='coerce')
    # Convert num_stop string to integer: If 'Non-stop' -> 0, else get first word as integer
    def convert_num_stop(x):
        if isinstance(x, str):
            if x.lower() == 'Nonstop':
                return 0
            else:
                try:
                    return int(x.split()[0])
                except:
                    return None
        return None
    df_clean['num_stop'] = df_clean['num_stop'].apply(convert_num_stop)
    # Drop duplicate rows again after conversion
    df_clean = df_clean.drop_duplicates()
    
    # 3. Load vào bảng Clean
    try:
        db_client.load_data(df_clean, table_name='flight_prices', if_exists='append')
        print("--- Đã lưu dữ liệu sạch vào flight_prices ---")
        
        # (Optional) Gửi tiếp 1 event báo Clean xong để AI Model sử dụng
        producer = FlightKafkaProducer()
        producer.send_event(KAFKA_TOPIC, "DATA_CLEANED", {"count": len(df_clean)})
        producer.close()
        
    except Exception as e:
        print(f"--- Lỗi lưu data clean: {e} ---")
    
    # consumer.close()


# def load_flight_data():
#     """
#     Task Load: Consume dữ liệu đã xử lý từ Kafka và lưu vào PostgreSQL.
#     """
#     print(f"--- Bắt đầu Load dữ liệu từ Kafka topic '{KAFKA_TOPIC}_processed' ---")

#     consumer = KafkaConsumer(
#         f"{KAFKA_TOPIC}_processed",
#         bootstrap_servers=KAFKA_BROKER,
#         value_deserializer=lambda v: json.loads(v.decode('utf-8')),
#         auto_offset_reset='earliest',
#         enable_auto_commit=True,
#         group_id='flight_load_group'
#     )

#     db_user = os.getenv("POSTGRES_USER")
#     db_password = os.getenv("POSTGRES_PASSWORD")
#     db_name = os.getenv("POSTGRES_DB")
#     db_host = "flight_postgres"
#     db_port = os.getenv("POSTGRES_PORT", "5432")

#     connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
#     engine = create_engine(connection_string)

#     for message in consumer:
#         data = message.value

#         try:
#             df = pd.DataFrame([data])
#             df.to_sql('processed_flight_data', engine, if_exists='append', index=False)
#             print(f"--- Đã lưu dữ liệu vào cơ sở dữ liệu ---")
#         except Exception as e:
#             print(f"--- Lỗi khi lưu dữ liệu vào DB: {e} ---")