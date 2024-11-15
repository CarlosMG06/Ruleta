import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import utils

WHITE = (255, 255, 255)
GRAY = (204, 204, 204)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0) 
BROWN = (153, 102, 51)

red_numbers = [3, 6, 7, 8, 12, 14, 16, 17, 19, 21, 22, 25, 26, 31, 32, 33, 34, 36]

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Window Title')

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
    return True

# Fer càlculs
def app_run():
    pass

# Dibuixar
def app_draw():
    # Pintar el fons de blanc
    screen.fill(WHITE)

    pygame.draw.circle(screen, BLACK, (180,180), 150, 5)
    pygame.draw.circle(screen, BROWN, (180,180), 100)
    
    for n in range(37):
        angle = 360/37*n
        if n == 0:
            color = GREEN
        elif n in red_numbers:
            color = RED
        else:
            color = BLACK
        
        p0 = utils.point_on_circle((180,180), 130, angle)
        p1 = utils.point_on_circle((180,180), 150, angle)

        prev_angle = angle - 360/37
        prev_0 = utils.point_on_circle((180,180), 130, prev_angle)
        prev_1 = utils.point_on_circle((180,180), 150, prev_angle)

        points = [
            (int(p0["x"]), int(p0["y"])),
            (int(p1["x"]), int(p1["y"])),
            (int(prev_1["x"]), int(prev_1["y"])),
            (int(prev_0["x"]), int(prev_0["y"]))
        ]

        
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, GRAY, points, 5)
    

    # Actualitzar el dibuix a la finestra
    pygame.display.update()

if __name__ == "__main__":
    main()