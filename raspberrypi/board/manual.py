from gpiozero import Servo
import sys
import termios
import tty
import time

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

def main():
    stop() # stop servos on program start
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

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop() # stop servos on exit
