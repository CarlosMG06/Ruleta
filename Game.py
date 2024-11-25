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
            give_out_prizes()
            log_game_info()
            current_mode["roulette"] = False
            current_mode["betting"] = True
            init_chips()
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
    starting_chips = list(zip(chip_values, (0,1,1,2,2))) # Las tuplas son: (NomFicha, Cantidad)
    for name in player_names:
        player_dict = {}
        for chip in starting_chips:
            chip_value = f'{chip[0]:03}'
            chip_amount = chip[1]
            player_dict[chip_value] = chip_amount
        players[name] = player_dict

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

def valid_chip_position(chip_index, chip, cell):
    '''Comprueba que la ficha puesta en el tablero de apuestas está en posición válida (True, False).
    
    Input:
        -chip(dict): chip dentro de el array chips
        -cell(str): representa la celda del tablero ('0', '27', 'ODD', 'RED', etc.)'''
    chip_in_cell = utils.is_point_in_rect(chip['pos'], board_cell_areas[cell]['rect'])
    chip_in_triangle = False
    if cell in ['0', 'column 1', 'column 2', 'column 3']:
        chip_in_triangle = utils.is_point_in_triangle(chip['pos'], board_cell_areas[cell]['vertices'])
    if chip_in_cell or chip_in_triangle:
        for i, chip in enumerate(chips):
            if i == chip_index: continue
            if chip["current_cell"] not in ('owner', cell):
                return False
        '''print(f'Valores de valid_chip_position() --> chip_in_cell={chip_in_cell}, chip_in_triangle={chip_in_triangle}')'''
        return True
    '''print(f'Valores de valid_chip_position() --> chip_in_cell={chip_in_cell}, chip_in_triangle={chip_in_triangle}')'''
    return False

def init_chip_positions():
    c_w = player_grid["cell"]["width"]
    c_1w, c_1h = player_grid["cell"]["1st_w"], player_grid["cell"]["1st_h"]
    for i in range(len(chip_values)):
        chip_x = player_grid['x'] + c_1w + c_w/2 + c_w*i
        chip_y = player_grid['y'] + c_1h/2
        chips_initial_positions[str(chip_values[i])] = {'x':chip_x, 'y':chip_y}

def init_chips():
    chips.clear()
    for value in chip_values:
        amount = players[current_player["name"]][f"{value:03}"]
        for _ in range(amount):
            chip_dict = {}
            chip_dict['value'] = value
            chip_dict['owner'] = current_player["name"]
            chip_dict['pos'] = {'x': chips_initial_positions[str(value)]['x'], 'y': chips_initial_positions[str(value)]['y']}
            chip_dict['radius'] = 6 + int(math.log2(chip_dict['value'])*3)
            chip_dict['dragged'] = False
            chip_dict['current_cell'] = 'owner'
            chips.append(chip_dict)

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
    bet_dict = {}
    units = 0
    for chip in chips:
        if chip["current_cell"] != 'owner':
            bet_dict["bet_on"] = chip["current_cell"]
            units += chip["value"]
            players[current_player["name"]][f"{chip["value"]:03}"] -= 1
    bet_dict["units"] = units
    current_bets.append(bet_dict)

def give_out_prizes():
    pass

def log_game_info():
    round_info = {}
    
    # tmp
    if len(current_bets) == 0:
        current_bets.extend([{"units": 5, "bet_on": "RED"}, {"units": 110, "bet_on": "7"}, {"units": 20, "bet_on": "ODD"}])
    
    round_info[game_info_keys[0]] = current_number["n"]
    round_info[game_info_keys[1]] = current_bets.copy()
    credits = []
    for i, name in enumerate(player_names): 
        credits.append(total_money_player(name))
    round_info[game_info_keys[2]] = credits
    game_info.append(round_info)

    current_bets.clear()

def show_game_info():
    game_info_chart["visible"] = True
    if len(game_info) > 6:
       gi_scroll["visible"] = True
       gi_scroll["percentage"] = 0

def hide_game_info():
    game_info_chart["visible"] = False

def set_chips_destination():
    '''Declara a qué posición deben ir las fichas, en función del resultado de la apuesta.'''
    # Definir clave 'dest' en chips, que tiene como valor un dict del tipo {'x':int, 'y':int, 'arrived':False}
    pass

def move_chips():
    '''Mueve cada una de las fichas del array 'chips' a la posición que le toca.'''
    for chip in chips:
        if not chip['dest']['arrived']:
            # Calculamos el ángulo
            delta_x = chip['pos']['x'] - chip['dest']['x'] 
            delta_y = chip['pos']['y'] - chip['dest']['y']
            rad = math.atan(delta_x / delta_y)
            # Calculamos la variación de posición en función del ángulo
            chip['pos']['x'] += math.sin(rad) * chip_speed
            chip['pos']['y'] += math.sin(rad) * chip_speed
            # Si la ficha está lo suficientemente cerca del destino, decidimos que ya ha llegado
            if utils.is_point_in_circle(chip['pos'], chip['dest'], r=5):
                chip['pos']['x'] = chip['dest']['x'] 
                chip['pos']['y'] = chip['dest']['y']
                chip['dest']['arrived'] = True