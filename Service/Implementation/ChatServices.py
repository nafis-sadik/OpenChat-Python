from abc import ABC

from Data.Entities import ChatHistory, Users
from Data.Model.ChatRecord import ChatRecord
from Repositories.IRepositoryBase import IRepositoryBase
from Repositories.RepositoryBase import RepositoryBase
from Service.Abstraction.IChatServices import IChatServices


class ChatServices(IChatServices, ABC):
    def __init__(self):
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
