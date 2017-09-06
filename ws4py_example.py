import logging
import uuid
from datetime import datetime

from ws4py.client.threadedclient import WebSocketClient

from myproducer import producer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

producer_uuid = uuid.uuid4()

class DummyClient(WebSocketClient):
    def opened(self):
        def data_provider():
            msg = """{"type": "subscribe","product_ids":["BTC-USD"]}"""
            return msg

        self.send(data_provider())

    def closed(self, code, reason=None):
        logging.warning("Closed down", code, reason)

    def received_message(self, m):
        value = {'timestamp': str(datetime.utcnow()), 'producerUUID': str(producer_uuid), 'data': str(m)}
        producer.produce(
            topic='ws4py-gdax',
            value=value,
            key=str(producer_uuid),
        )
        producer.poll(0)

if __name__ == '__main__':
    try:
        ws = DummyClient("wss://ws-feed.gdax.com")
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
