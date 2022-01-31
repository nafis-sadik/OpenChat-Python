import string
from socket import socket


class ClientModel:
    user_id: string
    connection: socket
    address: tuple
    user_name: string
    room_name: string
