import threading
from gpiozero import Servo
from gpiozero import DistanceSensor
import sys
import termios
import tty
import time

# Set GPIO for ultrasonic sensor
sensor = DistanceSensor(trigger=23, echo=24)  # physical pins 16, 18

# Set GPIO for servos
left_servo = Servo(27) # GPIO 27, physical pin 13
right_servo = Servo(17) # GPIO 17, physical pin 11

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

def read_sensor(sensor, stop_event):
    while not stop_event.is_set():
        distance = sensor.distance * 100  # convert to cm
        print(f"Distance: {distance:.2f} cm")
        time.sleep(0.5)

def main():
    # to constantly read sensor in a separate thread
    stop_event = threading.Event()
    sensor_thread = threading.Thread(target=read_sensor, args=(sensor, stop_event))
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

        # close sensor and sensor thread
        sensor.close()
        stop_event.set()
        sensor_thread.join()

if __name__ == "__main__":
    main()
