# Sử dụng base image chính thức của Airflow (phiên bản Python 3.9 hoặc 3.10 là ổn định nhất)
FROM apache/airflow:2.9.1-python3.9

# Chuyển sang user root để cài đặt các gói hệ thống nếu cần (ví dụ: git, libpq-dev cho postgres)
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential \
         libpq-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Chuyển lại về user airflow để cài đặt thư viện Python
USER airflow

# Copy file requirements.txt từ thư mục gốc vào trong container
# Lưu ý: Context khi build docker-compose sẽ là thư mục gốc dự án
COPY requirements.txt /requirements.txt

# Cài đặt các thư viện Python
# --no-cache-dir để giảm dung lượng image
RUN pip install --no-cache-dir -r /requirements.txt