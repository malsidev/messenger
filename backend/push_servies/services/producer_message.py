from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import json
from uuid import uuid4
from datetime import datetime, timezone
import uuid

from kafka_client import get_producer


async def producer_message(chat_id, text, sender_id, sender_name, receiver_id):
    print(f'в продусере вот такие данные {chat_id}, {text}, {sender_id}, {sender_name}')
    producer = get_producer()
    try:
        # Добавляем id и нормализуем created_at
        created_at = datetime.now(timezone.utc)
        message_id = uuid.uuid4()
        payload = {
            "id": str(message_id),
            "chat_id": chat_id,
            "text": text,
            "sender_id": sender_id,
            "sender_name": sender_name,
            "receiver_id": receiver_id,
            "created_at": created_at.isoformat()
        }
        
        await producer.send_and_wait(
            "message",
            json.dumps(payload, ensure_ascii=False).encode("utf-8")
        )
        
        return {"status": "sent", "id": str(message_id)}
    
    except Exception as e:
        print(f"Error sending message: {e}")
        return {'error': str(e)}


