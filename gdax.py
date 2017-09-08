from myproducer import producer

def create_raw(dt, data):
    raw = {'timestamp': str(dt), 'producerUUID': producer.uuid.bytes, 'data': data}
    return raw
