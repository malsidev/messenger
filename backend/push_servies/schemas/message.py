from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Message(BaseModel):
    text: str

class MessageCreate(BaseModel):
    id: str
    chat_id: int
    text: str
    sender_id: int
    sender_name: str