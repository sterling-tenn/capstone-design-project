# automatic predefined movement sequence
import time
from gpiozero import Servo

# Set GPIO for servos
left_servo = Servo(27) # GPIO 27, physical pin 13
right_servo = Servo(17) # GPIO 17, physical pin 11

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

def main():
    # stop servos on program start
    left_servo.detach()
    right_servo.detach()

    try:
        input("Press Enter to start the automatic movement sequence")
        while True:
            move_forward(1)      
            stop(2)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")

if __name__ == '__main__':
    main()