import socket
from gpiozero import Servo
from gpiozero import DistanceSensor
from gpiozero import LineSensor
from conf import *
import atexit
import json
import threading
import time
import struct
import generate_floorplans_map
from robot_controller import RobotController

HOST = "0.0.0.0" # Listen on all available interfaces
PORT = 5000

# Set GPIO for ultrasonic sensor
sensor_centre = DistanceSensor(trigger=TRIGGER_PIN_CENTRE, echo=ECHO_PIN_CENTRE)
sensor_left = DistanceSensor(trigger=TRIGGER_PIN_LEFT, echo=ECHO_PIN_LEFT)
sensor_right = DistanceSensor(trigger=TRIGGER_PIN_RIGHT, echo=ECHO_PIN_RIGHT)

# Set GPIO for servos
left_servo = Servo(LEFT_SERVO_PIN)
right_servo = Servo(RIGHT_SERVO_PIN)

# Set GPIO for IR sensor
ir_sensor = LineSensor(IR_SENSOR_PIN)

# Set flag to indicate if ground is detected
GROUND_DETECTED = True

def ground_detected():
    global GROUND_DETECTED
    GROUND_DETECTED = True

def no_ground_detected():
    global GROUND_DETECTED
    GROUND_DETECTED = False
    stop()

# Set callbacks for IR sensor
ir_sensor.when_line = ground_detected
ir_sensor.when_no_line = no_ground_detected

# Set flag to indicate if front obstacle is detected
FRONT_OBSTACLE_DETECTED = False

def front_obstacle_detected():
    global FRONT_OBSTACLE_DETECTED
    while True:
        l, c, r = read_sensors()

        if c < STOP_DISTANCE or l < STOP_DISTANCE or r < STOP_DISTANCE:
            print("Obstacle detected! Stopping the robot.")
            FRONT_OBSTACLE_DETECTED = True
            stop()
        else:
            FRONT_OBSTACLE_DETECTED = False

        time.sleep(0.1)

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
    if not GROUND_DETECTED or FRONT_OBSTACLE_DETECTED:
        return
        
    left_servo.value = FORWARD
    right_servo.value = BACKWARD
    # print("Moving forward")

def move_backward():
    left_servo.value = BACKWARD
    right_servo.value = FORWARD
    # print("Moving backward")

# counter clockwise
def turn_left():
    if not GROUND_DETECTED or FRONT_OBSTACLE_DETECTED:
        return
        
    left_servo.value = BACKWARD
    right_servo.value = BACKWARD
    # print("Turning left")

# clockwise
def turn_right():
    if not GROUND_DETECTED or FRONT_OBSTACLE_DETECTED:
        return
        
    left_servo.value = FORWARD
    right_servo.value = FORWARD
    # print("Turning right")

def stop():
    left_servo.detach()
    right_servo.detach()
    # print("Stopping")

def handle_client(client_socket):
    """Handles communication with a single client, processing text commands and image uploads."""
    try:
        # Receive the 4-byte header that determines the type (1 = text, 2 = image)
        header = client_socket.recv(4)
        if not header:
            print("Client disconnected.")
            return
        
        msg_type = struct.unpack("!I", header)[0]  # Read as an integer

        if msg_type == 1:  # Text Command
            data = client_socket.recv(1024).decode()
            print(f"Received command: {data}")
            result, msg = process_text_command(data)

            response = json.dumps({
                "received": data,
                "msg": msg,
                "result": result
            })
            client_socket.send(response.encode())

        elif msg_type == 2:  # Save the image uploaded as floorplans
            # Receive the image size (4 bytes)
            img_size_bytes = client_socket.recv(4)
            img_size = struct.unpack("!I", img_size_bytes)[0]
            print(f"Receiving image of size {img_size} bytes...")

            # Receive the image data
            image_data = b""
            while len(image_data) < img_size:
                chunk = client_socket.recv(min(4096, img_size - len(image_data)))
                if not chunk:
                    break
                image_data += chunk

            # Save the image
            if image_data:
                with open("floorplans.jpg", "wb") as f:
                    f.write(image_data)
                print("Image received and saved as floorplans.jpg")
                client_socket.send(b"Image received successfully")

                # Generate Floorplans Map
                generate_floorplans_map.generate("floorplans.jpg")
            else:
                print("Failed to receive image data.")

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

def process_text_command(cmd):
    """Processes text command received from the client."""
    result = None
    msg = "OK"

    if cmd.lower() == "move-forward":
        move_forward()
    elif cmd.lower() == "move-backward":
        move_backward()
    elif cmd.lower() == "turn-left":
        turn_left()
    elif cmd.lower() == "turn-right":
        turn_right()
    elif cmd.lower() == "stop":
        stop()
    elif cmd.lower() == "get-sensor-data":
        result = read_sensors()
    elif cmd.lower() == "auto-mcl":
        try:
            controller = RobotController()
            controller.run('auto_mcl', '/home/raspberrypi/capstone-design-project/raspberrypi/board/path_b.json', '/home/raspberrypi/capstone-design-project/raspberrypi/board/map_b.json')
        except Exception as e:
            msg = f"Error: {e}"
            print(f"Error: {e}")
    else:
        msg = f"Unknown command: {cmd}"
        print(f"Unknown command: {cmd}")

    return result, msg

# Register stop() to be called on exit
atexit.register(stop)

if __name__ == "__main__":
    stop()

    # to constantly read sensors in a separate thread to detect if an obstacle is in front
    sensor_thread = threading.Thread(target=front_obstacle_detected)
    sensor_thread.start()

    start_server()