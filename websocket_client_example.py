import uuid
import logging
import json
from datetime import datetime
from confluent_kafka import avro
import websocket

from myproducer import producer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

producer_uuid = uuid.uuid4()
key_schema = avro.loads(json.dumps({'type': 'string'}))
value_schema = avro.load('websocket-raw.avsc')

def on_message(ws, message):
    value = {'timestamp': str(datetime.utcnow()), 'producerUUID': str(producer_uuid), 'data': message}
    producer.produce(
        topic='websocket_client-gdax',
        value=value,
        value_schema=value_schema,
        key=str(producer_uuid),
        key_schema=key_schema,
    )

def on_error(ws, error):
    logging.warning(error)

def on_close(ws):
    logging.warning("### closed ###")

msg = """{"type": "subscribe","product_ids":["BTC-USD"]}"""

def on_open(ws):
    ws.send(msg)

if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws-feed.gdax.com",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()
