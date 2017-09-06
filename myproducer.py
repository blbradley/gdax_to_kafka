import os
import sys
import json
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

bootstrap_servers = os.environ['KAFKA_BOOTSTRAP_SERVERS']
schema_registry_url = os.environ['KAFKA_SCHEMA_REGISTRY_URL']

key_schema = avro.loads(json.dumps({'type': 'string'}))
value_schema = avro.load('websocket-raw.avsc')

producer = AvroProducer({
        'bootstrap.servers': bootstrap_servers,
        'schema.registry.url': schema_registry_url,
        'request.required.acks': 'all',
        'retries': 10000000,
        'max.in.flight.requests.per.connection': 1,
    },
    default_key_schema=key_schema,
    default_value_schema=value_schema,
)
