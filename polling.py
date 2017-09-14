import logging
import json

from apscheduler.schedulers.background import BlockingScheduler
from confluent_kafka import avro
import requests


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

key_schema = avro.loads(json.dumps({'type': 'string'}))

def produce_ticker():
    from myproducer import producer
    r = requests.get('https://api.gdax.com/products/BTC-USD/ticker')
    value = str(r.json())
    print(value)
    producer.produce(
        topic='gdax-polling-ticker',
        value=value,
        key=str(producer.uuid),
        key_schema=key_schema,
        value_schema=key_schema,
    )
    producer.poll(0)

def produce_trades():
    from myproducer import producer
    r = requests.get('https://api.gdax.com/products/BTC-USD/trades')
    value = str(r.json())
    print(value)
    producer.produce(
        topic='gdax-polling-trades',
        value=value,
        key=str(producer.uuid),
        key_schema=key_schema,
        value_schema=key_schema,
    )
    producer.poll(0)

if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_executor('processpool')
    sched.add_job(produce_ticker, 'interval', seconds=1)
    sched.add_job(produce_trades, 'interval', seconds=1)

    try:
        sched.start()
    except KeyboardInterrupt:
        pass
