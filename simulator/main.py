from ParticleFilter import *
from Robot import *
from Environment import *
from conf import *
import pygame

HEIGHT = 1000
WIDTH = 1000

if __name__ == "__main__":

    # create robot
    robot = Robot(
        x = ROBOT_STARTING_POS_X,
        y = ROBOT_STARTING_POS_Y,
        heading = ROBOT_STARTING_HEADING,
        
        # simulated robot actuator error
        movement_error = 0,
        heading_error = 0,
        measurement_error = 0
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
    print("qqqqqqqqqqqqqqq")
    particle_filter.move_robot(distance=10.0, rotation=10.0)
    particle_filter.move_particles(distance=10.0, rotation=10.0)
    particle_filter.update_particle_weightings()
    particle_filter.regenerate_particles()
    print(particle_filter.particles)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        particle_filter.move_robot(distance=10.0, rotation=10.0)
        particle_filter.move_particles(distance=10.0, rotation=10.0)
        particle_filter.update_particle_weightings()
        particle_filter.regenerate_particles()
        
        print("main")
        print(particle_filter.particles) 
        
        particles = particle_filter.return_particles()
        if particles:
            maze.particles = particles

        maze.insert_obstacles()
        maze.insert_robots_and_particles()
        
        
        
            

