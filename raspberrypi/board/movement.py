import time as t
import numpy as np
from gpiozero import Servo
import conf as conf

class Movement:

    def __init__(self) -> None:
        self.left_servo = Servo(conf.LEFT_SERVO_PIN)
        self.right_servo = Servo(conf.RIGHT_SERVO_PIN)
        self.stop()

    def move_forward(self, distance: float) -> None:
        self._execute_movement(distance, self._move_forward_logic)

    def move_backward(self, distance: float) -> None:
        self._execute_movement(distance, self._move_backward_logic)

    def turn_left(self, degrees: float) -> None:
        self._execute_turn(degrees, self._turn_left_logic)

    def turn_right(self, degrees: float) -> None:
        self._execute_turn(degrees, self._turn_right_logic)

    def stop(self) -> None:
        self.left_servo.detach()
        self.right_servo.detach()

    def _execute_movement(self, distance: float, move_logic) -> None:
        time = distance / (conf.WHEEL_RADIUS * conf.ANGULAR_VELOCITY)
        move_logic()
        t.sleep(time)
        self.stop()

    def _execute_turn(self, degrees: float, turn_logic) -> None:
        rads = np.radians(degrees)
        time = (rads * conf.INTERNAL_TURN_RADIUS) / (conf.WHEEL_RADIUS * conf.ANGULAR_VELOCITY)
        turn_logic()
        t.sleep(time)
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


if __name__ == "__main__":
    pass
    move = Movement()

    # move.move_forward(0.5)
    # move.move_backward(0.5)
    # move.move_forward(1)
    # move.move_backward(1)
    t.sleep(1)
    move.turn_right(90)
    move.turn_left(90)
    t.sleep(3)
    move.turn_right(180)
    move.turn_left(180)
    t.sleep(3)
    move.turn_right(360)
    move.turn_left(360)