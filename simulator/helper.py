import math

# return value at x, of a normal distribution pdf N(mu, sigma)
def normal_distribution(mu, sigma, x):
    exponent = -((x - mu) ** 2) / 2 * sigma ** 2
    return math.exp(exponent) / math.sqrt(2 * math.pi * sigma ** 2)