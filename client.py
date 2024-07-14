import socket
from threading import Thread

name = input("Enter your name:")


client = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
client.connect(("2409:408a:1bb0:caa6:acb4:46be:34cb:3dba",5550))

client.send(name.encode())

def send(client):
    while True:
        data = f'{name}:{input("")}'
        client.send(data.encode())

def receive(client):
    while True:
        try:
            data = client.recv(1024).decode()
            print(data)
        except:
            client.close()
            break

Thread1 = Thread(target=send,args=(client,))
Thread1.start()
Thread2 = Thread(target=receive,args=(client,))
Thread2.start()
