from fastapi import APIRouter, Depends, HTTPException

from Data.Model.ChatRecord import ChatRecord
from Service.Abstraction.IChatServices import IChatServices
from Service.Implementation.ChatServices import ChatServices
# from WebApplication import validate_jwt

chat_service = APIRouter(
    prefix='/api',
    tags=["Chat"],
    # dependencies=[Depends(validate_jwt)],
    responses={
        404: {"description": "Not found"},
        200: {"description": "OK"}
    }
)


@chat_service.get('/senders')
async def get_senders(chat_data: ChatRecord):
    chatting_service: IChatServices = ChatServices()
    response = chatting_service.get_senders(chat_data.receiver)
    return response


@chat_service.get('/messages/{receiver_id}/{sender_id}')
async def get_messages_by_sender(receiver_id: str, sender_id: str):
    chatting_service: IChatServices = ChatServices()
    return chatting_service.get_messages(receiver_id=receiver_id, sender_id=sender_id)
