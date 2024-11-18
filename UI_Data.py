from pygame import Surface, display

screen = display.set_mode((800, 450))
display.set_caption('Window Title')

WHITE = (255, 255, 255)
LIGHT_GRAY = (204, 204, 204)
GRAY = (128, 128, 128)
DARK_GRAY = (51, 51, 51)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 85, 17)
GREEN = (0, 255, 0)
GOLD = (255, 153, 0)
DARK_GOLD = (102, 61, 0)
BLUE  = (0, 102, 255)
PURPLE = (153, 0, 255)
ORANGE = (255, 102, 0) 
BROWN = (102, 68, 34)

current_number_text = {"text": None, "rect": None}

number_order = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27,
    13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 
    20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

# Ruleta
roulette = {"position": (10,10), "radius": 150,
"angle_offset": 360/37/2, "spin_speed": 0, "spin_acc": -100,
"about_to_spin": False, "spin_canceled": False, "spinning": False, "readjusting": False}

roulette_surface = Surface((roulette["radius"]*2 + 40,roulette["radius"]*2))
roulette_surface.fill(DARK_GREEN)

# Botó de gir
spin_button = {
    "x": roulette["position"][0] + roulette["radius"] - 40,
    "y": roulette["position"][1] + roulette["radius"] * 2.5 - 15,
    "width": 80, "height": 30}

# Taula
board = {"x": 350, "y": 20, "columns": 4, "rows": 12, "table_x": 50,
"cell": {"width": 28, "height": roulette["radius"]/3}, "ellipse": {"width": 22, "height": 40}}

grid_size = (board["cell"]["width"] * board["rows"], board["cell"]["height"] * board["columns"])
grid_surface = Surface(grid_size)
grid_surface.fill(DARK_GREEN)

board_size = (grid_size[0]+board["table_x"]+board["cell"]["width"]*1.5,grid_size[1])
board_surface = Surface(board_size)
board_surface.fill(DARK_GREEN)

board_cell_areas = {}
