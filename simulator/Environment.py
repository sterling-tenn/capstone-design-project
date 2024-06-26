from typing import *
from Robot import Robot
import pygame
import math
from helper import *
from conf import BLACK, GREY, RED, WHITE

class Environment(object):
    def __init__(self, obstacles: List[Tuple[float, float]], main_robot: Robot, particles: List[Robot], height: float, width: float) -> None:
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
        robot_color = GREY
        robot_radius = 25
        
        particle_color = RED
        particle_radius = 15
        
        # draw the robot circle and bearing
        pygame.draw.circle(self.display, robot_color, (self.main_robot.x, self.main_robot.y), robot_radius)

        robot_heading_x = self.main_robot.x + (robot_radius) * cos(self.main_robot.heading - 90)
        robot_heading_y = self.main_robot.y + (robot_radius) * sin(self.main_robot.heading - 90)
        pygame.draw.line(self.display, BLACK, (self.main_robot.x, self.main_robot.y), (robot_heading_x, robot_heading_y))

        # draw all particles
        for particle in self.particles:
            particle_heading_x = particle.x + (particle_radius) * cos(particle.heading - 90)
            particle_heading_y = particle.y + (particle_radius) * sin(particle.heading - 90)
            pygame.draw.line(self.display, BLACK, (particle.x, particle.y), (particle_heading_x, particle_heading_y))
            pygame.draw.circle(self.display, particle_color, (particle.x, particle.y), particle_radius)

        
        
        