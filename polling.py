import logging
import json
from datetime import datetime

from avro import schema
from apscheduler.schedulers.background import BlockingScheduler
from confluent_kafka import avro
import requests

import gdax

# monkey patch schema hash functions
def hash_func(self):
    return(hash(str(self)))

schema.ArraySchema.__hash__ = hash_func

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def produce_book(level):
    from myproducer import producer
    r = requests.get(
        f'https://api.gdax.com/products/BTC-USD/book?level={level}',
        timeout=5,
        )
    dt = datetime.utcnow()
    value = r.json()
    value['time_collected'] = dt.isoformat()
    value['producerUUID'] = producer.uuid.bytes
    value_schema = avro.load(f'schemas/polling-level{level}.avsc')
    producer.produce(
        topic=f'gdax-polling-book-level{level}',
        value=value,
        key=producer.uuid.bytes,
        value_schema=value_schema,
    )
    producer.poll(0)

def produce_level2_book():
  produce_book(2)

def produce_level3_book():
  produce_book(3)

def produce_ticker():
    from myproducer import producer
    r = requests.get(
        'https://api.gdax.com/products/BTC-USD/ticker',
        timeout=5,
        )
    dt = datetime.utcnow()
    value = r.json()
    value['time_collected'] = dt.isoformat()
    value['producerUUID'] = producer.uuid.bytes
    value_schema = avro.load('schemas/polling-ticker.avsc')
    producer.produce(
        topic='gdax-polling-ticker',
        value=value,
        key=producer.uuid.bytes,
        value_schema=value_schema,
    )
    producer.poll(0)

def produce_trades():
    from myproducer import producer
    r = requests.get(
        'https://api.gdax.com/products/BTC-USD/trades',
        timeout=5,
        )
    dt = datetime.utcnow()
    trades = r.json()
    value = {'time_collected': dt.isoformat(),  'producerUUID': producer.uuid.bytes, 'data': trades}
    value_schema = avro.load('schemas/polling-trades.avsc')
    producer.produce(
        topic='gdax-polling-trades',
        value=value,
        key=producer.uuid.bytes,
        value_schema=value_schema,
    )
    producer.poll(0)

if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_executor('processpool')
    if gdax.enable_level2:
        sched.add_job(produce_level2_book, 'interval', seconds=60)
    if gdax.enable_level3:
        sched.add_job(produce_level3_book, 'interval', seconds=60)
    sched.add_job(produce_ticker, 'interval', seconds=2)
    sched.add_job(produce_trades, 'interval', seconds=2)

    try:
        sched.start()
    except KeyboardInterrupt:
        pass
