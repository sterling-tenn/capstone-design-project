# automatic predefined movement sequence
import time
from gpiozero import Servo, DistanceSensor
import threading
import json
from conf import *

# Set GPIO for ultrasonic sensor
sensor = DistanceSensor(trigger=TRIGGER_PIN, echo=ECHO_PIN)

# Set GPIO for servos
left_servo = Servo(LEFT_SERVO_PIN)
right_servo = Servo(RIGHT_SERVO_PIN)

FORWARD = 1
BACKWARD = -1
STOP_TIME = 0.5 # how long we should stop between movements

SERVO_FACTOR = 7.5 # adjust so we can calculate time to move specified certain distance
TURNING_FACTOR = 90 / 1.3 # adjust so we can calculate time to turn specified angle

# estimated distance in metres
def move_forward(distance):
    left_servo.value = FORWARD
    right_servo.value = BACKWARD

    time.sleep(distance * SERVO_FACTOR)
    stop(STOP_TIME)

# estimated distance in metres
def move_backward(distance):
    left_servo.value = BACKWARD
    right_servo.value = FORWARD

    time.sleep(distance * SERVO_FACTOR)
    stop(STOP_TIME)

# counter clockwise
# estimated degrees to turn
def turn_left(degrees):
    left_servo.value = BACKWARD
    right_servo.value = BACKWARD

    time.sleep(degrees / TURNING_FACTOR)
    stop(STOP_TIME)

# clockwise
# estimated degrees to turn
def turn_right(degrees):
    left_servo.value = FORWARD
    right_servo.value = FORWARD

    time.sleep(degrees / TURNING_FACTOR)
    stop(STOP_TIME)

def stop(t):
    left_servo.detach()
    right_servo.detach()
    time.sleep(t)

def read_sensor(sensor, stop_event):
    while not stop_event.is_set():
        distance = sensor.distance * 100  # convert to cm
        print(f"Distance: {distance:.2f} cm")
        time.sleep(0.5)
        
def move_robot():
    with open("path.json", "r") as file:
        data = json.load(file)
        directions = data["directions"]

    # orientation and path to follow taken 
    # care of in the json direction file
    # here, we just move
    for direction in directions:
        if direction == "L":
            print("Turning left")
            turn_left(90)
        elif direction == "R":
            print("Turning right")
            turn_right(90)
        elif direction == "F":
            print("Moving forward")
            move_forward(0.3)

def main():
    # stop servos on program start
    left_servo.detach()
    right_servo.detach()

    try:
        input("Press Enter to start the automatic movement sequence")

        # to constantly read sensor in a separate thread
        stop_event = threading.Event()
        sensor_thread = threading.Thread(target=read_sensor, args=(sensor, stop_event))
        sensor_thread.start()

        move_robot()

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
    finally:
        # stop servos on program completion
        left_servo.detach()
        right_servo.detach()
        
        # close sensor and sensor thread
        sensor.close()
        stop_event.set()
        sensor_thread.join()

if __name__ == '__main__':
    main()