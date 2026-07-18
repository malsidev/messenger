from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.refresh_token_repo import save_refresh_token
from schemas.auth_schemas import LogUsers, RegUsers, UpdateUser
from models.models import Users
from security.password_hash import hash_password, verify_password
from security.create_token import create_access_token, create_refresh_token
from repositories.users_db import get_user, exists_user, post_reg_user


async def login_user(data: LogUsers, db: AsyncSession):
    user = await get_user(db, data.username)

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail='Неверный логин или пароль')     

    refresh_token = create_refresh_token(user.id)
    access_token = create_access_token(user.id, data.username)

    await save_refresh_token(db, user.id, refresh_token)

    return {
        'access_token' : access_token,
        "refresh_token": refresh_token.token,
        'user_id': user.id,
        'message': 'ok'
    }


async def register_user(data: RegUsers, db: AsyncSession):
    if data.password != data.password2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароли не совпадают"
        )
    
    existing = await exists_user(db, data) 
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует"
        )
    
    user = Users(
        first_name = data.first_name,
        last_name = data.last_name,
        username = data.username,
        password = hash_password(data.password)
    )

    await post_reg_user(db, user)

    return {"status": "ok"}
   

async def get_me(user_id: int, db: AsyncSession):
    user = await db.get(Users, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    print("USER ID =", user_id)
    return {
        "id": user.id,
        "email": user.username,
    }



async def update_me(
    user_id: int,
    data: UpdateUser,
    db: AsyncSession,
):
    user = await db.get(Users, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if data.first_name is not None:
        user.first_name = data.first_name

    if data.last_name is not None:
        user.last_name = data.last_name

    await db.commit()
    await db.refresh(user)

    return user
