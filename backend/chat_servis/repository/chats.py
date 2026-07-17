from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Users, Chats
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
# from schemas.chats import  Chat
from datetime import datetime, timedelta, timezone


async def get_user(username: str, db: AsyncSession):
    stmt = ( 
        select(Users.id, Users.username)
        .where(Users.username.ilike(f"%{username}%"))
        .limit(10)
    )

    result = await db.execute(stmt)
    users = result.mappings().all()
    return users

async def new_chat( sender_id: int, recipient_id: int,  db: AsyncSession):
    id1, id2 = sorted([sender_id, recipient_id])
    chat = Chats(
        user1_id = id1,
        user2_id = id2
    )
    db.add(chat)
    await db.commit()
    await db.refresh(chat)


    return {
        'id': chat.public_id,
        'title': str(chat.user2_id)
    }

async def get_chats(user_id: int, db : AsyncSession):
    print(user_id)
    stmt = select(Chats).where(Chats.user1_id == user_id)
    res = await db.execute(stmt)
    chats = res.scalars().all()

    if not chats:
        raise HTTPException(status_code=404, detail="Начните общение")
    print(chats)
    return [
        {
            "id": chat.public_id,
            "title": str(chat.user2_id),
        }
        for chat in chats
    ]

async def get_chat_id(public_id: str, db: AsyncSession ):
    stmt = select(Chats).where(Chats.public_id == public_id)
    res = await db.execute(stmt)
    chat = res.scalar_one_or_none()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    return chat.id