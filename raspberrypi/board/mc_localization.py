import numpy as np
import conf as conf
import random

class MCLocalization:
    def __init__(self, map, num_particles=1024):
        self.reset = False
        self.num_particles = num_particles
        self._map = map["obstacles"]
        self._world_size = map["dimensions"]
        self._particles = self._init_particles(self.num_particles)

    def _init_particles(self, num_particles) -> np.ndarray:
        particles = np.zeros((num_particles, 3))  # 3 = [x, y, theta]
        particles[:, 0] = np.random.uniform(0, self._world_size[0], size=num_particles)
        particles[:, 1] = np.random.uniform(0, self._world_size[1], size=num_particles)
        particles[:, 2] = np.random.uniform(0, 2 * np.pi, size=num_particles)

        print(particles)
        return particles                      

    def _move_particles(self, move):
        self._particles[:, 0] += move[0]
        self._particles[:, 1] += move[1]
        self._particles[:, 2] += move[2]

        self._particles[:, 0] = np.clip(self._particles[:, 0], 0, self._world_size[0])
        self._particles[:, 1] = np.clip(self._particles[:, 1], 0, self._world_size[1])

    def _update_particle_weights(self, sensors) -> np.ndarray:
        weights = np.ones(self.num_particles)

        for sensor in sensors:
            sensor_id = sensor.get_id()
            sigma_squared = conf.SENSOR_SIGMA ** 2
            normalization_factor = 1.0 / (np.sqrt(2 * np.pi) * conf.SENSOR_SIGMA)

            for idx in range(self.num_particles):
                particle = self._particles[idx]

                closest_distance = float('inf')
                for landmark in self._map:
                    dist_to_landmark = self._distance(particle, landmark)
                    if dist_to_landmark < closest_distance:
                        closest_distance = dist_to_landmark

                # If the closest distance is still infinity, set weight to a very small value
                if closest_distance == float('inf'):
                    weights[idx] *= conf.NULL_WEIGHT
                else:
                    weight = normalization_factor * np.exp(-((closest_distance - sensor.get_distance()) ** 2) / (2 * sigma_squared))    

                weights[idx] *= weight

        # Avoid NaN issues: If the sum of weights is zero, reset weights to a small uniform distribution
        weights_sum = np.sum(weights)
        if weights_sum == 0 or np.isnan(weights_sum):
            weights = np.ones(self.num_particles) / self.num_particles
        else:
            weights /= weights_sum  # Normalize the weights

        return weights

    def _resample_particles(self, weights):
        # Neff = 1.0 / np.sum(weights**2)

        # # Check if resampling is necessary (if Neff is too low, increase the number of particles)
        # if Neff < self.num_particles / 2:
        #     self.num_particles <<= 1 

        indices = random.choices(range(self.num_particles), k=self.num_particles, weights=weights)
        
        ret = np.array([self._particles[i] for i in indices])  # Convert list to NumPy array
        
        return ret

    def _distance(self, p, landmark):
        return np.sqrt((p[0] - landmark[0]) ** 2 + (p[1] - landmark[1]) ** 2) * conf.MAP_SCALE
    
    def _get_position_mean(self):
        mean = np.mean(self._particles, axis=0)
        return mean
    
    def _get_std_dev(self):
        deviation = np.std(self._particles, axis=0)
        return deviation

    def mcl(self, sensors, move):
        self._move_particles(move)  # Move particles based on control input | MOVE = [dx, dy, dtheta]
        weights = self._update_particle_weights(sensors)  # Update weights using sensor readings
        self._particles = self._resample_particles(weights)  # Resample particles based on weights

        position_estimate = self._get_position_mean()  # Get the estimated position
        std_dev = self._get_std_dev()
        return position_estimate, std_dev 


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    class FakeSensor:
        def __init__(self, noise=0.5, id=None):
            self.faux_sensor_readings = [0.0, 1.0]
            self.noise = noise
            self.id = id
            self.distance = self.update_distance()

        def update_distance(self):
            return self.faux_sensor_readings.pop(0) + random.uniform(-self.noise, self.noise)
        
        def get_id(self):
            return self.id
        
        def get_distance(self):
            return self.distance

    def plot_particles(particles, landmarks, estimated_position):
        plt.figure(figsize=(8, 8))
        plt.xlim(0, 10)
        plt.ylim(0, 10)
        
        # Plot landmarks
        for landmark in landmarks:
            plt.scatter(landmark[0], landmark[1], c='black', marker='s', s=100, label='Landmark')
        
        # Plot particles
        plt.scatter(particles[:, 0], particles[:, 1], c='red', s=5, alpha=0.5, label='Particles')
        
        # Plot estimated position
        plt.scatter(estimated_position[0], estimated_position[1], c='green', marker='o', s=100, label='Estimate')
        
        plt.legend()
        plt.show()

    # Create a test map with landmarks
    test_map = {
        "dimensions": (10, 10),  # World size
        "obstacles": [(2, 3), (5, 5), (7, 8)]  # Landmarks
    }

    # Initialize MCL algorithm
    mcl = MCLocalization(test_map, num_particles=10)

    # Fake sensors at each landmark
    sensors = [FakeSensor()]

    # Simulated movement (dx, dy, dtheta)
    movement = [0.5, 0.2, 0.1]

    print(mcl._particles)

    # Run the MCL algorithm
    estimated_position, std = mcl.mcl(sensors, movement)

    print(estimated_position)
    print(mcl._particles)

    # Display the result
    plot_particles(mcl._particles, test_map["obstacles"], estimated_position)