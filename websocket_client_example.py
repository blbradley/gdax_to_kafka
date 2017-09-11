import logging
from datetime import datetime
import json
import websocket

from gdax import create_raw
from myproducer import producer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def on_message(ws, message):
    dt = datetime.utcnow()
    logging.debug('received websocket message: {}'.format(message))

    value = create_raw(dt, message)
    if value['type'] == 'subscriptions':
        logging.info('received subscription response: {}'.format(message))
        return

    producer.produce(
        topic='websocket_client-gdax',
        value=value,
        key=producer.uuid.bytes,
    )
    producer.poll(0)

def on_error(ws, error):
    logging.warning(error)

def on_close(ws):
    logging.warning("### closed ###")

msg = json.dumps({
    'type': 'subscribe',
    'product_ids':['BTC-USD'],
    'channels': ['ticker', 'level2'],
})

def on_open(ws):
    ws.send(msg)
    logging.debug('sent websocket message: {}'.format(msg))

if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws-feed.gdax.com",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()
