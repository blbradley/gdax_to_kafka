import json

from myproducer import producer

def create_raw(dt, data):
    data_dict = json.loads(data)
    extra = {'timestamp': dt.isoformat(), 'producerUUID': producer.uuid.bytes}
    raw = {**extra, **data_dict}
    return raw
