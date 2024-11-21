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

    # Parámetros partida
    player_names = ['taronja','lila','blau']
    starting_chips = [(100,0),(50,1),(20,1),(10,2),(5,2)] # Las tuplas son: (NomFicha, Cantidad)
    
    players = {}
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
        -cell(str): nombre de la celda en el tablero'''
    for board_cell in board_cell_areas:
        if board_cell == cell:
            chip_in_cell= utils.is_point_in_rect(chip['pos'], board_cell['rect'])
            if chip_in_cell:
                return True
            return False

def init_chips():
    '''Genera un array de diccionarios, donde cada diccionario contiene información de cada ficha.
    
    La estructura de cada diccionario es:
    {'owner': str, 'value': int, 'pos': {'x': int, 'y': int}, 'dragged': bool}'''
    global chips
    chips = []

    for player_name in players:
        for chip in players[player_name]:
            chip_dict = {}
            chip_dict['value'] = int(chip)
            chip_dict['owner'] = player_name
            chip_dict['pos'] = {'x': 0, 'y': 0} # Necesito saber en qué posición van las fichas de X valor, para cada jugador
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

if __name__ == '__main__':
    init_players()
    init_chips()
    print(chips)

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