# import select
import socket
import sys

SERVER_IP_ADDRESS = '172.17.9.62'
SERVER_PORT = 8081

socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_.connect((SERVER_IP_ADDRESS, SERVER_PORT))

while True:
    stream_list = [sys.stdin, socket_]
    # read_sockets, write_sockets, error_sockets = select.select(stream_list, [], [])
    for stream in stream_list: # read_sockets
        if stream == socket_:
            message = socket_.recv(2048)
            print(message)
        else:
            message = sys.stdin.readline()
            socket_.send(bytes(message, 'utf-8'))
            sys.stdout.write('<You> ')
            sys.stdout.write(message)
            sys.stdout.flush()

socket_.close()