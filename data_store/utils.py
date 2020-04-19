import json
import os

from kafka import (
    KafkaProducer,
    KafkaConsumer,
)

from django.core.serializers.json import DjangoJSONEncoder


def get_producer():
    return KafkaProducer(
        bootstrap_servers=[
            f'{os.environ["KAFKA_HOST"]}:{os.environ["KAFKA_PORT"]}',
        ],
        value_serializer=lambda item: json.dumps(
            item,
            cls=DjangoJSONEncoder,
        ).encode('ascii'),
    )


def get_consumer():
    return KafkaConsumer(
        'profile-topic',
        bootstrap_servers=[
            f'{os.environ["KAFKA_HOST"]}:{os.environ["KAFKA_PORT"]}',
        ],
        value_deserializer=lambda item: json.loads(item),
    )
