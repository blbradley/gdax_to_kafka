from myproducer import producer

def create_raw(dt, data):
    raw = {'timestamp': dt.isoformat(), 'producerUUID': producer.uuid.bytes, 'data': data}
    return raw
