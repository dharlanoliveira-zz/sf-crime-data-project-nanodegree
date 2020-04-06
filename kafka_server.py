import producer_server


def run_kafka_server():
    zip_file = "police-department-calls-for-service.zip"
    input_file = "police-department-calls-for-service.json"

    producer = producer_server.ProducerServer(
        zip_file=zip_file,
        input_file=input_file,
        topic="udacity.sf-crime-data",
        bootstrap_servers=" localhost:9092 ",
        client_id="sf-crime-producer"
    )

    return producer


def feed():
    producer = run_kafka_server()
    producer.generate_data()


if __name__ == "__main__":
    feed()
