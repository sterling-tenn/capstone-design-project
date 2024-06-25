from ParticleFilter import *
from Robot import *
from conf import *

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

    # create particle filter
    particle_filter = ParticleFilter(
        num_particles = NUM_PARTICLES,
        robot = robot,
        obstacles = generate_obstacles(NUM_OBSTACLES, WIDTH, HEIGHT, OBSTACLE_SEED),
        width = WIDTH,
        height = HEIGHT
    )
