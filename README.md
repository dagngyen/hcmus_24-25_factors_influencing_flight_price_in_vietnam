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
├── Orchestration
│   └── 🎼 Apache Airflow
│       └── 📜 ETL DAG (pipeline)
│           ├── 1. Task: Extract (Gọi Crawler Service)
│           ├── 2. Task: Transform (Gọi Processing Service)
│           └── 3. Task: Load (Gọi SQL Loader Service)
│
├── Services
│   ├── 🤖 Crawler Service (logic crawl)
│   ├── 🔄 Data Processing Service (logic transform)
│   └── 📥 SQL Loader Service (logic load DB)
│
├── Storage Layer
│   └── 🗄️ Database
│
├── Application
│   ├── 📡 Backend API Service
│   └── 💻 Frontend Application
│
├── Infrastructure
│   └── 🐳 Docker / ⚙️ Kubernetes
│
└── 📜README.md
```

## **How to set up**