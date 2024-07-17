import socket
from threading import Thread
import struct
import time

server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server.bind(("localhost", 5550)) 
server.listen()
all_clients = {}

def client_thread(client):
    while True:
        try:
            header = client.recv(8)
            if len(header) < 8:
                raise ConnectionResetError

            msg_type, msg_length = struct.unpack('!II', header)
            msg = client.recv(msg_length)

            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            client_name = all_clients[client]

            if msg_type == 1:
                data = msg.decode('utf-8')
                broadcast_msg = f"{timestamp} - {client_name}: {data}"
            elif msg_type == 2:
                image_path = msg.decode('utf-8')
                broadcast_msg = f"{timestamp} - {client_name} sent an image"
            elif msg_type == 3:
                pdf_path = msg.decode('utf-8')
                broadcast_msg = f"{timestamp} - {client_name} sent a PDF"

            for c in all_clients:
                if c != client:
                    c.send(broadcast_msg.encode('utf-8'))

        except Exception as e:
            print(f"Connection error: {e}")
            name = all_clients[client]
            for c in all_clients:
                if c != client:
                    c.send(f"Someone {name} has left the room!".encode('utf-8'))
            del all_clients[client]
            client.close()
            break

while True:
    print("Server started...")
    client, address = server.accept()
    print(f"Connected: {address}")
    name = client.recv(1024).decode('utf-8')
    all_clients[client] = name
    for c in all_clients:
        if c != client:
            c.send(f"Someone {name} joined the room!".encode('utf-8'))
    thread = Thread(target=client_thread, args=(client,))
    thread.start()
