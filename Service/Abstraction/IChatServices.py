from typing import Optional
from starlette.websockets import WebSocket

from Data.Model.ChatGroup import ChatGroup
from Data.Model.ChatRecord import ChatRecord
from Data.Model.UserModel import UserModel


class IChatServices:
    def connect(self, websocket: WebSocket, user: UserModel) -> Optional[bool]:
        raise NotImplementedError

    def disconnect(self, websocket: WebSocket) -> None:
        raise NotImplementedError

    def create_group(self, user: UserModel, group: ChatGroup):
        raise NotImplementedError

    def join_group(self, user: UserModel, group: ChatGroup) -> Optional[bool]:
        raise NotImplementedError

    async def send(self, message: ChatRecord):
        raise NotImplementedError

    async def broadcast(self, message: str):
        raise NotImplementedError

    def get_senders(self, receiver_id: str) -> list:
        raise NotImplementedError

    def get_messages(self, sender_id: str, receiver_id: str) -> list:
        raise NotImplementedError
