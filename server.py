import socket
from threading import Thread


server = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
server.bind(("2409:408a:1bb0:caa6:4d38:6cc0:644a:31db",5550))

server.listen()
all_clients = {}

def client_thread(client):
    while True:
        try:    
            msg = client.recv(1024)
            for c in all_clients:
                c.send(msg)
        except:
            name = all_clients[client]
            for c in all_clients:
                if c != client:
                    c.send(f"{name} has left the room!".encode())
            del all_clients[client]
            break

while True:
    print("server is starting...")
    client , address = server.accept()
    print("connected")
    name =  client.recv(1024).decode()
    all_clients[client] = name
    for c in all_clients:
        if c != client:
            c.send(f"{name} has joined the room!".encode())
    thread = Thread(target=client_thread,args=(client,))
    thread.start()
