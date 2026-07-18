# from datetime import datetime, timezone

# from fastapi import Depends

# from schemas.message import Message, MessageCreate
# from services import producer_message


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