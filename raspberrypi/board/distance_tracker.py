import numpy as np
import time as t
from threading import Thread
from gyroscope import Gyro 

class DistanceTracker:

    def __init__(self) -> None:
        self.gyro = Gyro()

    def distance_tracker(self) -> None:
        while not self.reset:
            current_time = t.time_ns()
            time_diff = (current_time - self.prev_time) * 1e-9  # convert nanoseconds to seconds
            current_accel = self.gyro.get_accel_scaled()

            if len(self.accelerations) < 3:
                self.accelerations.append(current_accel)
                self.time_diffs.append(time_diff)
            else:
                # Simpson's rule
                h = self.time_diffs[-1] + self.time_diffs[-2]  # Total time interval
                velocity_increment = (h / 6.0) * (self.accelerations[-3] + 4 * self.accelerations[-2] + self.accelerations[-1])
                self.velocity += velocity_increment
                displacement_increment = (h / 6.0) * (self.velocity * self.time_diffs[-1])
                self.displacement += displacement_increment

                self.accelerations = self.accelerations[1:] + [current_accel]
                self.time_diffs = self.time_diffs[1:] + [time_diff]

            self.prev_time = current_time

    def start(self) -> None:
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.displacement = np.array([0.0, 0.0, 0.0])
        self.prev_time = t.time_ns()
        self.reset = False
        self.accelerations = []
        self.time_diffs = []
        self.thread = Thread(target=self.distance_tracker, daemon=True)
        self.thread.start()

    def finish(self) -> None:
        self.reset = True
        self.thread.join()

    def get_displacement(self) -> np.ndarray:
        return self.displacement

    def get_velocity(self) -> np.ndarray:
        return self.velocity
