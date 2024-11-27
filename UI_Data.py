from pygame import Surface, display, SRCALPHA

# Pantalla

screen = display.set_mode((800, 450))
display.set_caption('Window Title')

# Colors

WHITE = (255, 255, 255)
LIGHT_GRAY = (204, 204, 204)
GRAY = (128, 128, 128)
DARK_GRAY = (51, 51, 51)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (128, 0, 32)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 85, 17)
GOLD = (255, 153, 0)
DARK_GOLD = (102, 61, 0)
BROWN = (102, 68, 34)
ORANGE = (255, 102, 0) 
BLUE  = (0, 102, 255)
PURPLE = (128, 51, 221)

BLACK_ALPHA = (0, 0, 0, 192)

# Mode 'roulette'

roulette = {"position": (10,10), "radius": 150,
"angle_offset": 360/37/2, "spin_speed": 0, "spin_acc": -100,
"states": {"about_to_spin": False, "spinning": False, "readjusting": False, "idle": True, "spin_canceled": False}}

roulette_surface = Surface((roulette["radius"]*2 + 40,roulette["radius"]*2))
roulette_surface.fill(DARK_GREEN)

number_order = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27,
    13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 
    20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

spin_button = {
    "x": roulette["position"][0] + roulette["radius"] - 50,
    "y": roulette["position"][1] + roulette["radius"] * 2.1,
    "width": 100, "height": 50,
    "enabled": True, "pressed": False, "string": "Spin!"}

# Mode 'betting' i 'moving chips'

board = {"x": 350, "y": 10, "columns": 4, "rows": 12, "grid_x": 50, "grid_y": 50,
    "cell": {"width": 28, "height": roulette["radius"]/3},
    "ellipse": {"width": 22, "height": 40}
}

grid_size = (board["cell"]["width"] * board["rows"],
             board["cell"]["height"] * board["columns"])
grid_surface = Surface(grid_size)
grid_surface.fill(DARK_GREEN)

board_size = (grid_size[0] + board["grid_x"] + board["cell"]["width"]*1.5,
              grid_size[1] + board["grid_y"])
board_surface = Surface(board_size)
board_surface.fill(DARK_GREEN)

board_cell_areas = {}
house_space = {}

chips_initial_positions = {}
drag_offset = {'x': 0, 'y': 0}

bet_button = {
    "x": board["x"] + board["grid_x"] + board["cell"]["width"]*7 + 5, 
    "y": board["y"] + 5,
    "width": board["cell"]["width"]*4 - 10, 
    "height": board["grid_y"] - 10,
    "enabled": True, "pressed": False, "string": "Bet!"}

player_grid = {"x": board["x"] + board["grid_x"]/2, "y": 300, "rows": 4, "columns": 6,
    "cell": {"width": board["cell"]["width"]*2, "height": roulette["radius"]/5,
            "1st_w": board["cell"]["width"]*2 + board["grid_x"], "1st_h":  roulette["radius"]/3}
}

pg_width = player_grid["cell"]["1st_w"] + player_grid["cell"]["width"] * (player_grid["columns"]-1)
pg_height = player_grid["cell"]["1st_h"] + player_grid["cell"]["height"] * (player_grid["rows"]-1)
pg_size = (pg_width, pg_height)
player_grid_surface = Surface(pg_size)
player_grid_surface.fill(DARK_GREEN)

# Mode 'game_over'

game_over_screen = Surface((800, 450), SRCALPHA)
game_over_screen.fill(BLACK_ALPHA)

game_over_window = {"x": 240, "y": 135, "width": 320, "height": 180}

# Mode 'info'

gi_surface = Surface((800, 450), SRCALPHA)
gi_surface.fill(BLACK_ALPHA)

gi_window = {"x": 80, "y": 45, "width": 640, "height": 360}
game_info_chart = {
    "x": gi_window["x"] + 20, 
    "y": gi_window["y"] + 60,
    "width": gi_window["width"] - 80,
    "height": gi_window["height"] - 72,
    "visible": False
}

gi_button = {
    "x": spin_button["x"],
    "y": 400, "width": 100, "height": 30,
    "enabled": True, "pressed": False, "string": "Game Info"}

gi_close_button = {
    "x": gi_window["x"] + gi_window["width"] - 30, 
    "y": gi_window["y"] + 10, 
    "width": 20, "height": 20,
    "enabled": True, "pressed": False
}

gi_scroll = {"x": gi_window["x"] + gi_window["width"] - 20, 
             "y": gi_window["y"] + 55, 
             "width": 5, "height": 250, 
             "radius": 10, "percentage": 0, "dragging": False,
             "surface_offset": 0, "visible_height": game_info_chart["height"], "total_height": -1,
             "visible": False}
