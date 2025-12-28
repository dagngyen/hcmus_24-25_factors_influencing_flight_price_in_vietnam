.
├── airflow
│   ├── dags
│   │   └── ingestion_dag.py
│   ├── Dockerfile
│   └── requirement.txt
├── app
│   ├── main.py
│   ├── pages
│   └── requirements.txt
├── compose.yml
├── database
│   └── postgres
│       └── init.sql
├── notebooks
├── README.md
├── requirements.txt
└── src
    ├── database
    │   ├── db_client.py
    │   └── __init__.py
    ├── etl
    │   ├── __init__.py
    │   └── pipeline.py
    ├── __init__.py
    ├── kafka
    └── scraping
        ├── ggflight_scraper.py
        └── __init__.py
