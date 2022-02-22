from abc import ABC

from Data.Entities import ChatHistory
from Repositories.IRepositoryBase import IRepositoryBase
from Repositories.RepositoryBase import RepositoryBase
from Service.Abstraction.IMessageService import IMessageService


class MessageService(IMessageService, ABC):
    def __init__(self):
        self.message_repo: IRepositoryBase = RepositoryBase(ChatHistory)

    def save_message(self, message: dict):
        try:
            msg: ChatHistory = ChatHistory()
            max_pk = self.message_repo.max(ChatHistory.id)
            if max_pk:
                msg.id = max_pk + 1
            else:
                msg.id = 1
            msg.sender = message['sender']
            msg.receiver = message['receiver']
            msg.message = message['message']
            self.message_repo.add(msg)
        except Exception as e:
            print(str(e))
