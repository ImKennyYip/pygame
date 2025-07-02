import pygame
from sys import exit
import os

#game variables
TILE_SIZE = 32
GAME_WIDTH = 512
GAME_HEIGHT = 512

PLAYER_X = GAME_WIDTH/2
PLAYER_Y = GAME_HEIGHT/2
PLAYER_WIDTH = 42
PLAYER_HEIGHT = 48
PLAYER_JUMP_WIDTH = 52
PLAYER_JUMP_HEIGHT = 60
PLAYER_SHOOT_WIDTH = 62 #same height as PLAYER_HEIGHT
PLAYER_JUMP_SHOOT_WIDTH = 58 #same height as PLAYER_JUMP_HEIGHT
PLAYER_DISTANCE = 5

GRAVITY = 0.5
FRICTION = 0.4
PLAYER_VELOCITY_X = 5
PLAYER_VELOCITY_Y = -11

PLAYER_BULLET_WIDTH = 16
PLAYER_BULLET_HEIGHT = 12
PLAYER_BULLET_VELOCITY_X = 8

HEALTH_WIDTH = 16
HEALTH_HEIGHT = 4

#enemy variables
METALL_WIDTH = 36
METALL_HEIGHT = 30

#images
def load_image(image_name, scale=None):
    image = pygame.image.load(os.path.join("images", image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

background_image = load_image("background.png")
player_image_right = load_image("megaman-right.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_left = load_image("megaman-left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_jump_right = load_image("megaman-right-jump.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT))
player_image_jump_left = load_image("megaman-left-jump.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT))
player_image_shoot_right = load_image("megaman-right-shoot.png", (PLAYER_SHOOT_WIDTH, PLAYER_HEIGHT))
player_image_shoot_left = load_image("megaman-left-shoot.png", (PLAYER_SHOOT_WIDTH, PLAYER_HEIGHT))
player_image_jump_shoot_right = load_image("megaman-right-jump-shoot.png",
                                           (PLAYER_JUMP_SHOOT_WIDTH, PLAYER_JUMP_HEIGHT))
player_image_jump_shoot_left = load_image("megaman-left-jump-shoot.png",
                                           (PLAYER_JUMP_SHOOT_WIDTH, PLAYER_JUMP_HEIGHT))
player_image_bullet = load_image("bullet.png", (PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT))
floor_tile_image = load_image("floor-tile.png", (TILE_SIZE, TILE_SIZE))
metall_image_right = load_image("metall-right.png", (METALL_WIDTH, METALL_HEIGHT))
metall_image_left = load_image("metall-left.png", (METALL_WIDTH, METALL_HEIGHT))
health_image = load_image("health.png", (HEALTH_WIDTH, HEALTH_HEIGHT))

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Kenny Yip Coding - PyGame")
pygame.display.set_icon(player_image_right)
clock = pygame.time.Clock()

#Custom event
INVINCIBLE_END = pygame.USEREVENT + 0
SHOOTING_END = pygame.USEREVENT + 1

class Player(pygame.Rect):
    class Bullet(pygame.Rect):
        def __init__(self):
            if player.direction == "left":
                pygame.Rect.__init__(self, player.x, player.y + TILE_SIZE/2,
                                     PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
                self.velocity_x = -PLAYER_BULLET_VELOCITY_X
            elif player.direction == "right":
                pygame.Rect.__init__(self, player.x + player.width, player.y + TILE_SIZE/2,
                                     PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
                self.velocity_x = PLAYER_BULLET_VELOCITY_X
            self.image = player_image_bullet
            self.used = False

    def __init__(self):
        pygame.Rect.__init__(self, PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "right"
        self.jumping = False
        self.invincible = False
        self.max_health = 28
        self.health = self.max_health
        self.shooting = False
        self.bullets = []
    
    def update_image(self):
        if self.jumping and self.shooting:
            if self.direction == "right":
                self.image = player_image_jump_shoot_right
            elif self.direction == "left":
                self.image = player_image_jump_shoot_left
        elif self.shooting:
            if self.direction == "right":
                self.image = player_image_shoot_right
            elif self.direction == "left":
                self.image = player_image_shoot_left
        elif self.jumping:
            if self.direction == "right":
                self.image = player_image_jump_right
            elif self.direction == "left":
                self.image = player_image_jump_left
        else:
            if self.direction == "right":
                self.image = player_image_right
            elif self.direction == "left":
                self.image = player_image_left
    
    def set_invincible(self, milliseconds=1000):
        self.invincible = True
        pygame.time.set_timer(INVINCIBLE_END, milliseconds, 1) #event called, milliseconds, repetitions
    
    def set_shooting(self):
        if not self.shooting:
            self.shooting = True
            self.bullets.append(Player.Bullet())
            pygame.time.set_timer(SHOOTING_END, 250, 1)

class Metall(pygame.Rect):
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, METALL_WIDTH, METALL_HEIGHT)
        self.image = metall_image_left
        self.velocity_y = 0
        self.direction = "left"
        self.jumping = False
        self.health = 1
    
    def update_image(self):
        if self.direction == "right":
            self.image = metall_image_right
        elif self.direction == "left":
            self.image = metall_image_left

class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image

def create_map():
    for i in range(4):
        tile = Tile(player.x + i*TILE_SIZE, player.y + TILE_SIZE*2, floor_tile_image)
        tiles.append(tile)
    
    for i in range(16):
        tile = Tile(i*TILE_SIZE, player.y + TILE_SIZE*5, floor_tile_image)
        tiles.append(tile)

    for i in range(3):
        tile = Tile(TILE_SIZE*3, (i+10)*TILE_SIZE, floor_tile_image)
        tiles.append(tile)
    
    for i in range(3):
        metall = Metall(player.x + TILE_SIZE*(3+i*1.5), TILE_SIZE*6)
        metalls.append(metall)

def check_tile_collision(character):
    for tile in tiles:
        if character.colliderect(tile):
            return tile
    return None

def check_tile_collision_x(character):
    tile = check_tile_collision(character)
    if tile is not None:
        if character.velocity_x < 0: #going left
            character.x = tile.x + tile.width #right side of tile
        elif character.velocity_x > 0: #going right
            character.x = tile.x - character.width #left side of tile
        character.velocity_x = 0

def check_tile_collision_y(character):
    tile = check_tile_collision(character)
    if tile is not None:
        if character.velocity_y < 0: #going up
                character.y = tile.y + tile.height #bottom of tile
        elif character.velocity_y > 0: #going down
            character.y = tile.y - character.height #top of tile
            character.jumping = False
        character.velocity_y = 0

def move():
    global metalls
    #x movement
    if player.direction == "left" and player.velocity_x < 0:
        player.velocity_x += FRICTION
    elif player.direction == "right" and player.velocity_x > 0:
        player.velocity_x -= FRICTION
    else:
        player.velocity_x = 0

    player.x += player.velocity_x
    if player.x < 0:
        player.x = 0
    elif player.x + player.width > GAME_WIDTH:
        player.x = GAME_WIDTH - player.width

    check_tile_collision_x(player)

    #y movement
    player.velocity_y += GRAVITY
    player.y += player.velocity_y
    check_tile_collision_y(player)

    #bullets
    for bullet in player.bullets:
        bullet.x += bullet.velocity_x
        for metall in metalls:
            if metall.health > 0 and not bullet.used and bullet.colliderect(metall):
                metall.health -= 1
                bullet.used = True
    
    player.bullets = [bullet for bullet in player.bullets if not bullet.used \
                      and bullet.x + bullet.width > 0 and bullet.x < GAME_WIDTH]
    metalls = [metall for metall in metalls if metall.health > 0]

    #enemy y movement
    for metall in metalls:
        if player.x < metall.x:
            metall.direction = "left"
        else:
            metall.direction = "right"
        
        metall.velocity_y += GRAVITY
        metall.y += metall.velocity_y
        check_tile_collision_y(metall)

        if not player.invincible and player.colliderect(metall):
            player.health -= 1
            player.set_invincible()


def draw():
    window.fill((20, 18, 167))
    window.blit(background_image, (0, 80))

    for tile in tiles:
        window.blit(tile.image, tile)

    player.update_image()
    window.blit(player.image, player)

    for bullet in player.bullets:
        window.blit(bullet.image, bullet)

    for metall in metalls:
        metall.update_image()
        window.blit(metall.image, metall)

    pygame.draw.rect(window, "black", (TILE_SIZE, TILE_SIZE, HEALTH_WIDTH, HEALTH_HEIGHT * player.max_health))
    for i in range(player.max_health - player.health, player.max_health):
        window.blit(health_image, (TILE_SIZE, TILE_SIZE + i*HEALTH_HEIGHT, HEALTH_WIDTH, HEALTH_HEIGHT))

#start game
player = Player()
metalls = []
tiles = []
create_map()

while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == INVINCIBLE_END:
            player.invincible = False
        elif event.type == SHOOTING_END:
            player.shooting = False

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping:
        player.velocity_y = PLAYER_VELOCITY_Y
        player.jumping = True

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.velocity_x = -PLAYER_VELOCITY_X
        player.direction = "left"

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.velocity_x = PLAYER_VELOCITY_X
        player.direction = "right"
    
    if keys[pygame.K_x] or keys[pygame.K_SPACE]:
        player.set_shooting()

    move()
    draw()
    pygame.display.update()
    clock.tick(60) #60 frames per second (fps)
