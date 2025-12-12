import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from src.scrapers.ggflight_scraper import GGFlightScraper

# --- CẤU HÌNH ĐƯỜNG DẪN DỮ LIỆU ---
# Lưu ý: /opt/airflow/data là đường dẫn bên trong Docker container (đã mount volume)
DATA_DIR = "/opt/airflow/data"
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# # Đảm bảo thư mục tồn tại
# os.makedirs(RAW_DIR, exist_ok=True)
# os.makedirs(PROCESSED_DIR, exist_ok=True)

def extract_flight_data(
    departure_cities: list, 
    arrival_cities: list, 
    start_date: str, 
    end_date: str, 
    travel_classes: list,
    execution_date: str
):
    """
    Task Extract: Gọi Selenium Scraper và lưu kết quả Raw ra file CSV.
    execution_date: Dùng để định danh tên file theo ngày chạy (từ Airflow truyền vào).
    """
    os.makedirs(RAW_DIR, exist_ok=True)
    print(f"--- Bắt đầu Extract từ {start_date} đến {end_date} ---")
    
    # 1. Gọi hàm Scraper có sẵn
    # Khởi tạo df rỗng ban đầu hoặc None như logic của bạn
    df_result = GGFlightScraper(
        flight_df=None,
        departure_city=departure_cities,
        arrival_city=arrival_cities,
        start_date=start_date,
        end_date=end_date,
        travel_class=travel_classes
    )

    if df_result is not None and not df_result.empty:
        # 2. Lưu ra file CSV (Raw)
        filename = f"flights_raw_{execution_date}.csv"
        file_path = os.path.join(RAW_DIR, filename)
        
        df_result.to_csv(file_path, index=False)
        print(f"--- Đã lưu Raw Data tại: {file_path} | Số dòng: {len(df_result)} ---")
        return file_path
    else:
        print("--- Không cào được dữ liệu nào! ---")
        return None

def transform_flight_data(raw_file_path: str):
    """
    Task Transform: Đọc file Raw, chuẩn hóa kiểu dữ liệu.
    """
    if not raw_file_path or raw_file_path == "None":
        print("Không có file đầu vào để xử lý.")
        return None

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    print(f"--- Bắt đầu Transform file: {raw_file_path} ---")
    
    # 1. Đọc dữ liệu
    df = pd.read_csv(raw_file_path)

    # 2. Xử lý kiểu dữ liệu (Data Type Casting)
    # Convert price sang numeric (đề phòng sót ký tự lạ)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    
    # Convert datetime columns
    df['departure_datetime'] = pd.to_datetime(df['departure_datetime'])
    df['arrival_datetime'] = pd.to_datetime(df['arrival_datetime'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # 3. Thêm các logic làm sạch khác (nếu cần)
    # Ví dụ: Xóa các dòng có giá trị null quan trọng
    df.dropna(subset=['price', 'departure_datetime'], inplace=True)
    
    # Remove duplicates nếu scraper bị trùng
    df.drop_duplicates(inplace=True)

    # 4. Lưu ra file Processed
    filename = os.path.basename(raw_file_path).replace("raw", "processed")
    processed_path = os.path.join(PROCESSED_DIR, filename)
    
    df.to_csv(processed_path, index=False)
    print(f"--- Đã lưu Processed Data tại: {processed_path} ---")
    
    return processed_path

def load_flight_data(processed_file_path: str, table_name: str = "flight_prices"):
    """
    Task Load: Đọc file đã xử lý và đẩy vào PostgreSQL.
    """
    if not processed_file_path or processed_file_path == "None":
        print("Không có dữ liệu để Load vào DB.")
        return

    print(f"--- Bắt đầu Load vào bảng '{table_name}' ---")

    # 1. Lấy thông tin kết nối từ biến môi trường (đã set trong docker-compose/.env)
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")
    # Lưu ý: host là 'postgres' (tên service trong docker-compose), không phải localhost
    db_host = "postgres" 
    db_port = "5432"

    connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    try:
        # 2. Tạo Engine kết nối
        engine = create_engine(connection_string)
        
        # 3. Đọc dữ liệu từ file CSV
        df = pd.read_csv(processed_file_path)
        
        # 4. Đẩy vào DB
        # if_exists='append': Thêm vào bảng nếu đã có, 'replace': Xóa đi tạo lại
        df.to_sql(table_name, engine, if_exists='append', index=False)
        
        print(f"--- Đã Load thành công {len(df)} dòng vào database! ---")
        
    except Exception as e:
        print(f"--- LỖI khi Load vào DB: {e} ---")
        raise e