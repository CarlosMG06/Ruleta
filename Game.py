from GameData import *
from UI_Data import *
import math
import utils

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
            spin_counter["n"] += 1
            log_info()
            current_mode["roulette"] = False
            current_mode["betting"] = True
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
    roulette["spin_speed"] = sign * math.sqrt(200 * abs(adjustment))
    if abs(adjustment) > 360/37/10:
        roulette["spin_speed"] = sign * math.sqrt(200 * abs(adjustment))
    else:
        roulette["spin_speed"] = 0.1

def init_players():
    '''Inicia el diccionario que contiene información de los jugadores.'''
    global players

    starting_chips = list(zip(chip_values, (0,1,1,2,2))) # Las tuplas son: (NomFicha, Cantidad)
    
    for name in player_names:
        player_dict = {}
        for ficha in starting_chips:
            chip_value = f'{ficha[0]:03}'
            chip_amount = ficha[1]
            player_dict[chip_value] = chip_amount
        players[name] = player_dict
    return players

def total_money_player(player_name):
    '''Devuelve el dinero total que tiene el jugador, a partir de sus fichas'''
    total_money = 0
    for chip in players[player_name]:
        chip_value = int(chip)
        n_chips = players[player_name][chip]
        total_money += chip_value * n_chips
    return total_money

def redistribute_player_chips(player_name):
    '''Redistribuye las fichas que tiene un jugador para asegurar que tiene la mayor variedad de fichas posibles'''
    global players
    new_chips_dict = {'100': 0, '050': 0, '020': 0, '010': 0, '005': 0}
    player_money = total_money_player(player_name)
    new_chips_total = 0
    possible_chips = (100, 50, 20, 10, 5)

    i = 0
    while new_chips_total < player_money:
        chip = possible_chips[i]
        if player_money >= new_chips_total + chip:
            chip_key = f'{chip:03}'
            new_chips_dict[chip_key] += 1
            new_chips_total = sum(new_chips_dict.values())

        i += 1
        if i == len(possible_chips):
            i = 0

    players[player_name] = new_chips_dict

def valid_chip_position(chip, cell):
    '''Comprueba que la ficha puesta en el tablero de apuestas está en posición válida (True, False).
    
    Input:
        -chip(dict): chip dentro de el array chips
        -cell(str): representa la celda del tablero ('0', '27', 'ODD', 'RED', etc.)'''
    chip_in_cell= utils.is_point_in_rect(chip['pos'], board_cell_areas[cell]['rect'])
    chip_in_triangle = False # Esta condicion sólo es relevante si estamos en la casilla '0'
    if cell == '0':
        chip_in_triangle = utils.is_point_in_triangle(chip['pos'], board_cell_areas[cell]['vertices'])
    if chip_in_cell or chip_in_triangle:
        '''print(f'Valores de valid_chip_position() --> chip_in_cell={chip_in_cell}, chip_in_triangle={chip_in_triangle}')'''
        return True
    '''print(f'Valores de valid_chip_position() --> chip_in_cell={chip_in_cell}, chip_in_triangle={chip_in_triangle}')'''
    return False

def init_chips():
    '''Genera un array de diccionarios, donde cada diccionario contiene información de cada ficha.
    
    La estructura de cada diccionario es:
    {'owner': str, 'value': int, 'pos': {'x': int, 'y': int}, 'dragged': bool}'''
    global chips, chips_positions
    c_w = player_grid["cell"]["width"]
    c_1w, c_1h = player_grid["cell"]["1st_w"], player_grid["cell"]["1st_h"]
    for i in range(len(chip_values)):
        chip_x = player_grid['x'] + c_1w + c_w/2 + c_w*i
        chip_y = player_grid['y'] + c_1h/2
        chips_positions[str(chip_values[i])] = {'x':chip_x, 'y':chip_y}

    chips = []
    for player_name in players:
        for chip in players[player_name]:
            for i in range(players[player_name][chip]):
                chip_dict = {}
                chip_dict['value'] = int(chip)
                chip_dict['owner'] = player_name
                chip_name = str(chip_dict['value'])
                chip_dict['pos'] = {'x': chips_positions[chip_name]['x'], 'y': chips_positions[chip_name]['y']}
                chip_dict['radius'] = 6 + int(math.log2(chip_dict['value'])*3)
                chip_dict['dragged'] = False
                chip_dict['current cell'] = 'owner'
                chips.append(chip_dict)
    return chips

def any_chip_dragged():
    '''Devuelve True si alguna ficha está siendo arrastrada'''
    for chip in chips:
        if chip['dragged']:
            return True
    return False

def release_all_chips():
    '''Dentro del array 'chips', define el valor 'dragged' de todas las fichas como False'''
    for chip in chips:
        chip['dragged'] = False

def confirm_bet():
    pass

def log_info():
    pass

def show_info():
    pass

def hide_info():
    pass

if __name__ == '__main__':
    init_players()
    init_chips()

    # Test funciónes:
    # any_chip_dragged()
    # release_all_chips()
    '''
    print(any_chip_dragged())
    chips[0]['dragged'] = True
    print(any_chip_dragged())
    release_all_chips()
    print(any_chip_dragged())
    '''