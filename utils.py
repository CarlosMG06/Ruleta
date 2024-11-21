import math

def point_on_circle(center, radius, angle_degrees):
    # Returns the x,y position at circle perimeter
    angle_radians = math.radians(angle_degrees)  # Convert angle to radians
    x = center[0] + radius * math.cos(angle_radians)  # X coordinate
    y = center[1] + radius * math.sin(angle_radians)  # Y coordinate
    return (x,y)

def is_point_in_circle(point, center, r):
    distancia = math.sqrt((point["x"] - center["x"]) ** 2 + (point["y"] - center["y"]) ** 2)
    return distancia <= r

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

def triangle_area(x1, y1, x2, y2, x3, y3):
    '''Calcula el area de un triángulo a partir de sus vértices.'''
    return abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)) / 2
        
def is_point_in_triangle(point, vertices):
    '''Calcula si el punto está dentro del triángulo (definido por sus vértices).'''
    x1 = vertices[0][0]
    y1 = vertices[0][1]
    x2 = vertices[1][0]
    y2 = vertices[1][1]
    x3 = vertices[2][0]
    y3 = vertices[2][1]
    area = triangle_area(x1, y1, x2, y2, x3, y3)
    xp = point['x']
    yp = point['y']

    # Calculamos el area de los 3 triángulos formados por nuestro punto (xp, yp) y otros dos puntos vértices.
    a1 = triangle_area(xp, yp, x1, y1, x2, y2)
    a2 = triangle_area(xp, yp, x2, y2, x3, y3)
    a3 = triangle_area(xp, yp, x1, y1, x3, y3)
    # Si el punto está dentro del triángulo, la suma de estas 3 areas debe ser igual al area original.
    return round(a1 + a2 + a3, 10) == round(area, 10) # Redondeamos los resultados a 10 decimales para poder compararlos