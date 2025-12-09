from src.scrapers.ggflight_scraper import GGFlightScraper
from src.utils.db_client import PostgresClient
import pandas as pd
from datetime import datetime, timedelta

def run_pipeline():
    # 1. Định nghĩa tham số crawl
    departures = ['SGN']
    arrivals = ['HAN']
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    
    # 2. Gọi Scraper
    print("Running Scraper...")
    df = GGFlightScraper(None, departures, arrivals, start_date, end_date, ['Economy', 'Business'])
    
    # 3. Lưu vào DB
    if df is not None and not df.empty:
        # Xử lý data sơ bộ (convert types)
        df['price'] = pd.to_numeric(df['price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        db = PostgresClient()
        db.load_data(df, 'flight_prices')
    else:
        print("No data found.")