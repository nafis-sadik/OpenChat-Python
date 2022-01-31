import socket
import threading
import string

from WebApplication.Modesl.ClientModel import ClientModel

HEADER: int = 64
PORT: int = 5003
SERVER: str = '0.0.0.0'
# SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
print('SERVER', ADDR)
FORMAT: str = 'utf-8'
DISCONNECT_MESSAGE: str = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print('Socket successfully created')

server.bind(ADDR)
print(f'socket binded to {ADDR}')

rooms = {}
clients = {}


def client_handler():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, client_address = server.accept()
        conn.send(f"Please provide a user name : ".encode(FORMAT))
        msg_length: int = int(conn.recv(HEADER).decode(FORMAT))
        user_name: string = conn.recv(msg_length).decode(FORMAT)
        conn.send('You are connected'.encode(FORMAT))
        client: ClientModel = ClientModel()
        client.connection = conn
        client.address = client_address
        client.user_name = user_name
        clients[user_name] = client
        thread = threading.Thread(target=msg_handler, args=(client, client_address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def msg_handler(client: ClientModel, addr: tuple):
    # Register for a room
    while True:
        msg_length = int(client.connection.recv(HEADER).decode(FORMAT))
        message = client.connection.recv(msg_length).decode(FORMAT)

        if message.startswith('[ROOM JOIN]'):
            room_name: string = message.replace('[ROOM JOIN] ', '')
            client.room_name = room_name
            # If room doesn't exist, create room
            if room_name not in rooms.keys():
                rooms[room_name] = []
                print(f"Room {room_name} created")
                client.connection.send(f"Room {room_name} created".encode(FORMAT))

            if client not in rooms[room_name]:
                rooms[room_name].append(client)
                print(f"{client.user_name} joined {room_name}")
                client.connection.send(f"{client.user_name} joined {room_name}".encode(FORMAT))

            continue

        if message.startswith('[ROOM LEAVE]'):
            room_name: string = message.replace('[ROOM LEAVE] ', '')
            client.room_name = ''
            if room_name not in rooms.keys():
                rooms[room_name].pop(client)

            continue

        if hasattr(client, 'room_name'):
            clients_in_room = rooms[client.room_name]
            for user in clients_in_room:
                if user is not client:
                    user.connection.send(message.encode(FORMAT))
                else:
                    user.connection.send('Sent'.encode(FORMAT))