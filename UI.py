from UI_Data import *
from GameData import *
from pygame import draw, font
from pygame.transform import rotate
import utils
import math

font.init()
font_tiny = font.SysFont("Arial", 10, bold=True)
font_small = font.SysFont("Arial", 12, bold=True)
font_medium = font.SysFont("Arial", 15, bold=True)
font_big = font.SysFont("Arial", 18, bold=True)
font_huge = font.SysFont("Arial", 27, bold=True)
font_serif = font.SysFont("Times New Roman", 21)

def update_current_number():
    for i, n in enumerate(number_order):
        angle = (360/37*i + roulette["angle_offset"]) % 360
        prev_angle = angle - 360/37
        if angle + prev_angle < 360/37:
            current_number["n"] = n
            break
    
    text = font_big.render(f"Current number: {str(current_number["n"])}", True, WHITE)
    text_center = (roulette["position"][0] + roulette["radius"], roulette["position"][1] + roulette["radius"]*2 + 20)
    text_rect = text.get_rect(center = text_center)
    current_number_text["text"], current_number_text["rect"] = text, text_rect

def draw_spin_button():
    sb_rect_tuple = (spin_button["x"],spin_button["y"],spin_button["width"],spin_button["height"])
    
    fill_color = BLACK
    border_color = LIGHT_GRAY
    text_color = WHITE
    if roulette["about_to_spin"]:
        fill_color = GOLD
        border_color = BLACK
        text_color = BLACK
    elif roulette["spin_canceled"] or roulette["spinning"] or roulette["readjusting"]:
        fill_color = DARK_GRAY
        border_color = GRAY
        text_color = GRAY
    
    draw.rect(screen, fill_color, sb_rect_tuple)
    draw.rect(screen, border_color, sb_rect_tuple, 2)
    
    sb_text = font_big.render("Spin!", True, text_color)
    center = (spin_button["x"] + 40, spin_button["y"] + 15)
    sb_text_rect = sb_text.get_rect(center=center)
    screen.blit(sb_text, sb_text_rect)

def update_roulette():
    r = roulette["radius"]
    c = (r,r)

    draw.circle(roulette_surface, DARK_GOLD, c, r, 6)
    draw.circle(roulette_surface, BROWN, c, r-56)
    
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
        text_n = font_medium.render(str(n), True, WHITE)
        text_n_rotated = rotate(text_n, text_angle)
        text_n_rotated_rect = text_n_rotated.get_rect()
        text_n_rotated_rect.center = polygon_center
        roulette_surface.blit(text_n_rotated, text_n_rotated_rect)

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
        text_n = font_big.render(str(n), True, WHITE)
        text_n_rotated =  rotate(text_n, 90)
        text_n_rotated_rect = text_n_rotated.get_rect(center=(center_x, center_y))
        grid_surface.blit(text_n_rotated, text_n_rotated_rect)

        board_cell_areas[str(n)] = {"rect": {"x": x, "y": y, "width": c_w, "height": c_h}}

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

        board_cell_areas[string] = {"rect": {"x": x, "y": y, "width": c_w * 3, "height": c_h}}

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
    grid_x = board["grid_x"]
    rows = board["rows"]
    c_w, c_h = board["cell"]["width"], board["cell"]["height"]
    
    # Espai de zero
    zero_points = [
    (grid_x, 1),
    (grid_x*2/3, 1),
    (0, c_h * 1.5),
    (grid_x*2/3, c_h * 3),
    (grid_x, c_h * 3)]
    draw.lines(board_surface, LIGHT_GRAY, False, zero_points, 3)

    text_zero = font_huge.render("0", True, WHITE, DARK_GREEN)
    text_zero_rotated = rotate(text_zero, 90)
    text_zero_rotated_rect = text_zero_rotated.get_rect(center = (grid_x*5/9, c_h * 1.5))
    board_surface.blit(text_zero_rotated, text_zero_rotated_rect)

    board_cell_areas["0"] = {
        "rect": {"x": grid_x*2/3, "y": 1, "width": grid_x/3, "height": c_h * 3 - 1},
        "tri1": zero_points[1:3], "tri2": zero_points[2:4]
        }

    # Graella
    board_surface.blit(grid_surface, (grid_x, 0))

    # Espais de columnes
    for col in range(3):
        x = grid_x + c_w * rows
        y = c_h * col
        
        center = (x + c_w/2, y + c_h/2)
        text = font_medium.render("2 : 1", True, WHITE, DARK_GREEN)
        text_rotated = rotate(text, 90)
        text_rotated_rect = text_rotated.get_rect(center=center)
        board_surface.blit(text_rotated, text_rotated_rect)

        center = (center[0] - 1, center[1] + 1)
        points = [(x, y+1),
        (x + c_w*0.9, y+1),
        (x + c_w*1.4, y + c_h/2),
        (x + c_w*0.9, y + c_h),
        (x, y + c_h)]
        
        if col != 0: points.pop(0)
        draw.lines(board_surface, LIGHT_GRAY, False, points, 3)

        board_cell_areas[f"col{col+1}"] = {
            "rect": {"x": x, "y": y, "width": c_w * 0.9, "height": c_h - 1},
            "tri1": points[1:3], "tri2": points[2:4]
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

            # Primera cel·la: la banca
            if row == 0 and col == 0:
                text = font_serif.render("HOUSE", True, WHITE, DARK_GREEN)
                text_rect = text.get_rect(center=(center_x,center_y))
                player_grid_surface.blit(text, text_rect)
            
            # Primera fila: fitxes
            elif row == 0:
                if players[current_player["name"]][f"{chip_values[col-1]:03}"] > 0:
                    draw_chip({"value": f"{chip_values[col-1]:03}", "owner": f"{current_player["name"]}", "pos": (center_x, center_y)}, bet=False)

            # Primera columna: noms dels jugadors
            elif col == 0:
                name = player_names[row-1]
                match name:
                    case "taronja": color = ORANGE
                    case "blau": color = BLUE
                    case "lila": color = PURPLE
                text = font_medium.render(name, True, color, DARK_GREEN)
                text_rect = text.get_rect(center=(center_x,center_y))
                player_grid_surface.blit(text, text_rect)
            
            # Quantitats de fitxes de cada jugador
            else:
                amount = players[player_names[row-1]][f"{chip_values[col-1]:03}"]
                text = font_medium.render(f"× {str(amount)}", True, WHITE, DARK_GREEN)
                text_rect = text.get_rect(center=(center_x,center_y))
                player_grid_surface.blit(text, text_rect)
            
            

    #for name, dict in players.items():

def draw_chip(chip_dict, bet=True):
    value = int(chip_dict["value"])
    owner = chip_dict["owner"]
    pos = chip_dict["pos"]
    
    surface = screen if bet else player_grid_surface

    match owner:
        case "taronja": bg_color = ORANGE
        case "blau": bg_color = BLUE
        case "lila": bg_color = PURPLE
        #case "banca": bg_color = WHITE
    color = (bg_color[0]/2, bg_color[1]/2, bg_color[2]/2)

    radius = 8 + int(math.log2(value)*2)

    draw.circle(surface, bg_color, pos, radius)

    text_font = font_small
    text = text_font.render(str(value), True, color)
    text_rect = text.get_rect(center=pos)
    surface.blit(text, text_rect)

    for i in range(8):    
        angle = 360/8 * (i + 0.25)
        p0 = utils.point_on_circle(pos, radius*2/3, angle)
        p1 = utils.point_on_circle(pos, radius-1, angle)

        angle -= 360/8/2
        p2 = utils.point_on_circle(pos, radius-1, angle)
        p3 = utils.point_on_circle(pos, radius*2/3, angle)

        polygon_color = LIGHT_GRAY if i % 2 == 0 else DARK_GRAY #if bg_color != WHITE and i % 2 == 0 else DARK_GRAY
        points = [p0,p1,p2,p3]
        draw.polygon(surface, polygon_color, points)  

    border_width = 2
    inner_border_width = 1
    if value >= 50:
        border_width += 1
        inner_border_width += 1
    draw.circle(surface, color, pos, radius, border_width)
    draw.circle(surface, color, pos, radius*2/3, inner_border_width)   
    
