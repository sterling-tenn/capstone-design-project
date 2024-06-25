from Environment import *
from Robot import *
import pygame
import time

pygame.init()

main_robot = Robot(500.0, 500.0, 0, 0, 0, 0)

maze = Environment(
    obstacles=[[20.0, 20.0], [100.0, 25.0], [450.0, 350.0]], main_robot=main_robot, particles=[], height=1000, width=1000
)

maze.initialize_display()

main_robot.move(distance=0.0, heading_rotation= 180, width=maze.width, height=maze.height)

while True:
    for event in pygame.event.get():
        continue

    maze.display.fill((255, 255, 255))
    maze.insert_robots_and_particles()
    
    main_robot.move(distance=10.0, heading_rotation=0, width=maze.width, height=maze.height)

    maze.insert_obstacles()
    
    pygame.display.flip()
