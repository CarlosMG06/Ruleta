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
#BLUE  = (0, 0, 255)
#PURPLE = (128, 0, 128)
#ORANGE = (255, 165, 0) 
BROWN = (102, 68, 34)

roulette = {"center": (180,180), "angle_offset": 0, "spin_speed": 0, "spin_acc": -100, "about_to_spin": False}
red_numbers = [3, 6, 7, 8, 12, 14, 16, 17, 19, 21, 22, 25, 26, 28, 31, 33, 34, 36]
mouse = {"x": -1, "y": -1, 
"pressed": False, "held": False, "released": False}
spin_button = {"x": 140, "y": 400, "width": 80, "height": 30}

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Window Title')

fontBold = pygame.font.SysFont("Arial", 16, bold=True)

# Bucle de l'aplicació
def main():
    is_looping = True

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
    
    if utils.is_point_in_rect(mouse, spin_button) and roulette["spin_speed"] <= 1:
        if mouse["pressed"]:
            roulette["spin_speed"] = -50
            roulette["about_to_spin"] = True
        elif mouse["released"] and roulette["about_to_spin"]:
            roulette["spin_speed"] = random.randrange(40000,50000)/100
            roulette["about_to_spin"] = False
    elif roulette["about_to_spin"]:
        roulette["spin_speed"] = math.sqrt((-50)**2 - roulette["spin_speed"]**2)
        roulette["about_to_spin"] = False

    if roulette["spin_speed"] != 0:
        spin_roulette(delta_time)
    
    mouse["pressed"] = False
    mouse["released"] = False
            
# Dibuixar
def app_draw():
    # Pintar el fons de blanc
    screen.fill(DARK_GREEN)

    draw_spin_button()

    draw_roulette()

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
    elif roulette["spin_speed"] > 0:
        fill_color = DARK_GRAY
        border_color = GRAY
        text_color = GRAY
    pygame.draw.rect(screen, fill_color, sb_rect_tuple)
    pygame.draw.rect(screen, border_color, sb_rect_tuple, 2)
    sb_text = fontBold.render("Spin!", True, text_color)
    sb_text_rect = sb_text.get_rect(center=(180, 415))
    screen.blit(sb_text, sb_text_rect)

def draw_roulette():
    c = roulette["center"]
    pygame.draw.circle(screen, BLACK, c, 150, 5)
    pygame.draw.circle(screen, BROWN, c, 100)
    for n in range(37):
        angle = 360/37*n + roulette["angle_offset"]
        if n == 0:
            color = GREEN
        elif n in red_numbers:
            color = RED
        else:
            color = BLACK
        
        p0 = utils.point_on_circle(c, 130, angle)
        p1 = utils.point_on_circle(c, 150, angle)

        prev_angle = angle - 360/37
        prev_0 = utils.point_on_circle(c, 130, prev_angle)
        prev_1 = utils.point_on_circle(c, 150, prev_angle)

        points = [p0,p1,prev_1,prev_0]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, LIGHT_GRAY, points, 3)

        center = (int((p0[0]+prev_1[0])/2), int((p0[1]+prev_1[1])/2))

        text_angle = -angle - 90 + 360/37/2
        text_n = fontBold.render(str(n), True, WHITE)
        text_n_rotated = pygame.transform.rotate(text_n, text_angle)
        text_n_rotated_rect = text_n_rotated.get_rect()
        text_n_rotated_rect.center = center
        screen.blit(text_n_rotated, text_n_rotated_rect)

def spin_roulette(delta_time):
    sign = 1 if roulette["spin_speed"] > 0 else -1
    if abs(roulette["spin_speed"]) > 1:
        roulette["spin_speed"] += sign * roulette["spin_acc"] * delta_time
    else:
        roulette["spin_speed"] = 0
    roulette["angle_offset"] += roulette["spin_speed"] * delta_time

if __name__ == "__main__":
    main()