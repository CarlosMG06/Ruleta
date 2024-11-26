from GameData import *
from UI_Data import *
import math
import utils

def change_mode(to_info = False):
    for key, value in current_mode.items():
        if value == None: mode_none = key
        if value: 
            mode = key
            break
    if mode == "info":
        current_mode["info"] = False
        current_mode[mode_none] = True
    elif to_info:
        current_mode[mode] = None
        current_mode["info"] = True
    else:
        main_modes = [key for key in current_mode.keys() if key != "info"]
        new_mode_index = (main_modes.index(mode)+1) % len(main_modes)
        current_mode[mode] = False
        current_mode[main_modes[new_mode_index]] = True

def change_roulette_state(cancel_spin = False):
    for key, value in roulette["states"].items():
        if value: 
            state = key
            break
    if state == "spin_canceled":
        roulette["states"]["spin_canceled"] = False
        roulette["states"]["idle"] = True
    elif cancel_spin:
        roulette["states"]["about_to_spin"] = False
        roulette["states"]["spin_canceled"] = True
    else:
        main_states = [key for key in roulette["states"].keys() if key != "spin_canceled"]
        new_state_index = (main_states.index(state)+1) % len(main_states)
        roulette["states"][state] = False
        roulette["states"][main_states[new_state_index]] = True

def next_round():
    log_game_info()
    give_out_prizes()
    for name in player_names:
        redistribute_player_chips(name)
    change_mode()
    for name in player_names:
        chips[name].clear()
    init_chips()

# Girar la ruleta
def spin_roulette(delta_time):
    sign = 1 if roulette["spin_speed"] > 0 else -1
    if abs(roulette["spin_speed"]) > 0.5:
        roulette["spin_speed"] += sign * roulette["spin_acc"] * delta_time
    else:
        if roulette["states"]["readjusting"]:
            spin_counter["n"] += 1
            change_mode()
            set_chips_destination()
        if not roulette["states"]["about_to_spin"]:
            change_roulette_state()
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

    def limit_proportion(chip_value):
        match chip_value:
            case 100: return 5/9 - 0.001 # apareix a partir de 180 (excluit)
            case 50: return 5/8 - 0.001  # apareix a partir de 80 (excluit)
            case 20: return 2/3 - 0.001  # apareix a partir de 30 (excluit)
            case 10: return 1 - 0.001    # apareix a partir de 10 (excluit)
            case 5: return 1 # Sense límit

    for chip_value in chip_values:
        limit = int(limit_proportion(chip_value) * (player_money - new_chips_total) / chip_value)
        while player_money >= new_chips_total + chip_value and new_chips_dict[f"{chip_value:03}"] < limit:
            new_chips_dict[f"{chip_value:03}"] += 1
            new_chips_total += chip_value

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
        for i, chip in enumerate(chips[current_player["name"]]):
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
    chips[current_player["name"]].clear()
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
            chips[current_player["name"]].append(chip_dict)

def delete_unmoved_chips():
    # Esborrar les fitxes del jugador actual que no s'han mogut 
    moved_chips = []
    for chip in chips[current_player["name"]]:
        if chip["current_cell"] != 'owner':
            moved_chips.append(chip)
    chips[current_player["name"]] = moved_chips.copy()

def any_chip_dragged():
    '''Devuelve True si alguna ficha está siendo arrastrada'''
    for chip in chips[current_player["name"]]:
        if chip['dragged']:
            return True
    return False

def release_all_chips():
    '''Dentro del array 'chips', define el valor 'dragged' de todas las fichas como False'''
    for chip in chips[current_player["name"]]:
        chip['dragged'] = False

def confirm_bet():
    bet_dict = {}
    units = 0
    for chip in chips[current_player["name"]]:
        bet_dict["bet_on"] = chip["current_cell"]
        units += chip["value"]
        players[current_player["name"]][f"{chip["value"]:03}"] -= 1
    bet_dict["units"] = units
    current_bets.append(bet_dict)

def was_bet_correct(player_name):
    bet_dict = current_bets[player_names.index(player_name)]
    bet_on = bet_dict["bet_on"]
    n = current_number["n"]
    
    if bet_on.isdigit():
        return n == bet_on
    elif "column" in bet_on:
        column_number = int(bet_on[-1])
        return n % 3 == column_number
    else:
        order_i = number_order.index(n)
        match bet_on:
            case "EVEN":  return n % 2 == 0
            case "ODD":   return n % 2 == 1
            case "BLACK": return order_i % 2 == 0
            case "RED":   return order_i % 2 == 1

def give_out_prizes():
    pass

def log_game_info():
    round_info = {
        "result": current_number["n"],
        "bets": current_bets.copy(),
        "credits": [total_money_player(name) for name in player_names]
    }
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
    def destination(chip, correct_bet):
        if correct_bet:
            return chips_initial_positions[str(chip["value"])]
        else:
            return board_cell_areas["HOUSE"]["center"]
    
    for name in player_names:
        correct_bet = was_bet_correct(name)
        for chip in chips[name]:
            dest_pos = destination(chip, correct_bet)
            chip["dest"] = {
                "x": dest_pos["x"],
                "y": dest_pos["y"],
                "arrived": False
            }

def all_chips_arrived():
    return all(all(chip['dest']['arrived'] for chip in chips[name]) for name in player_names)

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