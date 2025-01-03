import math
import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import utils

from Game import *
from UI import *

pygame.init()
clock = pygame.time.Clock()

# Bucle de l'aplicació
def main():
    is_looping = True
    
    init_players()
    init_chip_positions()
    init_chips()

    init_roulette()
    init_betting_grid()
    init_betting_board()
    init_player_grid()
    init_game_info_chart()

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

    # Després de passar a una nova ronda, esperar 2 segons abans d'inicialitzar les fitxes
    if new_round_delay["bool"]:
        new_round_delay["timer"] += delta_time
        if new_round_delay["timer"] >= new_round_delay["wait_time"]:
            first_player()
            init_chips()
            new_round_delay["timer"] = 0
            new_round_delay["bool"] = False 
        return

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
                next_player()                  
        elif bet_button["pressed"]:
            bet_button["pressed"] = False

        drag_chips()
    elif current_mode["roulette"]:
        spin_button["enabled"] = not (any([roulette["states"]["spin_canceled"], roulette["states"]["spinning"], roulette["states"]["readjusting"]]))
        
        if utils.is_point_in_rect(mouse, spin_button) and spin_button["enabled"]:
            if mouse["pressed"]:
                # La ruleta gira una miqueta com a anticipació per fer efecte
                roulette["spin_speed"] = -50
                change_roulette_state()
                spin_button["pressed"] = True
            if mouse["released"] and spin_button["pressed"]:
                acc = abs(roulette["spin_acc"])
                angular_displacement = (54 + random.randint(1,37)) * 360/37 #Gira entre 55 i 91 números
                roulette["spin_speed"] = math.sqrt(angular_displacement*2/acc)*acc #Càlcul MCUA
                change_roulette_state()
                spin_button["pressed"] = False
        elif spin_button["pressed"]:
            # Si el mouse es mou fora del botó abans de deixar anar, la ruleta torna a la seva posició inicial
            roulette["spin_speed"] = math.sqrt((-50)**2 - roulette["spin_speed"]**2) #Càlcul MCUA
            change_roulette_state(cancel_spin=True)
            spin_button["pressed"] = False

        if roulette["spin_speed"] != 0:
            spin_roulette(delta_time)
        elif roulette["states"]["readjusting"]:
            readjust_roulette()
    elif current_mode["moving_chips"]:
        if not all_chips_arrived():
            move_chips_towards_destination()
        else:
            next_round()
            if any(players[name]["creditless"] for name in player_names):
                init_player_grid()
            if current_mode["game_over"]:
                init_game_over_screen()
    elif current_mode["info"]:
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
            drag_scroll()

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
    
    if roulette["states"]["idle"]:
        update_player_grid()
        if spin_counter["n"] > 0:
            # Dibuixar el número actual si la ruleta no està girant i s'ha girat una vegada com a mínim
            draw_current_number()
    else:
        # Actualitzar la ruleta quan està girant
        update_roulette()
        if roulette["states"]["readjusting"]:
            # Actualitzar número actual després de girar la ruleta
            update_current_number()

    # Dibuixar la ruleta
    screen.blit(roulette_surface, roulette["position"])

    # Dibuixar botó de gir
    draw_button(spin_button, spin_button=True)
    
    # Dibuixar botó d'informació de la partida
    draw_button(gi_button, gi_button=True)

    # Línia de separació
    pygame.draw.line(screen, LIGHT_GRAY, (340, 0), (340, 450), 2)
    
    # Dibuixar taula
    screen.blit(board_surface, (board["x"], board["y"]))

    # Dibuixar botó d'apostar
    draw_button(bet_button)

    # Dibuixar graella dels jugadors
    screen.blit(player_grid_surface, (player_grid["x"], player_grid["y"]))
        
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
    
    if current_mode["game_over"]:
        screen.blit(game_over_screen, (0,0))

    # Actualitzar el dibuix a la finestra
    pygame.display.update()
    
if __name__ == "__main__":
    main()