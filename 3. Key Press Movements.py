import pygame
from sys import exit

#game variables
GAME_WIDTH = 512
GAME_HEIGHT = 512

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Kenny Yip Coding - PyGame")
clock = pygame.time.Clock()

#left (x), top (y), width, height
player = pygame.Rect(150, 150, 50, 50)

def draw():
    window.fill((20, 18, 167))
    pygame.draw.rect(window, (2, 239, 238), player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        #KEYDOWN - key was pressed, KEYUP - key was pressed/release
        '''
        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_UP or event.key ==  pygame.K_w):
            if event.key in (pygame.K_UP, pygame.K_w):
                player.y -= 5
            if event.key in (pygame.K_DOWN, pygame.K_s):
                player.y += 5
            if event.key in (pygame.K_LEFT, pygame.K_a):
                player.x -= 5
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                player.x += 5'
        '''
    # allows you to hold onto the key
    keys = pygame.key.get_pressed() #access the keys currently pressed
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
