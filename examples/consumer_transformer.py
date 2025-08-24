from kafka import KafkaConsumer, KafkaProducer
import json
import logging
import random
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsumerTransformer:
    def __init__(self, bootstrap_servers='localhost:9092'):  # Changed to 9092
        self.consumer = KafkaConsumer(
            'raw-events',
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='transformer-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            key_deserializer=lambda x: x.decode('utf-8') if x else None
        )
        
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    
    def transform_message(self, message):
        """Apply transformations to the consumed message"""
        transformed = message.copy()
        
        # Add processing metadata
        transformed['processed_timestamp'] = datetime.utcnow().isoformat()
        transformed['processing_stage'] = 'transformed'
        
        # Apply transformations based on event type
        if message['event_type'] == 'user_activity':
            # Enrich user activity data
            transformed['data_quality'] = 'high'
            transformed['is_bot'] = False
            if 'session_duration' in transformed:
                transformed['session_minutes'] = round(transformed['session_duration'] / 60, 2)
            
        elif message['event_type'] == 'system_metric':
            # Add severity level for system metrics
            value = transformed.get('value', 0)
            if value > 90:
                transformed['severity'] = 'critical'
            elif value > 70:
                transformed['severity'] = 'warning'
            else:
                transformed['severity'] = 'normal'
                
        elif message['event_type'] == 'payment':
            # Normalize currency and add fraud risk score
            transformed['currency'] = transformed['currency'].upper()
            transformed['fraud_risk_score'] = round(random.uniform(0, 1), 2)
            if transformed['amount'] > 500:
                transformed['requires_review'] = True
        
        return transformed
    
    def process_messages(self):
        """Consume, transform, and produce messages"""
        logger.info("Starting consumer transformer...")
        
        try:
            for message in self.consumer:
                try:
                    # Transform the message
                    transformed = self.transform_message(message.value)
                    
                    # Send to new topic
                    self.producer.send(
                        'transformed-events',
                        value=transformed
                    )
                    
                    logger.info(f"Transformed and sent message: {transformed['event_type']}")
                    
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    # Send to error topic
                    error_message = {
                        'original_message': message.value,
                        'error': str(e),
                        'timestamp': datetime.utcnow().isoformat()
                    }
                    self.producer.send('error-events', value=error_message)
                    
        except KeyboardInterrupt:
            logger.info("Shutting down consumer transformer...")
        finally:
            self.consumer.close()
            self.producer.close()

if __name__ == "__main__":
    transformer = ConsumerTransformer(bootstrap_servers='localhost:9092')  # Use port 9092
    transformer.process_messages()
