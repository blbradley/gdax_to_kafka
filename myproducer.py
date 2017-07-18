import os
import sys
from kafka import KafkaProducer

bootstrap_servers = os.environ['KAFKA_BOOTSTRAP_SERVERS']
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    acks='all',
    retries=sys.maxsize,
    max_block_ms=sys.maxsize,
    max_in_flight_requests_per_connection=1,
    )
