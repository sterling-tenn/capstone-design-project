# ----- Store configuration variables -----

ROBOT_STARTING_POS_X = 250
ROBOT_STARTING_POS_Y = 250
ROBOT_STARTING_HEADING = 0

# Particle Filter Configuration
NUM_OBSTACLES = 5
OBSTACLE_SEED = 45
NUM_PARTICLES = 100
WIDTH = 500
HEIGHT = 500

# Expected mean and standard deviation of the movement, heading and measurement noise
MOVEMENT_MEAN = 1
MOVEMENT_STDDEV = 1
HEADING_MEAN = 1
HEADING_STDDEV = 1
MEASUREMENT_MEAN = 1
MEASUREMENT_STDDEV = 1

# Standard Deviations
# Tune based on how much tolerance we want to give to comparing each particle to the robot distance and heading measurements
# The higher the sigma, the more tolerant we are to differences in measurements
DISTANCE_SIGMA = 3
HEADING_SIGMA = 3