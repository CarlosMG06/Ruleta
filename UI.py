from UI_Data import *
from GameData import *
from pygame import draw, font
from pygame.transform import rotate
import utils
import math

font.init()
font_tiny = font.SysFont("Arial", 12, bold=True)
font_small = font.SysFont("Arial", 15, bold=True)
font_small_thin = font.SysFont("Arial", 15)
font_medium = font.SysFont("Arial", 18, bold=True)
font_big = font.SysFont("Arial", 27, bold=True)
font_big_thin = font.SysFont("Arial", 24)
font_huge = font.SysFont("Arial", 45, bold=True)
font_serif = font.SysFont("Times New Roman", 21)

def update_current_number():
    for i, n in enumerate(number_order):
        angle = (360/37*i + roulette["angle_offset"]) % 360
        prev_angle = angle - 360/37
        if angle + prev_angle < 360/37:
            current_number["n"] = n
            break

def draw_current_number():
    r = roulette["radius"]

    n = current_number["n"]
    i = number_order.index(n)
    if i == 0:
        color = GREEN
    elif i % 2 == 1:
        color = RED
    else:
        color = BLACK

    draw.rect(roulette_surface, color, (r-40, r-40, 80, 80))
    draw.rect(roulette_surface, GOLD, (r-40, r-40, 80, 80), 5)

    text = font_huge.render(str(n), True, WHITE)
    text_rect = text.get_rect(center = (r,r))
    roulette_surface.blit(text, text_rect)

def update_roulette():
    r = roulette["radius"]
    c = (r,r)

    draw.circle(roulette_surface, DARK_GOLD, c, r, 6)
    draw.circle(roulette_surface, BROWN, c, r-46)
    
    draw.rect(roulette_surface, DARK_GRAY, (r-40, r-40, 80, 80))
    draw.rect(roulette_surface, GOLD, (r-40, r-40, 80, 80), 5)

    arrow_points = [
    (c[0]+r+8, c[1]),
    (c[0]+r+23, c[1]+8),
    (c[0]+r+23, c[1]-8)]
    draw.polygon(roulette_surface, GOLD, arrow_points)
    
    for i, n in enumerate(number_order):
        angle = (360/37*i + roulette["angle_offset"]) % 360
        if i == 0:
            color = GREEN
        elif i % 2 == 1:
            color = RED
        else:
            color = BLACK
        
        p0 = utils.point_on_circle(c, r-30, angle)
        p1 = utils.point_on_circle(c, r-6, angle)

        prev_angle = angle - 360/37
        prev_0 = utils.point_on_circle(c, r-30, prev_angle)
        prev_1 = utils.point_on_circle(c, r-6, prev_angle)

        points = [p0,p1,prev_1,prev_0]
        draw.polygon(roulette_surface, color, points)
        draw.polygon(roulette_surface, LIGHT_GRAY, points, 3)

        polygon_center = (int((p0[0]+prev_1[0])/2), int((p0[1]+prev_1[1])/2))

        text_angle = -angle - 90 + 360/37/2
        text_n = font_small.render(str(n), True, WHITE)
        text_n_rotated = rotate(text_n, text_angle)
        text_n_rotated_rect = text_n_rotated.get_rect()
        text_n_rotated_rect.center = polygon_center
        roulette_surface.blit(text_n_rotated, text_n_rotated_rect)

def draw_button(button, spin_button=False, close_button=False):
    b_rect_tuple = (button["x"], button["y"], button["width"], button["height"])
    
    fill_color = BLACK
    border_color = LIGHT_GRAY
    text_color = WHITE
    if button["pressed"]:
        fill_color = GOLD
        border_color = BLACK
        text_color = BLACK
    elif not button["enabled"]:
        fill_color = DARK_GRAY
        border_color = GRAY
        text_color = GRAY
    
    surface = gi_surface if close_button else screen
    draw.rect(surface, fill_color, b_rect_tuple)
    width = button["height"]//15
    draw.rect(surface, border_color, b_rect_tuple, width)
    
    if close_button:
        p0 = (button["x"] + 4, button["y"] + 4)
        p1 = (button["x"] + button["width"] - 6, button["y"] + button["height"] - 5)
        p2 = (p0[0], p1[1])
        p3 = (p1[0], p0[1])
        draw.line(surface, text_color, p0, p1, 4)
        draw.line(surface, text_color, p2, p3, 4)
    else:
        b_font = font_big if spin_button else font_medium
        b_text = b_font.render(button["string"], True, text_color)
        center = (button["x"] + button["width"]/2, button["y"] + button["height"]/2)
        b_text_rect = b_text.get_rect(center=center)
        surface.blit(b_text, b_text_rect)

def init_grid_surface():
    # Abreujar noms
    cols, rows = board["columns"], board["rows"]
    c_w, c_h = board["cell"]["width"], board["cell"]["height"]
    e_w, e_h = board["ellipse"]["width"], board["ellipse"]["height"]

    # Números
    for i, n in enumerate(number_order):
        if n == 0: continue
        color = RED if i % 2 == 1 else BLACK
        row = (1, 3, 2)[n % 3] #1 2 3 4 5 6 7 8... → 3 2 1 3 2 1 3 2...
        col = math.ceil(n / 3) #1 2 3 4 5 6 7 8... → 1 1 1 2 2 2 3 3...
        x = c_w * (col-1)
        y = c_h * (row-1)
        ellipse_rect = [x + (c_w - e_w)/2, y + (c_h-e_h)/2, e_w, e_h]
        draw.ellipse(grid_surface, color, ellipse_rect)

        center_x = x + c_w / 2 - 1
        center_y = y + c_h / 2
        text_n = font_medium.render(str(n), True, WHITE)
        text_n_rotated =  rotate(text_n, 90)
        text_n_rotated_rect = text_n_rotated.get_rect(center=(center_x, center_y))
        grid_surface.blit(text_n_rotated, text_n_rotated_rect)

        board_cell_areas[str(n)] = {"rect": {"x": x + board['x'] + board['grid_x'], "y": y + board['y'] + board['grid_y'], "width": c_w, "height": c_h}}

    # Cel·les inferiors
    for bottom_cell in range(4):
        x = c_w * 3 * bottom_cell
        y = c_h * 3
        center_x = x + c_w * 1.5
        center_y = y + c_h * 0.5

        if bottom_cell in (0, 3):
            string = "EVEN" if bottom_cell == 0 else "ODD"
            
            text = font_serif.render(string, True, WHITE)
            text_rect = text.get_rect(center = (center_x, center_y))
            grid_surface.blit(text, text_rect)
        else:
            string = "RED" if bottom_cell == 2 else "BLACK"

            color = RED if string == "RED" else BLACK
            diamond_points = [
            (x + c_w * 0.3, center_y),
            (center_x, y + c_h * 0.1),
            (x + c_w * 2.7, center_y),
            (center_x, y + c_h * 0.9)]
            draw.polygon(grid_surface, color, diamond_points)
            draw.polygon(grid_surface, LIGHT_GRAY, diamond_points, 3)

        board_cell_areas[string] = {"rect": {"x": x + board['x'] + board['grid_x'], "y": y + board['y'] + board['grid_y'], "width": c_w * 3, "height": c_h}}

    #Quadre extern
    draw.rect(grid_surface, LIGHT_GRAY, (0, 0, grid_size[0], grid_size[1]), 3)

    #Línies internes
    for col in range(1, cols):
        y = c_h * col
        draw.line(grid_surface, LIGHT_GRAY, (0, y), (grid_size[0], y), 3)
    for row in range(1, rows):
        x = c_w * row
        y = grid_size[1]
        if row % 3 != 0:
            y -= c_h
        draw.line(grid_surface, LIGHT_GRAY, (x, 0), (x, y), 3)

def update_board():
    # Abreujar noms
    grid_x, grid_y = board["grid_x"], board["grid_y"]
    rows = board["rows"]
    c_w, c_h = board["cell"]["width"], board["cell"]["height"]
    
    # Espai de zero
    zero_points = [
    [grid_x,     grid_y + 1],
    [grid_x*2/3, grid_y + 1],
    [0,          grid_y + c_h * 1.5],
    [grid_x*2/3, grid_y + c_h * 3],
    [grid_x,     grid_y + c_h * 3]]
    draw.lines(board_surface, LIGHT_GRAY, False, zero_points, 3)

    text_zero = font_big.render("0", True, WHITE, DARK_GREEN)
    text_zero_rotated = rotate(text_zero, 90)
    text_zero_rotated_rect = text_zero_rotated.get_rect(center = (grid_x*5/9, zero_points[2][1]))
    board_surface.blit(text_zero_rotated, text_zero_rotated_rect)

    for i in range(len(zero_points)):
        zero_points[i][0] += board["x"]
        zero_points[i][1] += board["y"]
    board_cell_areas["0"] = {
        "rect": {"x": zero_points[1][0], "y": zero_points[1][1], "width": zero_points[0][0] - zero_points[3][0], "height": zero_points[3][1] - zero_points[0][1]},
        "vertices": zero_points[1:4]
        }

    # Graella
    board_surface.blit(grid_surface, (grid_x, grid_y))

    # Espai de la banca
    house_rect = [grid_x + c_w + 5, 5, c_w*4 - 10, grid_y - 10]
    draw.rect(board_surface, LIGHT_GRAY, house_rect, 3)

    center_x = house_rect[0] + house_rect[2]/2
    center_y = house_rect[1] + house_rect[3]/2
    text_house = font_serif.render("HOUSE", True, WHITE, DARK_GREEN)
    text_house_rect = text_house.get_rect(center=(center_x,center_y))
    board_surface.blit(text_house, text_house_rect)

    center_x += board["x"]
    center_y += board["y"]
    house_space["center"] = {"x": center_x, "y": center_y}

    # Espais de columnes
    x = grid_x + c_w * rows
    for col in range(3):
        y = grid_y + c_h * col
        
        center = (x + c_w/2, y + c_h/2)
        text = font_small.render("2 : 1", True, WHITE, DARK_GREEN)
        text_rotated = rotate(text, 90)
        text_rotated_rect = text_rotated.get_rect(center=center)
        board_surface.blit(text_rotated, text_rotated_rect)

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
            "rect": {"x": points[0][0], "y": points[0][1], "width": points[3][0] - points[0][0], "height": points[3][1] - points[0][1]},
            "vertices": points[1:4]
        }

    #draw_bets()

def update_player_grid():
    # Abreujar noms
    cols, rows = player_grid["columns"], player_grid["rows"]
    c_w, c_h = player_grid["cell"]["width"], player_grid["cell"]["height"]
    c_1w, c_1h = player_grid["cell"]["1st_w"], player_grid["cell"]["1st_h"]

    #Quadre extern
    #draw.rect(player_grid_surface, LIGHT_GRAY, (0, 0, pg_size[0], pg_size[1]), 3)

    #Línies internes
    for col in range(1, cols):
        x = c_1w + c_w * (col-1)
        draw.line(player_grid_surface, LIGHT_GRAY, (x, 0), (x, pg_size[1]), 3)
    for row in range(1, rows):
        y = c_1h + c_h * (row-1)
        draw.line(player_grid_surface, LIGHT_GRAY, (0, y), (pg_size[0], y), 3)
    
    for row in range(rows):
        y = 0 if row == 0 else c_1h + c_h * (row-1)
        center_y = y + c_1h/2 if row == 0 else y + c_h/2 
        for col in range(cols):
            x = 0 if col == 0 else c_1w + c_w * (col-1)
            center_x = x + c_1w/2 if col == 0 else x + c_w/2
            
            # Primera fila: res
            if row == 0:
                continue

            # Primera columna: noms dels jugadors
            elif col == 0:
                name = player_names[row-1]
                match name:
                    case "taronja": color = ORANGE
                    case "blau": color = BLUE
                    case "lila": color = PURPLE
                text = font_small.render(name, True, color, DARK_GREEN)
                text_rect = text.get_rect(center=(center_x,center_y))
                player_grid_surface.blit(text, text_rect)
            
            # Quantitats de fitxes de cada jugador
            else:
                amount = players[player_names[row-1]][f"{chip_values[col-1]:03}"]
                text = font_small.render(f"× {str(amount)}", True, WHITE, DARK_GREEN)
                text_rect = text.get_rect(center=(center_x,center_y))
                player_grid_surface.blit(text, text_rect)

def draw_chip(chip_dict):
    value = int(chip_dict["value"])
    owner = chip_dict["owner"]
    pos = tuple(chip_dict['pos'].values())

    match owner:
        case "taronja": bg_color = ORANGE
        case "blau": bg_color = BLUE
        case "lila": bg_color = PURPLE
    color = (bg_color[0]/2, bg_color[1]/2, bg_color[2]/2)

    radius = 8 + int(math.log2(value)*2)

    draw.circle(screen, bg_color, pos, radius)

    text_font = font_tiny
    text = text_font.render(str(value), True, color)
    text_rect = text.get_rect(center=pos)
    screen.blit(text, text_rect)

    for i in range(8):    
        angle = 360/8 * (i + 0.25)
        p0 = utils.point_on_circle(pos, radius*2/3, angle)
        p1 = utils.point_on_circle(pos, radius-1, angle)

        angle -= 360/8/2
        p2 = utils.point_on_circle(pos, radius-1, angle)
        p3 = utils.point_on_circle(pos, radius*2/3, angle)

        polygon_color = LIGHT_GRAY if i % 2 == 0 else DARK_GRAY
        points = [p0,p1,p2,p3]
        draw.polygon(screen, polygon_color, points)  

    border_width = 2
    inner_border_width = 1
    if value >= 50:
        border_width += 1
        inner_border_width += 1
    draw.circle(screen, color, pos, radius, border_width)
    draw.circle(screen, color, pos, radius*2/3, inner_border_width)   

def init_game_info_surface():
    # Finestra
    window_tuple = (gi_window["x"], gi_window["y"], gi_window["width"], gi_window["height"])
    draw.rect(gi_surface, DARK_GRAY, window_tuple)
    draw.rect(gi_surface, WHITE, window_tuple, 3)

    # Columnes
    col_y = 80
    subcol_y = 95
    header_line_y = 100
    p0 = (game_info_chart["x"], header_line_y)
    p1 = (game_info_chart["x"] + game_info_chart["width"], header_line_y)
    draw.line(gi_surface, LIGHT_GRAY, p0, p1, 3)
    for i, key in enumerate(round_info.keys()):
        string = key.capitalize()
        col_text = font_medium.render(string, True, WHITE)
        match i:
            case 0: 
                col_x = game_info_chart["x"] + 40
                col_line_x = col_x + 40
            case 1: 
                col_x = game_info_chart["x"] + 200
                col_line_x = col_x + 120
            case 2: 
                col_x = game_info_chart["x"] + 440
        col_text_rect = col_text.get_rect(centerx = col_x, bottom = col_y)
        gi_surface.blit(col_text, col_text_rect)
        if i != 2:
            p0 = (col_line_x, 55)
            p1 = (col_line_x, game_info_chart["y"] + game_info_chart["height"])
            draw.line(gi_surface, LIGHT_GRAY, p0, p1, 3)
        if i != 0:
            for i, name in enumerate(player_names):
                match name:
                    case "taronja": color = ORANGE
                    case "blau": color = BLUE
                    case "lila": color = PURPLE
                subcol_text = font_small.render(name, True, color)
                subcol_x = col_x + 80 * (i-1)
                subcol_text_rect = subcol_text.get_rect(centerx = subcol_x, bottom = subcol_y)
                gi_surface.blit(subcol_text, subcol_text_rect)

def update_game_info_chart():
    gi_chart_surface = Surface((game_info_chart["width"], 48 * len(game_info)), SRCALPHA)
    gi_chart_surface.fill(DARK_GRAY)
    for i, round_info in enumerate(game_info):
        y = 24 + 48 * i
        text_result = font_big_thin.render(str(round_info["result"]), True, WHITE, DARK_GRAY)
        text_result_rect = text_result.get_rect(center = (40, y))
        gi_chart_surface.blit(text_result, text_result_rect)

        for i, bet_dict in enumerate(round_info["bets"]):
            x = 120 + 80 * i
            text_chips = font_small_thin.render(f"{bet_dict["units"]} units", True, WHITE, DARK_GRAY)
            text_chips_rect = text_chips.get_rect(center = (x, y - 10))
            gi_chart_surface.blit(text_chips, text_chips_rect)
            text_bet_on = font_small_thin.render(f"on {bet_dict["bet_on"]}", True, WHITE, DARK_GRAY)
            text_bet_on_rect = text_bet_on.get_rect(center = (x, y + 10))
            gi_chart_surface.blit(text_bet_on, text_bet_on_rect)
        
        for i, credit in enumerate(round_info["credits"]):
            text_credit = font_big_thin.render(str(credit), True, WHITE, DARK_GRAY)
            text_credit_rect = text_credit.get_rect(center = (360 + 80 * i, y))
            gi_chart_surface.blit(text_credit, text_credit_rect)
    draw.line(gi_chart_surface, LIGHT_GRAY, (80, 0), (80, gi_chart_surface.get_height()), 3)
    draw.line(gi_chart_surface, LIGHT_GRAY, (320, 0), (320, gi_chart_surface.get_height()), 3)

    if gi_scroll["visible"]:
        sub_surface = gi_chart_surface.subsurface((0, gi_scroll["surface_offset"], gi_chart_surface.get_width(), gi_scroll["visible_height"]))
        gi_surface.blit(sub_surface, (game_info_chart["x"], game_info_chart["y"]))
    else:
        gi_surface.blit(gi_chart_surface, (game_info_chart["x"], game_info_chart["y"]))

def draw_scroll():
    rect_tuple = (gi_scroll["x"], gi_scroll["y"], gi_scroll["width"], gi_scroll["height"])
    draw.rect(screen, GRAY, rect_tuple)

    circle_x = int(gi_scroll["x"] + gi_scroll["width"] / 2)
    circle_y = int(gi_scroll["y"] + (gi_scroll["percentage"] / 100) * gi_scroll["height"])
    circle_tuple = (circle_x, circle_y)
    draw.circle(screen, WHITE, circle_tuple, gi_scroll["radius"])
