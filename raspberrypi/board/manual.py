from gpiozero import Servo
import keyboard
import time

# Set GPIO for servos
left_servo_pin = 17
right_servo_pin = 18
left_servo = Servo(left_servo_pin, min_pulse_width=1/1000, max_pulse_width=2/1000)
right_servo = Servo(right_servo_pin, min_pulse_width=1/1000, max_pulse_width=2/1000)

FORWARD = 180
BACKWARD = 0
STOP = 90

def move_forward():
    left_servo.value = FORWARD
    right_servo.value = FORWARD
    print("Moving Forward")

def move_backward():
    left_servo.value = BACKWARD
    right_servo.value = BACKWARD
    print("Moving Backward")

# counter clockwise
def move_left():
    left_servo.value = BACKWARD
    right_servo.value = FORWARD
    print("Moving Left")

# clockwise
def move_right():
    left_servo.value = FORWARD
    right_servo.value = BACKWARD
    print("Moving Right")

def stop():
    left_servo.value = STOP
    right_servo.value = STOP
    print("Stopped")

def main():
    while True:
        if keyboard.is_pressed('w'):
            move_forward()
        elif keyboard.is_pressed('s'):
            move_backward()
        elif keyboard.is_pressed('a'):
            move_left()
        elif keyboard.is_pressed('d'):
            move_right()
        elif keyboard.is_pressed('t'):
            stop()
        
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop() # stop servos on exit
