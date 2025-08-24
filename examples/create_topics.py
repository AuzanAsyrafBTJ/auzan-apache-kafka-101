from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

def create_topics():
    admin_client = KafkaAdminClient(
        bootstrap_servers='localhost:9092',
        client_id='topic-creator'
    )
    
    topic_list = [
        NewTopic(name='raw-events', num_partitions=3, replication_factor=1),
        NewTopic(name='transformed-events', num_partitions=3, replication_factor=1),
        NewTopic(name='error-events', num_partitions=1, replication_factor=1)
    ]
    
    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print("Topics created successfully!")
    except TopicAlreadyExistsError:
        print("Topics already exist!")
    except Exception as e:
        print(f"Error creating topics: {e}")
    finally:
        admin_client.close()

if __name__ == "__main__":
    create_topics()
