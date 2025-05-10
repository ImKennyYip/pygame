import pygame
from sys import exit #terminate the program
import os

#game variables
GAME_WIDTH = 512
GAME_HEIGHT = 512

PLAYER_X = GAME_WIDTH/2
PLAYER_Y = GAME_HEIGHT/2
PLAYER_WIDTH = 42
PLAYER_HEIGHT = 48
PLAYER_DISTANCE = 5

#images
background_image = pygame.image.load(os.path.join("images", "background.png"))
player_image_right = pygame.image.load(os.path.join("images", "megaman-right.png"))
player_image_right = pygame.transform.scale(player_image_right, (PLAYER_WIDTH, PLAYER_HEIGHT))

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Kenny Yip Coding - PyGame")
pygame.display.set_icon(player_image_right)
clock = pygame.time.Clock()

class Player(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right

player = Player()

def draw():
    window.fill((20, 18, 167)) #fill bg with a color to clear previous frame
    window.blit(background_image, (0, 80))
    window.blit(player.image, (player.x, player.y))

while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #user clicks the X button in window
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    # if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y - PLAYER_DISTANCE >= 0:
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= PLAYER_DISTANCE
        # if (player.y < 0):
            # player.y += PLAYER_DISTANCE
            # player.y = 0
        # player.y = max(player.y - PLAYER_DISTANCE, 0)
    
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y + player.height + PLAYER_DISTANCE <= GAME_HEIGHT:
    # if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        # player.y += PLAYER_DISTANCE
        player.y = min(player.y + PLAYER_DISTANCE, GAME_HEIGHT - player.height)

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        # player.x -= PLAYER_DISTANCE
        player.x = max(player.x - PLAYER_DISTANCE, 0)

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        # player.x += PLAYER_DISTANCE
        player.x = min(player.x + PLAYER_DISTANCE, GAME_WIDTH - player.width)

    draw()
    pygame.display.update()
    clock.tick(60) #60 frames per second (fps)
