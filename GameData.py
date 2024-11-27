mouse = {"x": -1, "y": -1, 
"pressed": False, "held": False, "released": False}

current_number = {"n": 0}
spin_counter = {"n": 0}

chip_values = [100, 50, 20, 10, 5]

player_names = ["taronja", "blau", "lila"]
current_player = {"name": "taronja", "index": 0}

players = {"taronja": {}, "blau": {}, "lila": {}}
chips = {"taronja": [], "blau": [], "lila": []}

current_mode = {"betting": True, "roulette": False, "moving_chips": False,  "info": False}
current_bets = {}

# Llista de diccionaris: {"result":, "bets":, "credits":}
game_info = []
round_info = {"result": -1, "bets": [], "credits": []}

new_round_delay = {"bool": False, "timer": 0, "wait_time": 2}