from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter
import json
from kafka.admin import KafkaAdminClient, NewTopic
from kafka_client import kafka
from schemas.messages import Message
from services.producer_message import  producer_message
router = APIRouter(tags=['/message'])

@router.post("/message")
async def message(data: Message):
    res = await producer_message(data)
    return res














@router.get("/messages")
async def get_messages():

    consumer = AIOKafkaConsumer(
        "message",
        bootstrap_servers="kafka:9092",
        group_id=None,              # временный consumer
        auto_offset_reset="earliest",
        enable_auto_commit=False,
    )

    await consumer.start()

    messages = []

    try:
        while True:
            result = await consumer.getmany(timeout_ms=1000)

            if not result:
                break

            for _, msgs in result.items():
                for msg in msgs:
                    try:
                        value = json.loads(msg.value.decode())
                    except Exception:
                        value = msg.value.decode()

                    messages.append({
                        "offset": msg.offset,
                        "partition": msg.partition,
                        "timestamp": msg.timestamp,
                        "value": value,
                    })

    finally:
        await consumer.stop()

    return messages


@router.delete("/message")
async def clear_topic():
    admin = KafkaAdminClient(
        bootstrap_servers="kafka:9092",
        client_id="debug-admin",
    )

    try:
        admin.delete_topics(["message"])
        admin.create_topics([
            NewTopic(
                name="message",
                num_partitions=1,
                replication_factor=1,
            )
        ])

        return {"message": "Topic recreated"}

    finally:
        admin.close()