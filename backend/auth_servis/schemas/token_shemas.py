from datetime import datetime

from pydantic import BaseModel

class RefreshTokenData(BaseModel):
    token: str
    iat_at: datetime
    exp_at: datetime
    jti: str