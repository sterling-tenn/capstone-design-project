import random
import time
from Robot import *
from typing import *
from conf import *
from helper import *
from tabulate import tabulate

class ParticleFilter:
    def __init__(self, num_particles: int, robot: Robot, obstacles: List[Tuple[float, float]]) -> None:
        self.num_particles = num_particles
        self.robot = robot
        self.obstacles = obstacles # act as reference points for the robot to estimate its position

        self.particles = self.create_particles()

        self.difference_error = [] # diagnostics: store the difference error for each time step

    # particles are essentially just simulated robots
    def create_particles(self) -> List[Robot]:
        particles = []
        for _ in range(self.num_particles):
            particle = Robot(
                x = random.randint(0, WIDTH),
                y = random.randint(0, HEIGHT),
                theta = random.uniform(-math.pi, math.pi), # doesn't this get normalized in radians anyway, so why not use radians?
                color = PARTICLE_COLOR,
                # each particle follows the same error distribution as the robot
                noise_linear = random.uniform(*PARTICLE_NOISE_LINEAR_RANGE),
                noise_angular = random.uniform(*PARTICLE_NOISE_ANGULAR_RANGE),
                noise_measurement = random.uniform(*PARTICLE_NOISE_MEASUREMENT_RANGE)
            )
            particles.append(particle)
        return particles

    def apply_movement(self) -> None:
        # randomly get the linear and angular motion data to move both the robot and particles
        dist = random.uniform(*MOVEMENT_DISTANCE_RANGE)
        rot = random.uniform(*MOVEMENT_ROTATION_RANGE)

        # move the robot
        self.robot.move(dist, rot)

        # move each particle
        for particle in self.particles:
            particle.move(dist, rot)

    def update_particle_weights(self) -> None:
        robot_distances = self.robot.observe(self.obstacles)

        # for each particle, check how good of an estimation it is compared to the robot's reported distance and heading
        for particle in self.particles:
            likelihood = 1 # using 1 as a percentages, how good of an estimation is this specific particle?
            particle_distances = particle.observe(self.obstacles)

            # scale likelihood using a normal distribution with the actual robot's measurements as a reference point
            for robot_dist, particle_dist in zip(robot_distances, particle_distances): # compare all distances
                likelihood *= normal_distribution(robot_dist, DISTANCE_SIGMA, particle_dist)
            likelihood *= normal_distribution(self.robot.theta, HEADING_SIGMA, particle.theta) # compare heading angles

            particle.weight = likelihood

    # create new generation of particles based on the weights of the previous generation
    def regenerate_particles(self) -> None:
        total_weight = sum(particle.weight for particle in self.particles) or 1
        normalized_weights = [particle.weight / total_weight for particle in self.particles] # store the normalized weight for each particle

        new_particles = [ self.select_particle(normalized_weights) for _ in range(len(self.particles)) ]

        # update the particles to the newly sampled ones and add (deadreckoning?) noise
        for i, new_particle in enumerate(new_particles):
            if new_particle is None: # TODO: idk what's going on here, if NUM_PARTICLES is like 100 it's fine but if it's like 10 it's wonky??
                continue
            # TODO: understand noise better, it breaks if you don't add the noise here and idk why
            self.particles[i].x = new_particle.x + new_particle.noise_linear
            self.particles[i].y = new_particle.y + new_particle.noise_linear
            self.particles[i].theta = normalize_angle_radians(new_particle.theta + new_particle.noise_angular)
            self.particles[i].color = new_particle.color
            self.particles[i].weight = new_particle.weight

            # generate new noise for the next iteration
            self.particles[i].noise_linear = random.uniform(*PARTICLE_NOISE_LINEAR_RANGE)
            self.particles[i].noise_angular = random.uniform(*PARTICLE_NOISE_ANGULAR_RANGE)
            self.particles[i].noise_measurement = random.uniform(*PARTICLE_NOISE_MEASUREMENT_RANGE)

    # we want to do random selection with bias towards higher weighted particles
    def select_particle(self, weights) -> Robot:
        threshold = random.uniform(0, 1) # since weights are normalized, total weight is 1
        running_sum = 0
        
        # search for the particle in which the threshold falls into its range
        for i, weight in enumerate(weights):
            running_sum += weight
            if running_sum > threshold:
                return self.particles[i]

    def run_particle_filter(self) -> None:
        while True:
            # self.print_robot_and_particle_info()
            self.apply_movement()
            self.update_particle_weights()
            self.regenerate_particles()
            time.sleep(0.15)

        # debug: first frame (comment out the while loop above to see this)
        # for p in self.particles:
        #     print(p.x, p.y, p.theta, p.weight)

    # same as run_particle_filter but with a set number of time steps for testing and analysis
    def run_particle_filter_num_time_steps(self, time_steps: int) -> None:
        for _ in range(time_steps):
            # diagnostics
            self.print_robot_and_particle_info()
            self.difference_error.append(self.get_avg_particle_difference_err())

            # actual algorithm
            self.apply_movement()
            self.update_particle_weights()
            self.regenerate_particles()
            time.sleep(0.15)
        print("Finished running particle filter for", time_steps, "time steps. Stopping...")
    
    def print_robot_and_particle_info(self) -> None:
        robot = ["ROBOT (true position)",self.robot.x, self.robot.y, self.robot.theta]

        best_particle = max(self.particles, key=lambda p: p.weight)
        best = ["BEST PARTICLE", best_particle.x, best_particle.y, best_particle.theta]

        difference_err = ["AVG DIFFERENCE ERR (all particles)"] + self.get_avg_particle_difference_err()

        print(tabulate([robot, best, difference_err], headers=["", "X POSITION", "Y POSITION", "HEADING ANGLE"]))
        print("----------------------------------------------------------------------------------------------")
    
    def get_avg_particle_difference_err(self) -> List[float]:
        avg_x = sum(p.x for p in self.particles) / len(self.particles)
        avg_y = sum(p.y for p in self.particles) / len(self.particles)
        avg_theta = sum(p.theta for p in self.particles) / len(self.particles)
        difference_err = [abs(avg_x - self.robot.x), abs(avg_y - self.robot.y), abs(avg_theta - self.robot.theta)]
        return difference_err