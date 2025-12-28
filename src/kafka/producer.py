import json
import os
from kafka import KafkaProducer
from datetime import datetime

class FlightKafkaProducer:
    def __init__(self):
        # Lấy địa chỉ Kafka từ biến môi trường (đã set trong docker-compose)
        # Mặc định là flight_kafka:29092 nếu chạy trong docker
        bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            # Serialize dữ liệu thành JSON trước khi gửi
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            # Encode key (nếu có)
            key_serializer=lambda v: v.encode('utf-8') if v else None
        )

    def send_event(self, topic: str, event_type: str, payload: dict):
        """
        Gửi một sự kiện lên Kafka
        :param topic: Tên topic (VD: 'flight_ingestion')
        :param event_type: Loại sự kiện (VD: 'DATA_EXTRACTED')
        :param payload: Dữ liệu đính kèm (VD: ngày bắt đầu, ngày kết thúc, số lượng record)
        """
        message = {
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "payload": payload
        }
        
        try:
            # Gửi message (bất đồng bộ)
            future = self.producer.send(topic, value=message)
            # Chờ xác nhận từ Kafka Broker để đảm bảo không mất tin
            result = future.get(timeout=10)
            print(f"--- [KAFKA] Sent to {result.topic} partition {result.partition} offset {result.offset} ---")
        except Exception as e:
            print(f"--- [KAFKA ERROR] Failed to send message: {e} ---")

    def close(self):
        self.producer.close()