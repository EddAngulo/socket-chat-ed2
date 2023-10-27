import socket
from _thread import *
from typing import List, NoReturn

ip_address = '172.17.9.62'
port = 8081
max_clients = 100
list_of_clients: List["socket.socket"] = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    for client in list_of_clients:
        if client != client_socket:
            try:
                client.send(message)
            except Exception as ex:
                client.close()
                remove(client)

def remove(client_socket: "socket.socket") -> None:
    if client_socket in list_of_clients:
        list_of_clients.remove(client_socket)

print(f'Server started at {ip_address}:{port} and listening...')

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((ip_address, port))
server_socket.listen(max_clients)

while True:
    client_socket, client_address = server_socket.accept()
    list_of_clients.append(client_socket)
    print(client_address[0], 'connected')
    start_new_thread(client_thread, (client_socket, client_address))

client_socket.close()
server_socket.close()