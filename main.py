import math
import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import utils

WHITE = (255, 255, 255)
LIGHT_GRAY = (204, 204, 204)
GRAY = (128, 128, 128)
DARK_GRAY = (51, 51, 51)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 85, 17)
GREEN = (0, 255, 0)
GOLD = (255, 128, 0)
DARK_GOLD = (128, 64, 0)
#BLUE  = (0, 0, 255)
#PURPLE = (128, 0, 128)
#ORANGE = (255, 165, 0) 
BROWN = (102, 68, 34)

number_order = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27,
    13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 
    20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

roulette = {"position": (10,10), "radius": 150,
"angle_offset": 360/37/2, "spin_speed": 0, "spin_acc": -100,
"about_to_spin": False, "spin_canceled": False, "spinning": False, "readjusting": False}

roulette_surface = pygame.Surface((roulette["radius"]*2 + 40,roulette["radius"]*2))
roulette_surface.fill(DARK_GREEN)

current_number = 0

spin_counter = 0

spin_button = {
    "x": roulette["position"][0] + roulette["radius"] - 40,
    "y": roulette["position"][1] + roulette["radius"] * 2.5 - 15,
    "width": 80, "height": 30}

board = {"x": 350, "y": 20, "columns": 4, "rows": 12, "table_x": 50,
"cell": {"width": 28, "height": roulette["radius"]/3}, "ellipse": {"width": 22, "height": 40}}

grid_size = (board["cell"]["width"] * board["rows"], board["cell"]["height"] * board["columns"])
grid_surface = pygame.Surface(grid_size)
grid_surface.fill(DARK_GREEN)

board_size = (grid_size[0]+board["table_x"]+board["cell"]["width"]*1.5,grid_size[1])
board_surface = pygame.Surface(board_size)
board_surface.fill(DARK_GREEN)

mouse = {"x": -1, "y": -1, 
"pressed": False, "held": False, "released": False}

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption('Window Title')

font_small = pygame.font.SysFont("Arial", 15, bold=True)
font_medium = pygame.font.SysFont("Arial", 18, bold=True)
font_big = pygame.font.SysFont("Arial", 27, bold=True)
font_serif = pygame.font.SysFont("Times New Roman", 21)

# Bucle de l'aplicació
def main():
    is_looping = True

    update_roulette()
    init_grid_surface()

    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()

        clock.tick(60) # Limitar a 60 FPS

    # Fora del bucle, tancar l'aplicació
    pygame.quit()
    sys.exit()

# Gestionar events
def app_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Botó tancar finestra
            return False
        elif event.type == pygame.MOUSEMOTION:
            mouse["x"], mouse["y"] = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse["pressed"] = True
            mouse["held"] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse["held"] = False
            mouse["released"] = True
    return True

# Fer càlculs
def app_run():
    delta_time = clock.get_time() / 1000.0
    
    if utils.is_point_in_rect(mouse, spin_button) and not roulette["spinning"]:
        if mouse["pressed"]:
            # La ruleta gira una miqueta com a anticipació per fer efecte
            roulette["spin_speed"] = -50
            roulette["about_to_spin"] = True
        if mouse["released"] and roulette["about_to_spin"]:
            acc = abs(roulette["spin_acc"])
            angular_displacement = random.randint(541,900) #Gira entre 1.5 i 2.5 revolucions
            roulette["spin_speed"] = math.sqrt(angular_displacement*2/acc)*acc #Càlcul MCUA
            roulette["spinning"] = True
            roulette["about_to_spin"] = False
    elif roulette["about_to_spin"]:
        # Si el mouse es mou fora del botó abans de deixar anar, la ruleta torna a la seva posició inicial
        roulette["spin_speed"] = math.sqrt((-50)**2 - roulette["spin_speed"]**2) #Càlcul MCUA
        roulette["about_to_spin"] = False
        roulette["spin_canceled"] = True

    if roulette["spin_speed"] != 0:
        spin_roulette(delta_time)
    elif roulette["readjusting"]:
        readjust_roulette()
        global spin_counter
        spin_counter += 1

    mouse["pressed"] = False
    mouse["released"] = False

# Girar la ruleta
def spin_roulette(delta_time):
    sign = 1 if roulette["spin_speed"] > 0 else -1
    if abs(roulette["spin_speed"]) > 0.5:
        roulette["spin_speed"] += sign * roulette["spin_acc"] * delta_time
    else:
        if roulette["spinning"]:
            roulette["spinning"] = False 
            roulette["readjusting"] = True
        elif roulette["readjusting"]:
            roulette["readjusting"] = False
        elif roulette["spin_canceled"]:
            roulette["spin_canceled"] = False
        roulette["angle_offset"] %= 360
        roulette["spin_speed"] = 0
    roulette["angle_offset"] += roulette["spin_speed"] * delta_time

# Ajustar la ruleta després de girar per tornar a alinear la casella amb la fletxa
def readjust_roulette():
    adjustment = (roulette["angle_offset"] - 360/37/2) % (360/37)
    if adjustment >= 360/37/2:
        adjustment -= 360/37
        sign = 1
    else:
        sign = -1
    if abs(adjustment) > 360/37/10:
        roulette["spin_speed"] = sign * math.sqrt(200 * abs(adjustment))
    else:
        roulette["readjusting"] = False
 
# Dibuixar
def app_draw():
    # Pintar el fons de verd fosc
    screen.fill(DARK_GREEN)

    # Número actual
    text = font_medium.render(f"Current number: {str(current_number)}", True, WHITE)
    text_center = (roulette["position"][0] + roulette["radius"], roulette["position"][1] + roulette["radius"]*2 + 20)
    text_rect = text.get_rect(center = text_center)

    if any([roulette["about_to_spin"], roulette["spinning"], roulette["readjusting"], roulette["spin_canceled"]]):
        # Actualitzar la ruleta quan està girant
        update_roulette()
    elif spin_counter > 0:
        # Dibuixar el número actual si la ruleta no està girant i s'ha girat una vegada com a mínim
        screen.blit(text, text_rect)
    # Dibuixar la ruleta
    screen.blit(roulette_surface, roulette["position"])

    draw_spin_button()

    draw_board()

    # Actualitzar el dibuix a la finestra
    pygame.display.update()

def draw_spin_button():
    sb_rect_tuple = (spin_button["x"],spin_button["y"],spin_button["width"],spin_button["height"])
    
    fill_color = BLACK
    border_color = LIGHT_GRAY
    text_color = WHITE
    if roulette["about_to_spin"]:
        fill_color = GOLD
        border_color = BLACK
        text_color = BLACK
    elif roulette["spinning"] or roulette["readjusting"] or roulette["spin_canceled"]:
        fill_color = DARK_GRAY
        border_color = GRAY
        text_color = GRAY
    
    pygame.draw.rect(screen, fill_color, sb_rect_tuple)
    pygame.draw.rect(screen, border_color, sb_rect_tuple, 2)
    
    sb_text = font_medium.render("Spin!", True, text_color)
    center = (spin_button["x"] + 40, spin_button["y"] + 15)
    sb_text_rect = sb_text.get_rect(center=center)
    screen.blit(sb_text, sb_text_rect)

def update_roulette():
    r = roulette["radius"]
    c = (r,r)

    pygame.draw.circle(roulette_surface, DARK_GOLD, c, r, 6)
    pygame.draw.circle(roulette_surface, BROWN, c, r-56)
    
    arrow_points = [
    (c[0]+r+8, c[1]),
    (c[0]+r+23, c[1]+8),
    (c[0]+r+23, c[1]-8)]
    pygame.draw.polygon(roulette_surface, GOLD, arrow_points)
    
    for i, n in enumerate(number_order):
        angle = (360/37*i + roulette["angle_offset"]) % 360
        if i == 0:
            color = GREEN
        elif i % 2 == 1:
            color = RED
        else:
            color = BLACK
        
        p0 = utils.point_on_circle(c, r-30, angle)
        p1 = utils.point_on_circle(c, r-6, angle)

        prev_angle = angle - 360/37
        prev_0 = utils.point_on_circle(c, r-30, prev_angle)
        prev_1 = utils.point_on_circle(c, r-6, prev_angle)

        if roulette["spin_speed"] == 0 and prev_angle + angle < 360/37:
            global current_number
            current_number = n

        points = [p0,p1,prev_1,prev_0]
        pygame.draw.polygon(roulette_surface, color, points)
        pygame.draw.polygon(roulette_surface, LIGHT_GRAY, points, 3)

        polygon_center = (int((p0[0]+prev_1[0])/2), int((p0[1]+prev_1[1])/2))

        text_angle = -angle - 90 + 360/37/2
        text_n = font_small.render(str(n), True, WHITE)
        text_n_rotated = pygame.transform.rotate(text_n, text_angle)
        text_n_rotated_rect = text_n_rotated.get_rect()
        text_n_rotated_rect.center = polygon_center
        roulette_surface.blit(text_n_rotated, text_n_rotated_rect)

def init_grid_surface():
    # Abreujar noms
    cols, rows = board["columns"], board["rows"]
    c_w, c_h = board["cell"]["width"], board["cell"]["height"]
    e_w, e_h = board["ellipse"]["width"], board["ellipse"]["height"]

    # Números
    for i, n in enumerate(number_order):
        if n == 0: continue
        color = RED if i % 2 == 1 else BLACK
        row = (1, 3, 2)[n % 3] #1 2 3 4 5 6 7 8... → 3 2 1 3 2 1 3 2...
        col = math.ceil(n / 3) #1 2 3 4 5 6 7 8... → 1 1 1 2 2 2 3 3...
        x = c_w * (col-1)
        y = c_h * (row-1)
        ellipse_rect = [x + (c_w - e_w)/2, y + (c_h-e_h)/2, e_w, e_h]
        pygame.draw.ellipse(grid_surface, color, ellipse_rect)

        center_x = x + c_w / 2 - 1
        center_y = y + c_h / 2
        text_n = font_medium.render(str(n), True, WHITE)
        text_n_rotated =  pygame.transform.rotate(text_n, 90)
        text_n_rotated_rect = text_n_rotated.get_rect(center=(center_x, center_y))
        grid_surface.blit(text_n_rotated, text_n_rotated_rect)

    # Cel·les inferiors
    for bottom_cell in range(4):
        x = c_w * (1.5 + 3 * bottom_cell)
        y = c_h * 3.5
        if bottom_cell in (0, 3):
            string = "EVEN" if bottom_cell == 0 else "ODD"
            text = font_serif.render(string, True, WHITE)
            text_rect = text.get_rect(center = (x, y))
            grid_surface.blit(text, text_rect)
        else:
            color = RED if bottom_cell == 2 else BLACK
            diamond_points = [
            (x - c_w * 1.2, y),
            (x, y - c_h * 0.4),
            (x + c_w * 1.2, y),
            (x, y + c_h * 0.4)]
            pygame.draw.polygon(grid_surface, color, diamond_points)
            pygame.draw.polygon(grid_surface, LIGHT_GRAY, diamond_points, 3)

    #Quadre extern
    pygame.draw.rect(grid_surface, LIGHT_GRAY, (0, 0, grid_size[0], grid_size[1]), 3)

    #Línies internes
    for row in range(1, cols):
        y = c_h * row
        pygame.draw.line(grid_surface, LIGHT_GRAY, (0, y), (grid_size[0], y), 3)
    for col in range(1, rows):
        x = c_w * col
        y = grid_size[1]
        if col % 3 != 0:
            y -= c_h
        pygame.draw.line(grid_surface, LIGHT_GRAY, (x, 0), (x, y), 3)

def draw_board():
    # Abreujar noms
    board_x, board_y, table_x = board["x"], board["y"], board["table_x"]
    cols, rows = board["columns"], board["rows"]
    c_w, c_h = board["cell"]["width"], board["cell"]["height"]
    
    # Espai de zero
    zero_points = [
    (table_x, 1),
    (table_x*2/3, 1),
    (0, c_h * 1.5),
    (table_x*2/3, c_h * 3),
    (table_x, c_h * 3)]
    pygame.draw.lines(board_surface, LIGHT_GRAY, False, zero_points, 3)

    text_zero = font_big.render("0", True, WHITE, DARK_GREEN)
    text_zero_rotated = pygame.transform.rotate(text_zero, 90)
    text_zero_rotated_rect = text_zero_rotated.get_rect(center = (table_x*5/9, c_h * 1.5))
    board_surface.blit(text_zero_rotated, text_zero_rotated_rect)

    # Graella
    board_surface.blit(grid_surface, (table_x, 0))

    # Espais de columnes
    for col in range(3):
        x = table_x + c_w * rows
        y = c_h * col
        
        center = (x + c_w/2, y + c_h/2)
        text = font_small.render("2 : 1", True, WHITE, DARK_GREEN)
        text_rotated = pygame.transform.rotate(text, 90)
        text_rotated_rect = text_rotated.get_rect(center=center)
        board_surface.blit(text_rotated, text_rotated_rect)

        center = (center[0] - 1, center[1] + 1)
        points = [(x, y+1),
        (x + c_w*0.9, y+1),
        (x + c_w*1.4, y + c_h/2),
        (x + c_w*0.9, y + c_h),
        (x, y + c_h)]
        
        if col != 0: points.pop(0)
        pygame.draw.lines(board_surface, LIGHT_GRAY, False, points, 3)

    #draw_bets()

    screen.blit(board_surface, (board_x, board_y))

if __name__ == "__main__":
    main()