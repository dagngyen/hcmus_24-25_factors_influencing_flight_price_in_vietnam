import json
import os
from kafka import KafkaConsumer

class FlightKafkaConsumer:
    def __init__(self, topic: str, group_id: str = 'flight_group'):
        bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest', # Đọc từ đầu nếu là consumer mới
            enable_auto_commit=True,
            group_id=group_id,
            # Deserialize JSON về dict
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def consume_once(self, timeout_ms=10000):
        """
        Hàm này dùng cho Airflow: Chỉ chờ nhận 1 message hoặc 1 batch rồi thoát.
        Tránh việc Airflow task chạy mãi mãi (infinite loop).
        """
        print(f"--- [KAFKA] Polling messages from topic... ---")
        try:
            # poll trả về dict: {TopicPartition: [List of Records]}
            messages = self.consumer.poll(timeout_ms=timeout_ms)
            
            if not messages:
                print("--- [KAFKA] No new messages found within timeout. ---")
                return []
            
            # Làm phẳng danh sách messages
            result_msgs = []
            for partition, msgs in messages.items():
                for msg in msgs:
                    result_msgs.append(msg.value)
            
            return result_msgs
            
        except Exception as e:
            print(f"--- [KAFKA ERROR] Consumer error: {e} ---")
            return []
    
    def close(self):
        self.consumer.close()