import socket
import struct
import os

HOST = "192.168.226.60"
PORT = 5000

def send_text_command(message):
    """Sends a text message to the server."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))

            # Step 1: Send header (1 = text)
            client_socket.send(struct.pack("!I", 1))

            # Step 2: Send message
            client_socket.sendall(message.encode())

            # Step 3: Receive response
            response = client_socket.recv(1024).decode()
            return response
    except Exception as e:
        print(f"Connection error: {e}")

def send_image(image_path):
    """Sends an image to the server."""
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' not found.")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))

            # Read image file
            with open(image_path, "rb") as f:
                image_data = f.read()

            # Step 1: Send header (2 = image)
            client_socket.send(struct.pack("!I", 2))

            # Step 2: Send image size
            client_socket.send(struct.pack("!I", len(image_data)))

            # Step 3: Send image data
            client_socket.sendall(image_data)

            # Step 4: Receive server response
            response = client_socket.recv(1024).decode()
            print("📩 Server response:", response)
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    while True:
        option = input("Enter 'msg' to send a message, 'img' to send an image, or 'exit' to quit: ")
        
        if option.lower() == "exit":
            break
        elif option.lower() == "msg":
            msg = input("Enter message to send: ")
            response = send_text_command(msg)
            print(f"Server response: {response}")
        elif option.lower() == "img":
            image_path = input("Enter image path: ")
            send_image(image_path)
        else:
            print("Invalid option. Please enter 'msg', 'img', or 'exit'.")
