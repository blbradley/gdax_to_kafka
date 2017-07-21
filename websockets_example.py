#!/usr/bin/env python

import uuid
import asyncio
import websockets

from myproducer import producer

producer_uuid = uuid.uuid4()

async def handler(websocket):
    while True:
        msg = await websocket.recv()
        future = producer.send('gdax', msg.encode('utf-8'), producer_uuid.bytes)
        result = future.get(timeout=10)

async def main():
    async with websockets.connect('wss://ws-feed.gdax.com') as websocket:
        msg = """{"type": "subscribe","product_ids":["BTC-USD"]}"""
        await websocket.send(msg)
        await handler(websocket)

if __name__ == "__main__":
   asyncio.get_event_loop().run_until_complete(main())
