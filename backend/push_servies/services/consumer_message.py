import asyncio
import json
import logging

from kafka_client import get_consumer
from websocket.manager import manager



async def consume_messages():
    consumer = get_consumer()

    async for msg in consumer:
        data = json.loads(
            msg.value.decode()
        )

        await manager.send(
            data["receiver_id"],
            data
        )