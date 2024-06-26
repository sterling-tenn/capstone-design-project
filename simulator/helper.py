import math

# return value at x, of a normal distribution pdf N(mu, sigma)
def normal_distribution(mu, sigma, x):
    exponent = -((x - mu) ** 2) / (2 * sigma ** 2)
    return math.exp(exponent) / math.sqrt(2 * math.pi * sigma ** 2)

def euclidian_distance(dest_x: float, dest_y: float, source_x: float, source_y: float, measurement_error: float):
    return math.sqrt((dest_x - source_x) ** 2 + (dest_y - source_y) ** 2 + measurement_error)

def cos(angle):
    return math.cos(angle*math.pi/180)

def sin(angle):
    return math.sin(angle*math.pi/180)
