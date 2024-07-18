# RASPBERRY PI 5: TESTING SERVO MOTOR WITH GPIOZERO, THIS WORKS

from gpiozero import Servo
from time import sleep

servo = Servo(17) # GPIO 17, physical pin 11

try:
    while True:
        print("Moving to min position...")
        servo.min()
        sleep(2) # Hold for 2 seconds

        print("Stopping...")
        servo.detach()
        sleep(2)

        print("Mid speed")
        servo.mid()
        sleep(2)

        print("Stopping...")
        servo.detach()
        sleep(2)

        print("Moving to max position...")
        servo.max()
        sleep(2)

        print("Stopping...")
        servo.detach()
        sleep(2)
except KeyboardInterrupt:
    servo.detach()
    print("Servo stopped and cleaned up.")