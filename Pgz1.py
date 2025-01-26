import pgzrun

#CONSTANTS
WIDTH = 800
HEIGHT = 600




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

# PLAYER VALUES
# gold = 0


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
    draw_comment("testing the menu")
    for i, option in enumerate(menu_options):
        color = "yellow" if i == selected_option else "white"
        screen.draw.text(option["label"], center=(WIDTH // 2, 200 + i * 50), fontsize=40, color=color)


def draw_level():
    screen.clear()
    screen.draw.text("Level 1", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")


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


pgzrun.go()