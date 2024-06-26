from ParticleFilter import *
from Robot import *
from Environment import *
from conf import *
import pygame
import time

if __name__ == "__main__":

    # create robot
    robot = Robot(
        x = ROBOT_STARTING_POS_X,
        y = ROBOT_STARTING_POS_Y,
        heading = 45,
        
        # simulated robot actuator error
        movement_error = random.uniform(MOVEMENT_NOISE[0], MOVEMENT_NOISE[1]),
        heading_error = random.uniform(HEADING_NOISE[0], HEADING_NOISE[1]),
        measurement_error = random.uniform(MEASUREMENT_NOISE[0], MEASUREMENT_NOISE[1])
    )
    
    obstacles = generate_obstacles(NUM_OBSTACLES, WIDTH, HEIGHT, OBSTACLE_SEED)

    # create particle filter
    particle_filter = ParticleFilter(
        num_particles = NUM_PARTICLES,
        robot = robot,
        obstacles = obstacles,
        width = WIDTH,
        height = HEIGHT
    )
    
    # print("aaaa")
    # print(particle_filter.particles)

    maze = Environment(
        obstacles=obstacles,
        main_robot=robot,
        particles=particle_filter.particles,
        height=HEIGHT,
        width=WIDTH
    )
    
    maze.initialize_display()
    # particle_filter.apply_movement()
    # particle_filter.update_particle_weightings()
    # particle_filter.regenerate_particles()
    # print("aaaa")
    # print(particle_filter.particles[0].x, particle_filter.particles[0].y, particle_filter.particles[0].heading, particle_filter.particles[0].weight)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                break  
            
        maze.display.fill(WHITE)
        
        particle_filter.apply_movement()
        particle_filter.update_particle_weightings()
        particle_filter.regenerate_particles()
        
        # print("main")
        # print(particle_filter.particles) 
        
        particles = particle_filter.particles
        if particles:
            maze.particles = particles
            
        # print(maze.particles[0].x, maze.particles[0].y, maze.particles[0].heading, maze.particles[0].weight)

        maze.insert_obstacles()
        maze.insert_robots_and_particles()
            
        pygame.display.flip()
        
        pygame.time.wait(25)
        
