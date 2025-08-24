# How to Run

- Clone the repo
    ```
    git clone https://github.com/ammfat/apache-kafka-101.git
    ```

- Start the docker containers
    ```
    docker-compose up -d
    docker ps
    ```

    Ensure the containers are running


# Kafka Python Client (Simple Producer & Consumer)

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
