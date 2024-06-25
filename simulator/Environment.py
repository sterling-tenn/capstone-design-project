from typing import List
from Robot import Robot
import pygame
import math
from helper import cos, sin

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Environment(object):
    def __init__(self, obstacles: List[tuple[float, float]], main_robot: Robot, particles: List[Robot], height: float, width: float) -> None:
        self.obstacles = obstacles
        self.main_robot = main_robot
        self.particles = particles
        self.width = width
        self.height = height
        self.display = None
    
    def initialize_display(self) -> None:
        self.display = pygame.display.set_mode((self.width, self.height)) 
        pygame.display.set_caption('Monte Carlo Localization')
        self.display.fill(WHITE)
    
    def insert_obstacles(self) -> None:
        # every obstacle on the screen will be a square
        obstacle_height = 15
        obstacle_thickness = 15
        obstacle_width = 15
        
        for x, y in self.obstacles:
            rectangle = pygame.Rect(x, y, obstacle_height, obstacle_width)
            pygame.draw.rect(self.display, BLACK, rectangle, obstacle_thickness)
    
    def insert_robots_and_particles(self) -> None:
        # every particle (including the robot) would be a circle
        # color of particle and robot would be different
        robot_color = (240, 240, 240)
        robot_radius = 50
        
        particle_color = (255, 0, 0)
        particle_radius = 5
        
        line = 100
        
        # draw the robot circle and bearing
        pygame.draw.circle(self.display, robot_color, (self.main_robot.x, self.main_robot.y), robot_radius)

        robot_heading_x = self.main_robot.x + (robot_radius) * cos(self.main_robot.heading)
        robot_heading_y = self.main_robot.y + (robot_radius) * sin(self.main_robot.heading)
        pygame.draw.line(self.display, BLACK, (self.main_robot.x, self.main_robot.y), (robot_heading_x, robot_heading_y))

        # draw all particles
        for x, y in self.particles:
            particle_heading_x = x + line * math.cos(self.main_robot.heading)
            particle_heading_y = y + line * math.sin(self.main_robot.heading)
            pygame.draw.line(self.display, BLACK, (x, y), (particle_heading_x, particle_heading_y))
            pygame.draw.circle(self.display, particle_color, (x, y), particle_radius)

        
        
        