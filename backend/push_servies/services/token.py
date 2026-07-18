import logging

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

    


def verify_ws_token(token: str):

    try:

        decoded = jwt.decode(
            token,
            _get_key(),
            algorithms=["HS256"]
        )


        claims = decoded.claims


        if claims.get("typ") != "access":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type"
            )


        if claims.get("iss") != "mess":
            raise HTTPException(
                status_code=401,
                detail="Invalid issuer"
            )


        if claims.get("aud") != "mobile":
            raise HTTPException(
                status_code=401,
                detail="Invalid audience"
            )


        user_id = claims.get("sub")
        username = claims.get("username")


        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="No user id"
            )


        return {
            "user_id": int(user_id),
            "username": username
        }


    except Exception as e:

        logging.error(
            f"JWT error: {e}"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )