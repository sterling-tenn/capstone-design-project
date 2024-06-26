from typing import *
from Robot import Robot
from helper import *
import random
from conf import *

class ParticleFilter(object):
    def __init__(self, num_particles: int, robot: Robot, obstacles: List[Tuple[float, float]], width: int, height: int) -> None:
        self.num_particles = num_particles
        self.robot = robot
        self.obstacles = obstacles # act as reference points for the robot to estimate its position

        # to distribute the particles along position
        self.width = width
        self.height = height

        self.particles = self.create_particles()
        self.normalize_particle_weights()

    # particles are essentially just simulated robots
    def create_particles(self) -> List[Robot]:
        particles = []
        for _ in range(self.num_particles):
            particle = Robot(
                x = random.randint(0, self.width),
                y = random.randint(0, self.height),
                heading = random.uniform(-180, 180),

                # each particle follows the same error distribution as the robot
                movement_error = 0,
                heading_error = 0,
                measurement_error = 0
            )
            particles.append(particle)
        return particles

    # should be provided either distance or rotation, not both (one of them should be 0)
    def move_robot(self, distance: float, rotation: float) -> None:
        self.robot.move(distance, rotation, self.width, self.height)
        
        # regenerate robot's error parameters for next movement
        self.robot.movement_error = random.gauss(MOVEMENT_ERR_MEAN, MOVEMENT_ERR_STDDEV * math.sqrt(distance)) # we want to scale variance by distance
        self.robot.heading_error = random.gauss(HEADING_ERR_MEAN, HEADING_ERR_STDDEV * math.sqrt(rotation))
        self.robot.measurement_error = random.gauss(MEASUREMENT_ERR_MEAN, MEASUREMENT_ERR_STDDEV * math.sqrt(distance))

    # should be provided either distance or rotation, not both (one of them should be 0)
    def move_particles(self, distance: float, rotation: float) -> None:
        for particle in self.particles:
            particle.move(distance, rotation, self.width, self.height)

            # regenerate particle's error parameters for next movement
            particle.movement_error = random.gauss(MOVEMENT_ERR_MEAN, MOVEMENT_ERR_STDDEV * math.sqrt(distance))
            particle.heading_error = random.gauss(HEADING_ERR_MEAN, HEADING_ERR_STDDEV * math.sqrt(rotation))
            particle.measurement_error = random.gauss(MEASUREMENT_ERR_MEAN, MEASUREMENT_ERR_STDDEV * math.sqrt(distance))

    # sample particles
    def update_particle_weightings(self) -> None:
        # get the robot's measurements
        robot_distances = self.robot.obstacle_distances(self.obstacles)

        # for each particle, check how good of an estimation it is compared to the robot's reported distance and heading
        for particle in self.particles:
            likelyhood = 1 # using 1 as a percentages, how good of an estimation is this specific particle?
            particle_distances = particle.obstacle_distances(self.obstacles)

            # scale likelyhood using a normal distribution with the actual robot's measurements as a reference point
            for robot_dist, particle_dist in zip(robot_distances, particle_distances): # compare all distances
                likelyhood *= normal_distribution(robot_dist, DISTANCE_SIGMA, particle_dist)
            likelyhood *= normal_distribution(self.robot.heading, HEADING_SIGMA, particle.heading) # compare heading angles

            particle.weight = likelyhood
        
        # normalize likelyhoods so the sum of all the particles' likelyhoods is 1 (convert to probability)
        self.normalize_particle_weights()

    # create new generation of particles, based on the previous generation's performance
    def regenerate_particles(self) -> None:
        new_particles = []

        for _ in self.particles:
            new_particle = self.select_particle()
            new_particles.append(new_particle)
        
        self.particles = new_particles

    # higher weighted particles have a higher chance of being selected
    def select_particle(self) -> Robot:
        total_weight = sum(particle.weight for particle in self.particles)

        # we want to do random selection with bias towards higher weighted particles
        threshold = random.uniform(0, total_weight)

        # search for the particle in which the threshold falls into its range
        running_sum = 0
        for particle in self.particles:
            running_sum += particle.weight
            if running_sum > threshold:
                return particle

        # should never get here
        return None
    
    # ensure weights of all particles sum up to 1
    def normalize_particle_weights(self) -> None:
        total_weight = sum(particle.weight for particle in self.particles)
        for particle in self.particles:
            particle.weight /= total_weight

# generate random obstacles within the given width and height of the particle filter
def generate_obstacles(n: int, width: int, height: int, seed: int = None) -> List[Tuple[float, float]]:
    if seed is not None:
        random.seed(seed)
    
    coordinates = []
    for _ in range(n):
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        coordinates.append((x, y))
    
    return coordinates
