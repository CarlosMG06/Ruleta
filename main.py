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

drag_offset = {'x': 0, 'y': 0}

# Bucle de l'aplicació
def main():
    global players, chips
    is_looping = True

    update_roulette()
    init_grid_surface()
    players = init_players()
    chips = init_chips()

    tmp = True

    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()
        if tmp:
            print(players)
            print(chips_positions)
            tmp = False

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
    global chips
    delta_time = clock.get_time() / 1000.0

    if current_mode["betting"]:
        if utils.is_point_in_rect(mouse, bet_button) and bet_button["enabled"]:
            if mouse["pressed"]:
                bet_button["pressed"] = True
            elif mouse["released"] and bet_button["pressed"]:
                bet_button["pressed"] = False
                confirm_bet()
                player_i = player_names.index(current_player["name"])
                if player_i < 2:
                    current_player["name"] = player_names[player_i+1]
                else:
                    current_player["name"] = player_names[0]
                    current_mode["betting"] = False
                    current_mode["roulette"] = True

    elif current_mode["roulette"]:
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

    """
    else:
        if utils.is_point_in_rect(mouse, close_button):
            if mouse["pressed"]:
                hide_info()
                if current_mode["roulette"] == None:
                    current_mode["roulette"] = True
                else:
                    current_mode["betting"] = True
                current_mode["info"] = False

    #if utils.is_point_in_rect(mouse, info_button) and not current_mode["info"]:
        if mouse["pressed"]:
                info_button["pressed"] = True
            elif mouse["released"] and info_button["pressed"]:
                info_button["pressed"] = False
                show_info()
                if current_mode["roulette"]:
                    current_mode["roulette"] = None
                else:
                    current_mode["betting"] = None
                current_mode["info"] = True
    """

    # Arrastrar fichas
    if not any_chip_dragged() and mouse['pressed']:
        # Una fitxa es dibuixa superposada sobre una altra, si la superposada apareix més endavant en la llista.
        # Recorrent la llista al revés, aconseguim que la fitxa seleccionada sigui la que vegem i no la que pugui haver-hi sota.
        for chip in reversed(chips): 
            if utils.is_point_in_circle(mouse, chip['pos'], chip['radius']):
                chip['dragged'] = True
                drag_offset["x"] = mouse['x'] - chip['pos']['x']
                drag_offset["y"] = mouse['y'] - chip['pos']['y']
                break
    else:
        if mouse["released"]:
            for chip in chips:
                if chip['dragged'] == True:
                    for board_cell in board_cell_areas:
                        valid = False
                        if valid_chip_position(chip, board_cell):
                            valid = True
                            '''print(f'Posición válida!')
                            print(f'Nombre casilla: {board_cell}')
                            print(f'Contenido de su diccionario: {board_cell_areas[board_cell]}')'''
                            break
                    if not valid:
                        '''print(f'Posición NO válida! Devolviendo ficha a la posición base...')'''
                        chip['pos']['x'] = 100
                        chip['pos']['y'] = 100
            release_all_chips()
        else:
            for chip in chips:
                if chip['dragged']:
                    chip['pos']['x'] = mouse['x'] - drag_offset['x']
                    chip['pos']['y'] = mouse['y'] - drag_offset['y']
        
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
        # Actualitzar taula i graella dels jugadors si la ruleta no està girant
        update_board()
        update_player_grid()
        if spin_counter["n"] > 0:
            # Dibuixar el número actual si la ruleta no està girant i s'ha girat una vegada com a mínim
            screen.blit(current_number_text["text"], current_number_text["rect"])
    # Dibuixar la ruleta
    screen.blit(roulette_surface, roulette["position"])

    # Dibuixar botó de gir
    draw_spin_button()
    
    # Línia de separació
    pygame.draw.line(screen, LIGHT_GRAY, (340, 0), (340, 450), 2)
    
    # Dibuixar taula
    screen.blit(board_surface, (board["x"], board["y"]))

    # Dibuixar botó d'apostar
    draw_bet_button()

    # Dibuixar graella dels jugadors
    screen.blit(player_grid_surface, (player_grid["x"], player_grid["y"]))
    
    # Muestra regiones del tablero a partir de sus Rect
    '''for board_cell in board_cell_areas:
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        rect_values = (board_cell_areas[board_cell]['rect']['x'], board_cell_areas[board_cell]['rect']['y'], board_cell_areas[board_cell]['rect']['width'], board_cell_areas[board_cell]['rect']['height'])
        pygame.draw.rect(screen, color, rect_values, 3)
        if board_cell == '0':
            pygame.draw.polygon(screen, color, board_cell_areas["0"]['vertices'], 3)'''

    # Muestra los centros de las posiciones originales de las fichas
    '''for chip in chips_positions:
        center = (chips_positions[chip]['x'], chips_positions[chip]['y'])
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        pygame.draw.circle(screen, color, center, 5)'''
    
    # Dibuixar fitxes
    for chip in chips:
        draw_chip(chip)

    # Actualitzar el dibuix a la finestra
    pygame.display.update()
    
if __name__ == "__main__":
    main()