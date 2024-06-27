from helper import *
from Robot import *
from Environment import *
from ParticleFilter import *
from conf import *
from typing import *
import random
import threading
import matplotlib.pyplot as plt

# Generate random obstacles for the particle filter
def generate_obstacles(n: int, seed: int = None) -> List[Tuple[float, float]]:
    if seed is not None:
        random.seed(seed)
    
    coordinates = []
    for _ in range(n):
        x = random.uniform(0, WIDTH)
        y = random.uniform(0, HEIGHT)
        coordinates.append((x, y))
    
    return coordinates

if __name__ == "__main__":

    # Create robot
    robot = Robot(
        x = ROBOT_STARTING_POS_X,
        y = ROBOT_STARTING_POS_Y,
        theta = ROBOT_STARTING_ANGLE,
        color = ROBOT_COLOR,
        noise_linear = random.uniform(*ROBOT_NOISE_LINEAR_RANGE),
        noise_angular = random.uniform(*ROBOT_NOISE_ANGULAR_RANGE),
        noise_measurement = random.uniform(*ROBOT_NOISE_MEASUREMENT_RANGE),
    )
    
    obstacles = generate_obstacles(NUM_OBSTACLES, OBSTACLE_SEED)

    # Create particle filter
    particle_filter = ParticleFilter(
        num_particles = NUM_PARTICLES,
        robot = robot,
        obstacles = obstacles
    )

    # Create pygame environment
    pygame = Environment(
        width = WIDTH,
        height = HEIGHT,
        obstacles = obstacles,
        robot = robot,
        particles = particle_filter.particles,
    )

    # Run the particle filter in a separate thread
    if NUM_TIME_STEPS == -1:
        run_pf = threading.Thread(target=particle_filter.run_particle_filter)
        run_pf.daemon = True # Set as daemon thread so it closes when the main thread closes
        run_pf.start()
        pygame.run()
        run_pf.join()
    else:
        # no pygame visualization, for data diagnostics
        run_pf = threading.Thread(target=particle_filter.run_particle_filter_num_time_steps, args=(NUM_TIME_STEPS,))
        run_pf.daemon = True
        run_pf.start()
        run_pf.join()
        
        # graph diagnostics
        time_steps = [i for i in range(NUM_TIME_STEPS)]
        difference_err = particle_filter.difference_error

        err1, err2, err3 = zip(*difference_err)
        plt.plot(time_steps, err1, label='X Position')
        plt.plot(time_steps, err2, label='Y Position')
        plt.plot(time_steps, err3, label='Heading Angle')

        plt.xlabel('Time Steps')
        plt.ylabel('Average Difference Error')
        plt.title(f'Average Difference Error Over Time')
        plt.legend()
        
        # configuration properties
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.25)
        configuration = f"""Configuration:
        Number of Particles: {NUM_PARTICLES}
        Number of Obstacles: {NUM_OBSTACLES}
        Number of Time Steps: {NUM_TIME_STEPS}
        Distance STDDEV: {DISTANCE_SIGMA}
        Heading STDDEV: {HEADING_SIGMA}
        """
        # configuration = f"""Configuration:
        # (other parameters unchanged)
        # Robot Noise Range - Movement: {ROBOT_NOISE_LINEAR_RANGE}
        # Robot Noise Range - Rotation: {ROBOT_NOISE_ANGULAR_RANGE}
        # Robot Noise Range - Sensor Measurement: {ROBOT_NOISE_MEASUREMENT_RANGE}
        # """
        plt.text(0.20, 0.95, configuration, transform=plt.gca().transAxes, fontsize=8, verticalalignment='top', horizontalalignment='left', bbox=props)

        # plt.show()
        plt.savefig(f'{NUM_PARTICLES}particles {NUM_OBSTACLES}obstacles {NUM_TIME_STEPS}timesteps SIGMAS-{DISTANCE_SIGMA}-{HEADING_SIGMA}.png', bbox_inches='tight')
        # plt.savefig(f'Robot Noise Range.png', bbox_inches='tight')