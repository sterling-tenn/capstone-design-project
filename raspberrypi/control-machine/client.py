import socket

HOST = "192.168.1.135"
PORT = 5000

def send_data(message):
    """Sends a message to the Raspberry Pi server and receives a response."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            client_socket.sendall(message.encode()) # Send data
            response = client_socket.recv(1024) # Receive response
            return response.decode()
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    while True:
        msg = input("Enter message to send (or 'exit' to quit): ")
        if msg.lower() == "exit":
            break
        response = send_data(msg)
        print(f"Server response: {response}")
