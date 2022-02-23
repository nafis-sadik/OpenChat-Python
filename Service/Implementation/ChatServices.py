import datetime
import json
from abc import ABC

import bcrypt
from starlette.websockets import WebSocket

from Data.Entities import *
from Data.Model.ChatGroup import ChatGroup
from Data.Model.ChatRecord import ChatRecord
from Data.Model.UserModel import UserModel
from Repositories.IRepositoryBase import IRepositoryBase
from Repositories.RepositoryBase import RepositoryBase
from Service.Abstraction.IChatServices import IChatServices


class ChatServices(IChatServices, ABC):
    ACTIVE_CONNECTIONS: dict = dict()

    def __init__(self):
        self.group_repo: IRepositoryBase = RepositoryBase(Groups)
        self.group_members_repo: IRepositoryBase = RepositoryBase(GroupMembers)
        self.chat_history_repository: IRepositoryBase = RepositoryBase(ChatHistory)
        self.user_repo: IRepositoryBase = RepositoryBase(Users)

    def get_senders(self, receiver_id: str) -> list:
        try:
            sender_ids: list = self.chat_history_repository.get_col(conditions=ChatHistory.receiver == receiver_id, cols=ChatHistory.receiver)
            senders: list = list()
            for user_id in sender_ids:
                user_name = self.user_repo.get_col(conditions=Users.id == user_id[0], cols=Users.user_name)[0][0]
                senders.append({'UserId': user_id[0], 'UserName': user_name})
            return senders
        except Exception as e:
            print(str(e))
            return []

    def get_messages(self, sender_id: str, receiver_id: str) -> list:
        try:
            msgs = self.chat_history_repository.get(ChatHistory.receiver == receiver_id, ChatHistory.sender == sender_id)
            messages: list = list()
            for msg in msgs:
                chat_record = ChatRecord()
                chat_record.receiver = msg.receiver
                chat_record.message = msg.message
                chat_record.sender = msg.sender
                messages.append(chat_record)
            return messages
        except Exception as e:
            print(str(e))
            return []

    async def connect(self, websocket: WebSocket, user: UserModel) -> [bool]:
        await websocket.accept()
        try:
            if user.id not in ChatServices.ACTIVE_CONNECTIONS.keys():
                ChatServices.ACTIVE_CONNECTIONS[user.id] = websocket
                return True
            return False
        except Exception as e:
            print(str(e))
            return None

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in ChatServices.ACTIVE_CONNECTIONS.values():
            key_list = list(ChatServices.ACTIVE_CONNECTIONS.keys())
            val_list = list(ChatServices.ACTIVE_CONNECTIONS.values())
            position = val_list.index(websocket)
            ChatServices.ACTIVE_CONNECTIONS.pop(key_list[position])

    def create_group(self, user: UserModel, group: ChatGroup):
        chat_group: Groups = Groups()
        chat_group.group_name = group.group_name
        chat_group.group_founder = user.id
        chat_group.group_create_date = datetime.datetime.now()

        if group.password:
            chat_group.password = bcrypt.hashpw(bytes(group.password, 'utf-8'), bcrypt.gensalt())
        else:
            chat_group.password = None

        pk = self.group_repo.max(Groups.id)
        if pk:
            chat_group.id = pk + 1
        else:
            chat_group.id = 1

        self.group_repo.add(chat_group)

    def join_group(self, user: UserModel, group: ChatGroup):
        try:
            chat_group_members: GroupMembers = GroupMembers()
            chat_group_members.group_id = group.id
            pk = self.group_members_repo.max(Groups.id)
            if pk:
                chat_group_members.id = pk + 1
            else:
                chat_group_members.id = 1

            existing_member = self.group_members_repo.get(GroupMembers.group_member == user.id)
            if existing_member is None or len(existing_member) <= 0:
                chat_group_members.group_member = user.id
                self.group_members_repo.add(chat_group_members)
                return True
            return False
        except Exception as e:
            print(str(e))
            return None

    async def send(self, message: ChatRecord):
        chat_history: ChatHistory = ChatHistory()
        chat_history.message = message.message
        chat_history.sender = message.sender
        chat_history.receiver = message.receiver
        pk = self.chat_history_repository.max(ChatHistory.id)
        if pk:
            chat_history.id = pk + 1
        else:
            chat_history.id = 1
        self.chat_history_repository.add(chat_history)
        if message.sender in ChatServices.ACTIVE_CONNECTIONS.keys():
            response: ChatRecord = ChatRecord()
            response.message = 'sent'
            await ChatServices.ACTIVE_CONNECTIONS[message.sender].send_text(json.dumps(response.__dict__))

        if message.receiver in ChatServices.ACTIVE_CONNECTIONS.keys():
            await ChatServices.ACTIVE_CONNECTIONS[message.receiver].send_text(json.dumps(message.__dict__))
            return

        group = self.group_repo.get(Groups.id == message.receiver)
        if group:
            group = group[0]
            group_members = self.group_members_repo.get(Groups.id == group.id)
            for user in group_members:
                if user.id in ChatServices.ACTIVE_CONNECTIONS.keys():
                    await ChatServices.ACTIVE_CONNECTIONS[user.id].send_text(json.dumps(message.__dict__))
                    return

    async def broadcast(self, message: str):
        for connection in ChatServices.ACTIVE_CONNECTIONS:
            msg_obj: ChatRecord = ChatRecord()
            msg_obj.message = message
            await connection.send_text(json.dumps(message.__dict__))
