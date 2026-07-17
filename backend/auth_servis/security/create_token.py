from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from joserfc import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from uuid import uuid4
import os
from fastapi import Depends, HTTPException, status
from schemas.token_shemas import RefreshTokenData
security = HTTPBearer()
load_dotenv()

from joserfc.jwk import OctKey

SECRET = os.getenv('SECRET_ACCESS_TOKEN')
ALGORITHM = os.getenv('ALGORITM')
ACCESS_LIFETIME = timedelta(hours=1)
REFRESH_LIFETIME = timedelta(days=30)



def _get_key() -> OctKey:
    return OctKey.import_key(SECRET)

def create_access_token(user_id: int, username: str) -> str:
    now = datetime.now(timezone.utc)
    payload_access_token = {
        'sub': str(user_id),  # ← было str(id) — баг! id это builtin
        'username': username,  # ← было str(id) — баг! id это builtin
        'typ': 'access',
        'iat': int(now.timestamp()),  # ← joserfc ожидает int, не datetime
        'exp': int((now + ACCESS_LIFETIME).timestamp()),
        'iss': 'mess',
        'aud': 'mobile',
    }
    token = jwt.encode(
        {'alg': ALGORITHM},    # ← header
        payload_access_token,  # ← claims
        _get_key()             # ← OctKey объект
    )
    return token

def create_refresh_token(user_id: int) -> RefreshTokenData:
    now = datetime.now(timezone.utc)
    expires_at = now + REFRESH_LIFETIME
    token_jti = str(uuid4())
    payload_refresh_token = {
        'sub': str(user_id),
        'typ': 'refresh',
        'iat': int(now.timestamp()),
        'exp': int(expires_at.timestamp()),
        'iss': 'mess',
        'aud': 'mobile',
        'jti': token_jti,
    }
    token = jwt.encode(
        {'alg': ALGORITHM},     # ← header
        payload_refresh_token,  # ← claims
        _get_key()              # ← OctKey объект
    )
    return RefreshTokenData(
        token=token,  # ← .token чтобы получить строку
        iat_at=now,
        exp_at=expires_at,
        jti=token_jti
    )


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    try:
        decoded = jwt.decode(credentials.credentials, _get_key())
        claims = decoded.claims

        if claims.get("typ") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        if claims.get("iss") != "mess":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid issuer",
            )

        if claims.get("aud") != "mobile":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid audience",
            )

        user_id = claims.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has no subject",
            )

        return int(user_id)

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )