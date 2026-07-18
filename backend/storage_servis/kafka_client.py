


import asyncio
import json
import logging
import os
from uuid import UUID

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from repostitory.messgae import create_message


logging.basicConfig(level=logging.INFO)


async def create_consumer():
    while True:
        try:
            consumer = AIOKafkaConsumer(
                "message",
                bootstrap_servers=os.getenv(
                    "KAFKA_BOOTSTRAP_SERVERS",
                    "kafka:9092",
                ),
                group_id="storage-service",
                auto_offset_reset="earliest",
                enable_auto_commit=False,
            )

            await consumer.start()
            print(consumer)
            return consumer

        except KafkaConnectionError:
            logging.warning("Kafka unavailable...")
            await asyncio.sleep(3)


async def consume():
    consumer = await create_consumer()

    try:
        async for msg in consumer:
            print("KAFKA MESSAGE:", msg.value)
            try:
                data = json.loads(msg.value.decode())

                await create_message(
                    chat_id=data["chat_id"],
                    id=UUID(data["id"]),
                    text=data["text"],
                    sender_id=data["sender_id"],
                    sender_name=data["sender_name"],
                    created_at=data["created_at"],
                )

                await consumer.commit()

                logging.info("Message saved")

            except Exception:
                logging.exception("Error while saving message")

    finally:
        await consumer.stop()

