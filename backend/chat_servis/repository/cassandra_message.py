from cassandra_client import cassandra
import asyncio


async def get_messages_chat(chat_id):

    query = """
    SELECT *
    FROM messages
    WHERE chat_id = ?
    ORDER BY created_at ASC
    """

    prepared = cassandra.session.prepare(query)

    loop = asyncio.get_running_loop()

    result = await loop.run_in_executor(
        None,
        lambda: cassandra.session.execute(
            prepared,
            [chat_id]
        )
    )

    messages = []

    for row in result:
        messages.append({
            "id": row.id,
            "sender_id": row.sender_id,
            "sender_name": row.sender_name,
            "text": row.text,
            "created_at": row.created_at
        })

    return messages