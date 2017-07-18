#!/usr/bin/env python

import asyncio
import websockets

from myproducer import producer

async def handler(websocket):
    while True:
        msg = await websocket.recv()
        future = producer.send('gdax', msg.encode('utf-8'))
        result = future.get(timeout=10)

async def main():
    async with websockets.connect('wss://ws-feed.gdax.com') as websocket:
        msg = """{"type": "subscribe","product_ids":["BTC-USD"]}"""
        await websocket.send(msg)
        await handler(websocket)

if __name__ == "__main__":
   asyncio.get_event_loop().run_until_complete(main())
