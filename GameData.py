current_number = {"n": 0}
spin_counter = {"n": 0}

chip_values = [100, 50, 20, 10, 5]

player_names = ["taronja", "blau", "lila"]
current_player = {"name": "taronja"}

players = {}
chips = {"taronja": [], "blau": [], "lila": []}

current_mode = {"betting": True, "roulette": False, "moving_chips": False,  "info": False}
current_bets = []

# Llista de diccionaris: {"result":, "bets":, "credits":}
game_info = []
game_info_keys = ["result", "bets", "credits"]