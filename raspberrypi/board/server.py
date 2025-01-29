import socket

HOST = "0.0.0.0" # Listen on all available interfaces
PORT = 5000

def handle_client(client_socket):
    """Handles communication with a single client."""
    try:
        while True:
            data = client_socket.recv(1024) # Receive data (up to 1024 bytes)
            if not data:
                break
            print(f"Received: {data.decode()}")

            # Send a response back
            response = f"ACK: {data.decode()}"
            client_socket.send(response.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    """Starts the TCP server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Allow up to 5 connections
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()