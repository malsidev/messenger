from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, DBAPIError

from models.models import Users

async def get_user(db: AsyncSession, username:str)-> Users|None:
    stmt = select(Users).where(Users.username == username)
    res = await db.execute(stmt) 
    user = res.scalar_one_or_none()


    if not user:
        raise HTTPException(status_code=400, detail='Неверный логин или пароль')

    return user  

async def exists_user(db: AsyncSession, data):
    stmt = select(Users).where(Users.username == data.username, Users.is_active == False)
    res = await db.execute(stmt)
    existing = res.scalars().first()
    
    return existing

async def post_reg_user(db: AsyncSession, data):
    try:
        db.add(data)
        await db.commit()
        await db.refresh(data)
    except HTTPException:
        # пробрасываем дальше (FastAPI сам обработает)
        raise

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Нарушение уникальности (username уже существует)"
        )

    except DBAPIError as e:
        await db.rollback()
        print(f" ERROR {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка базы данных"
        )

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )