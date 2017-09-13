import logging
import json

from apscheduler.schedulers.background import BlockingScheduler
from confluent_kafka import avro
import requests

from myproducer import producer


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sched = BlockingScheduler()

key_schema = avro.loads(json.dumps({'type': 'string'}))

baseurl = 'https://api.gdax.com/products/BTC-USD/'

type_to_topic = {
    'ticker': 'gdax-polling-ticker',
    'trades': 'gdax-polling-trades',
}

def my_job(type):
    r = requests.get(f'{baseurl}{type}')
    value = str(r.json())
    producer.produce(
        topic=type_to_topic[type],
        value=value,
        key=str(producer.uuid),
        key_schema=key_schema,
        value_schema=key_schema,
    )
    producer.poll(0)

sched.add_job(my_job, 'interval', ('ticker', ), seconds=2)
sched.add_job(my_job, 'interval', ('trades', ), seconds=2)
sched.start()
