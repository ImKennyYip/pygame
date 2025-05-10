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

#images
# some operating systems use / or \ as directory separators, use os to figure which to use
# background_image = pygame.image.load("images/background.png")
# background_image = pygame.image.load("images\\background.png")
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

#left (x), top (y), width, height
player = Player()


def draw():
    window.fill((20, 18, 167))
    # window.blit(background_image, (0, 0))
    window.blit(background_image, (0, 80))
    # window.blit(player.image, (player.x, player.y))
    window.blit(player.image, player)

while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= 5
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += 5
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += 5

    draw()
    pygame.display.update()
    clock.tick(60) #60 frames per second (fps)
