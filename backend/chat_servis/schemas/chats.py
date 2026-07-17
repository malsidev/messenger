from pydantic import BaseModel 

class Chat(BaseModel):
    user1_id : int
    user2_id : int

