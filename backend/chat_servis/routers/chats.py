from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime, timezone


from db import get_db
from repository.chats import get_chat_id, get_user, new_chat,get_chats
from repository.users import  get_me
from schemas.chats import Chat
from schemas.messages import Message, MessageCreate 
from services.producer_message import producer_message
from services.token import get_current_user_id
import time
from repository.cassandra_message import get_messages_chat
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

@router.get('/{public_id}/messages')
async def get_messages(public_id: str, db: AsyncSession = Depends(get_db)):
    chatid = await get_chat_id(public_id, db)
    return await get_messages_chat(chatid) 

# @router.post('/{public_id}/messages')
# async def post_messages(public_id: str, mess: Message, user_data: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
#     chatid = await get_chat_id(public_id, db)
#     message_id = uuid.uuid4()
#     created_at = datetime.now(timezone.utc)

#     message = MessageCreate(
#         id=str(message_id),
#         chat_id=chatid,
#         text=mess.text,
#         sender_id=user_data['user_id'],
#         sender_name=user_data['username']
#     )

#     await producer_message(message)
#     return {
#         'id': message_id,
#         'text': mess.text,
#         "senderId": user_data['user_id'],
#         'senderName': user_data['username'],
#         "createdAt": created_at.isoformat(),
#     }

# @router.post("/message")
# async def message(data: Message):
#     res = await producer_message(data)
#     return res