from uuid import UUID
from datetime import datetime


class Message:
    def __init__(
        self,
        chat_id: int,
        id: UUID,
        text: str,
        sender_id: int,
        sender_name: str,
        created_at: datetime
    ):
        self.chat_id = chat_id
        self.id = id
        self.sender_id = sender_id
        self.sender_name = sender_name
        self.text = text
        self.created_at = created_at