import pgzrun
import math

#CONSTANTS
WIDTH = 800
HEIGHT = 600
#images
player_png = Actor("player")
enemy1_png = Actor("bandit")
upgrade_png = Actor("upgrade")
level1bg_png = "level1bg"
#sounds

#...




upgrade_button_position = WIDTH * 0.56, HEIGHT * 0.94

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
cost_multiplier = 1.25

player_str = 5 #strength
player_str_level = 1
enemy_str = 5
enemy_str_level = 1

cur_player_hp = 100
max_player_hp = 100

cur_enemy_hp = 10
max_enemy_hp = 10

player = None
enemy_1 = None

player_speed = 5
enemy_speed = 3

level_is_initiated = False

player_position_x, player_position_y = WIDTH * 0.2, HEIGHT * 0.8

enemy1_position_x, enemy1_position_y = WIDTH * 0.8, HEIGHT * 0.8

player_animations = {
"idle" : ["player_idle1","player_idle2","player_idle3"],
"walk" : ["player_walk1","player_walk2", "player_walk3"],
"attack" : ["player_attack1","player_attack2","player_attack3"]
}

enemy_animations = {
"attack" : ["bandit_attack1","bandit_attack2","bandit_attack3"]
}


player_is_moving = False
player_is_in_action  = False
player_is_attacking = False
player_is_getting_damaged = False

enemy_is_moving = False
enemy_is_attacking = False
enemy_is_getting_damaged = False

current_frame = 0
animation_speed = 20
animation_timer = 0

enemy_current_frame = 0
enemy_animation_speed = 20
enemy_animation_timer = 0

damage_text = None
damage_text_frame = 0

background_is_playing = False

current_background_music = "the_wellerman"

music_started = False

def start_bg_music(name):
    global music_started
    if music_started == True:
        return
    print("runned once only")
    stop_bg_music()
    play_bg_music(name)
    music_started = True
    
    
def stop_bg_music():
    global background_is_playing
    if background_is_playing == False:
        return
    elif background_is_playing:
        music.stop()
        background_is_playing = False


def play_bg_music(name = current_background_music):
    global current_background_music, background_is_playing
    if background_is_playing == True:
        return
    elif background_is_playing == False:
        music.set_volume(0.3)
        music.play(name)
        print(f"playing {name}")
        current_background_music = name
        background_is_playing = True

play_bg_music()

class Animator():
    def animate_player_movement():
        global player_png
        global current_frame
        global animation_timer
        
        if player_is_in_action == False:
            if player_is_moving == False:
                animation_state = "idle"
            else:
                animation_state = "walk"
                
            animation_frames = player_animations[animation_state]
            
            
            if current_frame < len(animation_frames)-1:
                animation_timer +=1
                if animation_timer >= animation_speed:
                    current_frame += 1
                    animation_timer  = 0
            else:
                animation_timer += 1
                if animation_timer >= animation_speed:
                    current_frame = 0
                    animation_timer = 0
            
            player_png.image = animation_frames[current_frame]
        
    def animate_player_attack():
        global player_is_in_action
        global current_frame
        global animation_timer
        global player_is_attacking
        
        if player_is_attacking == False:
            return
        
        
        player_is_in_action = True
        
        animation_state = "attack"
        
        animation_frames = player_animations[animation_state]
            
        if current_frame < len(animation_frames)-1:
            animation_timer +=1
            #print(animation_timer)
            if animation_timer >= (animation_speed * (2-(current_frame*1.35))):
                current_frame += 1
                animation_timer  = 0
        else:
            animation_timer +=1
            if animation_timer >= animation_speed / 3:
                player_is_attacking = False
                player_is_in_action = False
                Animator.reset_animator_variables()
                enemy1.take_damage(player_str)
        
        player_png.image = animation_frames[current_frame]
        

        
    def animate_player_death():
        pass
        
    def animate_enemy_damaged():
        global enemy_is_getting_damaged
        enemy_is_getting_damaged = True
        enemy1_png.image = "bandit_damaged"
        Animator.animate_floating_damage_text()
        clock.schedule_unique(Animator.animate_enemy_idle_and_attack, 0.25)
        pass
        
    def animate_enemy_idle_and_attack():
        global enemy_is_getting_damaged
        enemy_is_getting_damaged = False
        
        enemy1_png.image = "bandit"
        
        clock.schedule_unique(Animator.set_enemy_attack_true, 0.15)
        
    def set_enemy_attack_true():
        global enemy_is_attacking
        enemy_is_attacking =  True
        if turn == 1:
            SoundManager.play_clip("magic_fireball", 0.30)
            SoundManager.play_clip("bat_attack1", 0.05)
        
    def animate_enemy_idle():
        global enemy_is_getting_damaged
        enemy_is_getting_damaged = False
        enemy1_png.image = "bandit"
        pass
        
    def animate_enemy_attack():
        global enemy_is_attacking
        global enemy_current_frame
        global enemy_animation_timer
        global turn
        
        if enemy_is_attacking == False:
            return
        
        #print ("enemy_attack_entered")
        animation_state = "attack"
        
        animation_frames = enemy_animations[animation_state]
            
        if enemy_current_frame < len(animation_frames)-1:
            enemy_animation_timer +=1
            #print(f"eemy atack if state entered anm timer : {enemy_animation_timer}")
            #print(f"current_frame: {current_frame}")
            if enemy_animation_timer >= enemy_animation_speed:
                enemy_current_frame += 1
                #print(f"cur frame =  {enemy_current_frame}")
                animation_timer  = 0
        else:
            #print("enemy  atafk els eeneterred")
            enemy_animation_timer +=1
            if enemy_animation_timer >= enemy_animation_speed *  2:
                enemy_is_attacking = False
                Animator.reset_enemy_animator_variables()
                player.take_damage(enemy_str)
                turn = 0
                clock.schedule_unique(Animator.animate_enemy_idle, 0.2)
        
        enemy1_png.image = animation_frames[enemy_current_frame]
        
        
        pass
        
    def animate_enemy_death():
        pass
    
    def animate_next_level():
        pass
        
    def animate_restart_from_level1():
        pass
        
    def draw_floating_damage_text():
        global damage_text, damage_text_frame
        damage_text_frame +=1
        damage_text = str(-player_str)
        damage_text_pos_x, damage_text_pos_y  = enemy1_position_x, enemy1_position_y-75
        damage_text_pos_y -= damage_text_frame
        screen.draw.text(damage_text, center =  (damage_text_pos_x, damage_text_pos_y), fontsize = 32, color = "red")
        clock.schedule_unique(Animator.reset_damage_frame, 0.25)
            
            
    def reset_damage_frame():
        global damage_text_frame
        damage_text_frame = 0
        
    def animate_floating_damage_text():
        global damage_text
        
        
    def reset_animator_variables():
        global current_frame, animation_speed, animation_timer
        
        current_frame = 0
        animation_speed = 20
        animation_timer = 0
        
    def reset_enemy_animator_variables():
        global enemy_current_frame, enemy_animation_speed, enemy_animation_timer
        
        enemy_current_frame = 0
        enemy_animation_speed = 20
        enemy_animation_timer = 0
        
        
            
        
class SoundManager():
    
    def play_clip(clip, volume = 1):
        # take a string as parameter
        # or make a dictionary its better
        # play sound if sounds_on
        if sounds_on:
            sound = getattr(sounds, clip, None)
            if sound:
                sound.set_volume(volume)
                sound.play()
       

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
    current_sound_text = "On" if sounds_on else "Off"
    screen.draw.text(f"Sounds are turned: {current_sound_text}", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")


def update():
    global turn
    Handle_Player_Movement()
    Animator.animate_player_movement()
    Animator.animate_player_attack()
    if turn == 1 and enemy_is_attacking and not enemy_is_getting_damaged:
        Animator.animate_enemy_attack()

def Handle_Player_Movement():
    global player_png, player_speed, player_position_x,player_position_y, player_is_moving
    if keyboard.right:
        if player_position_x <= ((WIDTH // 2)-48) :
            player_position_x += player_speed
            player_is_moving = True
    if keyboard.left:
        if player_position_x > 48:
            player_position_x -= player_speed
            player_is_moving = True
    if keyboard.up:
        if player_position_y > 64:
            player_position_y -= player_speed
            player_is_moving = True
    if keyboard.down:
        if player_position_y < HEIGHT -48:
            player_position_y += player_speed
            player_is_moving = True
            
    if not (keyboard.right or keyboard.left or keyboard.up or keyboard.down):
        player_is_moving = False

    

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
    global player
    global enemy1
    global level_is_initiated
    
    #screen.draw.text("Level 1", center=(WIDTH // 2, 25), fontsize=50, color="white")
    start_bg_music("goku_black")
    screen.clear()
    screen.blit(level1bg_png, (-250, 0))
    draw_character(player_png,(player_position_x, player_position_y), f"{cur_player_hp}/{max_player_hp}")
    draw_character(enemy1_png,(enemy1_position_x, enemy1_position_y), f"{cur_enemy_hp}/{max_enemy_hp}")
        
    draw_level_texts(turn,gold,level,player_str,cur_stat_increase_cost)
    
    draw_other_texts()
    
    
    player = Player(cur_player_hp,player_str)
    enemy1 = Enemy(cur_enemy_hp,enemy_str)

def draw_character(character, location, subtitle):
    character.pos = location
    character.draw()
    character_subtitle = subtitle
    locationx, locationy = location
    screen.draw.text(character_subtitle, center = (locationx,locationy-50), fontsize = 36, color = "red")
    
    
def draw_level_texts(turn,gold,level,player_str,cur_stat_increase_cost):
    turn_text = f"Turn: {str(turn)}"
    gold_text = f"Gold: {str(gold)}"
    level_text = f"Level: {str(level)}"
    player_str_text = f"STR: {str(player_str)}"
    cur_stat_increase_cost_text = f"Cost: {str(cur_stat_increase_cost)}"
    screen.draw.text(turn_text, center = (WIDTH // 20, HEIGHT // 20), fontsize = 24, color = "white")
    screen.draw.text(gold_text, center = (WIDTH *0.95, HEIGHT // 20), fontsize = 32, color = "gold")
    screen.draw.text(level_text, center = (WIDTH // 2, HEIGHT // 20), fontsize = 36, color = "white")
    screen.draw.text(player_str_text, center = (WIDTH * 0.5, HEIGHT * 0.93), fontsize = 24, color = "white")
    screen.draw.text(cur_stat_increase_cost_text, center = (WIDTH *0.5, HEIGHT * 0.96), fontsize = 24, color = "white")
    upgrade_png.pos = upgrade_button_position
    upgrade_png.draw()
    pass
    
    
def draw_other_texts():
    if enemy_is_getting_damaged:
        Animator.draw_floating_damage_text()
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
        
        
class Player:
    def __init__(self, hp, damage):
        self.hp = hp
        self.damage = damage

    def take_damage(self,damage):
        global cur_player_hp
        cur_player_hp -= damage
        if cur_player_hp  <= 0:
            self.player_death()

    def player_death(self):
        restart_game()

def restart_game():
    global gold, player_str, level, turn, cur_player_hp, max_player_hp, cur_enemy_hp, max_enemy_hp
    gold = 0
    player_str = math.ceil(player_str / 3)
    level = 1
    turn = 0
    cur_player_hp = 100
    max_player_hp = 100
    cur_enemy_hp = 10
    max_enemy_hp = 10

class Enemy:
    def __init__(self, hp, damage):
        self.hp = hp
        self.damage = damage

    def take_damage(self, damage):
        global cur_enemy_hp
        global turn
        global gold
        global enemy_is_attacking
        Animator.animate_enemy_damaged()
        SoundManager.play_clip("damaged4")
        cur_enemy_hp -= damage
        gold += damage
        if cur_enemy_hp <= 0:
            self.enemy_death()
        else:
            turn = 1
    def enemy_death(self):
        next_level()

def next_level():
    print("next level")
    global cur_enemy_hp, max_enemy_hp, level
    level += 1
    max_enemy_hp = math.ceil(max_enemy_hp * 1.2)
    cur_enemy_hp = max_enemy_hp
    
    
def change_gold(amount):
    global gold
    gold += amount
    
def change_player_str(amount):
    global player_str
    player_str += amount
    
def start_player_attack(pos):
    global player_is_attacking
    if enemy1_png.collidepoint(pos):
            if player_is_attacking == False:
                Animator.reset_animator_variables()
                player_is_attacking = True
                SoundManager.play_clip("yaa")
            
    else:
        pass

def change_upgrade_cost():
    global cur_stat_increase_cost
    cur_stat_increase_cost = math.ceil(cur_stat_increase_cost * cost_multiplier)

def on_mouse_down(pos):
    global sounds_on
    if current_screen == game_states["settings"]:
        sounds_on = False if sounds_on else True
    if turn == 0:
        start_player_attack(pos)
        
        if upgrade_png.collidepoint(pos):
            if gold >= cur_stat_increase_cost:
                change_gold(-cur_stat_increase_cost)
                change_player_str(3)
                change_upgrade_cost()
            pass
        
    
pgzrun.go()