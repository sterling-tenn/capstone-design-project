import math
from helper import *
from conf import *

class Robot:
    def __init__(self, x, y, theta, color, noise_linear, noise_angular, noise_measurement):
        self.x = x
        self.y = y
        self.theta = normalize_angle_radians(theta) # radians
        self.color = color
        self.weight = 0.0
        self.noise_linear = noise_linear
        self.noise_angular = noise_angular
        self.noise_measurement = noise_measurement

    #this function moves the agent
    def move(self, dist, rot):
        angle = self.theta + self.noise_angular
        angle = normalize_angle_radians(angle)

        new_x = self.x + (dist * math.cos(angle) + self.noise_linear)
        new_y = self.y + (dist * math.sin(angle) + self.noise_linear)

        #check boundaries and loop around if necessary
        if new_x > WIDTH:
            new_x = 0
        elif new_x < 0:
            new_x = WIDTH
        if new_y > HEIGHT:
            new_y = 0
        elif new_y < 0:
            new_y = HEIGHT
        
        self.x = new_x
        self.y = new_y
        self.theta += rot

    # we assume that robot can observe distances to ALL obstacles - this only works for a simulation, for real life this needs to be changed
    # robot vision/observation is limited to physical hardware, so we can't assume we can calculate the distance to all obstacles
    # for the particles though, we can assume we can calculated the distance to all obstacles since both particles and obstacles are known
    def observe(self, obstacles):
        distances = []
        for obstacle in obstacles:
            x, y = obstacle    
            distances.append((math.sqrt((x - self.x)**2 + (y - self.y)**2) + self.noise_measurement))
        return distances