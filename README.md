# **HCMUS - Intelligent Data Analysis Application**
Group 9: IntelHunter

Project: FLIGHT PRICE ANALYSIS (PHÂN TÍCH CÁC YẾU TỐ ẢNH HƯỞNG ĐẾN GIÁ VÉ MÁY BAY Ở VIỆT NAM)

Members:
- 20120524: Võ Đức Lợi
- 21120035: Nguyễn Hoài An
- 21120103: Phan Thảo Nguyên
- 21120179: Nguyễn Đặng Đăng Khoa
- 21120546: Nguyễn Thanh Sang

## **Architecture System**
```css
FLIGHT PRICE ANALYSIS
│
├── dags/                           # (Airflow) Nơi chứa các file định nghĩa quy trình (DAGs)
│   ├── ingestion_dag.py
│   └── transformation_dag.py
│
├── src/                            # (Core Logic) Chứa source code chính (ETL, Selenium, Producers)
│   ├── __init__.py
│   ├── scrapers/                   # Code Selenium nằm ở đây
│   │   ├── __init__.py
│   │   └── ggflight_scraper.py
│   ├── kafka_handlers/             # Code Producer/Consumer cho Kafka
│   └── utils/                      # Các hàm tiện ích dùng chung
├── apps/                           # Chứa các ứng dụng người dùng cuối
│   └── dashboard/                  # Thư mục chứa code Streamlit
│       ├── .streamlit/             # Config giao diện (theme, server settings)
│       ├── pages/                  # Các trang con (Multipage app)
│       ├── main.py                 # Entry point của Streamlit
│       └── requirements.txt        # Thư viện riêng cho Streamlit (charts, widgets)
│
├── tests/                          # Unit tests và Integration tests
│   ├── test_scrapers.py
│   └── test_dags.py
│
├── plugins/                        # (Airflow) Các custom operators/hooks của Airflow
│
├── docker/                         # Cấu hình chi tiết cho từng service (Docker)
│   ├── airflow/
│   │   └── Dockerfile              # Custom image cho Airflow (cài thêm selenium driver, java...)
│   ├── postgres/
│   │   └── init.sql                # Script tạo bảng ban đầu khi khởi chạy DB
│   └── selenium/                   # Nếu cần build custom image cho selenium node
│
├── config/                         # Các file cấu hình ứng dụng
│   ├── kafka_config.yaml
│   └── logging_config.ini
│
├── data/                           # (Local Only) Thư mục tạm chứa data khi chạy local
│   ├── raw/
│   └── processed/
│
├── notebooks/                      # Jupyter notebooks để EDA (Exploratory Data Analysis) hoặc test nhanh
│
├── .env                            # Biến môi trường (Credentials, Ports) - KHÔNG push lên git
├── .gitignore                      # File gitignore
├── docker-compose.yml              # File orchestration chính cho toàn bộ hạ tầng
├── README.md                       # Tài liệu hướng dẫn dự án
└── requirements.txt                # Các thư viện Python cần thiết
```

## **How to set up**