import os
import json

enable_level2 = os.getenv('GDAX_ENABLE_LEVEL2', '1')
enable_level3 = os.getenv('GDAX_ENABLE_LEVEL3', '0')

channels = ['ticker']

if enable_level2 is not '0':
  channels += ['level2']
if enable_level3 is not '0':
  channels += ['full']

subscription_message = {
    'type': 'subscribe',
    'product_ids': ['BTC-USD'],
    'channels': channels,
}

print(subscription_message)

def create_raw(dt, producer_uuid, data):
    data_dict = json.loads(data)
    extra = {'timestamp': dt.isoformat(), 'producerUUID': producer_uuid.bytes}
    raw = {**extra, **data_dict}
    return raw
