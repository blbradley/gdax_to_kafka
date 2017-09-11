import logging
import uuid
from datetime import datetime
import json

from ws4py.client.threadedclient import WebSocketClient

from gdax import create_raw, subscription_message
from myproducer import producer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DummyClient(WebSocketClient):
    def opened(self):
        def data_provider():
            return json.dumps(subscription_message)

        self.send(data_provider())

    def closed(self, code, reason=None):
        logging.warning("Closed down", code, reason)

    def received_message(self, m):
        dt = datetime.utcnow()
        value = create_raw(dt, str(m))
        producer.produce(
            topic='ws4py-gdax',
            value=value,
            key=producer.uuid.bytes,
        )
        producer.poll(0)

if __name__ == '__main__':
    try:
        ws = DummyClient("wss://ws-feed.gdax.com")
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
