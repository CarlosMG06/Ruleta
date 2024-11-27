from UI_Data import *
from GameData import *
from pygame import draw, font
from pygame.transform import rotate
import utils
import math

# Fonts

font.init()
font_tiny = font.SysFont("Arial", 12, bold=True)
font_small = font.SysFont("Arial", 15, bold=True)
font_small_thin = font.SysFont("Arial", 15)
font_medium = font.SysFont("Arial", 18, bold=True)
font_big = font.SysFont("Arial", 27, bold=True)
font_big_thin = font.SysFont("Arial", 24)
font_huge = font.SysFont("Arial", 45, bold=True)
font_serif = font.SysFont("Times New Roman", 21)

# Mode 'roulette'

def update_current_number():
    """Actualitza el número actual basant-se en la seva posició angular."""
    for i, n in enumerate(number_order):
        angle = (360/37*i + roulette["angle_offset"]) % 360
        prev_angle = angle - 360/37
        if angle + prev_angle < 360/37:
            current_number["n"] = n
            break

def draw_current_number():
    """Dibuixa el número actual dins el panell central de la ruleta."""
    r = roulette["radius"]
    c = (r,r)
    n = current_number["n"]
    i = number_order.index(n)
    color = get_roulette_number_color(i)

    draw_current_number_panel(color)

    render_centered_text(roulette_surface, font_huge,
                         str(n), c, WHITE)

def init_roulette():
    """Dibuixa les parts estàtiques de la ruleta i dibuixa l'anell de números un cop."""
    r = roulette["radius"]
    c = (r,r)

    draw.circle(roulette_surface, DARK_GOLD, c, r, 6)
    draw.circle(roulette_surface, BROWN, c, r-46)
    
    draw_current_number_panel(DARK_GRAY)

    # Fletxa
    arrow_points = [
        (c[0]+r+8, c[1]),
        (c[0]+r+23, c[1]+8),
        (c[0]+r+23, c[1]-8)
    ]
    draw.polygon(roulette_surface, GOLD, arrow_points)

    update_roulette()

def update_roulette():
    """Actualitza l'anell de números de la ruleta"""
    r = roulette["radius"]
    c = (r,r)

    for i, n in enumerate(number_order):
        color = get_roulette_number_color(i)
        
        # Polígon
        angle = (360/37*i + roulette["angle_offset"]) % 360
        p0 = utils.point_on_circle(c, r-30, angle)
        p1 = utils.point_on_circle(c, r-6, angle)

        prev_angle = angle - 360/37
        prev_0 = utils.point_on_circle(c, r-30, prev_angle)
        prev_1 = utils.point_on_circle(c, r-6, prev_angle)

        points = [p0,p1,prev_1,prev_0]
        draw.polygon(roulette_surface, color, points)
        draw.polygon(roulette_surface, LIGHT_GRAY, points, 3)

        # Text
        polygon_center = (int((p0[0]+prev_1[0])/2), int((p0[1]+prev_1[1])/2))
        text_angle = -angle - 90 + 360/37/2
        render_centered_text(roulette_surface, font_small, str(n),
                             polygon_center, WHITE, rotation_angle=text_angle)

# Funcions auxiliars ruleta

def get_roulette_number_color(i):
    """Retorna el color corresponent al número en funció del seu índex."""
    if i == 0:
        return GREEN
    elif i % 2 == 1:
        return RED
    else:
        return BLACK

def draw_current_number_panel(fill_color):
    """Dibuixa el panell central la ruleta que mostra el nñumero actual."""
    r = roulette["radius"]
    draw.rect(roulette_surface, fill_color, (r-40, r-40, 80, 80))
    draw.rect(roulette_surface, GOLD, (r-40, r-40, 80, 80), 5)

# Mode 'betting' i 'moving_chips'

def init_betting_grid():
    """Inicialitza la graella principal de la taula d'apostes."""
    cols, rows = board["columns"], board["rows"]
    c_w, c_h = board["cell"]["width"], board["cell"]["height"]
    e_w, e_h = board["ellipse"]["width"], board["ellipse"]["height"]

    # Números
    for i, n in enumerate(number_order):
        if n == 0:
            continue
        color = RED if i % 2 == 1 else BLACK
        col = math.ceil(n / 3) #1 2 3 4 5 6 7 8... → 1 1 1 2 2 2 3 3...
        row = (1, 3, 2)[n % 3] #1 2 3 4 5 6 7 8... → 3 2 1 3 2 1 3 2...

        x = c_w * (col-1)
        y = c_h * (row-1)
        center_x = x + c_w / 2 - 1
        center_y = y + c_h / 2
        
        ellipse_rect = [center_x - e_w / 2, center_y - e_h / 2, e_w, e_h]
        draw.ellipse(grid_surface, color, ellipse_rect)

        render_centered_text(grid_surface, font_medium, str(n), (center_x - 1, center_y), WHITE, rotation_angle=90)

        board_cell_areas[str(n)] = {
            "rect": {"x": x + board['x'] + board['grid_x'], 
                     "y": y + board['y'] + board['grid_y'], 
                     "width": c_w, "height": c_h}
        }

    # Cel·les inferiors
    for bottom_cell in range(4):
        x, y = c_w * 3 * bottom_cell, c_h * 3
        center_x, center_y = x + c_w * 1.5, y + c_h * 0.5

        if bottom_cell in (0, 3):
            string = "EVEN" if bottom_cell == 0 else "ODD"
            render_centered_text(grid_surface, font_serif, string, (center_x, center_y), WHITE)
        else:
            string = "RED" if bottom_cell == 2 else "BLACK"

            color = RED if string == "RED" else BLACK
            diamond_points = [(x + c_w * 0.3, center_y), (center_x, y + c_h * 0.1),
                              (x + c_w * 2.7, center_y), (center_x, y + c_h * 0.9)]
            draw.polygon(grid_surface, color, diamond_points)
            draw.polygon(grid_surface, LIGHT_GRAY, diamond_points, 3)

        board_cell_areas[string] = {"rect": {"x": x + board['x'] + board['grid_x'], 
                                             "y": y + board['y'] + board['grid_y'], 
                                             "width": c_w * 3, "height": c_h}}

    # Quadre extern i línies internes
    draw.rect(grid_surface, LIGHT_GRAY, (0, 0, grid_size[0], grid_size[1]), 3)
    for col in range(1, cols):
        draw.line(grid_surface, LIGHT_GRAY, (0, c_h * col), (grid_size[0], c_h * col), 3)
    for row in range(1, rows):
        x = c_w * row
        y_end = grid_size[1] if row % 3 == 0 else grid_size[1] - c_h
        draw.line(grid_surface, LIGHT_GRAY, (x, 0), (x, y_end), 3)

def init_betting_board():
    """Inicialitza la taula d'apostes."""
    grid_x, grid_y = board["grid_x"], board["grid_y"]
    rows = board["rows"]
    c_w, c_h = board["cell"]["width"], board["cell"]["height"]

    # Espai de zero
    zero_points = [[grid_x, grid_y + 1], [grid_x * 2 / 3, grid_y + 1],
                   [0, grid_y + c_h * 1.5], [grid_x * 2 / 3, grid_y + c_h * 3], [grid_x, grid_y + c_h * 3]]
    draw.lines(board_surface, LIGHT_GRAY, False, zero_points, 3)
    center = (grid_x * 5/9, zero_points[2][1])
    render_centered_text(board_surface, font_big, "0", 
                         center, WHITE, DARK_GREEN, rotation_angle=90)

    for point in zero_points:
        point[0] += board["x"]
        point[1] += board["y"]
    board_cell_areas["0"] = {
        "rect": {"x": zero_points[1][0], "y": zero_points[1][1], 
                 "width": zero_points[0][0] - zero_points[3][0], 
                 "height": zero_points[3][1] - zero_points[0][1]},
        "vertices": zero_points[1:4]
    }

    # Graella
    board_surface.blit(grid_surface, (grid_x, grid_y))

    # Espai de la banca
    house_rect = [grid_x + c_w + 5, 5, c_w * 4 - 10, grid_y - 10]
    draw.rect(board_surface, LIGHT_GRAY, house_rect, 3)
    center_x = house_rect[0] + house_rect[2]/2
    center_y = house_rect[1] + house_rect[3]/2
    render_centered_text(board_surface, font_serif, "HOUSE",
                         (center_x, center_y), WHITE, DARK_GREEN)

    center_x += board["x"]
    center_y += board["y"]
    house_space["center"] = {"x": center_x, "y": center_y}

    # Espais de columnes
    x = grid_x + c_w * rows
    for col in range(3):
        y = grid_y + c_h * col
        center = (x + c_w / 2, y + c_h / 2)
        render_centered_text(board_surface, font_small, "2 : 1", 
                             center, WHITE, DARK_GREEN, rotation_angle=90)
        
        center = (center[0] - 1, center[1] + 1)
        points = [[x, y+1],
        [x + c_w*0.9, y+1],
        [x + c_w*1.4, y + c_h/2],
        [x + c_w*0.9, y + c_h],
        [x, y + c_h]]
        
        lines_points = points if col == 0 else points[1:]
        draw.lines(board_surface, LIGHT_GRAY, False, lines_points, 3)

        for i in range(len(points)):
            points[i][0] += board["x"]
            points[i][1] += board["y"]
        board_cell_areas[f"column {3-col}"] = {
            "rect": {"x": points[0][0], "y": points[0][1], 
                     "width": points[3][0] - points[0][0], 
                     "height": points[3][1] - points[0][1]},
            "vertices": points[1:4]
        }

def init_player_grid():
    """Inicialitza la primera col·lumna i la primera fila de la graella dels jugadors
    i dibuixa les quantitats de fitxes un cop."""

    # Abreujar noms
    cols, rows = player_grid["columns"], player_grid["rows"]
    c_w, c_h = player_grid["cell"]["width"], player_grid["cell"]["height"]
    c_1w, c_1h = player_grid["cell"]["1st_w"], player_grid["cell"]["1st_h"]

    # Noms dels jugadors i siluetes de fitxes
    for row in range(rows):
        center_y = c_1h / 2 if row == 0 else c_1h + c_h * (row - 0.5)
        name = player_names[row - 1]
        for col in range(cols):
            center_x = c_1w / 2 if col == 0 else c_1w + c_w * (col - 0.5)
    
            # Primera cel·la: buida
            if row == 0 and col == 0:
                continue
            
            # Primera fila: siluetes de fitxes
            elif row == 0:
                chip_dict = {
                    "value": chip_values[col-1],
                    "pos": {"x": center_x, "y": center_y},
                    "radius": 8 + int(math.log2(chip_values[col-1])*2)
                }
                draw_chip(chip_dict, silhouette=True)

            # Primera columna: noms dels jugadors
            elif col == 0:
                color = get_player_color(name)
                
                if players[name]["creditless"]:
                    x = 0
                    y = center_y - c_h * 0.5
                    draw.rect(player_grid_surface, DARK_RED, [x, y, c_1w, c_h])
                
                render_centered_text(player_grid_surface, font_small, name, 
                                     (center_x, center_y), color)
    
    # Línies internes
    for col in range(1, cols):
        x = c_1w + c_w * (col - 1)
        draw.line(player_grid_surface, LIGHT_GRAY, (x, 0), (x, pg_size[1]), 3)
    for row in range(1, rows):
        y = c_1h + c_h * (row - 1)
        draw.line(player_grid_surface, LIGHT_GRAY, (0, y), (pg_size[0], y), 3)
    
    update_player_grid()

def update_player_grid():
    """Actualitza les quantitats de fitxes de la graella dels jugadors."""
    cols, rows = player_grid["columns"], player_grid["rows"]
    c_w, c_h = player_grid["cell"]["width"], player_grid["cell"]["height"]
    c_1w, c_1h = player_grid["cell"]["1st_w"], player_grid["cell"]["1st_h"]

    for row in range(1, rows):
        center_y = c_1h + c_h * (row - 0.5)
        name = player_names[row - 1]
        for col in range(1, cols):
            center_x = c_1w + c_w * (col - 0.5)

            color = DARK_RED if players[name]["creditless"] else DARK_GREEN
            
            x = center_x - c_w * 0.5
            y = center_y - c_h * 0.5
            draw.rect(player_grid_surface, color, [x+2, y+2, c_w-3, c_h-4])

            amount = players[name]["chips"][f"{chip_values[col - 1]:03}"]
            render_centered_text(player_grid_surface, font_small, f"× {str(amount)}", 
                                 (center_x, center_y), WHITE)


def draw_chip(chip_dict, silhouette=False):
    """Dibuixa una fitxa a partir del seu diccionari."""
    value = int(chip_dict["value"])
    pos = tuple(chip_dict['pos'].values())
    radius = chip_dict["radius"]

    if silhouette:
        polygon_color1 = DARK_GREEN
        polygon_color2 = tuple(c * 7/5 for c in polygon_color1)
        color = tuple(c * 9/10 for c in polygon_color1)
        bg_color = tuple(c * 7/6 for c in polygon_color1)
    else:
        owner = chip_dict["owner"]
        bg_color = get_player_color(owner)
        color = tuple(c / 2 for c in bg_color)

    surface = player_grid_surface if silhouette else screen

    draw.circle(surface, bg_color, pos, radius)
    render_centered_text(surface, font_tiny, str(value), pos, color)

    # Patró decoratiu
    for i in range(8):    
        angle = 360/8 * (i + 0.25)
        p0 = utils.point_on_circle(pos, radius*2/3, angle)
        p1 = utils.point_on_circle(pos, radius-1, angle)

        angle -= 360/8/2
        p2 = utils.point_on_circle(pos, radius-1, angle)
        p3 = utils.point_on_circle(pos, radius*2/3, angle)

        if silhouette:
            polygon_color = polygon_color2 if i % 2 == 0 else polygon_color1
        else:
            polygon_color = LIGHT_GRAY if i % 2 == 0 else DARK_GRAY
        draw.polygon(surface, polygon_color, [p0,p1,p2,p3])  

    # Vores
    border_width = 2
    inner_border_width = 1
    if value >= 50:
        border_width += 1
        inner_border_width += 1
    draw.circle(surface, color, pos, radius, border_width)
    draw.circle(surface, color, pos, radius*2/3, inner_border_width)   

# Mode 'info'

def init_game_info_chart():
    """Inicialitza les parts estàtiques de la pantalla de la informació de la partida."""
    # Finestra
    window_tuple = (gi_window["x"], gi_window["y"], gi_window["width"], gi_window["height"])
    draw.rect(gi_surface, DARK_GRAY, window_tuple)
    draw.rect(gi_surface, WHITE, window_tuple, 3)

    # Línia de capçalera
    header_line_y = 100
    draw.line(gi_surface, LIGHT_GRAY,
              (game_info_chart["x"], header_line_y), 
              (game_info_chart["x"] + game_info_chart["width"], header_line_y), 3)

    # Coordenades base per columnes
    column_positions = [
        {"col_x": game_info_chart["x"] + 40, "line_x": game_info_chart["x"] + 80},
        {"col_x": game_info_chart["x"] + 200, "line_x": game_info_chart["x"] + 320},
        {"col_x": game_info_chart["x"] + 440, "line_x": None}
    ]

    col_y = 70
    subcol_y = 88
    for i, (key, col_pos) in enumerate(zip(round_info.keys(), column_positions)):
        render_centered_text(gi_surface, font_medium, key.capitalize(),
                             (col_pos["col_x"], col_y), WHITE, None)

        # Línia divisoria de columna
        if col_pos["line_x"]:
            draw.line(gi_surface, LIGHT_GRAY, 
                      (col_pos["line_x"], 55), 
                      (col_pos["line_x"], game_info_chart["y"] + game_info_chart["height"]), 3)

        # Dibuixar subcolumnes (per a columna 2 i 3)
        if i > 0:
            for j, name in enumerate(player_names):
                color = get_player_color(name)
                subcol_x = col_pos["col_x"] + 80 * (j - 1)
                render_centered_text(gi_surface, font_small, name, 
                                     (subcol_x, subcol_y), color, None)
            
def update_game_info_chart():
    """Actualitza la graella de la informació de la partida."""
    width = game_info_chart["width"]
    height = 48 * sum(max(len(bet_list) for bet_list in round_info["bets"].values()) for round_info in game_info)
    gi_chart_surface = Surface((width, height), SRCALPHA)
    gi_chart_surface.fill(DARK_GRAY)
    
    y = 0
    for round_i, round_info in enumerate(game_info):
        len_max = max(len(bet_list) for bet_list in round_info["bets"].values())
        center_y = y + 24 * len_max
        
        render_centered_text(gi_chart_surface, font_big_thin, str(round_info["result"]), (40, center_y), WHITE, DARK_GRAY)

        for bet_i, bet_list in enumerate(round_info["bets"].values()):
            x = 120 + 80 * bet_i
            list_bet_y = [center_y + 24 * i for i in range(-len(bet_list) + 1, len(bet_list), 2)]
            for bet_i, bet_dict in enumerate(bet_list):
                bet_y = list_bet_y[bet_i]
                render_centered_text(gi_chart_surface, font_small_thin, f"{bet_dict['units']} units", (x, bet_y - 10), WHITE, DARK_GRAY)
                render_centered_text(gi_chart_surface, font_small_thin, f"on {bet_dict['bet_on']}", (x, bet_y + 10), WHITE, DARK_GRAY)
        
        for credit_i, credit in enumerate(round_info["credits"]):
            render_centered_text(gi_chart_surface, font_big_thin, str(credit), (360 + 80 * credit_i, center_y), WHITE, DARK_GRAY)
        
        if round_i < len(game_info) - 1:
            y += 48 * len_max
            draw.line(gi_chart_surface, LIGHT_GRAY, (0, y), (width, y), 3)
    draw.line(gi_chart_surface, LIGHT_GRAY, (80, 0), (80, height), 3)
    draw.line(gi_chart_surface, LIGHT_GRAY, (320, 0), (320, height), 3)

    if gi_scroll["visible"]:
        gi_scroll["total_height"] = height
        sub_surface = gi_chart_surface.subsurface((0, gi_scroll["surface_offset"], width, gi_scroll["visible_height"]))
        gi_surface.blit(sub_surface, (game_info_chart["x"], game_info_chart["y"]))
    else:
        gi_surface.blit(gi_chart_surface, (game_info_chart["x"], game_info_chart["y"]))

def draw_scroll():
    """Dibuixa el scroll en funció del percentatge."""
    rect_tuple = (gi_scroll["x"], gi_scroll["y"], gi_scroll["width"], gi_scroll["height"])
    draw.rect(screen, GRAY, rect_tuple)

    circle_x = int(gi_scroll["x"] + gi_scroll["width"] / 2)
    circle_y = int(gi_scroll["y"] + (gi_scroll["percentage"] / 100) * gi_scroll["height"])
    circle_tuple = (circle_x, circle_y)
    draw.circle(screen, WHITE, circle_tuple, gi_scroll["radius"])

# Funcions auxiliars info

def show_game_info():
    """Mostra la informació de la partida."""
    game_info_chart["visible"] = True
    if sum(max(len(bet_list) for bet_list in round_info["bets"].values()) for round_info in game_info) > 6:
       gi_scroll["visible"] = True
       gi_scroll["percentage"] = 0

def hide_game_info():
    """Amaga la informació de la partida."""
    game_info_chart["visible"] = False

# Botons

def get_button_colors(button):
    """Calcula els colors d'un botó segons el seu estat."""
    if button["pressed"]:
        return GOLD, BLACK, BLACK
    elif not button["enabled"]:
        return DARK_GRAY, GRAY, GRAY
    else:
        return BLACK, LIGHT_GRAY, WHITE

def draw_button(button, spin_button=False, close_button=False, gi_button=False):
    """Dibuixa un botó segons el seu estat fent servir el seu diccionari."""
    b_rect_tuple = (button["x"], button["y"], button["width"], button["height"])
    fill_color, border_color, text_color = get_button_colors(button)

    surface = game_over_screen if gi_button and current_mode["game_over"] else screen
    draw.rect(surface, fill_color, b_rect_tuple)
    width = button["height"]//15
    draw.rect(surface, border_color, b_rect_tuple, width)
    
    if close_button:
        # Icona de tancar
        p0 = (button["x"] + 4, button["y"] + 4)
        p1 = (button["x"] + button["width"] - 6, button["y"] + button["height"] - 5)
        p2 = (p0[0], p1[1])
        p3 = (p1[0], p0[1])
        draw.line(surface, text_color, p0, p1, 4)
        draw.line(surface, text_color, p2, p3, 4)
    else:
        # Text
        b_font = font_big if spin_button else font_medium
        center = (button["x"] + button["width"]/2, button["y"] + button["height"]/2)
        render_centered_text(surface, b_font, button["string"], center, text_color)

# Mode 'game_over'

def init_game_over_screen():
    """Inicialitza la pantalla del final de la partida."""
    # Finestra
    window_tuple = (game_over_window["x"], game_over_window["y"], game_over_window["width"], game_over_window["height"])
    draw.rect(game_over_screen, DARK_GRAY, window_tuple)
    draw.rect(game_over_screen, WHITE, window_tuple, 3)

    # Text
    font_1 = font_huge
    center_x = game_over_window["x"] + game_over_window["width"]/2
    center_y = game_over_window["y"] + game_over_window["margin"]["y"] + font_1.get_linesize()/2
    render_centered_text(game_over_screen, font_1, "GAME OVER",
                         (center_x, center_y), DARK_RED)
    font_2 = font_serif
    center_y += font_1.get_linesize()/2 + 3 + font_2.get_linesize()/2
    render_centered_text(game_over_screen, font_2, "The house wins.",
                         (center_x, center_y), WHITE)

# Funcions auxiliars generals

def get_player_color(name):
    """Retorna el color associat al jugador."""
    match name:
        case "taronja": return ORANGE
        case "blau": return BLUE
        case "lila": return PURPLE

def render_centered_text(surface, font, text, position, color, bg_color=None, rotation_angle=None):
    """Renderitza i dibuixa text centrat en una posició específica."""
    rendered_text = font.render(text, True, color, bg_color)
    if rotation_angle:
        rendered_text = rotate(rendered_text, rotation_angle)
    text_rect = rendered_text.get_rect(center=position)
    surface.blit(rendered_text, text_rect)
