from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import json


from kafka_client import  get_producer


async def producer_message(data):
    producer = get_producer()
    try: 
        await producer.send_and_wait(
            "message",
            json.dumps(data, ensure_ascii=False).encode("utf-8")
        )
        return True
    
    except Exception as e: 
        return {'messgae': str(e)}

