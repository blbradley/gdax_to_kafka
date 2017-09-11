import json

from myproducer import producer


subscription_message = {
    'type': 'subscribe',
    'product_ids': ['BTC-USD'],
    'channels': ['ticker', 'level2'],
}

def create_raw(dt, data):
    data_dict = json.loads(data)
    extra = {'timestamp': dt.isoformat(), 'producerUUID': producer.uuid.bytes}
    raw = {**extra, **data_dict}
    return raw
