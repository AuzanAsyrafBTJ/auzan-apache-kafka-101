# Kafka Python Client (Simple Producer & Consumer with transformation)

- Clone the repo
    ```
    git clone https://github.com/AuzanAsyrafBTJ/auzan-apache-kafka-101.git
    ```

- Create virtual environment
    ```
    python3 -m venv myenv
    ```
    
- Resolve permission
    ```
    sudo chown -R 1001:1001 ./dockervol/kafka
    ```
    
- Start Your Docker Containers
    ```
    docker-compose up -d
    ```
    
- Install the dependencies
    ```
    pip install kafka-python
    ```
    
- Create Topics
    ```
    python examples/create_topics.py
    ```
    
- Run Data Generator (Terminal 1)
    ```
    python examples/data_generator.py
    ```

- Run Consumer Transformer (Terminal 2)
    ```
    python examples/consumer_transformer.py
    ```
- Access the Kafka UI at http://localhost:8080 to check the pipeline results
  
- What all of these do
  ```
  A complete Kafka data pipeline demonstrating message production, consumption, transformation, and streaming.
  This project implements a complete data pipeline using Apache Kafka with:
  Data Generator: Produces sample messages with different schemas
  Kafka Topics: Partitioned topics for raw and transformed data
  Consumer Transformer: Processes and enriches messages
  Docker Setup: Containerized Kafka infrastructure
  ```
- Data flow
  ```
  1. Raw Events → raw-events topic (3 partitions)
  2. Transformation → Consumer processes and enriches data
  3. Transformed Events → transformed-events topic
  4. Errors → error-events topic (if any)
  ```
- Configuration
  ```
  - Kafka Broker: localhost:9092
  - Kafka UI: http://localhost:8080
  - Topics: raw-events, transformed-events, error-events
  ```
