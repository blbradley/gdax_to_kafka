#!/usr/bin/env python

import uuid
from datetime import datetime
import asyncio
import websockets

from myproducer import producer

producer_uuid = uuid.uuid4()

async def handler(websocket):
    while True:
        msg = await websocket.recv()
        value = {'timestamp': str(datetime.utcnow()), 'producerUUID': str(producer_uuid), 'data': msg}
        producer.produce(
            topic='websockets-gdax',
            value=value,
            key=str(producer_uuid),
        )
        producer.poll(0)

async def main():
    async with websockets.connect('wss://ws-feed.gdax.com') as websocket:
        msg = """{"type": "subscribe","product_ids":["BTC-USD"]}"""
        await websocket.send(msg)
        await handler(websocket)

if __name__ == "__main__":
   asyncio.get_event_loop().run_until_complete(main())
