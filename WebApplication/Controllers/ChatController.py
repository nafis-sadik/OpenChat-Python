from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from Data.Model.ChatRecord import ChatRecord
from Service.Abstraction.IChatServices import IChatServices
from Service.Implementation.ChatServices import ChatServices

reusable_oauth2 = OAuth2PasswordBearer(
    scheme_name="JWT",
    tokenUrl="/api/login/"
)

chat_service = APIRouter(
    prefix='/api',
    tags=["Chat"],
    dependencies=[Depends(reusable_oauth2)],
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
