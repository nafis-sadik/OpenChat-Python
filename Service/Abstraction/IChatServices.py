class IChatServices:
    def get_senders(self, receiver_id: str) -> list:
        raise NotImplementedError

    def get_messages(self, sender_id: str, receiver_id: str) -> list:
        raise NotImplementedError
