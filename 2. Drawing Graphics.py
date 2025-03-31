import pygame
from sys import exit #terminate the program

#game variables
GAME_WIDTH = 512
GAME_HEIGHT = 512

pygame.init() #always needed to initialize pygame
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Kenny Yip Coding - PyGame") #title of the window
clock = pygame.time.Clock() #used for the game loop

#left (x), top (y), width, height
player = pygame.Rect(200, 150, 150, 50)

def draw():
    # window.fill("blue")
    # window.fill("#54de9e")
    # window.fill((84, 222, 158))
    window.fill((20, 18, 167))
    pygame.draw.rect(window, (2, 239, 238), player)

while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #user clicks the X button in window
            pygame.quit()
            exit()

    draw()
    pygame.display.update()
    clock.tick(60) #60 frames per second (fps)
