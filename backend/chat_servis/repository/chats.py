from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Users, Chats
from sqlalchemy import or_, select, insert
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

async def get_chats(user_id: int, db: AsyncSession):
    stmt = select(Chats).where(or_(Chats.user1_id == user_id, Chats.user2_id == user_id))
    res = await db.execute(stmt)
    chats = res.scalars().all()

    if not chats:
        raise HTTPException(status_code=404, detail="Chats not found")

    result = []
    for chat in chats:
        other_user_id = chat.user2_id if chat.user1_id == user_id else chat.user1_id

        user_stmt = select(Users).where(Users.id == other_user_id)
        user_res = await db.execute(user_stmt)
        other_user = user_res.scalar_one_or_none()

        result.append({
            "id": chat.public_id,
            "title": other_user.username if other_user else "Неизвестный пользователь",
        })

    return result

async def get_chat_id(public_id: str, db: AsyncSession ):
    stmt = select(Chats).where(Chats.public_id == public_id)
    res = await db.execute(stmt)
    chat = res.scalar_one_or_none()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    return chat.id