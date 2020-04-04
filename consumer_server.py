from kafka import KafkaConsumer
from json import loads


def consume():
    consumer = KafkaConsumer(
        'udacity.nanodegree.sf.crime-data',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        group_id='consumer-sf-crime',
        value_deserializer=lambda x: loads(x.decode()))

    for message in consumer:
        message = message.value
        print('message received {}'.format(message))


if __name__ == "__main__":
    consume()
