import threading
from gpiozero import Servo
from gpiozero import DistanceSensor
import sys
import termios
import tty
import time
from conf import *

# Set GPIO for ultrasonic sensor
sensor_centre = DistanceSensor(trigger=TRIGGER_PIN_CENTRE, echo=ECHO_PIN_CENTRE)
sensor_left = DistanceSensor(trigger=TRIGGER_PIN_LEFT, echo=ECHO_PIN_LEFT)
sensor_right = DistanceSensor(trigger=TRIGGER_PIN_RIGHT, echo=ECHO_PIN_RIGHT)

# Set GPIO for servos
left_servo = Servo(LEFT_SERVO_PIN)
right_servo = Servo(RIGHT_SERVO_PIN)

FORWARD = 1
BACKWARD = -1

def move_forward():
    left_servo.value = FORWARD
    right_servo.value = BACKWARD

def move_backward():
    left_servo.value = BACKWARD
    right_servo.value = FORWARD

# counter clockwise
def turn_left():
    left_servo.value = BACKWARD
    right_servo.value = BACKWARD

# clockwise
def turn_right():
    left_servo.value = FORWARD
    right_servo.value = FORWARD

def stop():
    left_servo.detach()
    right_servo.detach()

# get keyboard input
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def read_sensors(sensors, stop_event):
    while not stop_event.is_set():
        centre, left, right = sensors
        c = centre.distance * 100  # convert to cm
        l = left.distance * 100
        r = right.distance * 100
        print(f"[Distances] Left: {l:.2f} cm | Centre: {c:.2f} cm | Right: {r:.2f} cm")

        time.sleep(0.1)

def main():
    # to constantly read sensors in a separate thread
    stop_event = threading.Event()
    sensors = [sensor_centre, sensor_left, sensor_right]
    sensor_thread = threading.Thread(target=read_sensors, args=(sensors, stop_event))
    sensor_thread.start()
    
    stop()  # stop servos on program start
    try:
        while True:
            char = getch()
            if char == 'w':
                print("Moving Forward")
                move_forward()
            elif char == 's':
                print("Moving Backward")
                move_backward()
            elif char == 'a':
                print("Turning Left")
                turn_left()
            elif char == 'd':
                print("Turning Right")
                turn_right()
            elif char == 't':
                print("Stopping")
                stop()
            elif char == 'q':
                print("Exiting")
                break
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        # stop servos on program completion
        stop()

        # close sensors and sensor thread
        sensor_centre.close()
        sensor_left.close()
        sensor_right.close()
        stop_event.set()
        sensor_thread.join()

if __name__ == "__main__":
    main()
