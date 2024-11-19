import math
import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import utils

from UI import *
from Game import *

mouse = {"x": -1, "y": -1, 
"pressed": False, "held": False, "released": False}

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption('Window Title')

# Bucle de l'aplicació
def main():
    is_looping = True

    update_roulette()
    init_grid_surface()
    init_players()

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
        # Posición del mouse
        # Click pulsado
        # Click soltado
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
            angular_displacement = (54 + random.randint(1,37)) * 360/37 #Gira entre 55 i 91 números
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
        spin_counter["n"] += 1

    mouse["pressed"] = False
    mouse["released"] = False
        
# Dibuixar
def app_draw():
    # Pintar el fons de verd fosc
    screen.fill(DARK_GREEN)

    if roulette["readjusting"]:
        # Actualitzar número actual després de girar la ruleta
        update_current_number()
    if any([roulette["about_to_spin"], roulette["spin_canceled"], roulette["spinning"], roulette["readjusting"]]):
        # Actualitzar la ruleta quan està girant
        update_roulette()
    else:
        # Actualitzar taula si la ruleta no està girant
        update_board()
        if spin_counter["n"] > 0:
            # Dibuixar el número actual si la ruleta no està girant i s'ha girat una vegada com a mínim
            screen.blit(current_number_text["text"], current_number_text["rect"])
    # Dibuixar la ruleta
    screen.blit(roulette_surface, roulette["position"])

    #Dibuixar botó de gir
    draw_spin_button()
    
    # temporal: prova per veure com són les fitxes
    draw_chip(chip_dict={"value": f"{100:03}", "owner": "taronja", "pos": (500,400)})
    draw_chip(chip_dict={"value": f"{50:03}", "owner": "banca", "pos": (550,400)})
    draw_chip(chip_dict={"value": f"{20:03}", "owner": "lila", "pos": (600,400)})
    draw_chip(chip_dict={"value": f"{10:03}", "owner": "taronja", "pos": (650,400)})
    draw_chip(chip_dict={"value": f"{5:03}", "owner": "blau", "pos": (700,400)})
    
    # Dibuixar taula
    screen.blit(board_surface, (board["x"], board["y"]))

    # Actualitzar el dibuix a la finestra
    pygame.display.update()
    
if __name__ == "__main__":
    main()