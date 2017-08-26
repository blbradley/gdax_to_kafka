import uuid
import logging
import websocket

from myproducer import producer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

producer_uuid = uuid.uuid4()

def on_message(ws, message):
    future = producer.send('gdax', message.encode('utf-8'), producer_uuid.bytes)
    result = future.get(timeout=10)

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
