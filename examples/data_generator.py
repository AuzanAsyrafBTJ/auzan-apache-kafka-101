from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataGenerator:
    def __init__(self, bootstrap_servers='localhost:9092'):  # Changed to 9092
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: str(v).encode('utf-8') if v else None
        )
        
    def generate_sample_data(self):
        """Generate sample messages with different schemas"""
        events = [
            {
                'event_type': 'user_activity',
                'user_id': random.randint(1, 1000),
                'action': random.choice(['login', 'logout', 'purchase', 'view']),
                'timestamp': datetime.utcnow().isoformat(),
                'device': random.choice(['mobile', 'desktop', 'tablet']),
                'session_duration': random.randint(1, 3600)
            },
            {
                'event_type': 'system_metric',
                'metric_name': random.choice(['cpu_usage', 'memory_usage', 'disk_io']),
                'value': round(random.uniform(0, 100), 2),
                'timestamp': datetime.utcnow().isoformat(),
                'server_id': f'server-{random.randint(1, 10)}'
            },
            {
                'event_type': 'payment',
                'transaction_id': f'txn-{random.randint(10000, 99999)}',
                'amount': round(random.uniform(10, 1000), 2),
                'currency': random.choice(['USD', 'EUR', 'GBP']),
                'status': random.choice(['completed', 'failed', 'pending']),
                'timestamp': datetime.utcnow().isoformat()
            }
        ]
        return random.choice(events)
    
    def produce_messages(self, num_messages=100, delay=0.1):
        """Produce messages to Kafka topic"""
        for i in range(num_messages):
            message = self.generate_sample_data()
            
            # Use user_id or server_id as key for partitioning
            key = message.get('user_id') or message.get('server_id') or message.get('transaction_id')
            
            # Send to partitioned topic
            self.producer.send(
                'raw-events',
                key=key,
                value=message
            )
            
            logger.info(f"Produced message {i+1}: {message}")
            time.sleep(delay)
        
        self.producer.flush()
        logger.info(f"Finished producing {num_messages} messages")

if __name__ == "__main__":
    generator = DataGenerator(bootstrap_servers='localhost:9092')  # Use port 9092
    generator.produce_messages(num_messages=50, delay=0.2)
