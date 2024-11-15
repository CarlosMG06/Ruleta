import math

def point_on_circle(center, radius, angle_degrees):
    # Returns the x,y position at circle perimeter
    angle_radians = math.radians(angle_degrees)  # Convert angle to radians
    x = center[0] + radius * math.cos(angle_radians)  # X coordinate
    y = center[1] + radius * math.sin(angle_radians)  # Y coordinate
    return { "x": x, "y": y }