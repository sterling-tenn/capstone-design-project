import time
from gpiozero import Servo, DistanceSensor
import threading
import json
from conf import *

# Set GPIO for ultrasonic sensors
sensor_centre = DistanceSensor(trigger=TRIGGER_PIN_CENTRE, echo=ECHO_PIN_CENTRE)
sensor_left = DistanceSensor(trigger=TRIGGER_PIN_LEFT, echo=ECHO_PIN_LEFT)
sensor_right = DistanceSensor(trigger=TRIGGER_PIN_RIGHT, echo=ECHO_PIN_RIGHT)

# Set GPIO for servos
left_servo = Servo(LEFT_SERVO_PIN)
right_servo = Servo(RIGHT_SERVO_PIN)

FORWARD = 1
BACKWARD = -1
# STOP_TIME = 0.5 # how long we should stop between movements

SERVO_FACTOR = 7.5 # adjust so we can calculate time to move specified certain distance
TURNING_FACTOR = 90 / 1.3 # adjust so we can calculate time to turn specified angle

# estimated distance in metres
def move_forward(distance):
    left_servo.value = FORWARD
    right_servo.value = BACKWARD

    time.sleep(distance * SERVO_FACTOR)

# estimated distance in metres
def move_backward(distance):
    left_servo.value = BACKWARD
    right_servo.value = FORWARD

    time.sleep(distance * SERVO_FACTOR)

# counter clockwise
# estimated degrees to turn
def turn_left(degrees):
    left_servo.value = BACKWARD
    right_servo.value = BACKWARD

    time.sleep(degrees / TURNING_FACTOR)

# clockwise
# estimated degrees to turn
def turn_right(degrees):
    left_servo.value = FORWARD
    right_servo.value = FORWARD

    time.sleep(degrees / TURNING_FACTOR)

def stop():
    left_servo.detach()
    right_servo.detach()

def read_sensors(sensors, stop_event):
    while not stop_event.is_set():
        centre, left, right = sensors
        c = centre.distance * 100  # convert to cm
        l = left.distance * 100
        r = right.distance * 100
        print(f"[Distances] Left: {l:.2f} cm | Centre: {c:.2f} cm | Right: {r:.2f} cm")

        if c < STOP_DISTANCE or l < STOP_DISTANCE or r < STOP_DISTANCE:
            print("Obstacle detected! Stopping the robot.")
            stop()
            stop_event.set()  # This will stop the sensor thread

        time.sleep(0.1)

def move_robot(stop_event):
    with open("path.json", "r") as file:
        data = json.load(file)
        directions = data["directions"]

    for direction in directions:
        if stop_event.is_set():
            break

        if direction == "L":
            print("Turning left")
            turn_left(90)
        elif direction == "R":
            print("Turning right")
            turn_right(90)
        elif direction == "F":
            print("Moving forward")
            move_forward(BLOCK_SIZE)

def main():
    # stop servos on program start
    left_servo.detach()
    right_servo.detach()

    try:
        input("Press Enter to start the automatic movement sequence")

        # to constantly read sensors in a separate thread
        stop_event = threading.Event()
        sensors = [sensor_centre, sensor_left, sensor_right]
        sensor_thread = threading.Thread(target=read_sensors, args=(sensors, stop_event))
        sensor_thread.start()

        move_robot(stop_event)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
    finally:
        # stop servos on program completion
        stop()
        
        # close sensors and sensor thread
        sensor_centre.close()
        sensor_left.close()
        sensor_right.close()
        stop_event.set()
        sensor_thread.join()

if __name__ == '__main__':
    main()