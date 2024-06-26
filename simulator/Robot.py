import math
from typing import *
from helper import euclidian_distance
from helper import cos, sin

class Robot(object):
    def __init__(self, x: float, y: float, heading: float, movement_error: float, heading_error: float, measurement_error: float) -> None:
        self.x = x
        self.y = y
        self.heading = heading
        self.movement_error = movement_error
        self.heading_error = heading_error
        self.measurement_error = measurement_error
        self.weight = 0
        
    def obstacle_distances(self, obstacles: List[Tuple[float, float]]) -> None:
        obstacle_measurements = []
        for obstacle_x, obstacle_y in obstacles:
            distance_to_obstacle = euclidian_distance(obstacle_x, obstacle_y, self.x, self.y, self.measurement_error)
            obstacle_measurements.append(distance_to_obstacle)
        
        return obstacle_measurements
    
    def move(self, distance: float, heading_rotation: float, width: float, height: float) -> None:
        current_heading = self.heading + self.heading_error
        
        new_position_x = self.x + (distance * cos(current_heading) + self.measurement_error)
        new_position_y = self.y + (distance * sin(current_heading) + self.measurement_error)

        if new_position_x > width:
            new_position_x = width
        elif new_position_x < 0:
            new_position_x = 0
        
        if new_position_y > height:
            new_position_y = height
        elif new_position_y < 0:
            new_position_y = 0
        
        self.x = new_position_x
        self.y = new_position_y
        self.heading -= heading_rotation