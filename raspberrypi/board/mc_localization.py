import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class MCLocalization:
    def __init__(self, num_particles=1000, landmarks=None, world_size=(100, 100), 
                 standard_deviation_movement=0.1, standard_deviation_rotational=0.01):
        self.num_particles = num_particles
        self.world_size = world_size
        self.landmarks = landmarks or []
        self.sigma_m = standard_deviation_movement
        self.sigma_r = standard_deviation_rotational
        self.particles = self._init_particles()
        self.history = []

    def _init_particles(self) -> np.ndarray:
        particles = np.zeros((self.num_particles, 3))  # 3 = [x, y, theta]
        particles[:, 0] = np.random.uniform(0, self.world_size[0], size=self.num_particles)
        particles[:, 1] = np.random.uniform(0, self.world_size[1], size=self.num_particles)
        particles[:, 2] = np.random.uniform(0, 2 * np.pi, size=self.num_particles)
        return particles

    def _move_particles(self, move):
        move_noise = np.random.normal(0, self.sigma_m, size=(self.num_particles, 1))
        turn_noise = np.random.normal(0, self.sigma_r, size=self.num_particles)

        self.particles[:, 0] += move[0] * np.cos(self.particles[:, 2]) + move_noise[:, 0]
        self.particles[:, 1] += move[0] * np.sin(self.particles[:, 2]) + move_noise[:, 0]
        self.particles[:, 2] += move[1] + turn_noise

        self.particles[:, 0] = np.clip(self.particles[:, 0], 0, self.world_size[0])
        self.particles[:, 1] = np.clip(self.particles[:, 1], 0, self.world_size[1])

    def _sensor_update(self, sensors) -> np.ndarray:
        weights = np.ones(self.num_particles)

        for sensor in sensors:
            sensor_id = sensor['id']
            sigma_squared = sensor['sigma'] ** 2
            normalization_factor = 1.0 / (np.sqrt(2 * np.pi) * sensor['sigma'])

            for idx in range(self.num_particles):
                particle = self.particles[idx]
                particle_x, particle_y, particle_theta = particle

                closest_distance = float('inf')
                for landmark in self.landmarks:
                    dist_to_landmark = self._distance(particle, landmark)
                    if self._is_within_fov(particle, landmark, sensor):
                        if dist_to_landmark < closest_distance:
                            closest_distance = dist_to_landmark

                # If the closest distance is still infinity, set weight to a very small value
                if closest_distance == float('inf'):
                    weights[idx] *= 1e-6  # Small probability for invalid sensor readings
                else:
                    weight = normalization_factor * np.exp(-((closest_distance - sensor['value']) ** 2) / (2 * sigma_squared))
                    weights[idx] *= weight

        # Avoid NaN issues: If the sum of weights is zero, reset weights to a small uniform distribution
        weights_sum = np.sum(weights)
        if weights_sum == 0 or np.isnan(weights_sum):
            weights = np.ones(self.num_particles) / self.num_particles
        else:
            weights /= weights_sum  # Normalize the weights

        return weights


    def _is_withindwa_fov(self, particle, landmark, sensor):
        sensor_angle = particle[2]  # Orientation of the particle
        sensor_id = sensor['id']
        
        # Define the field of view for each sensor
        if sensor_id == 0:  # Forward-facing sensor
            angle_range = np.pi / 4  # 45 degrees field of view
        elif sensor_id == 1:  # Left side sensor
            angle_range = np.pi / 4
        elif sensor_id == 2:  # Right side sensor
            angle_range = np.pi / 4
        
        angle_to_landmark = np.arctan2(landmark[1] - particle[1], landmark[0] - particle[0])
        angle_diff = np.abs((angle_to_landmark - sensor_angle) % (2 * np.pi))

        return angle_diff < angle_range / 2 or angle_diff > (2 * np.pi - angle_range / 2)

    def _resample_particles(self, weights):
        if np.isnan(weights).any() or np.sum(weights) == 0:
            raise ValueError("Weights contain NaN or sum to zero.")
        
        indices = np.random.choice(self.num_particles, size=self.num_particles, p=weights)
        self.particles = self.particles[indices]

    def _get_position_estimate(self):
        mean_position = np.mean(self.particles, axis=0)
        return mean_position.tolist()

    def mcl(self, sensors, move):
        self._move_particles(move)  # Move particles based on control input
        weights = self._sensor_update(sensors)  # Update weights using sensor readings
        self._resample_particles(weights)  # Resample particles based on weights

        position_estimate = self._get_position_estimate()  # Get the estimated position
        self.history.append({
            'particles': self.particles.copy(),  # Store a copy of particles
            'position_estimate': position_estimate
        })
        return position_estimate

    def _distance(self, p, landmark):
        return np.sqrt((p[0] - landmark[0]) ** 2 + (p[1] - landmark[1]) ** 2)

# Simulation and GUI
def simulate_mcl():
    landmarks = [(20, 30), (50, 50), (80, 20), (90, 90)]  # Landmarks in the world
    mcl = MCLocalization(num_particles=500, landmarks=landmarks)

    fig, ax = plt.subplots()
    particles_scatter = ax.scatter([], [], color='blue', s=5, label='Particles')
    robot_scatter = ax.scatter([], [], color='red', s=50, label='Robot')
    landmarks_scatter = ax.scatter(*zip(*landmarks), color='green', s=100, marker='X', label='Landmarks')
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.legend()

    path = [[5 + i, 5 + i * 0.5] for i in range(20)]  # Robot's defined path

    def dynamic_sensors(robot_pos, robot_theta):
        """
        Calculate sensor readings with line-of-sight (LOS) and field-of-view (FOV) checks.
        """
        sensors = []
        sensor_fovs = [np.pi / 4, np.pi / 4, np.pi / 4]  # 45-degree FOV for each sensor
        sensor_angles = [0, np.pi / 2, -np.pi / 2]  # Forward, left, and right sensor angles

        for sensor_id, sensor_angle in enumerate(sensor_angles):
            fov = sensor_fovs[sensor_id]
            closest_distance = float('inf')
            for landmark in landmarks:
                # Calculate distance to the landmark
                dist = np.sqrt((robot_pos[0] - landmark[0]) ** 2 + (robot_pos[1] - landmark[1]) ** 2)
                
                # Check if the landmark is within the sensor's FOV
                angle_to_landmark = np.arctan2(landmark[1] - robot_pos[1], landmark[0] - robot_pos[0])
                relative_angle = (angle_to_landmark - robot_theta - sensor_angle + np.pi) % (2 * np.pi) - np.pi
                
                # If the landmark is within the FOV, update the closest distance
                if abs(relative_angle) <= fov / 2:
                    if dist < closest_distance:
                        closest_distance = dist

            # If a landmark is within LOS, record the sensor value (with noise), otherwise, max range
            sensor_value = closest_distance + np.random.normal(0, 0.5) if closest_distance != float('inf') else 100.0
            sensors.append({'id': sensor_id, 'value': sensor_value, 'sigma': 1.5})  # Assign sensor readings
        return sensors

    def update(frame):
        # Robot's current position along a predefined path
        robot_pos = path[frame % len(path)]
        robot_theta = 0  # For simplicity, assume no rotation in this example
        
        # Get dynamic sensor readings based on robot's current position and orientation
        sensors = dynamic_sensors(robot_pos, robot_theta)

        # Update the MCL localization based on the dynamic sensor readings
        move = [2.0, 0.05]  # Control inputs: move forward, small rotation
        estimated_position = mcl.mcl(sensors, move)

        # Update particles' positions
        particles = mcl.particles
        particles_scatter.set_offsets(particles[:, :2])

        # Update robot's scatter plot (moving along the path)
        robot_scatter.set_offsets([robot_pos])

        return particles_scatter, robot_scatter

    ani = FuncAnimation(fig, update, frames=len(path), interval=200)
    plt.show()

if __name__ == '__main__':
    simulate_mcl()