from abc import ABC

from Data.Entities import ChatHistory, Users
from Data.Model.ChatRecord import ChatRecord
from Repositories.IRepositoryBase import IRepositoryBase
from Repositories.RepositoryBase import RepositoryBase
from Service.Abstraction.IChatServices import IChatServices


class ChatServices(IChatServices, ABC):
    def __init__(self):
        self.chat_history_repository: IRepositoryBase = RepositoryBase(ChatHistory)

    def get_senders(self, receiver_id: str) -> list:
        sender_ids = self.chat_history_repository.get(ChatHistory.receiver == receiver_id, ChatHistory.sender)
        senders: list = list()
        for user in sender_ids:
            senders.append(self.chat_history_repository.get(Users.id == user, Users.user_name, Users.id))
        return senders

    def get_messages(self, sender_id: str, receiver_id: str) -> list:
        msgs = self.chat_history_repository.get(ChatHistory.receiver == receiver_id, ChatHistory.sender == sender_id)
        messages: list = list()
        for msg in msgs:
            chat_record = ChatRecord()
            chat_record.message = msg.message
            messages.append(chat_record)
        return messages
