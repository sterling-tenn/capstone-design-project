import time as t
import numpy as np
from gpiozero import Servo
from gyroscope import Gyro
import conf as conf
from distance_tracker import DistanceTracker

class Movement:

    def __init__(self) -> None:
        # Set GPIO for servos
        self.left_servo = Servo(conf.LEFT_SERVO_PIN)
        self.right_servo = Servo(conf.RIGHT_SERVO_PIN)
        self.gyro = Gyro()
        self.distance_tracker = DistanceTracker()
        self.time_delta = 0.001

    def move_forward(self, distance) -> None:
        self.distance_tracker.start()
        self.left_servo.max()
        self.right_servo.min()
        while np.linalg.norm(self.distance_tracker.get_displacement()) < distance:
            t.sleep(self.time_delta) 
        self.stop()
        self.distance_tracker.finish()

    def move_backward(self, distance) -> None:
        self.distance_tracker.start()
        self.left_servo.min()
        self.right_servo.max()
        while np.linalg.norm(self.distance_tracker.get_displacement()) < distance:
            t.sleep(self.time_delta)  
        self.stop()
        self.distance_tracker.finish()

    def turn_left(self, degrees) -> None:
        self.left_servo.min()
        self.right_servo.min()
        while abs(self.gyro.get_x_rotation()) < degrees:
            t.sleep(self.time_delta) 
        self.stop()

    def turn_right(self, degrees) -> None:
        self.left_servo.max()
        self.right_servo.max()
        while abs(self.gyro.get_x_rotation()) < degrees:
            t.sleep(self.time_delta) 
        self.stop()


    def stop(self) -> None:
        self.left_servo.detach()
        self.right_servo.detach()
