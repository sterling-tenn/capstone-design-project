import math

def euclidian_distance(dest_x: float, dest_y: float, source_x: float, source_y: float, measurement_error: float):
    return math.sqrt((dest_x - source_x) ** 2 + (dest_y - source_y) ** 2 + measurement_error)

def cos(angle):
    return math.cos(angle*math.pi/180)

def sin(angle):
    return math.sin(angle*math.pi/180)