import logging
import json

from avro import schema
from apscheduler.schedulers.background import BlockingScheduler
from confluent_kafka import avro
import requests

# monkey patch schema hash functions
def hash_func(self):
    return(hash(str(self)))

schema.ArraySchema.__hash__ = hash_func

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

key_schema = avro.loads(json.dumps({'type': 'string'}))

def produce_book():
    from myproducer import producer
    r = requests.get('https://api.gdax.com/products/BTC-USD/book?level=3')
    value = r.json()
    value_schema = avro.load('schemas/polling-level3.avsc')
    producer.produce(
        topic='gdax-polling-book',
        value=value,
        key=str(producer.uuid),
        key_schema=key_schema,
        value_schema=value_schema,
    )
    producer.poll(0)

def produce_ticker():
    from myproducer import producer
    r = requests.get('https://api.gdax.com/products/BTC-USD/ticker')
    value = r.json()
    value_schema = avro.load('schemas/polling-ticker.avsc')
    producer.produce(
        topic='gdax-polling-ticker',
        value=value,
        key=str(producer.uuid),
        key_schema=key_schema,
        value_schema=value_schema,
    )
    producer.poll(0)

def produce_trades():
    from myproducer import producer
    r = requests.get('https://api.gdax.com/products/BTC-USD/trades')
    value = r.json()
    value_schema = avro.load('schemas/polling-trades.avsc')
    producer.produce(
        topic='gdax-polling-trades',
        value=value,
        key=str(producer.uuid),
        key_schema=key_schema,
        value_schema=value_schema,
    )
    producer.poll(0)

if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_executor('processpool')
    sched.add_job(produce_book, 'interval', seconds=10)
    sched.add_job(produce_ticker, 'interval', seconds=1)
    sched.add_job(produce_trades, 'interval', seconds=1)

    try:
        sched.start()
    except KeyboardInterrupt:
        pass
