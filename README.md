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

- Access the Kafka UI at http://localhost:8080


# Kafka Python Client (Simple Producer & Consumer)

- Install the dependencies
    ```
    pip install -r requirements.txt
    ```

- Run the producer
    ```
    python examples/main.py producer
    ```

- Run the consumer
    ```
    python examples/main.py consumer test-group-python
    ```
