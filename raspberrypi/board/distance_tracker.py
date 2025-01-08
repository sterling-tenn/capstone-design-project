import numpy as np
import time as t
from gyroscope import Gyro 

class DistanceTracker:

    def __init__(self) -> None:
        self.gyro = Gyro()
        self.reset = False
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.displacement = np.array([0.0, 0.0, 0.0])
        self.integration_method = self.simpsons_rule

    def simpsons_rule(self, accelerations, time_diffs) -> np.ndarray:
        h = time_diffs[-1] + time_diffs[-2]
        return (h / 6.0) * (accelerations[-3] + 4 * accelerations[-2] + accelerations[-1])

    def trapezoidal_rule(self, accelerations, time_diffs) -> np.ndarray:
        h = time_diffs[-1]
        return h * (accelerations[-2] + accelerations[-1]) / 2.0

    def midpoint_rule(self, accelerations, time_diffs) -> np.ndarray:
        h = time_diffs[-1]
        return h * accelerations[-2]

    def rectangular_rule(self, accelerations, time_diffs) -> np.ndarray:
        h = time_diffs[-1]
        return h * accelerations[-1]

    def booles_rule(self, accelerations, time_diffs) -> np.ndarray:
        h = time_diffs[-1] + time_diffs[-2] + time_diffs[-3] + time_diffs[-4]
        return (2 * h / 45) * (7 * accelerations[-5] + 32 * accelerations[-4] + 12 * accelerations[-3] + 32 * accelerations[-2] + 7 * accelerations[-1])
    
    def _distance_tracker(self) -> None:
        current_time = t.time_ns()
        time_diff = (current_time - self.prev_time) * 1e-9  # Convert nanoseconds to seconds
        current_accel = self.gyro.get_accel_scaled()

        if len(self.accelerations) > 5:
            self.accelerations.append(current_accel)
            self.time_diffs.append(time_diff)
        else:
            self.accelerations = self.accelerations[1:] + [current_accel]
            self.time_diffs = self.time_diffs[1:] + [time_diff]
            velocity_increment = self._integration_method(self.accelerations, self.time_diffs)
            self.velocity += velocity_increment
            displacement_increment = velocity_increment * time_diff
            self.displacement += displacement_increment

        self.prev_time = current_time

    def start(self) -> None:
        self.accelerations = []
        self.time_diffs = []
        self.prev_time = t.time_ns()

        while not self.reset:
            self._distance_tracker()
            
    def stop(self) -> None:
        self.reset = True

    def get_displacement(self) -> np.ndarray:
        return self.displacement.copy()

    def get_velocity(self) -> np.ndarray:
        return self.velocity.copy()

    def set_integration_method(self, method) -> None:
        self._integration_method = method
