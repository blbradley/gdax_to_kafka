import logging
import json

from apscheduler.schedulers.background import BlockingScheduler
from confluent_kafka import avro
import requests

from myproducer import producer


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sched = BlockingScheduler()

key_schema = avro.loads(json.dumps({'type': 'string'}))

def my_job():
    logging.warning('foo')
    r = requests.get('https://api.gdax.com/products/BTC-USD/ticker')
    print(r.json())
    value = str(r.json())
    producer.produce(
        topic='gdax-polling',
        value=value,
        key=str(producer.uuid),
        key_schema=key_schema,
        value_schema=key_schema,
    )
    producer.poll(0)

sched.add_job(my_job, 'interval', seconds=1)
sched.start()
