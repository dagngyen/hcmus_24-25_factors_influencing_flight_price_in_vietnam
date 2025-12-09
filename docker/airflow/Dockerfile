FROM apache/airflow:2.7.1-python3.9

USER root
# Cài thêm các gói hệ thống nếu cần (ví dụ driver cho postgres)
RUN apt-get update && apt-get install -y libpq-dev gcc

USER airflow
# Copy file requirements nếu bạn có, hoặc cài trực tiếp
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir pandas selenium sqlalchemy psycopg2-binary