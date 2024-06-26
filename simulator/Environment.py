import pygame
import math
import sys

class Environment:
    def __init__(self, width, height, obstacles, robot, particles):
        pygame.init()

        self.width = width
        self.height = height
        self.obstacles = obstacles
        self.robot = robot
        self.particles = particles

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Monte Carlo Localization - Particle Filter")

        self.clock = pygame.time.Clock()

        # Set up colors
        self.white = (255, 255, 255)
        self.blue = (0, 0, 255)
        self.red = (255, 255, 0)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)

        self.draw_robot_measurements = False
        self.draw_circle_measurements = False
        self.draw_particles = True

    def draw_obstacle(self, x, y, width, height):
        half_width = width / 2.0
        half_height = height / 2.0
        pygame.draw.rect(self.screen, self.blue, (x-half_width, y-half_height, width, height))

    def draw_agent(self, x, y, theta, radius, color):
        line_length = 25
        pygame.draw.circle(self.screen, color, [x, y], radius, 0)
        pygame.draw.line(self.screen, self.black, [x, y], [x + line_length * math.cos(theta), y + line_length * math.sin(theta)], 2)

    def draw_robot_obstacles_measurements(self, obstacle_x, obstacle_y):
        pygame.draw.line(self.screen, (255, 158, 158, 1), [self.robot.x, self.robot.y], [obstacle_x, obstacle_y], 2)

    def draw_circle_obstacles_measurements(self, obstacle_x, obstacle_y, radius):
        pygame.draw.circle(self.screen, (37,156,198,255), [obstacle_x, obstacle_y], radius, 2)
        

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_m]:
                if self.draw_robot_measurements == False:
                    self.draw_robot_measurements = True
                else:
                    self.draw_robot_measurements = False

            if keys[pygame.K_c]:
                if self.draw_circle_measurements == False:
                    self.draw_circle_measurements = True
                else:
                    self.draw_circle_measurements = False

            if keys[pygame.K_p]:
                if self.draw_particles == False:
                    self.draw_particles = True
                else:
                    self.draw_particles = False

            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

            # Draw obstacles on the screen
            self.screen.fill((self.white))
            for obstacle in self.obstacles:
                self.draw_obstacle(obstacle[0], obstacle[1], 20, 20)


            #Draw particles on the screen
            if self.draw_particles:
                for particle in self.particles:
                    self.draw_agent(particle.x, particle.y, particle.theta, 10, particle.color)
            
            # Draw robot's measurement
            if self.draw_robot_measurements:
                for obstacle in self.obstacles:
                    self.draw_robot_obstacles_measurements(obstacle[0], obstacle[1])

            if self.draw_circle_measurements:
                for obstacle in self.obstacles:
                    self.draw_circle_obstacles_measurements(obstacle[0], obstacle[1], math.sqrt((obstacle[0] - self.robot.x)**2 + (obstacle[1] - self.robot.y)**2))
                    

            # Draw the robot on the screen
            self.draw_agent(self.robot.x, self.robot.y, self.robot.theta, 10, self.robot.color)

            # Update display
            pygame.display.flip()

            # Control the game loop speed
            self.clock.tick(30)