from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.auth_schemas import LogUsers, RegUsers, UpdateUser
from security.create_token import get_current_user_id
from services.auth_service import get_me, login_user, register_user, update_me

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/login')
async def login(data: LogUsers, db: AsyncSession = Depends(get_db)):
    return await login_user(data, db)

@router.post('/register')
async def register(data: RegUsers, db: AsyncSession = Depends(get_db)):
    return await register_user(data, db)


@router.get("/me")
async def me(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await get_me(user_id, db)

@router.patch("/me")
async def update_profile(
    data: UpdateUser,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await update_me(user_id, data, db)