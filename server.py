import socket
from threading import Thread
import struct
import time

server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server.bind(("2409:408a:1bb0:caa6:746f:f475:57e8:60c4", 5550))
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
        data = msg.decode()
        broadcast_msg = f"{timestamp} - {client_name}: {data}"
      elif msg_type == 2:
        broadcast_msg = f"{timestamp} - {client_name}: [Image Received]"
      elif msg_type == 3:
        broadcast_msg = f"{timestamp} - {client_name}: [PDF Received]"
      for c in all_clients:
        if c != client:
            c.send(broadcast_msg.encode())
            if msg_type in [2, 3]:
                c.send(header + msg)
    except:
      name = all_clients[client]
      for c in all_clients:
        if c != client:
            c.send(f"someone {name} has left the room!".encode())
      del all_clients[client]
      break

while True:
    print("Server started...")
    client, address = server.accept()
    print("Connected")
    name = client.recv(1024).decode()
    all_clients[client] = name
    for c in all_clients:
        if c != client:
            c.send(f"someone {name} joined the room!".encode())
    thread = Thread(target=client_thread, args=(client,))
    thread.start()
