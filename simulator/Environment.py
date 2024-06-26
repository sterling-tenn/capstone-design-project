from typing import List
from Robot import Robot
import pygame
import math
from helper import cos, sin
from conf import BLACK, GREY, RED, WHITE

class Environment(object):
    def __init__(self, obstacles: List[tuple[float, float]], main_robot: Robot, particles: List[Robot], height: float, width: float) -> None:
        self.obstacles = obstacles
        self.main_robot = main_robot
        self.particles = particles
        
        # print("inside env")
        # print(self.particles)
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
        robot_radius = 50
        
        # print("drawing")
        # print(self.particles)
        
        particle_color = RED
        particle_radius = 5
        
        line = 100
        
        # draw the robot circle and bearing
        pygame.draw.circle(self.display, robot_color, (self.main_robot.x, self.main_robot.y), robot_radius)

        robot_heading_x = self.main_robot.x + (robot_radius) * cos(self.main_robot.heading)
        robot_heading_y = self.main_robot.y + (robot_radius) * sin(self.main_robot.heading)
        pygame.draw.line(self.display, BLACK, (self.main_robot.x, self.main_robot.y), (robot_heading_x, robot_heading_y))

        # draw all particles
        for particle in self.particles:
            particle_heading_x = particle.x + line * math.cos(self.main_robot.heading)
            particle_heading_y = particle.y + line * math.sin(self.main_robot.heading)
            pygame.draw.line(self.display, BLACK, (particle.x, particle.y), (particle_heading_x, particle_heading_y))
            pygame.draw.circle(self.display, particle_color, (particle.x, particle.y), particle_radius)

        
        
        