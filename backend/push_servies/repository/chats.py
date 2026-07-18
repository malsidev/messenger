from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.chat_model import Chats


async def get_chat_id(public_id: str, db: AsyncSession ):
    stmt = select(Chats).where(Chats.public_id == public_id)
    res = await db.execute(stmt)
    chat = res.scalar_one_or_none()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    return chat.id

async def get_receiver_id(
    chat_id: int,
    sender_id: int,
    db: AsyncSession
):
    stmt = select(Chats).where(Chats.id == chat_id)
    res = await db.execute(stmt)
    chat = res.scalar_one_or_none()

    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    if chat.user1_id == sender_id:
        return chat.user2_id

    if chat.user2_id == sender_id:
        return chat.user1_id

    raise HTTPException(
        status_code=403,
        detail="User not in this chat"
    )