import socket
from _thread import *
from typing import List, NoReturn

IP_ADDRESS = '172.17.9.62'
PORT = 8081
MAX_CLIENTS = 100
LIST_OF_CLIENTS: List["socket.socket"] = []

SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def client_thread(client_socket: "socket.socket", client_address: "socket._RetAddress") -> NoReturn:
    client_socket.send(b'Welcome to this chatroom')
    while True:
        try:
            message = client_socket.recv(2048)
            if message:
                print(f'<{client_address[0]}>', message)
                message_to_send = f'<{client_address[0]}> {message}'
                message_to_send = bytes(message_to_send, 'utf-8')
                broadcast(message_to_send, client_socket)
            else:
                remove(client_socket)
        except Exception as ex:
            continue

def broadcast(message: bytes, client_socket: "socket.socket") -> None:
    for client in LIST_OF_CLIENTS:
        if client != client_socket:
            try:
                client.send(message)
            except Exception as ex:
                client.close()
                remove(client)

def remove(client_socket: "socket.socket") -> None:
    if client_socket in LIST_OF_CLIENTS:
        LIST_OF_CLIENTS.remove(client_socket)

print(f'Server started at {IP_ADDRESS}:{PORT} and listening...')

SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER_SOCKET.bind((IP_ADDRESS, PORT))
SERVER_SOCKET.listen(MAX_CLIENTS)

while True:
    client_socket, client_address = SERVER_SOCKET.accept()
    LIST_OF_CLIENTS.append(client_socket)
    print(client_address[0], 'connected')
    start_new_thread(client_thread, (client_socket, client_address))

client_socket.close()
SERVER_SOCKET.close()