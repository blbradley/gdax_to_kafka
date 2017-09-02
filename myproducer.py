import os
import sys
from confluent_kafka.avro import AvroProducer

bootstrap_servers = os.environ['KAFKA_BOOTSTRAP_SERVERS']
schema_registry_url = os.environ['KAFKA_SCHEMA_REGISTRY_URL']

producer = AvroProducer({
    'bootstrap.servers': bootstrap_servers,
    'schema.registry.url': schema_registry_url,
    'request.required.acks': 'all',
    'retries': 10000000,
    'max.in.flight.requests.per.connection': 1,
})
