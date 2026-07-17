from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Refresh_token
from schemas.token_shemas import RefreshTokenData

async def save_refresh_token(db: AsyncSession, user_id: int, data: RefreshTokenData):
    try:
        token = Refresh_token(
            user_id = user_id,
            iat_at = data.iat_at,
            exp_at = data.exp_at,
            jti = data.jti
        )

        db.add(token)
        await db.commit()
        return 'ok' 
    except:
        await db.rollback()
        raise
        # 'iat_at': now,
        # 'exp_at': expires_at,
        # 'jti': token_jti