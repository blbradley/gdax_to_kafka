import uuid

from ws4py.client.threadedclient import WebSocketClient

from myproducer import producer

producer_uuid = uuid.uuid4()

class DummyClient(WebSocketClient):
    def opened(self):
        def data_provider():
            msg = """{"type": "subscribe","product_ids":["BTC-USD"]}"""
            return msg

        self.send(data_provider())

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, m):
        future = producer.send('gdax', str(m).encode('utf-8'), producer_uuid.bytes)
        result = future.get(timeout=10)

if __name__ == '__main__':
    try:
        ws = DummyClient("wss://ws-feed.gdax.com")
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
