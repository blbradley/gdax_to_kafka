import json
from myproducer import producer

def create_raw(dt, data):
    extra = {'time_collected': str(dt), 'producerUUID': producer.uuid.bytes}
    raw = {**json.loads(data), **extra}
    return raw
