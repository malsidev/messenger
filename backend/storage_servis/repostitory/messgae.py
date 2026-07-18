import asyncio
from uuid import uuid4
from datetime import datetime

from cassandra_client import cassandra


QUERY = """
INSERT INTO messages (
    chat_id,
    id,
    text,
    sender_id,
    sender_name,
    created_at
)
VALUES (?, ?, ?, ?, ?, ?)
"""

prepared = cassandra.session.prepare(QUERY)


async def create_message(
    chat_id,
    id,
    text,
    sender_id,
    sender_name,
    created_at
):
    # Парсим created_at если это строка (ISO format из JSON)
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))

    await asyncio.to_thread(
        cassandra.session.execute,
        prepared,
        (
            chat_id,
            id,
            text,
            sender_id,
            sender_name,
            created_at
        ),
    )

    return {
        "id": str(id),
        "text": text,
        "created_at": created_at.isoformat(),
    }