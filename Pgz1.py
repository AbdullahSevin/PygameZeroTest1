import pgzrun

#CONSTANTS
WIDTH = 800
HEIGHT = 600

player_png = Actor("goku")
enemy_png = Actor("goku")



#DICTIONARIES
game_states = {
    "menu": "menu",
    "level1": "level1",
    "settings": "settings"
}



#LISTS
menu_options = [
    {"label": "Play", "action": "switch_to_level1"},
    {"label": "Settings", "action": "switch_to_settings"},
    {"label": "Quit", "action": "quit_game"}
]



# CHANGABLE GLOBALS
selected_option = 0
current_screen = game_states["menu"]
sounds_on = True

turn = 0
level = 1


gold = 0
base_stat_increase_cost = 10
cur_stat_increase_cost = 10
cost_multiplier = 1.1

player_str = 1 #strength

cur_player_hp = 100
max_player_hp = 100

cur_enemy_hp = 10
max_enemy_hp = 10

def draw():
    draw_function_name = f"draw_{current_screen}"
    draw_function = globals().get(draw_function_name, None)
    if callable(draw_function):
        draw_function()


def draw_subtitle(comment):
    screen.draw.text(comment, center =  (WIDTH // 2, HEIGHT * 0.9), fontsize = 16, color = "gold")

def draw_menu():
    screen.clear()
    screen.draw.text("Main Menu", center=(WIDTH // 2, 100), fontsize=60, color="white")
    draw_subtitle("testing the menu")
    for i, option in enumerate(menu_options):
        color = "yellow" if i == selected_option else "white"
        screen.draw.text(option["label"], center=(WIDTH // 2, HEIGHT/2.5 + i * 50), fontsize=40, color=color)


def draw_level1():
    Initiate_Level()
"""
# level manager:
# things inside a level:
# player png, enemy png
# cur/max health of player and enemy
# cur level value
# place to buy stats, and cost of stats
# cur gold value
    screen.clear()
    screen.draw.text("Level 1", center=(WIDTH // 2, 25), fontsize=50, color="white")
    player_png.pos = (WIDTH // 5, HEIGHT // 2)
    player_png.draw()
"""

def draw_settings():
    screen.clear()
    screen.draw.text("Settings", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")


def update():
    pass


def on_key_down(key):
    key_function_name = f"handle_key_{current_screen}"
    key_function = globals().get(key_function_name, None)
    if callable(key_function):
        key_function(key)


def handle_key_menu(key):
    global selected_option

    if key == keys.UP:
        navigate_menu(-1)
    elif key == keys.DOWN:
        navigate_menu(1)
    elif key == keys.RETURN:
        execute_menu_action()


def navigate_menu(direction):
    global selected_option
    selected_option = (selected_option + direction) % len(menu_options)


def execute_menu_action():
    action_function_name = menu_options[selected_option]["action"]
    action_function = globals().get(action_function_name, None)
    if callable(action_function):
        action_function()


def switch_to_level1():
    global current_screen
    current_screen = game_states["level1"]


def switch_to_settings():
    global current_screen
    current_screen = game_states["settings"]


def quit_game():
    quit()


def Initiate_Level():
    screen.clear()
    #screen.draw.text("Level 1", center=(WIDTH // 2, 25), fontsize=50, color="white")
    draw_character(player_png,(WIDTH * 0.2, HEIGHT // 2), f"{cur_player_hp}/{max_player_hp}")
    draw_character(enemy_png,(WIDTH * 0.8, HEIGHT // 2), f"{cur_enemy_hp}/{max_enemy_hp}")
    draw_level_texts(turn,gold,level,player_str,cur_stat_increase_cost)

def draw_character(character, location, subtitle):
    character.pos = location
    character.draw()
    character_subtitle = subtitle
    screen.draw.text(character_subtitle, center = location,  fontsize = 24, color = "red")
    
    
def draw_level_texts(turn,gold,level,player_str,cur_stat_increase_cost):
    screen.draw.text(str(turn), center = (WIDTH // 20, HEIGHT // 20), fontsize = 24, color = "white")
    screen.draw.text(str(gold), center = (WIDTH *0.95, HEIGHT // 20), fontsize = 24, color = "gold")
    screen.draw.text(str(level), center = (WIDTH // 2, HEIGHT // 20), fontsize = 36, color = "white")
    screen.draw.text(str(player_str), center = (WIDTH * 0.8, HEIGHT // 20), fontsize = 24, color = "white")
    screen.draw.text(str(cur_stat_increase_cost), center = (WIDTH *0.85, HEIGHT // 20), fontsize = 24, color = "white")
    pass
    

def request_to_save_data():
    save_data(turn, level, gold, player_str)

def save_data(turn, level, gold, player_str):
    #data_to_save = f"{turn}\t{level}\t{gold}\t{player_strength}"
    with open("savedata.txt", "w") as file:
        line = "\t".join(turn, level, gold, player_str)
        file.write(line)
        file.save
        
def load_data():
    global turn
    global level
    global gold
    global player_str
    try:
    
        with open("savedata.txt", "r") as file:
            turn, level, gold, player_str = line.strip().split('\t')
            
    except:
        print("something went wrong")
    




pgzrun.go()