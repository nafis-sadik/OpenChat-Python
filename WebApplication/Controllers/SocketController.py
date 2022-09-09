import json

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from Data.Model.ChatRecord import ChatRecord
from Data.Model.UserModel import UserModel
from Service.Abstraction.IChatServices import IChatServices
from Service.Abstraction.IMessageService import IMessageService
from Service.Abstraction.IUserService import IUserService
from Service.Implementation.ChatServices import ChatServices
from Service.Implementation.MessageService import MessageService
from Service.Implementation.UserService import UserService

socket_module = APIRouter(prefix='/sock')
manager: IChatServices = ChatServices()


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


@socket_module.websocket("/connect/{user_id}")
async def websocket_connect(websocket: WebSocket, user_id: str):
    user: UserModel = UserModel()
    user.id = user_id
    connected = manager.connect(websocket, user)
    try:
        while connected:
            data = await websocket.receive_text()
            message = json.loads(data)

            message_object: ChatRecord = ChatRecord()
            message_object.message = message['message']
            message_object.sender = user_id
            message_object.receiver = message['receiver']
            await manager.send(message_object)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user_id} left the chat")
