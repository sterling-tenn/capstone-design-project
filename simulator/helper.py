import math

# return value at x, of a normal distribution pdf N(mu, sigma)
def normal_distribution(mu, sigma, x):
    exponent = -((x - mu) ** 2) / (2 * sigma ** 2)
    return math.exp(exponent) / math.sqrt(2 * math.pi * sigma ** 2)

# Ensure the angle is within the range [-pi, pi]
def normalize_angle_radians(angle):
    normalized_angle = angle % (2 * math.pi)

    if normalized_angle > math.pi:
        normalized_angle -= 2 * math.pi

    return normalized_angle