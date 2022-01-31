import socket
import string
import threading

HEADER = 64
PORT = 5003
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.11.201.29"
ADDR = (SERVER, PORT)


class Client:
    def __init__(self) -> None:
        pass

    def connect(self) -> bool:
        try:
            self.client: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(ADDR)
            return True
        except Exception as ex:
            print(str(ex))
            return False

    def send(self, msg: string) -> str:
        try:
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            self.client.send(send_length)
            self.client.send(message)
            return self.client.recv(2048).decode(FORMAT)
        except Exception as ex:
            return "[Client Error] " + str(ex)

    def recieve(self):
        while True:
            msg = self.client.recv(2048).decode(FORMAT)
            if msg:
                print(msg)

    def disconnect(self) -> str:
        return self.send(DISCONNECT_MESSAGE)


if __name__ == '__main__':
    client: Client = Client()
    client.connect()
    thread = threading.Thread(target=client.recieve)
    thread.start()
    print(client.send(input()))
    msg: str = ''
    while msg != 'DISCONNECT':
        msg = input()
        print(client.send(msg))
    client.send(DISCONNECT_MESSAGE)
