from models.models import Users, Chats
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status




async def get_me(user_id: int, db: AsyncSession):
    print('в гет ми')
    user = await db.get(Users, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    print("USER ID =", user_id)
    return user

async def get_chats(user_id: int, db : AsyncSession):
    chats = await db.get(Chats, user_id)

    if not chats:
        raise HTTPException(status_code=404, detail="Начните общение")
    print(chats)
    return chats