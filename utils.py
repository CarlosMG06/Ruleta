import math

def point_on_circle(center, radius, angle_degrees):
    # Returns the x,y position at circle perimeter
    angle_radians = math.radians(angle_degrees)  # Convert angle to radians
    x = center[0] + radius * math.cos(angle_radians)  # X coordinate
    y = center[1] + radius * math.sin(angle_radians)  # Y coordinate
    return (x,y)

def is_point_in_rect(point, rectangle):
    return (rectangle["x"] <= point["x"] <= rectangle["x"] + rectangle["width"] and
            rectangle["y"] <= point["y"] <= rectangle["y"] + rectangle["height"])

def is_point_in_right_triangle(point, hypotenuse, orientation):
    p1, p2 = hypotenuse
    width = abs(p1[0]-p2[0])
    height = abs(p1[1]-p2[1])
    match orientation:
        case "top_left":
            return point["x"]*height + point["y"]*width - width*height < 0
        case "bottom_right":
            return point["x"]*height + point["y"]*width - width*height > 0
        case "top_right":
            return point["x"]*height + point["y"]*width > 0
        case "bottom_left":
            return point["x"]*height + point["y"]*width < 0