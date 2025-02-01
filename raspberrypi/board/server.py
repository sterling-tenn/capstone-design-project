import socket
from gpiozero import Servo
from gpiozero import DistanceSensor
from conf import *
import atexit
import json

HOST = "0.0.0.0" # Listen on all available interfaces
PORT = 5000

# Set GPIO for ultrasonic sensor
sensor_centre = DistanceSensor(trigger=TRIGGER_PIN_CENTRE, echo=ECHO_PIN_CENTRE)
sensor_left = DistanceSensor(trigger=TRIGGER_PIN_LEFT, echo=ECHO_PIN_LEFT)
sensor_right = DistanceSensor(trigger=TRIGGER_PIN_RIGHT, echo=ECHO_PIN_RIGHT)

# Set GPIO for servos
left_servo = Servo(LEFT_SERVO_PIN)
right_servo = Servo(RIGHT_SERVO_PIN)

def read_sensors():
    centre, left, right = sensor_centre, sensor_left, sensor_right
    
    # convert to cm
    c = centre.distance * 100
    l = left.distance * 100
    r = right.distance * 100
    # print(f"[Distances] Left: {l:.2f} cm | Centre: {c:.2f} cm | Right: {r:.2f} cm")
    return l, c, r

FORWARD = 1
BACKWARD = -1

def move_forward():
    left_servo.value = FORWARD
    right_servo.value = BACKWARD
    # print("Moving forward")

def move_backward():
    left_servo.value = BACKWARD
    right_servo.value = FORWARD
    # print("Moving backward")

# counter clockwise
def turn_left():
    left_servo.value = BACKWARD
    right_servo.value = BACKWARD
    # print("Turning left")

# clockwise
def turn_right():
    left_servo.value = FORWARD
    right_servo.value = FORWARD
    # print("Turning right")

def stop():
    left_servo.detach()
    right_servo.detach()
    # print("Stopping")

def handle_client(client_socket):
    """Handles communication with a single client."""
    try:
        while True:
            data = client_socket.recv(1024) # Receive data (up to 1024 bytes)
            if not data:
                break
            print(f"Received: {data.decode()}")
            result, msg = process_data(data.decode())

            response = json.dumps({
                "received": data.decode(),
                "msg": msg,
                "result": result
            })

            # Send a response back
            client_socket.send(response.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    """Starts the TCP server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse if address is in use
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket)

def process_data(data):
    """Processes data received from the client."""
    result = None
    msg = "OK"

    if data.lower() == "move-forward":
        move_forward()
    elif data.lower() == "move-backward":
        move_backward()
    elif data.lower() == "turn-left":
        turn_left()
    elif data.lower() == "turn-right":
        turn_right()
    elif data.lower() == "stop":
        stop()
    elif data.lower() == "get-sensor-data":
        result = read_sensors()
    else:
        msg = f"Unknown command: {data}"
        print(f"Unknown command: {data}")

    return result, msg

# Register stop() to be called on exit
atexit.register(stop)

if __name__ == "__main__":
    stop() # stop servos on program completion
    start_server()