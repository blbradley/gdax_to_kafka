import os
import json

enable_level2 = os.getenv('GDAX_ENABLE_LEVEL2', '1') == '1'
enable_level3 = os.getenv('GDAX_ENABLE_LEVEL3', '0') == '1'

channels = ['ticker']

if enable_level2:
  channels += ['level2']
if enable_level3:
  channels += ['full']

subscription_message = {
    'type': 'subscribe',
    'product_ids': ['BTC-USD'],
    'channels': channels,
}

def create_raw(dt, producer_uuid, data):
    data_dict = json.loads(data)
    extra = {'time_collected': dt.isoformat(), 'producerUUID': producer_uuid.bytes}
    raw = {**extra, **data_dict}
    return raw
