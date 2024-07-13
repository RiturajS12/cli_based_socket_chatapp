import socket
from threading import Thread


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("192.168.57.132",5550))

server.listen()
all_clients = {}

def client_thread(client):
    while True:
        try:    
            msg = client.recv(1024)
            for c in all_clients:
                c.send(msg)
        except:
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
