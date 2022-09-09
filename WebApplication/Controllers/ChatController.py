from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer

from Data.Model.ChatRecord import ChatRecord
from ExtensionMethods import get_current_user
from Service.Abstraction.IChatServices import IChatServices
from Service.Implementation.ChatServices import ChatServices

auth_sceme = HTTPBearer()

chat_service = APIRouter(
    prefix='/api',
    tags=["Chat"],
    dependencies=[Depends(auth_sceme)],
    responses={
        404: {"description": "Not found"},
        200: {"description": "OK"}
    }
)


@chat_service.get('/senders')
async def get_senders(request: Request):
    chatting_service: IChatServices = ChatServices()
    response = chatting_service.get_senders(get_current_user(request=request))
    return response


@chat_service.get('/messages/{sender_id}')
async def get_messages_by_sender(receiver_id: str, request: Request):
    chatting_service: IChatServices = ChatServices()
    return chatting_service.get_messages(receiver_id=receiver_id, sender_id=get_current_user(request=request))
