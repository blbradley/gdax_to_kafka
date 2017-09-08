#!/usr/bin/env python

import uuid
from datetime import datetime
import asyncio
import websockets

from gdax import create_raw
from myproducer import producer

async def handler(websocket):
    while True:
        msg = await websocket.recv()
        dt = datetime.utcnow()
        value = create_raw(dt, msg)
        producer.produce(
            topic='websockets-gdax',
            value=value,
            key=producer.uuid.bytes,
        )
        producer.poll(0)

async def main():
    async with websockets.connect('wss://ws-feed.gdax.com') as websocket:
        msg = """{"type": "subscribe","product_ids":["BTC-USD"]}"""
        await websocket.send(msg)
        await handler(websocket)

if __name__ == "__main__":
   asyncio.get_event_loop().run_until_complete(main())
