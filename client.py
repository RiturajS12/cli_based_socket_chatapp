import socket
from threading import Thread
from PIL import Image
import struct

name = input("Enter your name: ")

client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
client.connect(("localhost", 5550))

client.send(name.encode('utf-8'))

def send(client):
    while True:
        choice = input("Enter 't' for text, 'i' for image, 'p' for PDF: \n").strip().lower()
        
        if choice == 't':
            message = input("Enter your message: \n")
            data = f'{name}: {message}'
            msg_type = 1
            msg_length = len(data.encode('utf-8'))
            header = struct.pack('!II', msg_type, msg_length)
            client.send(header + data.encode('utf-8'))
        
        elif choice == 'i':
            image_path = input("Enter the path to the image: \n")
            msg_type = 2
            msg_length = len(image_path.encode('utf-8'))
            header = struct.pack('!II', msg_type, msg_length)
            client.send(header + image_path.encode('utf-8'))
            print("Image path sent successfully")

        elif choice == 'p':
            pdf_path = input("Enter the path to the PDF: \n")
            msg_type = 3
            msg_length = len(pdf_path.encode('utf-8'))
            header = struct.pack('!II', msg_type, msg_length)
            client.send(header + pdf_path.encode('utf-8'))
            print("PDF path sent successfully")

        else:
            print("Invalid choice. Please enter 't' for text, 'i' for image, or 'p' for PDF.")

def receive(client):
    while True:
        try:
            header = client.recv(8)
            if len(header) < 8:
                raise ConnectionResetError
            
            msg_type, msg_length = struct.unpack('!II', header)
            msg = client.recv(msg_length)

            if msg_type == 2:
                print(f"Received an image!")
                image_path = msg.decode('utf-8')
                img = Image.open(image_path)
                img.show()
            elif msg_type == 3:
                    print(f"Received: {msg.decode('utf-8')}")
            else:
                print(msg.decode('utf-8'))

        except Exception as e:
            print(f"Connection error: {e}")
            client.close()
            break

Thread1 = Thread(target=send, args=(client,))
Thread1.start()
Thread2 = Thread(target=receive, args=(client,))
Thread2.start()
