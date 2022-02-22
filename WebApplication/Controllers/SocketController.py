import json

from fastapi import APIRouter, WebSocket

from Service.Abstraction.IMessageService import IMessageService
from Service.Abstraction.IUserService import IUserService
from Service.Implementation.MessageService import MessageService
from Service.Implementation.UserService import UserService

socket_module = APIRouter(prefix='/sock')


@socket_module.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data = json.loads(data)
        user_service: IUserService = UserService()
        message_service: IMessageService = MessageService()
        data['sender'] = user_service.get_username_from_user_id(data['sender'])
        data['receiver'] = user_service.get_username_from_user_id(data['receiver'])
        message_service.save_message(data)
        print(f"Message text was: {data}")
        counter: int = 15
        while counter > 0:
            await websocket.send_text(json.dumps(data))
            counter = counter - 1