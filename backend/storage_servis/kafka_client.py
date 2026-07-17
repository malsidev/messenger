import asyncio
import logging
import os
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


async def create_consumer():
    while True:
        try:
            consumer = AIOKafkaConsumer(
                "message",
                bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
                group_id=os.getenv("KAFKA_CONSUMER_GROUP", "storage-service"),
                auto_offset_reset="earliest",
                enable_auto_commit=False,
            )

            logging.info("Starting consumer...")
            await consumer.start()
            await consumer.seek_to_beginning()
            logging.info("Consumer started")
            return consumer

        except KafkaConnectionError as e:
            logging.warning("Kafka is not available: %s", e)
            await asyncio.sleep(3)


async def consume():
    consumer = await create_consumer()

    try:
        async for msg in consumer:
            logging.info("Received: %s", msg.value.decode())
            await consumer.commit()
    finally:
        await consumer.stop()

