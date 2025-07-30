import pygame
from sys import exit
import os
import random
import tile_map

#game variables
TILE_SIZE = 32
ROW_COUNT = 16
COLUMN_COUNT = ROW_COUNT
GAME_WIDTH = TILE_SIZE * COLUMN_COUNT
GAME_HEIGHT = TILE_SIZE * ROW_COUNT
GAME_MAP = tile_map.OPTIMIZED_GAME_MAP1

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

METALL_BULLET_WIDTH = 12
METALL_BULLET_HEIGHT = METALL_BULLET_WIDTH
METALL_BULLET_VELOCITY_X = 2
METALL_BULLET_VELOCITY_Y = METALL_BULLET_VELOCITY_X

BLADER_WIDTH = 32
BLADER_HEIGHT = 40
BLADER_VELOCITY_X = 4
BLADER_VELOCITY_Y = 2

#item variables
LIFE_ENERGY_WIDTH = 20
LIFE_ENERGY_HEIGHT = 24
BIG_LIFE_ENERGY_WIDTH = 28
BIG_LIFE_ENERGY_HEIGHT = 32
ITEM_VELOCITY_Y = -11 #item flies up first and gravity pulls it down

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
wall_tile_image = load_image("wall-tile.png", (TILE_SIZE, TILE_SIZE))
beam_tile_image = load_image("beam-tile.png", (TILE_SIZE, TILE_SIZE))
rock_tile1_image = load_image("rock-tile1.png", (TILE_SIZE, TILE_SIZE))
rock_tile2_image = load_image("rock-tile2.png", (TILE_SIZE, TILE_SIZE))
rock_tile3_image = load_image("rock-tile3.png", (TILE_SIZE, TILE_SIZE))
rock_tile4_image = load_image("rock-tile4.png", (TILE_SIZE, TILE_SIZE))
door_tile_image = load_image("door-tile.png", (TILE_SIZE, TILE_SIZE))
room_tile_image = load_image("room-tile.png", (TILE_SIZE, TILE_SIZE))

metall_image_right = load_image("metall-right.png", (METALL_WIDTH, METALL_HEIGHT))
metall_image_left = load_image("metall-left.png", (METALL_WIDTH, METALL_HEIGHT))
metall_image_guard_right = load_image("metall-right-guard.png", (METALL_WIDTH, METALL_HEIGHT))
metall_image_guard_left = load_image("metall-left-guard.png", (METALL_WIDTH, METALL_HEIGHT))
metall_image_bullet = load_image("metall-bullet.png", (METALL_BULLET_WIDTH, METALL_BULLET_HEIGHT))
health_image = load_image("health.png", (HEALTH_WIDTH, HEALTH_HEIGHT))
life_energy_image = load_image("life-energy.png", (LIFE_ENERGY_WIDTH, LIFE_ENERGY_HEIGHT))
big_life_energy_image = load_image("big-life-energy.png", (BIG_LIFE_ENERGY_WIDTH, BIG_LIFE_ENERGY_HEIGHT))
score_ball_image = load_image("score-ball.png", (TILE_SIZE/2, TILE_SIZE/2))
spike_image = load_image("spike.png", (TILE_SIZE, TILE_SIZE))
blader_image_right = load_image("blader-right.png", (BLADER_WIDTH, BLADER_HEIGHT))
blader_image_left = load_image("blader-left.png", (BLADER_WIDTH, BLADER_HEIGHT))

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Kenny Yip Coding - PyGame")
pygame.display.set_icon(player_image_right)
clock = pygame.time.Clock()
pygame.font.init()
# game_font = pygame.font.SysFont("Arial", 24)
game_font = pygame.font.Font("./megaman-game-font.otf", 24)

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
        self.score = 0
    
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
    class Bullet(pygame.Rect):
        def __init__(self, metall, velocity_y):
            if metall.direction == "left":
                pygame.Rect.__init__(self, metall.x, metall.y + TILE_SIZE/2,
                                     METALL_BULLET_WIDTH, METALL_BULLET_HEIGHT)
                self.velocity_x = -METALL_BULLET_VELOCITY_X
            elif metall.direction == "right":
                pygame.Rect.__init__(self, metall.x + metall.width, metall.y + TILE_SIZE/2,
                                     METALL_BULLET_WIDTH, METALL_BULLET_HEIGHT)
                self.velocity_x = METALL_BULLET_VELOCITY_X
            self.velocity_y = velocity_y
            self.image = metall_image_bullet
            self.used = False                

    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, METALL_WIDTH, METALL_HEIGHT)
        self.image = metall_image_left
        self.velocity_y = 0
        self.direction = "left"
        self.jumping = False
        self.health = 1
        self.bullets = []
        self.last_fired = pygame.time.get_ticks() #time in ms after pygame.initialize
        self.guarding = False
    
    def update_image(self):
        if self.direction == "right":
            if self.guarding:
                self.image = metall_image_guard_right
            else:
                self.image = metall_image_right
        elif self.direction == "left":
            if self.guarding:
                self.image = metall_image_guard_left
            else:
                self.image = metall_image_left
    
    def set_shooting(self):
        if abs(self.x - player.x) <= TILE_SIZE*4:
            self.guarding = False
            now = pygame.time.get_ticks()
            if now - self.last_fired > 1000:
                self.last_fired = now
                self.bullets.append(Metall.Bullet(self, -METALL_BULLET_VELOCITY_Y))
                self.bullets.append(Metall.Bullet(self, 0))
                self.bullets.append(Metall.Bullet(self, METALL_BULLET_VELOCITY_Y))
        else:
            self.guarding = True

class Blader(pygame.Rect):
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, BLADER_WIDTH, BLADER_HEIGHT)
        self.image = blader_image_right
        self.direction = "right"
        self.health = 3
        self.velocity_x = BLADER_VELOCITY_X
        self.velocity_y = BLADER_VELOCITY_Y
        self.start_x = x
        self.start_y = y
        self.max_range_x = TILE_SIZE*4
        self.max_range_y = TILE_SIZE
    
    def update_image(self):
        if self.direction == "right":
            self.image = blader_image_right
        elif self.direction == "left":
            self.image = blader_image_left

class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image

class Item(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, image.get_width(), image.get_height())
        self.image = image
        self.jumping = False
        self.velocity_y = ITEM_VELOCITY_Y
        self.used = False

def append_tiles(map_code, tile):
    if map_code < 0:
        background_tiles.append(tile)
    else:
        tiles.append(tile)

def create_map():
    for column in range(len(GAME_MAP[0])):
        for row in range(len(GAME_MAP)):
            map_code = GAME_MAP[row][column]
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            if map_code == 0: #empty tile
                continue
            elif abs(map_code) == 1:
                append_tiles(map_code, Tile(x, y, rock_tile1_image))
            elif abs(map_code) == 2:
                append_tiles(map_code, Tile(x, y, rock_tile2_image))
            elif abs(map_code) == 3:
                append_tiles(map_code, Tile(x, y, rock_tile3_image))
            elif abs(map_code) == 4:
                append_tiles(map_code, Tile(x, y, rock_tile4_image))
            elif abs(map_code) == 5:
                append_tiles(map_code, Tile(x, y, floor_tile_image))
            elif abs(map_code) == 6:
                append_tiles(map_code, Tile(x, y, wall_tile_image))
            elif map_code == 7:
                background_tiles.append(Tile(x, y, beam_tile_image))
            elif map_code == 8:
                spikes.append(Tile(x, y, spike_image))
            elif map_code == 9:
                background_tiles.append(Tile(x, y, door_tile_image))
            elif map_code == 10:
                background_tiles.append(Tile(x, y, room_tile_image))
            elif map_code == 11:
                metalls.append(Metall(x, y))
            elif map_code == 12:
                bladers.append(Blader(x, y))                

def check_tile_collision(character):
    for tile in tiles:
        if character.colliderect(tile):
            return tile
        elif tile.x - character.x > GAME_WIDTH:
            return None
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

def drop_item(character):
    random_number = random.randint(1, 100) #inclusive of 100
    if 0 < random_number <= 20:
        items.append(Item(character.x, character.y, big_life_energy_image))
    elif 20 < random_number <= 50:
        items.append(Item(character.x, character.y, life_energy_image))
    elif 50 < random_number <= 75:
        items.append(Item(character.x, character.y, score_ball_image))

def move_player_x(velocity_x):
    move_map_x(velocity_x)
    tile = check_tile_collision(player)
    if tile is not None:
        move_map_x(-velocity_x)

def move_map_x(velocity_x):
    for tile in background_tiles:
        tile.x += velocity_x

    for tile in tiles:
        tile.x += velocity_x
    
    for metall in metalls:
        metall.x += velocity_x
        for bullet in metall.bullets:
            bullet.x += velocity_x

    for bullet in metall_bullets:
        bullet.x += velocity_x
    
    for item in items:
        item.x += velocity_x
    
    for spike in spikes:
        spike.x += velocity_x
    
    for blader in bladers:
        blader.start_x += velocity_x
        blader.x += velocity_x

def move():
    global metalls, items, bladers, metall_bullets
    #x movement
    # if player.direction == "left" and player.velocity_x < 0:
    #     player.velocity_x += FRICTION
    # elif player.direction == "right" and player.velocity_x > 0:
    #     player.velocity_x -= FRICTION
    # else:
    #     player.velocity_x = 0

    # player.x += player.velocity_x
    # if player.x < 0:
    #     player.x = 0
    # elif player.x + player.width > GAME_WIDTH:
    #     player.x = GAME_WIDTH - player.width

    # check_tile_collision_x(player)

    #y movement
    player.velocity_y += GRAVITY
    player.y += player.velocity_y
    check_tile_collision_y(player)

    for spike in spikes:
        if player.colliderect(spike):
            player.health = 0 #game over

    #bullets
    for bullet in player.bullets:
        bullet.x += bullet.velocity_x
        for metall in metalls:
            if metall.health > 0 and not bullet.used and bullet.colliderect(metall):
                bullet.used = True
                if not metall.guarding:
                    metall.health -= 1
                    if metall.health <= 0:
                        drop_item(metall)
                        # metall_bullets += metall.bullets
                        metall_bullets.extend(metall.bullets)
                        player.score += 500
        
        for blader in bladers:
            if blader.health > 0 and not bullet.used and bullet.colliderect(blader):
                bullet.used = True
                blader.health -= 1
                if blader.health <= 0:
                    drop_item(blader)
                    player.score += 500
    
    player.bullets = [bullet for bullet in player.bullets if not bullet.used \
                      and bullet.x + bullet.width > 0 and bullet.x < GAME_WIDTH]
    metalls = [metall for metall in metalls if metall.health > 0]
    bladers = [blader for blader in bladers if blader.health > 0]

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
        
        #enemy bullets
        metall.set_shooting()
        for bullet in metall.bullets:
            bullet.x += bullet.velocity_x
            bullet.y += bullet.velocity_y
            if not player.invincible and player.colliderect(bullet):
                player.health -= 2
                bullet.used = True
                player.set_invincible()
        
        metall.bullets = [bullet for bullet in metall.bullets if not bullet.used \
                          and bullet.x + bullet.width > 0 and bullet.x < GAME_WIDTH]

    for bullet in metall_bullets:
        bullet.x += bullet.velocity_x
        bullet.y += bullet.velocity_y
        if not player.invincible and player.colliderect(bullet):
            player.health -= 2
            bullet.used = True
            player.set_invincible()
    
    metall_bullets = [bullet for bullet in metall_bullets if not bullet.used \
                        and bullet.x + bullet.width > 0 and bullet.x < GAME_WIDTH]

    for blader in bladers:
        if abs(blader.x + blader.velocity_x - blader.start_x) >= blader.max_range_x:
            blader.velocity_x *= -1
            if blader.velocity_x < 0:
                blader.direction = "left"
            elif blader.velocity_x > 0:
                blader.direction = "right"
        else:
            blader.x += blader.velocity_x

        if abs(blader.y + blader.velocity_y - blader.start_y) >= blader.max_range_y:
            blader.velocity_y *= -1
        else:
            blader.y += blader.velocity_y
        
        if not player.invincible and player.colliderect(blader):
            player.health -= 1
            player.set_invincible()

    for item in items:
        item.velocity_y += GRAVITY
        item.y += item.velocity_y
        check_tile_collision_y(item)
        if player.colliderect(item):
            item.used = True
            if item.image == life_energy_image:
                player.health = min(player.health + 2, player.max_health)
            elif item.image == big_life_energy_image:
                player.health = min(player.health + 8, player.max_health)
            elif item.image == score_ball_image:
                player.score += 1000
    items = [item for item in items if not item.used]

def draw():
    window.fill((20, 18, 167))
    window.blit(background_image, (0, 80))

    for tile in background_tiles:
        if tile.x > GAME_WIDTH:
            break
        window.blit(tile.image, tile)

    for tile in tiles:
        if tile.x > GAME_WIDTH:
            break
        window.blit(tile.image, tile)
    
    for spike in spikes:
        if spike.x > GAME_WIDTH:
            break
        window.blit(spike.image, spike)

    player.update_image()
    window.blit(player.image, player)

    for bullet in player.bullets:
        window.blit(bullet.image, bullet)

    for metall in metalls:
        if metall.x > GAME_WIDTH:
            break
        metall.update_image()
        window.blit(metall.image, metall)
        for bullet in metall.bullets:
            window.blit(bullet.image, bullet)

    for bullet in metall_bullets:
        window.blit(bullet.image, bullet)

    for blader in bladers:
        if blader.x > GAME_WIDTH:
            break
        blader.update_image()
        window.blit(blader.image, blader)

    for item in items:
        if item.x > GAME_WIDTH:
            break
        window.blit(item.image, item)

    pygame.draw.rect(window, "black", (TILE_SIZE, TILE_SIZE, HEALTH_WIDTH, HEALTH_HEIGHT * player.max_health))
    for i in range(player.max_health - player.health, player.max_health):
        window.blit(health_image, (TILE_SIZE, TILE_SIZE + i*HEALTH_HEIGHT, HEALTH_WIDTH, HEALTH_HEIGHT))

    #score
    text_score = str(player.score)
    while len(text_score) < 7: #7 digits in score
        text_score = "0" + text_score
    text_surface = game_font.render(text_score, False, "white")
    window.blit(text_surface, (GAME_WIDTH/2, TILE_SIZE/2))

#start game
player = Player()
metalls = []
metall_bullets = [] #used to keep bullets active when metall is destroyed
tiles = []
background_tiles = []
items = []
spikes = [] #traps, hazards
bladers = []
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
        # player.velocity_x = -PLAYER_VELOCITY_X
        move_player_x(PLAYER_VELOCITY_X)
        player.direction = "left"

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        # player.velocity_x = PLAYER_VELOCITY_X
        move_player_x(-PLAYER_VELOCITY_X)
        player.direction = "right"
    
    if keys[pygame.K_x] or keys[pygame.K_SPACE]:
        player.set_shooting()

    move()
    draw()
    pygame.display.update()
    clock.tick(60) #60 frames per second (fps)
