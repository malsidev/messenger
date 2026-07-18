from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio


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


async def start_kafka():

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


async def stop_kafka():

    if kafka.consumer_task:
        kafka.consumer_task.cancel()

    if kafka.consumer:
        await kafka.consumer.stop()

    if kafka.producer:
        await kafka.producer.stop()


    print("Kafka stopped")

def get_producer() -> AIOKafkaProducer:
    if kafka.producer is None:
        raise RuntimeError("Producer not initialized")

    return kafka.producer


def get_consumer() -> AIOKafkaConsumer:
    if kafka.consumer is None:
        raise RuntimeError("Consumer not initialized")

    return kafka.consumer