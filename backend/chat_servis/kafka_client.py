from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
from contextlib import asynccontextmanager

class KafkaState:
    def __init__(self):
        self.producer = None
        self.consumer = None
        self.consumer_task = None

kafka = KafkaState()


async def consume_messages():
    consumer = kafka.consumer

    try:
        async for msg in consumer:
            print(msg.value.decode())
    except asyncio.CancelledError:
        pass


@asynccontextmanager
async def lifespan(app):

    producer = AIOKafkaProducer(
        bootstrap_servers="kafka:9092"
    )

    consumer = AIOKafkaConsumer(
        "message",
        bootstrap_servers="kafka:9092",
        group_id="my-group",
        auto_offset_reset="earliest",
    )

    await producer.start()
    await consumer.start()

    kafka.producer = producer
    kafka.consumer = consumer

    kafka.consumer_task = asyncio.create_task(
        consume_messages()
    )

    print("Kafka started")

    try:
        yield

    finally:
        kafka.consumer_task.cancel()

        await consumer.stop()
        await producer.stop()

        print("Kafka stopped")

def get_producer() -> AIOKafkaProducer:
    if kafka.producer is None:
        raise RuntimeError("Producer not initialized")

    return kafka.producer