from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from joserfc import jwt
from dotenv import load_dotenv
import os
from joserfc.jwk import OctKey

load_dotenv()
security = HTTPBearer()
SECRET = os.getenv('SECRET_ACCESS_TOKEN')

def _get_key() -> OctKey:
    return OctKey.import_key(SECRET)

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
        username = claims.get("username")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has no subject",
            )
        print(user_id)
        print(username)
        return {
            "user_id": int(user_id),
            "username": username,
        }

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )