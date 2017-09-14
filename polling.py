import logging
import json

from apscheduler.schedulers.background import BlockingScheduler
from confluent_kafka import avro
import requests

from myproducer import producer


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sched = BlockingScheduler()

key_schema = avro.loads(json.dumps({'type': 'string'}))

def produce_ticker():
    r = requests.get('https://api.gdax.com/products/BTC-USD/ticker')
    value = str(r.json())
    producer.produce(
        topic='gdax-polling-ticker',
        value=value,
        key=str(producer.uuid),
        key_schema=key_schema,
        value_schema=key_schema,
    )
    producer.poll(0)

def produce_trades():
    r = requests.get('https://api.gdax.com/products/BTC-USD/trades')
    value = str(r.json())
    producer.produce(
        topic='gdax-polling-trades',
        value=value,
        key=str(producer.uuid),
        key_schema=key_schema,
        value_schema=key_schema,
    )
    producer.poll(0)


sched.add_job(produce_ticker, 'interval', seconds=2)
sched.add_job(produce_trades, 'interval', seconds=2)
sched.start()
