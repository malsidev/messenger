from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import os
db = os.getenv('DB')

engine = create_async_engine(f'postgresql+asyncpg://malsi:fubkz13love@postgres:5433/malsseneger', echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_ws_db():

    async with AsyncSessionLocal() as session:
        yield session