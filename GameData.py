# Ratolí

mouse = {"x": -1, "y": -1, 
"pressed": False, "held": False, "released": False}

# Inicialitzar dades

player_names = ["taronja", "blau", "lila"]
players = {"taronja": {}, "blau": {}, "lila": {}}

chip_values = [100, 50, 20, 10, 5]
chips = {"taronja": [], "blau": [], "lila": []}

# Mode 'betting'

current_player = {"name": player_names[0], "index": 0}
current_bets = {}
current_mode = {"betting": True, "roulette": False, "moving_chips": False, "game_over": False, "info": False}

# Mode 'roulette'

current_number = {"n": 0}
spin_counter = {"n": 0}

# Següent ronda

round_info = {"result": -1, "bets": [], "credits": []}
new_round_delay = {"bool": False, "timer": 0, "wait_time": 2}

# Mode info

game_info = []
