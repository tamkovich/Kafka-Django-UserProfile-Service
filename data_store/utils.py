import os
import socket

from confluent_kafka import (
    Producer,
    Consumer,
)


def get_producer() -> Producer:
    return Producer({
        'bootstrap.servers': f'{os.environ["KAFKA_HOST"]}:{os.environ["KAFKA_PORT"]}',
        'client.id': socket.gethostname(),
    })


def get_consumer() -> Consumer:
    return Consumer({
        'bootstrap.servers': f'{os.environ["KAFKA_HOST"]}:{os.environ["KAFKA_PORT"]}',
        'group.id': "user-topic",
        'auto.offset.reset': 'smallest',
    })
