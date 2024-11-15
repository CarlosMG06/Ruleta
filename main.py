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

red_numbers = [3, 6, 7, 8, 12, 14, 16, 17, 19, 21, 22, 25, 26, 28, 31, 33, 34, 36]

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

        center = (int((p0["x"]+prev_1["x"])/2), int((p0["y"]+prev_1["y"])/2))
    

        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, GRAY, points, 3)

        text_angle = -angle - 90 + 360/37/2
        text_n = fontBold.render(str(n), True, WHITE)
        text_n_rotated = pygame.transform.rotate(text_n, text_angle)
        text_n_rotated_rect = text_n_rotated.get_rect()
        text_n_rotated_rect.center = center
        screen.blit(text_n_rotated, text_n_rotated_rect)
    

    # Actualitzar el dibuix a la finestra
    pygame.display.update()

if __name__ == "__main__":
    main()