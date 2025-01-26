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

def Initiate_Level(player_png,enemy_png):
    screen.clear()
    screen.draw.text("Level 1", center=(WIDTH // 2, 25), fontsize=50, color="white")
    draw_character(player_png,(WIDTH * 0.2, HEIGHT // 2), f"{cur_player_hp}/{max_player_hp}")
    draw_character(enemy_png,(WIDTH * 0.8, HEIGHT // 2), f"{cur_enemy_hp}/{max_enemy_hp}")
    draw_level_texts(turn,gold,level,player_str,cur_stat_increase_cost)

def draw_character(character, location, subtitle):
    character.pos = location
    character.draw()
    character_subtitle = subtitle
    character_subtitle.pos = character.pos - character.height
    screen.draw.text(character_subtitle, center = character_subtitle.pos, fontsize = 24, color = "red")
    
    
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
        print("somecharacter went wrong")
    