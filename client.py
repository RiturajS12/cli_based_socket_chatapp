import socket
from threading import Thread
import struct
from PIL import Image
import io

name = input("Enter your name:")

client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
client.connect(("2409:408a:1bb0:caa6:746f:f475:57e8:60c4", 5550))

client.send(name.encode())

def send(client):
    while True:
        choice = input("Enter 't' for text, 'i' for image, 'p' for PDF: \n").strip().lower()
        
        if choice == 't':
            message = input("Enter your message: \n")
            data = f'{name}:{message}'
            msg_type = 1
            msg_length = len(data.encode())
            header = struct.pack('!II', msg_type, msg_length)
            client.send(header + data.encode())
        
        elif choice == 'i':
            image_path = input("Enter the path to the image: \n")
            try:
                with Image.open(image_path) as img:
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format=img.format)
                    img_data = img_byte_arr.getvalue()

                    msg_type = 2
                    msg_length = len(img_data)
                    header = struct.pack('!II', msg_type, msg_length)
                    client.send(header + img_data)
                    print("Image sent successfully")
            except Exception as e:
                print(f"Failed to send image: {e}")

        elif choice == 'p':
            pdf_path = input("Enter the path to the PDF: \n")
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_data = file.read()

                    msg_type = 3
                    msg_length = len(pdf_data)
                    header = struct.pack('!II', msg_type, msg_length)
                    client.send(header + pdf_data)
                    print("PDF sent successfully")
            except Exception as e:
                print(f"Failed to send PDF: {e}")

        else:
            print("Invalid choice. Please enter 't' for text, 'i' for image, or 'p' for PDF.")

def receive(client):
    while True:
        try:
            header = client.recv(8)
            if len(header) < 8:
                raise ConnectionResetError
            
            msg_type, msg_length = struct.unpack('!II', header)
            data = client.recv(msg_length).decode()
            
            print(data)
        except:
            client.close()
            break

Thread1 = Thread(target=send, args=(client,))
Thread1.start()
Thread2 = Thread(target=receive, args=(client,))
Thread2.start()
