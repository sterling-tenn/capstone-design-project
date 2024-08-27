import time as t
import numpy as np
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from gyroscope import Gyro
import conf as conf
from distance_tracker import DistanceTracker

class Movement:

    def __init__(self) -> None:
        self.myfactory = PiGPIOFactory()
        self.left_servo = Servo(conf.LEFT_SERVO_PIN, pin_factory=self.myfactory)
        self.right_servo = Servo(conf.RIGHT_SERVO_PIN, pin_factory=self.myfactory)
        self.gyro = Gyro()
        self.distance_tracker = DistanceTracker()
        self.wheel_circumference = conf.WHEEL_CIRCUMFERENCE

    def move_forward(self, distance: float) -> None:
        self._execute_movement(distance, self._move_forward_logic)

    def move_backward(self, distance: float) -> None:
        self._execute_movement(distance, self._move_backward_logic)

    def turn_left(self, degrees: float) -> None:
        self._execute_turn(degrees, self._turn_left_logic)

    def turn_right(self, degrees: float) -> None:
        self._execute_turn(degrees, self._turn_right_logic)

    def stop(self) -> None:
        self.left_servo.mid()
        self.right_servo.mid()

    def _execute_movement(self, distance: float, move_logic) -> None:
        self.distance_tracker.start()
        move_logic()
        while np.linalg.norm(self.distance_tracker.get_displacement()) < distance:
            t.sleep(conf.TIME_DELTA)
        self.stop()
        self.distance_tracker.finish()

    def _execute_turn(self, degrees: float, turn_logic) -> None:
        turn_logic()
        while abs(self.gyro.get_x_rotation(*self.gyro.get_accel_scaled())) < degrees:
            t.sleep(conf.TIME_DELTA)
        self.stop()

    def _move_forward_logic(self) -> None:
        self.left_servo.max()
        self.right_servo.min()

    def _move_backward_logic(self) -> None:
        self.left_servo.min()
        self.right_servo.max()

    def _turn_left_logic(self) -> None:
        self.left_servo.min()
        self.right_servo.min()

    def _turn_right_logic(self) -> None:
        self.left_servo.max()
        self.right_servo.max()
