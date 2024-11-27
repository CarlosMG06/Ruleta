from GameData import *
from UI_Data import *
import math
import utils
from pygame.time import delay

# Inicialitzar dades

def init_players():
    """Inicialitza el diccionari que conté informació dels jugadors."""
    starting_chips = list(zip(chip_values, (0,1,1,2,2))) # Las tuplas son: (NomFicha, Cantidad
    for name in player_names:
        starting_chips_dict = {}
        for chip in starting_chips:
            chip_value = f'{chip[0]:03}'
            chip_amount = chip[1]
            starting_chips_dict[chip_value] = chip_amount
        players[name]["chips"] = starting_chips_dict
        players[name]["credit"] = total_credit_player(name)

def total_credit_player(player_name):
    """Retorna el crèdit total que té el jugador, a partir de les seves fitxes."""
    total_credit = 0
    for chip_value, chip_amount in players[player_name]["chips"].items():
        total_credit += int(chip_value) * chip_amount
    return total_credit

def init_chips():
    """Inicialitza les fitxes del jugador actual."""
    chips[current_player["name"]].clear()
    for value in chip_values:
        amount = players[current_player["name"]]["chips"][f"{value:03}"]
        for _ in range(amount):
            chip_dict = {}
            chip_dict['value'] = value
            chip_dict['owner'] = current_player["name"]
            chip_dict['pos'] = {'x': chips_initial_positions[str(value)]['x'], 'y': chips_initial_positions[str(value)]['y']}
            chip_dict['radius'] = 8 + int(math.log2(value)*2)
            chip_dict['dragged'] = False
            chip_dict['current_cell'] = 'owner'
            chips[current_player["name"]].append(chip_dict)

def init_chip_positions():
    """Inicialitza les posicions inicials de les fitxes segons el seu valor."""
    c_w = player_grid["cell"]["width"]
    c_1w, c_1h = player_grid["cell"]["1st_w"], player_grid["cell"]["1st_h"]
    for i in range(len(chip_values)):
        chip_x = player_grid['x'] + c_1w + c_w/2 + c_w*i
        chip_y = player_grid['y'] + c_1h/2
        chips_initial_positions[str(chip_values[i])] = {'x':chip_x, 'y':chip_y}

# Mode 'betting'

def valid_chip_position(chip, cell):
    '''Comprova que la fitxa posada en la taula d'apostes està en una posició vàlida.'''
    chip_in_rect = utils.is_point_in_rect(chip['pos'], board_cell_areas[cell]['rect'])
    chip_in_triangle = False
    if cell in ['0', 'column 1', 'column 2', 'column 3']:
        chip_in_triangle = utils.is_point_in_triangle(chip['pos'], board_cell_areas[cell]['vertices'])
    
    if chip_in_rect or chip_in_triangle:
        return True
    return False

def any_chip_dragged():
    '''Retorna True si qualsevol fitxa s'està arrossegant.'''
    for chip in chips[current_player["name"]]:
        if chip['dragged']:
            return True
    return False

def release_all_chips():
    """Canvia el valor "dragged" de totes les fitxes a False."""
    for chip in chips[current_player["name"]]:
        chip['dragged'] = False

def drag_chips():
    """Controla l'arrossegament de les fitxes, actualitzant els seus diccionaris."""
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
            for chip in chips[current_player["name"]]:
                if chip['dragged'] == True:
                    for board_cell in board_cell_areas:
                        valid = False
                        if valid_chip_position(chip, board_cell):
                            # Posició vàlida
                            valid = True
                            chip["current_cell"] = board_cell
                            break
                    if not valid:
                        # Posició invàlida. Es retorna a la posició inicial.
                        chip["current_cell"] = 'owner'
                        chip['pos']['x'] = chips_initial_positions[str(chip['value'])]['x']
                        chip['pos']['y'] = chips_initial_positions[str(chip['value'])]['y']
            release_all_chips()
        else:
            for chip in chips[current_player["name"]]:
                if chip['dragged']:
                    chip['pos']['x'] = mouse['x'] - drag_offset['x']
                    chip['pos']['y'] = mouse['y'] - drag_offset['y']

def delete_unmoved_chips():
    """Esborra les fitxes del jugador actual que no s'han mogut."""
    moved_chips = []
    for chip in chips[current_player["name"]]:
        if chip["current_cell"] != 'owner':
            moved_chips.append(chip)
    chips[current_player["name"]] = moved_chips.copy()

def confirm_bet():
    """Confirma el conjunt d'apostes del jugador actual i guarda la llista."""
    cur_p_name = current_player["name"]
    
    bet_dict = {}
    for chip in chips[cur_p_name]:
        current_cell = chip["current_cell"]
        bet_dict[current_cell] = bet_dict.get(current_cell, 0) + chip["value"]
        players[cur_p_name]["chips"][f"{chip['value']:03}"] -= 1
    
    bet_list = [{"bet_on": cell, "units": units} for cell, units in bet_dict.items()]
    
    players[cur_p_name]["credit"] = total_credit_player(cur_p_name)
    current_bets[cur_p_name] = bet_list

def next_player():
    """Passa el torn al següent jugador amb crèdit. 
    Si n'és el primer jugador, canvia de mode. En cas contrari, inicialitza les seves fitxes."""
    next_player_i = current_player["index"]
    while True:
        next_player_i += 1
        next_player_i %= len(player_names)
        
        current_player["index"] = next_player_i
        current_player["name"] = player_names[next_player_i]
        
        if current_player["index"] == 0:
            change_mode()
            break
        elif players[current_player["name"]]["credit"] > 0:
            init_chips()
            break

def change_mode(to_info = False, to_game_over = False):
    """Canvia el mode del joc."""
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
    elif to_game_over:
        current_mode[mode] = False
        current_mode["game_over"] = True
    else:
        main_modes = [key for key in current_mode.keys() if key not in ("info", "game_over")]
        new_mode_index = (main_modes.index(mode)+1) % len(main_modes)
        current_mode[mode] = False
        current_mode[main_modes[new_mode_index]] = True

# Mode 'roulette'

def change_roulette_state(cancel_spin = False):
    """Canvia l'estat de la ruleta."""
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

def spin_roulette(delta_time):
    """Gira la ruleta."""
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

def readjust_roulette():
    """Reajusta la ruleta després de girar per tornar a alinear la casella amb la fletxa"""
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

# Mode 'moving_chips'

def was_bet_correct(bet_dict):
    """Determina si una aposta ha sigut acertada o no."""
    bet_on = bet_dict["bet_on"]
    n = current_number["n"]
    
    if bet_on.isdigit():
        return n == int(bet_on)
    elif n == 0:
        return False
    elif "column" in bet_on:
        column_number = int(bet_on[-1])
        return n % 3 == column_number % 3
    else:
        order_i = number_order.index(n)
        match bet_on:
            case "EVEN":  return n % 2 == 0
            case "ODD":   return n % 2 == 1
            case "BLACK": return order_i % 2 == 0
            case "RED":   return order_i % 2 == 1

def set_chips_destination():
    """Declara a quina posició han d'anar les fitxes, en funció del resultat de l'aposta."""
    # Definir clave 'dest' en chips, que tiene como valor un dict del tipo {'x':int, 'y':int, 'arrived':False}
    def destination(chip, correct_bet):
        if correct_bet:
            return chips_initial_positions[str(chip["value"])]
        else:
            return house_space["center"]
    
    for player_name, bet_list in current_bets.items():
        for bet_dict in bet_list:
            correct_bet = was_bet_correct(bet_dict)
            for chip in chips[player_name]:
                if chip["current_cell"] == bet_dict["bet_on"]:
                    dest_pos = destination(chip, correct_bet)
                    chip["dest"] = {
                        "x": dest_pos["x"],
                        "y": dest_pos["y"],
                        "arrived": False
                    }

def all_chips_arrived():
    """Retorna True si totes les fitxes han arribat a on han d'anar."""
    return all(all(chip['dest']['arrived'] for chip in chips[name]) for name in player_names)

def move_chips_towards_destination():
    """Mou cadascuna de les fitxes cap a on li toca."""
    chip_speed = 2
    for name in player_names:
        for chip in chips[name]:
            if not chip['dest']['arrived']:
                # Calculamos el ángulo
                delta_x = chip['pos']['x'] - chip['dest']['x'] 
                delta_y = chip['pos']['y'] - chip['dest']['y']
                rad = math.atan2(delta_y, delta_x) 
                # Calculamos la variación de posición en función del ángulo
                chip['pos']['x'] -= math.cos(rad) * chip_speed
                chip['pos']['y'] -= math.sin(rad) * chip_speed
                # Si la ficha está lo suficientemente cerca del destino, decidimos que ya ha llegado
                if utils.is_point_in_circle(chip['pos'], chip['dest'], r=5):
                    chip['pos']['x'] = chip['dest']['x'] 
                    chip['pos']['y'] = chip['dest']['y']
                    chip['dest']['arrived'] = True

# Següent ronda

def next_round():
    """Passa a la següent ronda."""
    hand_out_prizes()
    for name in player_names:
        redistribute_player_chips(name)
    log_round_info()
    
    delay(int(new_round_delay["wait_time"]*1000/2)) # Esperar un segon abans d'esborrar les fitxes
    for name in player_names:
        chips[name].clear()

    if all(players[name]["credit"] == 0 for name in player_names):
        game_over()
    else:
        change_mode()
        new_round_delay["bool"] = True

def hand_out_prizes():
    """Atorga premis per les apostes acertades de cada jugador."""
    for player_name, bet_list in current_bets.items():
        for bet_dict in bet_list:
            if was_bet_correct(bet_dict):
                bet_units = bet_dict["units"]
                prize = bet_units # Retornar les unitats apostades

                bet_on = bet_dict["bet_on"]
                if bet_on.isdigit():
                    prize += bet_units * 35
                elif "column" in bet_on:
                    prize += bet_units * 2
                else:
                    prize += bet_units
                
                players[player_name]["credit"] += prize

def redistribute_player_chips(player_name):
    """Redistribueix les fitxes que té un jugador per assegurar que té la major varietat de fitxes possibles."""
    global players
    new_chips_dict = {'100': 0, '050': 0, '020': 0, '010': 0, '005': 0}
    player_credit = players[player_name]["credit"]
    new_chips_total = 0

    def limit_proportion(chip_value):
        match chip_value:
            case 100: return 5/9 - 0.001 # apareix a partir de 180 (excluit)
            case 50: return 5/8 - 0.001  # apareix a partir de 80 (excluit)
            case 20: return 2/3 - 0.001  # apareix a partir de 30 (excluit)
            case 10: return 1 - 0.001    # apareix a partir de 10 (excluit)
            case 5: return 1 # Sense límit

    for chip_value in chip_values:
        limit = int(limit_proportion(chip_value) * (player_credit - new_chips_total) / chip_value)
        while player_credit >= new_chips_total + chip_value and new_chips_dict[f"{chip_value:03}"] < limit:
            new_chips_dict[f"{chip_value:03}"] += 1
            new_chips_total += chip_value

    players[player_name]["chips"] = new_chips_dict

def log_round_info():
    """Registra l'informació de la ronda actual."""
    round_info = {
        "result": current_number["n"],
        "bets": current_bets.copy(),
        "credits": [players[name]["credit"] for name in player_names]
    }
    game_info.append(round_info)

    current_bets.clear()

# Mode 'info'

def drag_scroll():
    """Controla l'arrossegament del scroll, actualitzant el offset de la superfície."""
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
    
    gi_scroll["surface_offset"] = int((gi_scroll["percentage"] / 100) * (gi_scroll["total_height"] - gi_scroll["visible_height"]))

# Mode 'game_over'

def game_over():
    change_mode(to_game_over=True)
    margin_x = (game_over_window["width"] - gi_button["width"])/2
    gi_button["x"] = game_over_window["x"] + margin_x
    margin_y = margin_x/4
    gi_button["y"] = game_over_window["y"] + game_over_window["height"] - gi_button["height"] - margin_y
    game_over_window["margin"] = {"x": margin_x, "y": margin_y}