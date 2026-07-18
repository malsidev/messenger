import asyncio

from aiokafka import (
    AIOKafkaProducer,
    AIOKafkaConsumer
)



class KafkaState:

    def __init__(self):

        self.producer = None
        self.consumer = None



kafka = KafkaState()



async def start_kafka():

    kafka.producer = AIOKafkaProducer(
        bootstrap_servers="kafka:9092"
    )


    kafka.consumer = AIOKafkaConsumer(
        "message",
        bootstrap_servers="kafka:9092",
        group_id="push-service",
        auto_offset_reset="latest"
    )


    await kafka.producer.start()

    await kafka.consumer.start()


    print(
        "Kafka started"
    )



async def stop_kafka():

    if kafka.consumer:

        await kafka.consumer.stop()


    if kafka.producer:

        await kafka.producer.stop()


    print(
        "Kafka stopped"
    )



def get_producer():

    if not kafka.producer:

        raise Exception(
            "Producer not started"
        )


    return kafka.producer



def get_consumer():

    if not kafka.consumer:

        raise Exception(
            "Consumer not started"
        )


    return kafka.consumer