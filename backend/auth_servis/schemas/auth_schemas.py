from pydantic import BaseModel
from typing import Optional

class LogUsers(BaseModel):
    username: str
    password: str

class RegUsers(BaseModel):
    first_name: str
    last_name: str|None
    username : str
    password: str
    password2: str


class UpdateUser(BaseModel):
    first_name: str | None = None
    last_name: str | None = None