import numpy as np
import conf as conf
import random
import math

class MCLocalization:
    def __init__(self, map, start_position, num_particles=1024):
        self.start_position = np.array(start_position)
        self.num_particles = num_particles
        self._map = np.array(map["obstacles"])
        self._world_size = np.array(map["dimensions"])
        self._particles = self._init_particles(num_particles)

    def _init_particles(self, num_particles) -> np.ndarray:
        particles = np.zeros((num_particles, 3))  # [x, y, theta]

        # Properly generate random positions per particle
        particles[:, 0] = np.random.normal(self.start_position[0], conf.INIT_POS_SIGMA, num_particles)
        particles[:, 1] = np.random.normal(self.start_position[1], conf.INIT_POS_SIGMA, num_particles)
        particles[:, 2] = np.random.normal(self.start_position[2], conf.INIT_POS_SIGMA, num_particles)  # Angle variation

        # Ensure particles stay within world bounds
        particles[:, 0] = np.clip(particles[:, 0], 0, self._world_size[0])
        particles[:, 1] = np.clip(particles[:, 1], 0, self._world_size[1])

        # print("particles:", particles)

        return particles                      

    def _move_particles(self, move):
        self._particles[:, 0] += move[0]
        self._particles[:, 1] += move[1]
        self._particles[:, 2] += move[2]

        # Keep within bounds
        self._particles[:, 0] = np.clip(self._particles[:, 0], 0, self._world_size[0])
        self._particles[:, 1] = np.clip(self._particles[:, 1], 0, self._world_size[1])

        # Ensure angles stay within -π to π
        self._particles[:, 2] = (self._particles[:, 2] + np.pi) % (2 * np.pi) - np.pi

    def _update_particle_weights(self, sensors) -> np.ndarray:
        weights = np.ones(self.num_particles)

        for sensor in sensors:
            sigma_squared = conf.SENSOR_SIGMA ** 2
            normalization_factor = 1.0 / (np.sqrt(2 * np.pi) * conf.SENSOR_SIGMA)

            for idx in range(self.num_particles):
                particle = self._particles[idx]
                particle_x, particle_y, particle_theta = particle  # Unpack pose

                visible_landmarks = [
                    landmark for landmark in self._map
                    if self._is_in_field_of_view(particle, landmark)
                ]

                if len(visible_landmarks) > 0:
                    closest_distance = min(self._distance(particle, landmark) for landmark in visible_landmarks)
                    measured_distance = sensor.get_distance()

                    # Apply Gaussian probability model
                    weight = normalization_factor * np.exp(-((closest_distance - measured_distance) ** 2) / (2 * sigma_squared))

                    # Angle penalty: Reduce weight if the landmark is not in the correct forward-facing direction
                    expected_angle = np.arctan2(visible_landmarks[0][1] - particle_y, visible_landmarks[0][0] - particle_x)
                    angle_diff = abs(expected_angle - particle_theta)
                    angle_penalty = np.exp(-angle_diff ** 2 / (2 * (np.pi / 8) ** 2))  # Penalize deviations > 22.5 degrees

                    weights[idx] *= weight * angle_penalty

                else: 
                    weights[idx] = conf.NULL_WEIGHT

        # Normalize weights, handle zero weights
        weights_sum = np.sum(weights)
        if weights_sum == 0 or np.isnan(weights_sum):
            weights.fill(1.0 / self.num_particles)  # Uniform distribution
        else:
            weights /= weights_sum  

        return weights

    def _is_in_field_of_view(self, particle, landmark) -> bool:
        """Checks if a landmark is within the sensor's field of view."""
        particle_x, particle_y, particle_theta = particle
        landmark_x, landmark_y = landmark

        angle_to_landmark = np.arctan2(landmark_y - particle_y, landmark_x - particle_x)
        angle_diff = abs(angle_to_landmark - particle_theta)

        return angle_diff < (conf.SENSOR_FOV_ANGLE / 2)  # Check if within half the field of view

    def _resample_particles(self, weights):
        # print("Weights:", weights)
        indices = random.choices(range(self.num_particles), k=self.num_particles, weights=weights)

        ret = []
        for i in indices:
            ret.append(self._particles[i])
        ret = np.array([self._particles[i] for i in indices])  # Convert list to NumPy array

        # print("particles:", ret)

        return ret

    def _distance(self, p, landmark):
        return np.sqrt((p[0] - landmark[0]) ** 2 + (p[1] - landmark[1]) ** 2) * conf.MAP_SCALE
    
    def _get_position_mean(self):
        return np.mean(self._particles, axis=0)
    
    def _get_std_dev(self):
        return np.std(self._particles, axis=0)

    def mcl(self, sensors, move):
        self._move_particles(move)  
        weights = self._update_particle_weights(sensors)  
        self._particles = self._resample_particles(weights)  

        # position_estimate = self._get_position_mean()  
        # std_dev = self._get_std_dev()
        # return position_estimate, std_dev 




if __name__ == "__main__":
    import matplotlib.pyplot as plt

    class FakeSensor:
        def __init__(self, noise=0.025, max_distance=15):
            self.noise = noise
            self.max_distance = max_distance  # Maximum distance the sensor can measure
            self.distance = max_distance  # To be updated with each reading
        
        def get_id(self):
            return "FakeSensor"
        def update_distance(self, position, theta, obstacles):
            """
            Update the distance based on the robot's position and heading (theta).
            The distance is calculated to the closest obstacle in the direction of theta.
            """
            # Raycast in the direction of theta to find the distance to the closest obstacle
            x, y = position
            dx = math.cos(math.radians(theta))  # Direction vector along X-axis
            dy = math.sin(math.radians(theta))  # Direction vector along Y-axis
            
            # We will iterate in small steps along the direction of movement to find the obstacle
            step_size = 0.25  # Step size for raycasting
            current_distance = 0.0
            
            while current_distance < self.max_distance:
                current_distance += step_size
                check_x = x + dx * current_distance
                check_y = y + dy * current_distance
                
                # Check if the current point is an obstacle
                if (round(check_x), round(check_y)) in obstacles:
                    # If an obstacle is found, set the distance to this point
                    self.distance = current_distance
                    break
            else:
                # If no obstacle is found, set the distance to the maximum sensor range
                self.distance = self.max_distance
            
            # Add some noise to the sensor reading to simulate real-world inaccuracies
            self.distance += random.uniform(-self.noise, self.noise)
        
        def get_distance(self):
            """Return the current sensor reading."""
            return self.distance

    def plot_particles(particles, landmarks, estimated_position, theoretical_position):
        plt.figure(figsize=(8, 8))
        plt.xlim(0, 10)
        plt.ylim(0, 10)

        # Plot landmarks
        for landmark in landmarks:
            plt.scatter(*landmark, c='black', marker='s', s=100, label='Landmark')

        # Plot particle orientations (theta) as arrows
        for particle in particles:
            x, y, theta = particle
            dx = np.cos(theta) * 0.15  # Adjust the multiplier for arrow length
            dy = np.sin(theta) * 0.15
            plt.arrow(x, y, dx, dy, head_width=0.1, head_length=0.1, fc='red', ec='red')

        # Plot estimated position with heading (only the arrow)
        estimated_x, estimated_y, estimated_theta = estimated_position
        estimated_dx = np.cos(estimated_theta) * 0.5  # Smaller arrow length
        estimated_dy = np.sin(estimated_theta) * 0.5
        plt.arrow(estimated_x, estimated_y, estimated_dx, estimated_dy, head_width=0.2, head_length=0.25, fc='green', ec='green')

        # Plot theoretical position with heading (only the arrow)
        theoretical_x, theoretical_y, theoretical_theta = theoretical_position
        theoretical_dx = np.cos(theoretical_theta) * 0.5  # Smaller arrow length
        theoretical_dy = np.sin(theoretical_theta) * 0.5
        plt.arrow(theoretical_x, theoretical_y, theoretical_dx, theoretical_dy, head_width=0.2, head_length=0.25, fc='purple', ec='purple')

        plt.show()

    # Test map
    test_map = {
        "dimensions": (10, 10),  
        "obstacles": [
            # Borders
            *[(x, 0) for x in range(10)],  # Bottom border
            *[(x, 9) for x in range(10)],  # Top border
            *[(0, y) for y in range(10)],  # Left border
            *[(9, y) for y in range(10)],  # Right border
            
            # Clustered obstacles
            (3, 3), (3, 4), (4, 3), (4, 4),  # Square block
            (6, 6), (6, 7), (7, 6), (7, 7),  # Another square
            # Random obstacles
            (2, 6), (5, 2), (8, 3)
        ]  
    }

    # Initialize MCL algorithm
    start_position = [4.0, 7.0, -45.0]
    mcl = MCLocalization(test_map, start_position, num_particles=1000)

    # Fake sensors
    sensors = [FakeSensor() for _ in range(1)]

    # Movement sequence for multiple steps
    movements = [
        [0.5, -0.5, -0],  # Move 1: dx=1, dy=-1, dtheta=90
        [0.5, -0.5, -0],  # Move 2: dx=1, dy=1, dtheta=-45
        [0.5, -0.5, -0],  # Move 3: dx=-1, dy=0, dtheta=45
        [0.5, -0.5, -0],   # Move 4: dx=0, dy=-2, dtheta=90
        [0.5, -0.5, -0],  # Move 3: dx=-1, dy=0, dtheta=45
        [0.5, -0.5, -0]   # Move 4: dx=0, dy=-2, dtheta=90
    ]

    # Simulate multiple steps
    theoretical_position = np.array(mcl.start_position)
    for step, move in enumerate(movements, start=1):
        print(f"\nStep {step}:")
        # print("Initial Particles:\n", mcl._particles)

        # Run MCL
        estimated_position, std = mcl.mcl(sensors, move)
        theoretical_position = theoretical_position + np.array(move)

        for sensor in sensors:
            sensor.update_distance(theoretical_position[:2], theoretical_position[2], test_map["obstacles"])
            print(f"Sensor {sensor.get_id()} distance: {sensor.get_distance()}")

        print("Theoretical Position:", theoretical_position)
        print("Estimated Position:", estimated_position)
        # print("Updated Particles:\n", mcl._particles)

        # Show results for this step
        plot_particles(mcl._particles, test_map["obstacles"], estimated_position, theoretical_position)
