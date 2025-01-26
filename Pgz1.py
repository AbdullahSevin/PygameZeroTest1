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
            dx *= 0.7071
            dy *= 0.7071

        
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))


obstacle_spawn_point_x_randomizer = random.randint(0,WIDTH)

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
        
    def move(self):
        self.y += self.speed
        # Respawn it when it goes below screen
        if self.y > HEIGHT:
            self.respawn()

    def respawn(self):
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = random.uniform(1, 5)

obstacle1 = Obstacle1(
    x=random.randint(0, WIDTH - 50),
    y=-50,
    size=50,
    color=(255, 0, 0),
    speed=random.uniform(3, 5),
)
obstacle2 = Obstacle1(
    x=random.randint(0, WIDTH - 50),
    y=-50,
    size=50,
    color=(255, 0, 0),
    speed=random.uniform(3, 5),
)
obstacle3 = Obstacle1(
    x=random.randint(0, WIDTH - 50),
    y=-50,
    size=50,
    color=(255, 0, 0),
    speed=random.uniform(3, 5),
)

        
player = Player(WIDTH // 2, HEIGHT // 2, size=50, color=(0, 255, 0), speed=5) 

BACKGROUND_COLOR = (0, 0, 255) #BLUE


def draw():
    screen.fill(BACKGROUND_COLOR)
    player.draw()
    obstacle1.draw()
    obstacle2.draw()
    obstacle3.draw()


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
    obstacle1.move()
    obstacle2.move()
    obstacle3.move()

# add collisions
# add shooting
# add levels