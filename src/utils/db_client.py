import os
import pandas as pd
from sqlalchemy import create_engine

class PostgresClient:
    def __init__(self):
        # Lấy config từ biến môi trường (được set trong docker-compose)
        user = os.getenv('POSTGRES_USER', 'user')
        password = os.getenv('POSTGRES_PASSWORD', '00000000')
        host = 'postgres' # Tên service trong docker-compose
        db = os.getenv('POSTGRES_DB', 'ggflight')
        port = 5432
        
        self.engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')

    def load_data(self, df, table_name):
        try:
            with self.engine.connect() as conn:
                df.to_sql(table_name, conn, if_exists='append', index=False)
            print(f"✅ Đã lưu {len(df)} dòng vào bảng {table_name}")
        except Exception as e:
            print(f"❌ Lỗi lưu DB: {e}")
            raise e