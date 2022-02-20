from fastapi import APIRouter

from Data.Model.ChatRecord import ChatRecord
from Service.Abstraction.IChatServices import IChatServices
from Service.Implementation.ChatServices import ChatServices

chat_service = APIRouter(prefix='/api')


@chat_service.get('/senders')
async def get_senders(chat_data: ChatRecord):
    chatting_service: IChatServices = ChatServices()
    response = chatting_service.get_senders(chat_data.receiver)
    return response


@chat_service.get('/messages')
async def get_messages_by_sender(chat_data: ChatRecord):
    chatting_service: IChatServices = ChatServices()
    return chatting_service.get_messages(receiver_id=chat_data.receiver, sender_id=chat_data.sender)
