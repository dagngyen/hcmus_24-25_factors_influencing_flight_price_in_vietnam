.
├── apps
│   ├── main.py
│   └── pages
├── compose.yml
├── dags
│   └── ingestion_dag.py
├── docker
│   ├── airflow
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── postgres
│   │   └── init.sql
│   └── selenium
├── notebooks
├── README.md
├── requirements.txt
└── src
    ├── etl
    │   └── flight_etl.py
    ├── __init__.py
    ├── kafka
    ├── scrapers
    │   ├── ggflight_scraper.py
    │   └── __init__.py
    └── utils
        └── db_client.py