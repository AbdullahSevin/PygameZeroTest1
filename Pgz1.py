import random

WIDTH, HEIGHT = 640, 640

class Player:
    def __init__(self, x, y, size, color, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed

    def draw(self):
        screen.draw.filled_rect(Rect((self.x, self.y), (self.size, self.size)), self.color)

    def move(self, dx, dy):
        # diagonal move speed fix
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1 / sqrt(2)
            dy *= 0.7071

        
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))


class Obstacle1:
    def __init__(self, x, y, size, color, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        #add:
        #self.damage
        #self.hp?

    def draw(self):
        screen.draw.filled_rect(Rect((self.x, self.y), (self.size, self.size)), self.color)
        
        
obstacle_spawn_point_x_randomizer = random.range(0,WIDTH)
obstacle_spawn_point_y_randomizer = random.range(0,HEIGHT)

obstacle_spawn_point_1 = WIDTH, HEIGHT
player = Player(WIDTH // 2, HEIGHT // 2, size=50, color=(0, 255, 0), speed=5)  

obstacle1 = Obstacle1(obstacle_spawn_point_x_randomizer, obstacle_spawn_point_y_randomizer, size=40, color=(255, 0, 0), speed=5)

BACKGROUND_COLOR = (0, 255, 0) #green?


def draw():
    screen.fill(BACKGROUND_COLOR)
    player.draw()


def update():
    # put this in a def
    dx, dy = 0, 0
    if keyboard.left:
        dx -= 1
    if keyboard.right:
        dx += 1
    if keyboard.up:
        dy -= 1
    if keyboard.down:
        dy += 1

    player.move(dx, dy)
    obstacle1.move(-1)
