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

    # particles are essentially just simulated robots
    def create_particles(self) -> List[Robot]:
        particles = []
        for _ in range(self.num_particles):
            particle = Robot(
                x = random.randint(0, self.width),
                y = random.randint(0, self.height),
                heading = random.uniform(HEADING_RANGE[0], HEADING_RANGE[1]),

                # each particle follows the same error distribution as the robot
                movement_error = random.uniform(MOVEMENT_NOISE[0], MOVEMENT_NOISE[1]),
                heading_error = random.uniform(HEADING_NOISE[0], HEADING_NOISE[1]),
                measurement_error = random.uniform(MEASUREMENT_NOISE[0], MEASUREMENT_NOISE[1])
            )
            particles.append(particle)
        return particles

    def apply_movement(self):
        dist = random.uniform(MOVEMENT_DIST[0], MOVEMENT_DIST[1])
        rot = random.uniform(HEADING_ROTATION[0], HEADING_ROTATION[1])

        # move the robot
        self.robot.move(dist, rot, self.width, self.height)

        # move each particle
        for particle in self.particles:
            particle.move(dist, rot, self.width, self.height)

    def update_particle_weightings(self):
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

    def regenerate_particles(self):
        # normalize the weights
        total_weight = sum(particle.weight for particle in self.particles)
        if total_weight == 0:
            total_weight = 1
        
        # scaled weight corresponding to each particle
        normalized_weight = [particle.weight / total_weight for particle in self.particles] # sum equals 1

        # regenerate particles based on their weight
        new_particles = []
        for _ in range(self.num_particles):
            particle_index = self.select_particle(normalized_weight)
            if not particle_index:
                continue
            
            # TODO: check if this is correct
            self.particles[particle_index].weight = 0 # reset the weight of the selected particle, will be recalculated in the next iteration
            
            new_particles.append(self.particles[particle_index])

        # update the particles with the new set
        for i, particle in enumerate(self.particles):
            particle.x = new_particles[i].x
            particle.y = new_particles[i].y
            particle.heading = normalize_angle_degrees(new_particles[i].heading)
            particle.weight = new_particles[i].weight

            # apply new noise
            particle.movement_error = random.uniform(MOVEMENT_NOISE[0], MOVEMENT_NOISE[1])
            particle.heading_error = random.uniform(HEADING_NOISE[0], HEADING_NOISE[1])
            particle.measurement_error = random.uniform(MEASUREMENT_NOISE[0], MEASUREMENT_NOISE[1])

    # we want to do random selection with bias towards higher weighted particles
    def select_particle(self, weights) -> int:
        threshold = random.uniform(0, 1) # since weights are normalized, total weight is 1
        running_sum = 0
        
        # search for the particle in which the threshold falls into its range
        for i, weight in enumerate(weights):
            running_sum += weight
            if running_sum > threshold:
                return i

        return None

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
