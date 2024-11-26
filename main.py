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
drag_offset = {'x': 0, 'y': 0}

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption('Window Title')

# Bucle de l'aplicació
def main():
    is_looping = True

    update_roulette()
    init_grid_surface()
    init_game_info_surface()
    init_players()
    init_chip_positions()
    init_chips()

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

    bet_button["enabled"] = False
    spin_button["enabled"] = False
    gi_button["enabled"] = not current_mode["info"] and spin_counter["n"] > 0

    if current_mode["betting"]:
        for chip in chips[current_player["name"]]:
            if chip["current_cell"] != 'owner':
                bet_button["enabled"] = True
                break

        if utils.is_point_in_rect(mouse, bet_button) and bet_button["enabled"]:
            if mouse["pressed"]:
                bet_button["pressed"] = True
            elif mouse["released"] and bet_button["pressed"]:
                bet_button["pressed"] = False
                delete_unmoved_chips()
                confirm_bet()
                player_i = player_names.index(current_player["name"])
                if player_i < 2:
                    current_player["name"] = player_names[player_i+1]
                    init_chips()
                else:
                    current_player["name"] = player_names[0]
                    change_mode()
        elif bet_button["pressed"]:
            bet_button["pressed"] = False

        # Arrossegar fitxes
        if not any_chip_dragged() and mouse['pressed']:
            # Una fitxa es dibuixa superposada sobre una altra, si la superposada apareix més endavant en la llista.
            # Recorrent la llista al revés, aconseguim que la fitxa seleccionada sigui la que vegem i no la que pugui haver-hi sota.
            for chip in reversed(chips[current_player["name"]]): 
                if utils.is_point_in_circle(mouse, chip['pos'], chip['radius']):
                    chip['dragged'] = True
                    drag_offset["x"] = mouse['x'] - chip['pos']['x']
                    drag_offset["y"] = mouse['y'] - chip['pos']['y']
                    break
        else:
            if mouse["released"]:
                for i, chip in enumerate(chips[current_player["name"]]):
                    if chip['dragged'] == True:
                        for board_cell in board_cell_areas:
                            valid = False
                            if valid_chip_position(i, chip, board_cell):
                                valid = True
                                chip["current_cell"] = board_cell
                                '''print(f'Posición válida!')
                                print(f'Nombre casilla: {board_cell}')
                                print(f'Contenido de su diccionario: {board_cell_areas[board_cell]}')'''
                                break
                        if not valid:
                            '''print(f'Posición NO válida! Devolviendo ficha a la posición base...')'''
                            chip["current_cell"] = 'owner'
                            chip['pos']['x'] = chips_initial_positions[str(chip['value'])]['x']
                            chip['pos']['y'] = chips_initial_positions[str(chip['value'])]['y']
                release_all_chips()
            else:
                for chip in chips[current_player["name"]]:
                    if chip['dragged']:
                        chip['pos']['x'] = mouse['x'] - drag_offset['x']
                        chip['pos']['y'] = mouse['y'] - drag_offset['y']
    elif current_mode["roulette"]:
        spin_button["enabled"] = not (any([roulette["spin_canceled"], roulette["spinning"], roulette["readjusting"]]))

        if utils.is_point_in_rect(mouse, spin_button) and spin_button["enabled"]:
            if mouse["pressed"]:
                # La ruleta gira una miqueta com a anticipació per fer efecte
                roulette["spin_speed"] = -50
                roulette["about_to_spin"] = True
                spin_button["pressed"] = True
            if mouse["released"] and spin_button["pressed"]:
                acc = abs(roulette["spin_acc"])
                angular_displacement = (54 + random.randint(1,37)) * 360/37 #Gira entre 55 i 91 números
                roulette["spin_speed"] = math.sqrt(angular_displacement*2/acc)*acc #Càlcul MCUA
                roulette["spinning"] = True
                roulette["about_to_spin"] = False
                spin_button["pressed"] = False
        elif spin_button["pressed"]:
            # Si el mouse es mou fora del botó abans de deixar anar, la ruleta torna a la seva posició inicial
            roulette["spin_speed"] = math.sqrt((-50)**2 - roulette["spin_speed"]**2) #Càlcul MCUA
            roulette["spin_canceled"] = True
            roulette["about_to_spin"] = False
            spin_button["pressed"] = False

        if roulette["spin_speed"] != 0:
            spin_roulette(delta_time)
        elif roulette["readjusting"]:
            readjust_roulette()

        roulette["idle"] = not (any([roulette["about_to_spin"], roulette["spin_canceled"], roulette["spinning"], roulette["readjusting"]]))    
    elif current_mode["moving_chips"]:
        moved_chips = True
        """for name in player_names:
            for chip in chips[name]:
                if chip["current_cell"] not in ('owner', 'house'):
                    moved_chips = False
                    break
            if not moved_chips: break"""
        moved_chips = True # tmp: Saltarse mover las fichas, borrar esta línea cuando esté hecho
        if not moved_chips:
            move_chips()
        else:
            next_round()
    else:
        gi_close_button["enabled"] = True
        if utils.is_point_in_rect(mouse, gi_close_button) and gi_close_button["enabled"]:
            if mouse["pressed"]:
                gi_close_button["pressed"] = True
            if mouse["released"] and gi_close_button["pressed"]:
                gi_close_button["pressed"] = False
                change_mode()
                hide_game_info()
        elif gi_close_button["pressed"]:
            gi_close_button["pressed"] = False

        if gi_scroll["visible"]:
            circle_center = {
                "x": int(gi_scroll["x"] + gi_scroll["width"] / 2),
                "y": int(gi_scroll["y"] + (gi_scroll["percentage"] / 100) * gi_scroll["height"])
            }
            if mouse["pressed"] and not gi_scroll["dragging"] and utils.is_point_in_circle(mouse, circle_center, gi_scroll["radius"]):
                gi_scroll["dragging"] = True

            if gi_scroll["dragging"]:
                relative_y = max(min(mouse["y"], gi_scroll["y"] + gi_scroll["height"]), gi_scroll["y"])
                gi_scroll["percentage"] = ((relative_y - gi_scroll["y"]) / gi_scroll["height"]) * 100

            if mouse["released"]:
                gi_scroll["dragging"] = False

            gi_scroll["surface_offset"] = int((gi_scroll["percentage"] / 100) * (48 * len(game_info) - gi_scroll["visible_height"]))

    if utils.is_point_in_rect(mouse, gi_button) and gi_button["enabled"]:
        if mouse["pressed"]:
            gi_button["pressed"] = True
        elif mouse["released"] and gi_button["pressed"]:
            gi_button["pressed"] = False
            show_game_info()
            change_mode(to_info=True)
    elif gi_button["pressed"]:
        gi_button["pressed"] = False
     
    mouse["pressed"] = False
    mouse["released"] = False

# Dibuixar
def app_draw():
    # Pintar el fons de verd fosc
    screen.fill(DARK_GREEN)
    
    if roulette["idle"]:
        # Actualitzar taula i graella dels jugadors si la ruleta no està girant
        update_board()
        update_player_grid()
        if spin_counter["n"] > 0:
            # Dibuixar el número actual si la ruleta no està girant i s'ha girat una vegada com a mínim
            draw_current_number()
    else:
        # Actualitzar la ruleta quan està girant
        update_roulette()
        if roulette["readjusting"]:
            # Actualitzar número actual després de girar la ruleta
            update_current_number()

    # Dibuixar la ruleta
    screen.blit(roulette_surface, roulette["position"])

    # Dibuixar botó de gir
    draw_button(spin_button, spin_button=True)
    
    # Dibuixar botó d'informació de la partida
    draw_button(gi_button)

    # Línia de separació
    pygame.draw.line(screen, LIGHT_GRAY, (340, 0), (340, 450), 2)
    
    # Dibuixar taula
    screen.blit(board_surface, (board["x"], board["y"]))

    # Dibuixar botó d'apostar
    draw_button(bet_button)

    # Dibuixar graella dels jugadors
    screen.blit(player_grid_surface, (player_grid["x"], player_grid["y"]))
    
    # Muestra regiones del tablero a partir de sus Rect
    """
    for board_cell in board_cell_areas:
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        rect_values = (board_cell_areas[board_cell]['rect']['x'], board_cell_areas[board_cell]['rect']['y'], board_cell_areas[board_cell]['rect']['width'], board_cell_areas[board_cell]['rect']['height'])
        pygame.draw.rect(screen, color, rect_values, 3)
        if board_cell in ("0", "col1", "col2", "col3"):
            pygame.draw.polygon(screen, color, board_cell_areas[board_cell]['vertices'], 3)
    """

    # Muestra los centros de las posiciones originales de las fichas
    '''for chip in chips_positions:
        center = (chips_positions[chip]['x'], chips_positions[chip]['y'])
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        pygame.draw.circle(screen, color, center, 5)'''
        
    # Dibuixar fitxes
    for name in player_names:
        for chip in chips[name]:
            draw_chip(chip)

    if game_info_chart["visible"]:
        update_game_info_chart()
        screen.blit(gi_surface, (0,0))
        if gi_scroll["visible"]:
            draw_scroll()
        draw_button(gi_close_button, close_button=True)

    # Actualitzar el dibuix a la finestra
    pygame.display.update()
    
if __name__ == "__main__":
    main()