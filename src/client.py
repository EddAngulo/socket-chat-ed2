# import select
import socket
import sys

server_ip_address = '172.17.9.62'
server_port = 8081

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((server_ip_address, server_port))
while True:
    stream_list = [sys.stdin, server_socket]
    # read_sockets, write_sockets, error_sockets = select.select(stream_list, [], [])
    for stream in stream_list: # read_sockets
        if stream == server_socket:
            message = stream.recv(2048)
            print(message)
        else:
            message = sys.stdin.readline()
            server_socket.send(bytes(message, 'utf-8'))
            sys.stdout.write('<You> ')
            sys.stdout.write(message)
            sys.stdout.flush()

server_socket.close()