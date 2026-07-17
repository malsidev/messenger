from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime, timezone


from db import get_db
from repository.chats import get_chat_id, get_user, new_chat,get_chats
from repository.users import  get_me
from schemas.chats import Chat
from schemas.messages import Message 
from services.producer_message import producer_message
from services.token import get_current_user_id
import time
router = APIRouter(prefix='/chats',tags=['/chats'])

@router.get('/')
async def get_chat(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await get_chats(user_id['user_id'], db)

@router.get('/search')
async def get_users(username: str, db: AsyncSession = Depends(get_db)):
    return await get_user(username, db)

@router.post('/start')
async def start_chat(data: Chat, db: AsyncSession = Depends(get_db)):
    print(data)
    return await new_chat(int(data.user1_id), int(data.user2_id), db)

@router.post('/{public_id}/messages')
async def post_messages(public_id: str, mess: Message, user_data: int = Depends(get_current_user_id)):
    message_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc)

    data = {'id': message_id, 'text' : mess.message, 'sender_id': user_data['user_id'], 'sender_name' : user_data['username'], 'created_at': created_at.isoformat()}


    await producer_message(data)
    return {
        'id': message_id,
        'text': mess.message,
        "senderId": user_data['user_id'],
        'senderName': user_data['username'],
        "createdAt": created_at.isoformat(),
    }



# @router.post("/message")
# async def message(data: Message):
#     res = await producer_message(data)
#     return res