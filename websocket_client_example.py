import logging
from datetime import datetime
import websocket

from myproducer import producer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def on_message(ws, message):
    value = {'timestamp': str(datetime.utcnow()), 'producerUUID': producer.uuid.bytes, 'data': message}
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
